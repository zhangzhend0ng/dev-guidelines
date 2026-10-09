#!/usr/bin/env python3
"""Coverage audit for the AI MR reviewer (advisory, read-only, always exit 0).

Checks that every MR in scope has an AI review sticky note whose marker sha
equals the MR head sha - i.e. the final state was actually reviewed. This is
the read-side evidence chain for the "100% review coverage" acceptance
criterion: the reviewer job itself fails silently by design (allow_failure +
exit 0), so only an after-the-fact audit can prove or disprove coverage.

Status per MR:
    covered - a sticky note's marker sha == MR head sha
    stale   - sticky notes exist, but none at the current head (silent
              failure or a push that never got reviewed)
    missing - no sticky note at all

Usage:
    GITLAB_HOST=<internal-gitlab-host> AI_REVIEW_GITLAB_TOKEN=... \
        python scripts/ai_coverage_audit.py --project 72 \
        [--state opened|merged|all] [--days 14] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

MARKER_RE = re.compile(r"<!-- ai-review:sticky v1 \| sha:([0-9a-f]+)")


def get(url: str, token: str):
    req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": token})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    return json.loads(raw) if raw else None


def pages(base: str, project: str, path: str, token: str, cap: int = 10):
    """Yield items from a paginated list endpoint (up to cap*100 items)."""
    sep = "&" if "?" in path else "?"
    for page in range(1, cap + 1):
        chunk = get(f"http://{base}/api/v4/projects/{project}/"
                    f"{path}{sep}per_page=100&page={page}", token)
        if not chunk:
            return
        yield from chunk


def list_mrs(base: str, project: str, token: str, state: str, updated_after: str):
    path = f"merge_requests?state={state}&order_by=updated_at&sort=desc"
    if updated_after:
        path += f"&updated_after={updated_after}"
    yield from pages(base, project, path, token)


def review_shas(base: str, project: str, mr_iid, token: str) -> list[str]:
    """All marker shas across the MR's notes (any author: ghost notes count)."""
    shas: list[str] = []
    for note in pages(base, project, f"merge_requests/{mr_iid}/notes?sort=desc", token):
        if note.get("system"):
            continue
        m = MARKER_RE.search(note.get("body") or "")
        if m:
            shas.append(m.group(1))
    return shas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--state", choices=["opened", "merged", "all"], default="opened")
    ap.add_argument("--days", type=int, default=14,
                    help="only MRs updated in the last N days (0 = no filter)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    base = os.environ.get("GITLAB_HOST")
    token = os.environ.get("AI_REVIEW_GITLAB_TOKEN") or os.environ.get("GITLAB_TOKEN")
    if not (base and token):
        print("ERROR: GITLAB_HOST / AI_REVIEW_GITLAB_TOKEN missing", file=sys.stderr)
        return 2

    updated_after = ""
    if args.days > 0:
        updated_after = (datetime.now(timezone.utc)
                         - timedelta(days=args.days)).isoformat()

    rows = []
    for mr in list_mrs(base, args.project, token, args.state, updated_after):
        shas = review_shas(base, args.project, mr["iid"], token)
        if mr["sha"] in shas:
            status = "covered"
        elif shas:
            status = "stale"
        else:
            status = "missing"
        rows.append({"iid": mr["iid"], "state": mr["state"], "status": status,
                     "head_sha": mr["sha"][:8],
                     "latest_review_sha": shas[0][:8] if shas else None,
                     "title": mr["title"][:60]})

    covered = sum(r["status"] == "covered" for r in rows)
    if args.json:
        print(json.dumps({"summary": {"total": len(rows), "covered": covered},
                          "mrs": rows}, ensure_ascii=False, indent=2))
    else:
        for r in rows:
            print(f"!{r['iid']:>4} [{r['state']:<7}] {r['status']:<8} "
                  f"head={r['head_sha']} review={r['latest_review_sha'] or '-':<8} "
                  f"{r['title']}")
        print(f"\ncoverage: {covered}/{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
