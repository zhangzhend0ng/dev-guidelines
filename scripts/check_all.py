#!/usr/bin/env python3
"""Run all repository health checks in one command.

Combines:
  - validate.py (frontmatter, xref, id uniqueness, staleness)
  - generate_index.py --check (INDEX.md sync)
  - check_feedback_signals.py (feedback log accumulation)
  - check_review_signals.py --audit-harnesses (harness tier inflation)

Exit code is non-zero if any sub-check fails. Output is prefixed per check
so failures are easy to locate.

Usage:
    python scripts/check_all.py
    python scripts/check_all.py --stale   # include staleness check
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT  # this script lives in scripts/


def run(name, script_and_args, stale=False, capture=False):
    """script_and_args: list where first element is the script filename,
    remaining elements are CLI args to that script.

    capture: if True, do not inherit stdout to the terminal and instead return
    the captured text (used for advisory checks whose findings must be surfaced
    in the SUMMARY rather than only in scrollback).
    """
    print(f"\n=== {name} ===", flush=True)
    script_path = str(SCRIPTS / script_and_args[0])
    args = [sys.executable, script_path] + list(script_and_args[1:])
    if stale and "validate.py" in script_and_args[0]:
        args.append("--stale")
    result = subprocess.run(
        args, cwd=str(ROOT.parent),
        capture_output=capture, text=True,
    )
    if capture and result.stdout:
        print(result.stdout, end="")
    # Normalize: any non-zero returncode is a failure (bool), avoid bit-OR of values like 2/4
    return 0 if result.returncode == 0 else 1, result.stdout if capture else ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--stale", action="store_true", help="include staleness check in validate.py")
    args = ap.parse_args()

    failures = []
    advisory_notes = []  # (script_name, findings_text) for non-blocking findings
    for name, cmd in [
        ("validate.py", ["validate.py"]),
        ("generate_index.py --check", ["generate_index.py", "--check"]),
        ("check_feedback_signals.py", ["check_feedback_signals.py"]),
        # --dry-run: a health check must not mutate a tracked file. The audit
        # is advisory (exit 0); we capture its stdout to surface findings in the
        # SUMMARY rather than only in scrollback.
        ("check_review_signals.py --audit-harnesses",
         ["check_review_signals.py", "--audit-harnesses", "--dry-run"]),
    ]:
        capture = "check_review_signals.py" in cmd[0]
        rc, out = run(name, cmd, stale=args.stale, capture=capture)
        if rc != 0:
            failures.append(name)
        # The audit is advisory: even at exit 0 it may report tier inflation.
        # Extract the per-harness finding lines so the SUMMARY mentions them.
        if capture and "Detected" in out and "tier inflation" in out:
            findings = [ln for ln in out.splitlines()
                        if ln.strip().startswith("- ")]
            if findings:
                advisory_notes.append((name, findings))

    print(f"\n=== SUMMARY ===", flush=True)
    if advisory_notes:
        for sname, findings in advisory_notes:
            print(f"Advisory findings from {sname}:")
            for f in findings:
                print(f"  {f}")
        print()
    if not failures and not advisory_notes:
        print("All checks passed.")
        return 0
    if not failures and advisory_notes:
        print("All checks passed (with advisory findings above).")
        return 0
    print(f"Failed: {', '.join(failures)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
