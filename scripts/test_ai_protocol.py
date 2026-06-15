#!/usr/bin/env python3
"""Regression tests for AI protocol checking.

Good fixtures must pass. Bad fixtures must fail.
"""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "run_ai_protocol_check.py"
EVALS = ROOT / "docs" / "ai" / "evals" / "weak-model"

GOOD = [
    EVALS / "good-plan.plan.output.md",
    EVALS / "good-patch.patch.output.md",
    EVALS / "good-review.review.output.md",
    EVALS / "good-verification.verification.output.md",
]

BAD = [
    EVALS / "missing-harness.plan.output.md",
    EVALS / "fake-verification.patch.output.md",
    EVALS / "progress-spam.plan.output.md",
    EVALS / "verification-success-without-command.verification.output.md",
    EVALS / "over-budget-verification.verification.output.md",
]


def run(files):
    return subprocess.run(
        [sys.executable, str(CHECK), *[str(path) for path in files]],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def main():
    errors = []

    good = run(GOOD)
    if good.returncode != 0:
        errors.append("good fixtures failed protocol checks")
        print(good.stdout)
        print(good.stderr, file=sys.stderr)

    for bad in BAD:
        result = run([bad])
        if result.returncode == 0:
            errors.append(f"bad fixture unexpectedly passed: {bad}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("AI protocol regression tests passed.")


if __name__ == "__main__":
    main()
