#!/usr/bin/env python3
"""Infer AI protocol check mode from file names and run check_ai_protocol.py.

Filename suffixes:
    *.plan.md, *.plan.output.md -> plan
    *.patch.md, *.patch.output.md -> patch
    *.review.md, *.review.output.md -> review
    *.verification.md, *.verification.output.md -> verification
"""

import argparse
import subprocess
import sys
from pathlib import Path


MODE_SUFFIXES = {
    "plan": [".plan.md", ".plan.output.md"],
    "patch": [".patch.md", ".patch.output.md"],
    "review": [".review.md", ".review.output.md"],
    "verification": [".verification.md", ".verification.output.md"],
}


def infer_mode(path):
    name = path.name
    for mode, suffixes in MODE_SUFFIXES.items():
        if any(name.endswith(suffix) for suffix in suffixes):
            return mode
    return None


def main():
    parser = argparse.ArgumentParser(description="Run AI protocol checks by filename")
    parser.add_argument("files", nargs="+", help="AI output files to check")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    script = Path(__file__).resolve().parent / "check_ai_protocol.py"
    failures = 0

    for file_name in args.files:
        path = Path(file_name)
        mode = infer_mode(path)
        if not mode:
            print(f"ERROR: cannot infer mode from {path}", file=sys.stderr)
            failures += 1
            continue

        cmd = [sys.executable, str(script), "--mode", mode, str(path)]
        if args.json:
            cmd.append("--json")
        result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            failures += 1

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

