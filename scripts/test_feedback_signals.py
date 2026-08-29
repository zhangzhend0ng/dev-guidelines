#!/usr/bin/env python3
"""Regression tests for check_feedback_signals.py (iter 18).

Covers the three bugs found by the iter 17 scan:
- B1: open qualifier vocabulary (orphan / frontmatter / manual text) must
  parse — a closed word list silently dropped 15/24 real log entries.
- B2: an unparseable ### header must flush the pending entry, so a
  following Signal line cannot overwrite the previous entry.
- M1: --threshold < 1 is a usage error (exit 2), never an IndexError.

NOTE on real-log assertions: the log is append-only and monotone, so
lower-bound (">=") assertions are stable; equality assertions would rot
on the next appended entry. The >=3 gap signals for
common-code-review-checklist embed a known producer limitation (orphan
FAILs are attributed to the report's first harness — see
check_review_signals.py harness_files[0][0]); if producer attribution is
fixed later, update that assertion deliberately.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from check_feedback_signals import parse_log  # noqa: E402

SCRIPT = ROOT / "scripts" / "check_feedback_signals.py"
REAL_LOG = ROOT / "common" / "meta" / "harness-feedback-log.md"

SAMPLE = """# Harness Feedback Log

## Entry schema

```
### <YYYY-MM-DD> — <target>, item <N> (or "general")
- **Signal:** gap
```

## Log

### 2026-08-01 — cpp-foo, item 3 (entity classification)
- **Signal:** gap

### 2026-08-02 — cpp-foo, orphan
- **Signal:** gap

### 2026-08-03 — cpp-foo, frontmatter
- **Signal:** misleading

### 2026-08-04 — cpp-bar, item 20/37 (manual)
- **Signal:** under-coverage

### 2026-08-05 — totally-not-an-entry free prose after the comma
- **Signal:** gap

### 2026-08-06 – en-dash-target, general
- **Signal:** inoperable

### 2026-08-07 — bold-target, general
- **Signal:** **gap**

#### 2026-08-08 — drift-target, general
- **Signal:** gap
"""


def main():
    errors = []

    with tempfile.TemporaryDirectory() as tmp:
        log = Path(tmp) / "log.md"
        log.write_text(SAMPLE, encoding="utf-8")
        entries, unparsed = parse_log(log)

        # B1: open vocabulary — 6 parseable entries (prose + #### excluded).
        if len(entries) != 6:
            errors.append(f"expected 7 parsed entries, got {len(entries)}")
        items = {e["harness"]: e["item"] for e in entries}
        for harness, expected in [("cpp-foo", None), ("cpp-bar", None),
                                  ("en-dash-target", None), ("bold-target", None)]:
            if harness not in items:
                errors.append(f"expected entry for {harness!r}, missing")
        cpp_foo = [e for e in entries if e["harness"] == "cpp-foo"]
        got = sorted(e["item"] for e in cpp_foo)
        if got != ["frontmatter", "item 3", "orphan"]:
            errors.append(f"cpp-foo qualifiers wrong: {got}")

        # B2: prose header + #### drift header count as unparsed (after ## Log);
        # their Signal lines must NOT attach to any entry.
        if unparsed != 2:
            errors.append(f"expected 2 unparsed headers, got {unparsed}")
        if any(e["harness"] in ("totally-not-an-entry", "drift-target") for e in entries):
            errors.append("unparseable header leaked into entries")
        bold = next((e for e in entries if e["harness"] == "bold-target"), None)
        if not bold or bold["signal"] != "gap":
            errors.append("bold-target entry missing or signal corrupted")

        # en-dash + bold-value normalization.
        endash = next((e for e in entries if e["harness"] == "en-dash-target"), None)
        if not endash or endash["signal"] != "inoperable":
            errors.append("en-dash header or its signal mis-parsed")

        # M1: threshold < 1 is a usage error, never a crash.
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--threshold", "0", "--json"],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        if result.returncode != 2:
            errors.append(f"--threshold 0 expected exit 2, got {result.returncode}")

    # Real log: structural, lower-bound assertions (append-only monotone).
    entries, unparsed = parse_log(REAL_LOG)
    if unparsed != 0:
        errors.append(f"real log has {unparsed} unparsed header(s) — format drift")
    if len(entries) < 20:
        errors.append(f"real log entries dropped: only {len(entries)} (was 24)")
    orphan_items = {e["item"] for e in entries}
    # "orphan" is present in real data; "frontmatter" is producer vocabulary
    # (check_review_signals.py:305) with no current real instance — it is
    # covered by the synthetic sample above instead.
    if "orphan" not in orphan_items:
        errors.append(f"real log missing orphan qualifier; got {sorted(orphan_items)}")
    # iter 23: orphan signals are retargeted to the "orphan" pseudo-target
    # (unframed FAILs from multi-harness reviews); ccc/AGENTS no longer
    # receive misattributed entries. Lower bound: append-only log.
    orphan_e = [e for e in entries if e["harness"] == "orphan" and e["signal"] == "gap"]
    if len(orphan_e) < 10:
        errors.append(f"orphan pseudo-target gap signals {len(orphan_e)} < 10 "
                      "(retargeted entries lost by the parser?)")
    if any(e["harness"] == "AGENTS" for e in entries):
        errors.append("misattributed 'AGENTS' target resurfaced in the log")
    flagged = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    payload = json.loads(flagged.stdout)
    if payload.get("total_entries", 0) < 20:
        errors.append("CLI JSON total_entries regressed")
    if payload.get("unparsed_headers") != 0:
        errors.append("CLI JSON reports unparsed headers on healthy log")
    names = {f["harness"] for f in payload.get("flagged_for_rereview", [])}
    if "orphan" not in names:
        errors.append("orphan pseudo-target not flagged_for_rereview")
    if "common-code-review-checklist" in names or "AGENTS" in names:
        errors.append("misattributed re-review flag resurfaced (ccc/AGENTS)")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("Feedback signals regression tests passed.")


if __name__ == "__main__":
    main()
