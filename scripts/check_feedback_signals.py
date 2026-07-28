#!/usr/bin/env python3
"""Scan harness-feedback-log.md and report accumulated signals per harness.

This script is the read-side of the distillation->evolution bridge:
- docs/ai/conversation-distillation.md writes signals to the log.
- common/meta/harness-evolution.md Item 3 uses this script's output to
  decide when accumulated signals trigger a re-review.

The script is best-effort and never blocks: exit 0 always. Its purpose is
to surface "harness X has accumulated N signals, M of the same type" so a
human can decide whether to re-review.

Usage:
    python scripts/check_feedback_signals.py
    python scripts/check_feedback_signals.py --threshold 3   # default
    python scripts/check_feedback_signals.py --json

Exit codes:
    0 = always (best-effort script; signals are advisory, not errors)
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "common" / "meta" / "harness-feedback-log.md"

# An entry header looks like:
#   ### 2026-07-27 — cpp-feature-design-prerequisites, item 3 (entity classification)
# or:
#   ### 2026-07-27 — common-harness-evolution, general (tier)
# or (tooling target, not a harness):
#   ### 2026-07-28 — tool/scripts/check_review_signals.py, general (schema gap)
#
# The target may be a harness id ([a-zA-Z0-9_-]+) OR a tooling path prefixed
# with tool/ (tool/...path). Tooling targets let the log record feedback about
# scripts/prompts/templates, closing the gap where only harnesses were valid
# targets (see harness-feedback-log.md 2026-07-27 inoperable entry).
TARGET_RE = r"tool/[a-zA-Z0-9_./-]+|[a-zA-Z0-9_-]+"
ENTRY_RE = re.compile(
    r"^###\s+(\d{4}-\d{2}-\d{2})\s+[—-]\s+"   # date + em-dash or hyphen
    rf"({TARGET_RE})"                          # harness id OR tool/<path>
    r"(?:,\s*(item\s+\d+|general))?"           # optional ", item N" or ", general"
    r"(?:\s*\(([^)]*)\))?\s*$"                 # optional "(detail)"
)

SIGNAL_TYPES = {"gap", "inoperable", "misleading", "under-coverage", "tier-mismatch"}
SIGNAL_RE = re.compile(r"\*\*Signal:\*\*\s*(\S+)")


def parse_log(path: Path):
    """Yield dicts: {date, harness, item, detail, signal}."""
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    current = None
    for line in lines:
        m = ENTRY_RE.match(line)
        if m:
            if current:
                yield current
            date, harness, item, detail = m.groups()
            current = {
                "date": date,
                "harness": harness,
                "item": item or "general",
                "detail": detail or "",
                "signal": None,
            }
        elif current and line.startswith("- **Signal:**"):
            sm = SIGNAL_RE.search(line)
            if sm:
                current["signal"] = sm.group(1).rstrip(",")
    if current:
        yield current


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--threshold", type=int, default=3,
                    help="Signal count per harness that flags for re-review (default 3)")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = ap.parse_args()

    entries = list(parse_log(LOG_PATH))

    # Aggregate
    per_harness = defaultdict(list)
    for e in entries:
        per_harness[e["harness"]].append(e)

    flagged = []
    summary = {}
    for harness, items in sorted(per_harness.items()):
        signal_counts = Counter(i["signal"] for i in items if i["signal"])
        same_type_max = max(signal_counts.values()) if signal_counts else 0
        total = len(items)
        summary[harness] = {
            "total": total,
            "signals": dict(signal_counts),
            "same_type_max": same_type_max,
            "flagged": same_type_max >= args.threshold,
        }
        if same_type_max >= args.threshold:
            top_signal = signal_counts.most_common(1)[0][0]
            flagged.append((harness, total, top_signal, same_type_max))

    if args.json:
        out = {"threshold": args.threshold, "total_entries": len(entries), "harnesses": summary}
        if flagged:
            out["flagged_for_rereview"] = [
                {"harness": h, "total_signals": t, "top_signal": s, "count": c}
                for h, t, s, c in flagged
            ]
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0

    # Text output
    print(f"# Harness Feedback Signal Summary")
    print(f"# Log: {LOG_PATH.relative_to(ROOT)}")
    print(f"# Total entries: {len(entries)}  |  Re-review threshold: ≥{args.threshold} same-type signals")
    print()

    if not summary:
        print("(no entries found — log is empty or unparsed)")
        print()
        print("If the log exists but nothing parsed, check entry header format against")
        print("the ENTRY_RE pattern in this script.")
        return 0

    for harness, data in sorted(summary.items(), key=lambda kv: -kv[1]["total"]):
        flag = "  *** FLAGGED FOR RE-REVIEW ***" if data["flagged"] else ""
        print(f"## {harness}  ({data['total']} entries){flag}")
        if data["signals"]:
            for sig, cnt in sorted(data["signals"].items(), key=lambda kv: -kv[1]):
                mark = " ← threshold" if cnt >= args.threshold else ""
                known = "" if sig in SIGNAL_TYPES else f" (UNKNOWN type — expected one of {sorted(SIGNAL_TYPES)})"
                print(f"   - {sig}: {cnt}{mark}{known}")
        else:
            print("   - (entries missing **Signal:** field)")
        print()

    if flagged:
        print("=== Action recommended ===")
        print("Per harness-evolution.md Item 3, the following harnesses have accumulated")
        print(f"≥{args.threshold} same-type signals and should be re-reviewed:")
        for harness, total, sig, cnt in flagged:
            print(f"  - {harness}: {cnt}× {sig} (of {total} total)")
        print()
        print("Re-review scope: re-read the harness, check the flagged signal type's items,")
        print("decide amend / split / deprecate per evolution Item 4 or Item 7.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
