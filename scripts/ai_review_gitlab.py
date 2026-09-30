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

Output contract (markdown, English):
1. First line: **VERDICT: APPROVE_WITH_COMMENTS | REQUEST_CHANGES** (pick one).
2. "### Findings" — table: | # | Location | Severity | Issue & suggested fix |.
3. "### Checklist coverage" — which harnesses were applied vs N/A for this diff.
4. "### Action items" — checkbox list for the author.
5. One final line on limitations.
Be concise: the report is posted as one MR comment."""

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

        trunc_note = "NOTE: diff is truncated.\n" if truncated else ""
        user_prompt = (
            f"Merge request !{args.mr}: {mr['title']}\n"
            f"Branch: {mr['source_branch']} -> {mr['target_branch']} @ {sha[:8]}\n"
            f"Changed files: {', '.join(changed)}\n\n"
            f"{trunc_note}"
            f"## Harness checklists routed for these paths\n{harness_ctx}\n\n"
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
        return 0 if in_ci else 1


if __name__ == "__main__":
    sys.exit(main())
