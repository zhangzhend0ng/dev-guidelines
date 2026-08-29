#!/usr/bin/env python3
"""Regression tests for planning and debugging protocol checks."""

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLAN_CHECK = ROOT / "scripts" / "check_plan_protocol.py"
DEBUG_CHECK = ROOT / "scripts" / "check_debug_report.py"

GOOD = [
    (PLAN_CHECK, ROOT / "docs" / "protocols" / "planning" / "good-plan.plan.md"),
    (DEBUG_CHECK, ROOT / "docs" / "protocols" / "debugging" / "good-debug.debug.md"),
]

BAD = [
    (PLAN_CHECK, ROOT / "docs" / "protocols" / "planning" / "bad-plan.plan.md"),
    (DEBUG_CHECK, ROOT / "docs" / "protocols" / "debugging" / "bad-debug.debug.md"),
]

INLINE_BAD = [
    (
        PLAN_CHECK,
        """Goal: Fix one bug
Harnesses: common/planning/task-decomposition.md
Scope: one file
This extra line should fail
Steps: edit
Verification: python scripts/validate.py --json
Stop / escalate: stop on missing harness
""",
    ),
    (
        DEBUG_CHECK,
        """Symptom: crash
Evidence: stack trace
Reproduction:
Root cause: null dereference
Fix: add guard
Verification: ctest --test-dir build
Residual risk: none
""",
    ),
]


def run(script, path):
    return subprocess.run(
        [sys.executable, str(script), str(path)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def run_inline(script, text):
    return subprocess.run(
        [sys.executable, str(script)],
        input=text,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main():
    errors = []

    for script, path in GOOD:
        result = run(script, path)
        if result.returncode != 0:
            errors.append(f"good fixture failed: {path}")
            print(result.stdout)
            print(result.stderr, file=sys.stderr)

    for script, path in BAD:
        result = run(script, path)
        if result.returncode == 0:
            errors.append(f"bad fixture unexpectedly passed: {path}")

    for script, text in INLINE_BAD:
        result = run_inline(script, text)
        if result.returncode == 0:
            errors.append(f"bad inline fixture unexpectedly passed for {script.name}")

    # BOM tolerance (iter 19): BOM before "Goal:" must not false-fail.
    with tempfile.TemporaryDirectory() as tmp:
        for script, source in GOOD:
            bom_path = Path(tmp) / ("bom-" + source.name)
            bom_path.write_bytes(bytes([0xef, 0xbb, 0xbf]) + source.read_bytes())
            result = run(script, bom_path)
            if result.returncode != 0:
                errors.append(f"BOM'd good fixture failed: {source.name}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("Planning and debugging protocol regression tests passed.")


if __name__ == "__main__":
    main()
