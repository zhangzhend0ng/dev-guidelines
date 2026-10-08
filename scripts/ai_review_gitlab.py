#!/usr/bin/env python3
"""AI harness reviewer for GitLab merge requests.

Pipeline: MR diff (GitLab API) -> route_harnesses.py (apply_globs) -> LLM
(OpenAI-compatible endpoint) -> single sticky MR note, edited in place on
every re-run (hidden HTML marker `ai-review:sticky` + head SHA).

Designed to run as a GitLab CI job on `merge_request_event` pipelines, but
works locally against any MR for dry-runs:

    AI_REVIEW_GITLAB_TOKEN=glpat-... DEEPSEEK_API_KEY=sk-... \
        python scripts/ai_review_gitlab.py --project 72 --mr 586

Never gates: the script exits 0 even on internal failure (the CI job also
sets allow_failure: true), so a broken reviewer never blocks an MR.

Required env in CI:
    CI_PROJECT_ID, CI_MERGE_REQUEST_IID      (provided by runner)
    GITLAB_HOST                              (set in .gitlab-ci.yml)
    AI_REVIEW_GITLAB_TOKEN                   (masked CI variable)
    AI_REVIEW_LLM_API_KEY                    (masked CI variable)
Optional env:
    AI_REVIEW_LLM_BASE_URL (default https://api.deepseek.com)
    AI_REVIEW_MODEL        (default deepseek-v4-pro)
    AI_REVIEW_PROJECT_STANDARDS (e.g. projects/snapmaker-orca; path inside
                                this repo whose standards get appended)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DG_ROOT = Path(__file__).resolve().parent.parent
MARKER_RE = re.compile(r"<!-- ai-review:sticky v1 \| sha:([0-9a-f]+)")
MAX_DIFF_CHARS = 600_000
MAX_HARNESS_CHARS = 400_000
LLM_TIMEOUT_S = 300

SYSTEM_PROMPT = """You are a rigorous C++ code reviewer for a slicer fork (Orca codebase).
You review a merge request diff against the routed harness checklists supplied below.

Rules:
- Every finding must be evidence-based: cite the file and approximate line from the
  diff or the provided source context. Never invent line numbers or code.
- Tag each finding with its authority tier: (N) normative standard, (C) consensus
  guideline, (A) advisory, (P) project convention.
- Do not re-report what is already correct; a short "verified correct" list is fine.
- Distinguish real defects from style questions; severity order: BLOCKING > QUESTION > MINOR > ADVISORY.
- If the diff is partial (truncated) or coverage is incomplete, say so explicitly.
- Severity discipline: BLOCKING is reserved for defects provable from the provided
  diff/context. Facts you cannot verify (external repos, branch names, environment
  config, other files) must at most be QUESTION severity, never BLOCKING, and must
  be phrased as unverified assumptions.

Output contract (markdown, English):
1. First line: **VERDICT: APPROVE_WITH_COMMENTS | REQUEST_CHANGES** (pick one).
   Prefer APPROVE_WITH_COMMENTS unless at least one BLOCKING or confirmed (not
   speculative) defect exists; unverifiable concerns stay findings, not verdict.
2. "### Findings" — table: | # | Location | Severity | Issue & suggested fix |.
3. "### Checklist coverage" — which harnesses were applied vs N/A for this diff.
4. "### Action items" — checkbox list for the author.
5. One final line on limitations.
Be concise: the report is posted as one MR comment.

A "## Repo context" section may be supplied below the diff: real source fetched
from the repository at the MR head specifically to verify this change. Cite it
like any other evidence; if something you would verify is missing from it, say
so under limitations instead of guessing."""

PLAN_PROMPT = """You are the context planner for a code review. Below are a merge request
diff and the routed harness checklists. Decide what repository evidence is needed
to verify the change beyond the diff itself.

Return ONLY a JSON object (no markdown fence, no prose):
{"files": [{"path": "src/...", "reason": "why"}],
 "searches": ["symbol-or-pattern", ...]}

Limits: at most 8 files, at most 5 searches. Only request files whose content
could confirm or refute a finding (callers/callees of changed functions, types
used, config definitions). If the diff is self-contained (e.g. config/i18n-only),
return empty lists."""

NOTE_HEADER = """<!-- ai-review:sticky v1 | sha:{sha} | mode:{mode} -->
## :robot: AI Harness Review — `{sha8}` — **VERDICT: {verdict}**

> Advisory report by AI reviewer (dev-guidelines harness pipeline). Not a gate —
> human review per repo rules still decides. This comment is edited in place on
> new pushes.
"""


def env(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name, default)


def http(method: str, url: str, token: str | None = None, payload: dict | None = None,
         headers: dict | None = None, timeout: int = 60):
    hdrs = dict(headers or {})
    if token:
        hdrs["PRIVATE-TOKEN"] = token
    data = json.dumps(payload).encode() if payload is not None else None
    if data:
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=hdrs)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else None


def gitlab(base: str, project: str, path: str, token: str, method: str = "GET",
           payload: dict | None = None):
    url = f"http://{base}/api/v4/projects/{project}/{path}"
    return http(method, url, token=token, payload=payload)


def fetch_mr(base: str, project: str, mr_iid: str, token: str):
    mr = gitlab(base, project, f"merge_requests/{mr_iid}", token)
    diffs = gitlab(base, project, f"merge_requests/{mr_iid}/diffs?per_page=100", token)
    return mr, diffs


def route_harnesses(changed_files: list[str]) -> tuple[list[str], list[str]]:
    """Returns (harness_relpaths, unmatched_files). Exit 1 = partial coverage."""
    script = DG_ROOT / "scripts" / "route_harnesses.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--files", *changed_files, "--json"],
        cwd=DG_ROOT, capture_output=True, text=True)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [], changed_files
    harnesses: list[str] = []
    for route in data.get("routes", []):
        for h in route.get("harnesses", []):
            if h not in harnesses:
                harnesses.append(h)
    return harnesses, data.get("unmatched", [])


def read_harness_context(harnesses: list[str], standards_dir: str | None) -> str:
    parts: list[str] = []
    budget = MAX_HARNESS_CHARS
    if standards_dir:
        for name in ("AGENTS.md", "coding-standards.md"):
            p = DG_ROOT / standards_dir / name
            if p.is_file():
                text = p.read_text(encoding="utf-8", errors="replace")
                parts.append(f"### Project conventions ({standards_dir}/{name})\n{text}")
                budget -= len(text)
    for rel in harnesses:
        if budget <= 0:
            parts.append(f"### {rel}\n(omitted: harness content budget exhausted)")
            continue
        p = DG_ROOT / rel
        if not p.is_file():
            continue
        text = p.read_text(encoding="utf-8", errors="replace")[:budget]
        parts.append(f"### Harness checklist: {rel}\n{text}")
        budget -= len(text)
    return "\n\n".join(parts)


def build_diff_text(diffs: list[dict]) -> tuple[str, bool]:
    lines: list[str] = []
    for d in diffs:
        lines.append(f"--- a/{d['old_path']}\n+++ b/{d['new_path']}\n{d.get('diff') or ''}\n")
    text = "\n".join(lines)
    truncated = False
    if len(text) > MAX_DIFF_CHARS:
        text = text[:MAX_DIFF_CHARS] + "\n... (diff truncated at budget)"
        truncated = True
    return text, truncated


def changed_regions(diff_text: str, radius: int = 30) -> dict[str, list[tuple[int, int]]]:
    """Parse the unified diff for (start, end) new-file line spans per changed file,
    padded by `radius`, to scope repo-context reads around actual edits."""
    regions: dict[str, list[tuple[int, int]]] = {}
    cur: str | None = None
    new_ln = 0
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            cur = line[6:]
            regions.setdefault(cur, [])
        elif line.startswith("@@"):
            m = re.search(r"\+(\d+)", line)
            if m and cur:
                new_ln = int(m.group(1))
                lo = max(1, new_ln - radius)
                regions[cur].append((lo, new_ln))
        elif cur is not None and new_ln and not line.startswith("-"):
            regions[cur][-1] = (regions[cur][-1][0], new_ln + radius)
            if line.startswith("+"):
                new_ln += 1
            elif not line.startswith("\\"):
                new_ln += 1
    return regions


def run_git(cache_dir: Path, *args: str, timeout: int = 300) -> str:
    proc = subprocess.run(["git", "-C", str(cache_dir), *args],
                          capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args[:3])}: {proc.stderr.strip()[:200]}")
    return proc.stdout


def ensure_cache_repo(cache_dir: Path, repo_url: str):
    if not (cache_dir / ".git").exists():
        print(f"initializing blobless cache clone into {cache_dir} (one-time)...")
        cache_dir.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--filter=blob:none", repo_url, str(cache_dir)],
                       check=True, capture_output=True, text=True, timeout=1800)
    return cache_dir


def read_file_windows(cache_dir: Path, sha: str, path: str,
                      spans: list[tuple[int, int]], cap: int = 30_000) -> str:
    try:
        blob = run_git(cache_dir, "show", f"{sha}:{path}")
    except RuntimeError:
        return f"(file {path} not present at {sha[:8]})"
    lines = blob.splitlines()
    if not spans:
        spans = [(1, min(len(lines), 200))]
    merged: list[tuple[int, int]] = []
    for lo, hi in sorted(spans):
        if merged and lo <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    parts, used = [], 0
    for lo, hi in merged:
        chunk = "\n".join(f"{n}: {lines[n-1]}" for n in range(lo, min(hi, len(lines)) + 1))
        if used + len(chunk) > cap:
            parts.append(f"({path}: window {lo}-{hi} omitted, budget)")
            continue
        parts.append(f"--- {path}:{lo}-{hi} ---\n{chunk}")
        used += len(chunk)
    return "\n".join(parts)


def search_repo(cache_dir: Path, sha: str, pattern: str, cap: int = 6_000) -> str:
    try:
        out = run_git(cache_dir, "grep", "-n", "-I", pattern, sha, "--", "*.cpp", "*.hpp", "*.h", "*.cc")
    except RuntimeError:
        return f"(no matches for '{pattern}')"
    return f"--- grep '{pattern}' ---\n" + out[:cap]


def plan_context(llm_base, llm_key, model, effort, diff_text, harness_ctx) -> dict:
    raw = call_llm(llm_base, llm_key, model, PLAN_PROMPT,
                   f"## Routed harnesses (titles only)\n{harness_ctx[:3000]}\n\n## Diff\n```diff\n{diff_text}\n```")
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return {}
    try:
        plan = json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}
    plan.setdefault("files", [])
    plan.setdefault("searches", [])
    return plan


def gather_context(base, project, mr_iid, token, diff_text, harness_ctx,
                   llm_base, llm_key, model, effort) -> str:
    repo_url = env("AI_REVIEW_REPO_URL") or env("CI_REPOSITORY_URL")
    if not repo_url:
        return ""
    cache_dir = Path(env("AI_REVIEW_CACHE_DIR") or
                     Path(os.environ.get("USERPROFILE") or tempfile.gettempdir())
                     / ".ai-review-cache" / re.sub(r"[^\w.-]", "_", f"{base}_{project}"))
    ensure_cache_repo(cache_dir, repo_url)
    run_git(cache_dir, "fetch", "--filter=blob:none", "origin",
            f"refs/merge-requests/{mr_iid}/head", timeout=600)
    sha = run_git(cache_dir, "rev-parse", "FETCH_HEAD").strip()
    plan = plan_context(llm_base, llm_key, model, effort, diff_text, harness_ctx)
    regions = changed_regions(diff_text)
    print(f"context plan: {len(plan['files'])} files, {len(plan['searches'])} searches @ {sha[:8]}")
    parts, budget = [], 200_000
    for f in plan["files"][:8]:
        if budget <= 0:
            break
        path = f.get("path", "")
        spans = regions.get(path) or [(1, 200)]
        chunk = read_file_windows(cache_dir, sha, path, spans)
        parts.append(f"### {path} (reason: {f.get('reason', '?')})\n{chunk}")
        budget -= len(chunk)
    for pat in plan["searches"][:5]:
        if budget <= 0:
            break
        chunk = search_repo(cache_dir, sha, pat)
        parts.append(chunk)
        budget -= len(chunk)
    return "\n\n".join(parts)


def call_llm(base_url: str, api_key: str, model: str, system: str, user: str,
             effort: str = "low") -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": 0.2,
        "max_tokens": 16000,
        "reasoning_effort": effort,
    }
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=LLM_TIMEOUT_S) as resp:
        data = json.loads(resp.read())
    choice = data["choices"][0]
    usage = data.get("usage", {})
    print(f"llm usage: prompt={usage.get('prompt_tokens')} "
          f"completion={usage.get('completion_tokens')} "
          f"(reasoning={usage.get('completion_tokens_details', {}).get('reasoning_tokens')}) "
          f"finish={choice.get('finish_reason')}")
    content = (choice["message"].get("content") or "").strip()
    if not content:
        raise RuntimeError(
            f"LLM returned empty content (finish_reason={choice.get('finish_reason')}, "
            f"usage={usage}); raise max_tokens or lower reasoning effort")
    return content


def extract_verdict(body: str) -> str:
    m = re.search(r"VERDICT:\s*(APPROVE_WITH_COMMENTS|APPROVE|REQUEST_CHANGES)", body)
    return m.group(1) if m else "SEE_REPORT"


def post_sticky_note(base: str, project: str, mr_iid: str, token: str, body: str):
    """Find the previous sticky note (by marker) authored by this token, edit it;
    otherwise post a new one."""
    notes = gitlab(base, project, f"merge_requests/{mr_iid}/notes?per_page=100&sort=desc",
                   token)
    user = http("GET", f"http://{base}/api/v4/user", token=token)
    uid = user["id"]
    for note in notes:
        if note["author"]["id"] == uid and MARKER_RE.search(note["body"]):
            gitlab(base, project, f"merge_requests/{mr_iid}/notes/{note['id']}", token,
                   method="PUT", payload={"body": body})
            return f"updated note {note['id']}"
    note = gitlab(base, project, f"merge_requests/{mr_iid}/notes", token, method="POST",
                  payload={"body": body})
    return f"posted note {note['id']}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=env("CI_PROJECT_ID"))
    ap.add_argument("--mr", default=env("CI_MERGE_REQUEST_IID"))
    args = ap.parse_args()
    if not (args.project and args.mr):
        print("ERROR: --project/--mr (or CI variables) required", file=sys.stderr)
        return 2

    base = env("GITLAB_HOST")
    token = env("AI_REVIEW_GITLAB_TOKEN") or env("GITLAB_TOKEN")
    llm_key = env("AI_REVIEW_LLM_API_KEY") or env("DEEPSEEK_API_KEY")
    llm_base = env("AI_REVIEW_LLM_BASE_URL", "https://api.deepseek.com")
    model = env("AI_REVIEW_MODEL", "deepseek-v4-pro")
    effort = env("AI_REVIEW_LLM_EFFORT", "low")
    standards = env("AI_REVIEW_PROJECT_STANDARDS")
    in_ci = env("CI") == "true"
    if not (base and token and llm_key):
        print("ERROR: GITLAB_HOST / token / LLM key missing", file=sys.stderr)
        return 2

    try:
        mr, diffs = fetch_mr(base, args.project, args.mr, token)
        sha = mr["sha"]
        changed = [d["new_path"] for d in diffs]
        print(f"MR !{args.mr}: {len(changed)} files @ {sha[:8]}")

        harnesses, unmatched = route_harnesses(changed)
        print(f"routed {len(harnesses)} harnesses, {len(unmatched)} unmatched files")

        diff_text, truncated = build_diff_text(diffs)
        harness_ctx = read_harness_context(harnesses, standards)

        context = ""
        if env("AI_REVIEW_CONTEXT", "on") == "on" and llm_key:
            try:
                context = gather_context(base, args.project, args.mr, token,
                                         diff_text, harness_ctx,
                                         llm_base, llm_key, model, effort)
            except Exception as ctx_err:  # noqa: BLE001 - diff-only fallback
                print(f"context gathering failed (diff-only fallback): {ctx_err}")

        trunc_note = "NOTE: diff is truncated.\n" if truncated else ""
        ctx_section = f"\n## Repo context (fetched from {sha[:8]} for verification)\n{context}\n" if context else ""
        user_prompt = (
            f"Merge request !{args.mr}: {mr['title']}\n"
            f"Branch: {mr['source_branch']} -> {mr['target_branch']} @ {sha[:8]}\n"
            f"Changed files: {', '.join(changed)}\n\n"
            f"{trunc_note}"
            f"## Harness checklists routed for these paths\n{harness_ctx}\n\n"
            f"{ctx_section}"
            f"## Full MR diff\n```diff\n{diff_text}\n```\n\nProduce the review report now."
        )
        report = call_llm(llm_base, llm_key, model, SYSTEM_PROMPT, user_prompt, effort=effort)

        body = (NOTE_HEADER.format(sha=sha, sha8=sha[:8], mode="ci" if in_ci else "local",
                                   verdict=extract_verdict(report))
                + "\n" + report + f"\n\n---\n:model `{model}` :pipeline "
                f"`{env('CI_PIPELINE_URL', 'local dry-run')}`\n")
        result = post_sticky_note(base, args.project, args.mr, token, body)
        print("sticky note:", result)
        return 0
    except Exception as exc:  # noqa: BLE001 - reviewer must never gate an MR
        print(f"ERROR: {exc}", file=sys.stderr)
        if in_ci:
            # A green job with a stale report is indistinguishable from a real
            # review - surface the failure on the MR itself (best effort; if the
            # GitLab token itself is dead this will also fail and log only).
            try:
                sha = "unknown"
                try:
                    mr, _ = fetch_mr(base, args.project, args.mr, token)
                    sha = mr["sha"]
                except Exception:
                    pass
                body = (NOTE_HEADER.format(sha=sha, sha8=str(sha)[:8], mode="ci",
                                           verdict="REVIEW_FAILED")
                        + f"\n**AI review failed**: `{exc}`\n\n"
                        + "Check the job log; the previous report below may be stale.\n")
                print("sticky note:", post_sticky_note(base, args.project, args.mr, token, body))
            except Exception as nested:  # noqa: BLE001
                print(f"ERROR: could not post failure notice: {nested}", file=sys.stderr)
        return 0 if in_ci else 1


if __name__ == "__main__":
    sys.exit(main())
