#!/usr/bin/env python3
"""Infer AI protocol check mode from file names and run check_ai_protocol.py.

Filename suffixes:
    *.plan.md, *.plan.output.md -> plan
    *.patch.md, *.patch.output.md -> patch
    *.review.md, *.review.output.md -> review
    *.verification.md, *.verification.output.md -> verification

--json output contract: exactly one file -> the checker's single JSON
object (pass-through). Multiple files -> one JSON array of per-file
objects. (Concatenating objects was invalid JSON — nothing could parse
it, iter 21 m3.)
"""

import argparse
import json
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
    aggregate_json = args.json and len(args.files) > 1
    payloads = []

    for file_name in args.files:
        path = Path(file_name)
        mode = infer_mode(path)
        if not mode:
            print(f"ERROR: cannot infer mode from {path}", file=sys.stderr)
            failures += 1
            if aggregate_json:
                payloads.append(
                    {"file": str(path), "mode": None, "pass": False,
                     "errors": ["cannot infer mode from filename"]}
                )
            continue

        cmd = [sys.executable, str(script), "--mode", mode, str(path)]
        if args.json:
            cmd.append("--json")
        if aggregate_json:
            result = subprocess.run(cmd, check=False, capture_output=True, text=True)
            sys.stderr.write(result.stderr)
            try:
                payloads.append(json.loads(result.stdout))
            except json.JSONDecodeError:
                payloads.append(
                    {"file": str(path), "mode": mode, "pass": False,
                     "errors": ["invalid checker output"]}
                )
        else:
            result = subprocess.run(cmd, check=False)
        if result.returncode != 0:
            failures += 1

    if aggregate_json:
        print(json.dumps(payloads, indent=2))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

