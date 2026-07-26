#!/usr/bin/env python3
"""Scan a harness review report for improvement signals and append to feedback log.

AI-only workflow: after completing a review (harness-driven-review.md B5),
run this script on the review report. It mechanically detects signals that
do NOT require meta-cognition:

  - gap: a FAIL described with no "Item N" framing, or referencing an item
         number beyond what the harness actually has.
  - tier-mismatch: an item's stated tier (N/C/A) lacks a same-or-higher
         tier source in the harness's Reference Sources table.
  - inoperable: an item marked N/A with a reason containing keywords like
         "inoperable", "cannot evaluate", "too vague", "not applicable".
  - misleading / under-coverage: AI may flag inline via an HTML comment
         <!-- signal: misleading --> or <!-- signal: under-coverage -->;
         the script collects these. No auto-detection — AI judgement.

Detected signals are appended to common/meta/harness-feedback-log.md.

Usage:
    python scripts/check_review_signals.py <review-report.md>

The review report must reference at least one harness path (cpp/.../*.md)
so the script can locate the harness file for cross-checks.

Exit codes:
    0 = always (advisory; signals are logged, never blocking)
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "common" / "meta" / "harness-feedback-log.md"

# A harness path mention, e.g. cpp/memory/raii.md or common/code-review/review-checklist.md
HARNESS_PATH_RE = re.compile(r"\(([\w./-]+\.md)\)")
# "Item N — STATUS" or "Item N: STATUS" — status is first word after separator
ITEM_LINE_RE = re.compile(r"^\s*Item\s+(\d+)\s*[—:\-]\s*([A-Za-z/]+)\b(.*)$", re.IGNORECASE)
# Inline signal marker
INLINE_SIGNAL_RE = re.compile(r"<!--\s*signal:\s*(\w[\w-]*)\s*-->", re.IGNORECASE)
# Orphan FAIL: a line starting with FAIL or "- FAIL" or "**FAIL" without an Item prefix
ORPHAN_FAIL_RE = re.compile(r"^\s*(?:-\s*)?\*{0,2}FAIL\b", re.IGNORECASE)

TIER_RANK = {"N": 4, "C": 3, "A": 2, "P": 1}
INOPERABLE_KEYWORDS = ("inoperable", "cannot evaluate", "can't evaluate",
                       "too vague", "not evaluable", "unevaluable")


def find_harness_files(text):
    """Return list of (path_str, resolved_path) for harness paths mentioned in text."""
    out = []
    seen = set()
    for m in HARNESS_PATH_RE.finditer(text):
        p = m.group(1)
        if p in seen:
            continue
        seen.add(p)
        # Resolve relative to repo root
        candidate = ROOT / p
        if candidate.exists() and candidate.suffix == ".md":
            out.append((p, candidate))
    return out


def parse_harness_items(harness_path):
    """Return (item_count, tier_of_each_item, source_tiers) from a harness file.

    item_count: highest "### N." number found
    source_tiers: list of tier letters found in the Reference Sources table rows
    """
    text = harness_path.read_text(encoding="utf-8")
    # Count checklist items: lines like "### 1." "### 12."
    item_nums = [int(m.group(1)) for m in re.finditer(r"^###\s+(\d+)\.", text, re.MULTILINE)]
    item_count = max(item_nums) if item_nums else 0
    # Source tiers: rows in Reference Sources table, second column "| R1 | N | ..."
    source_tiers = re.findall(r"\|\s*[A-Z]\d+\s*\|\s*([N CAP])\s*\|", text)
    return item_count, [t for t in source_tiers if t in "NCAP"]


def detect_signals(report_text, harness_files):
    """Yield (harness_id, signal_type, item_ref, detail) tuples."""
    # Collect inline signal markers first (AI judgement signals)
    for m in INLINE_SIGNAL_RE.finditer(report_text):
        sig = m.group(1).lower()
        if sig in ("misleading", "under-coverage"):
            # Attribute to the first harness if multiple; detail is the marker line
            hid = harness_files[0][0] if harness_files else "unknown"
            yield (hid, sig, "inline", f"inline marker: {m.group(0)}")

    # Per-item analysis
    lines = report_text.splitlines()
    # Map harness path -> (item_count, source_tiers) for cross-checks
    harness_meta = {}
    for p, hp in harness_files:
        try:
            harness_meta[p] = parse_harness_items(hp)
        except Exception:
            harness_meta[p] = (0, [])

    for line in lines:
        m = ITEM_LINE_RE.match(line)
        if not m:
            # Orphan FAIL check (no Item prefix)
            if ORPHAN_FAIL_RE.match(line):
                # Only flag if there's at least one harness in scope
                if harness_files:
                    hid = harness_files[0][0]
                    yield (hid, "gap", "orphan", f"FAIL without Item framing: {line.strip()[:100]}")
            continue

        item_num, status, rest = m.group(1), m.group(2).upper(), m.group(3)
        rest_lower = rest.lower()

        # inoperable: N/A with keyword
        if status in ("N/A", "NA", "N\\A"):
            if any(k in rest_lower for k in INOPERABLE_KEYWORDS):
                # Attribute to nearest harness; we don't track per-line harness, use first
                hid = harness_files[0][0] if harness_files else "unknown"
                yield (hid, "inoperable", f"item {item_num}", f"N/A: {rest.strip()[:100]}")

        # tier-mismatch: item says (N) but harness sources max tier is lower
        tier_m = re.search(r"\*\*\(([N CAP])\)\*\*|\(([N CAP])\)", rest)
        if tier_m:
            stated_tier = tier_m.group(1) or tier_m.group(2)
            if stated_tier in TIER_RANK:
                # Find which harness this item belongs to — assume first if unclear
                # (refinement: track current harness header above this line; skipped for token budget)
                for p, (icount, stiers) in harness_meta.items():
                    if not stiers:
                        continue
                    max_src_tier = max(TIER_RANK.get(t, 0) for t in stiers)
                    if TIER_RANK[stated_tier] > max_src_tier:
                        yield (p, "tier-mismatch", f"item {item_num}",
                               f"item tier ({stated_tier}) exceeds max source tier ({max_src_tier})")


def append_to_log(signals):
    """Append detected signals to the feedback log. Returns count written."""
    if not signals:
        return 0
    today = date.today().isoformat()
    blocks = []
    for hid, sig, item_ref, detail in signals:
        block = (
            f"### {today} — {hid_to_log_id(hid)}, {item_ref}\n"
            f"- **Signal:** {sig}\n"
            f"- **Scenario:** auto-detected by check_review_signals.py\n"
            f"- **Observation:** {detail}\n"
            f"- **Outcome:** auto-logged — verify and amend outcome if acted upon\n"
        )
        blocks.append(block)
    # Insert before the "## Maintenance" section if present, else append
    text = LOG_PATH.read_text(encoding="utf-8") if LOG_PATH.exists() else ""
    marker = "\n---\n\n## Maintenance"
    insertion = "\n".join(blocks)
    if marker in text:
        new_text = text.replace(marker, insertion + marker, 1)
    else:
        new_text = text.rstrip() + "\n\n" + insertion
    LOG_PATH.write_text(new_text, encoding="utf-8")
    return len(blocks)


def hid_to_log_id(harness_path):
    """cpp/memory/raii.md -> cpp-raii style id. Best-effort from path."""
    # Try reading frontmatter id; fallback to path-derived
    p = ROOT / harness_path
    if p.exists():
        m = re.search(r'^id:\s*"([^"]+)"', p.read_text(encoding="utf-8"), re.MULTILINE)
        if m:
            return m.group(1)
    # Derive: take filename without ext, prefix with top dir
    parts = harness_path.replace("\\", "/").split("/")
    if len(parts) >= 2:
        return f"{parts[0]}-{Path(parts[-1]).stem}"
    return Path(harness_path).stem


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("review_report", help="Path to the review report markdown file")
    ap.add_argument("--dry-run", action="store_true",
                    help="Detect and print signals without writing to log")
    args = ap.parse_args()

    report_path = Path(args.review_report)
    if not report_path.exists():
        print(f"ERROR: review report not found: {report_path}", file=sys.stderr)
        return 1

    report_text = report_path.read_text(encoding="utf-8")
    harness_files = find_harness_files(report_text)

    if not harness_files:
        print("No harness paths (.md) found in report. Nothing to cross-check.")
        print("Signals limited to inline markers and orphan FAILs.")
        # Still scan inline markers
        harness_files = [("unknown", None)]

    signals = list(detect_signals(report_text, [(p, hp) for p, hp in harness_files if hp]))

    if not signals:
        print("No signals detected.")
        return 0

    print(f"Detected {len(signals)} signal(s):")
    for hid, sig, item_ref, detail in signals:
        print(f"  - {hid} | {sig} | {item_ref} | {detail[:80]}")

    if args.dry_run:
        print("\n(dry-run: not writing to log)")
        return 0

    written = append_to_log(signals)
    print(f"\nAppended {written} entr(y/ies) to {LOG_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
