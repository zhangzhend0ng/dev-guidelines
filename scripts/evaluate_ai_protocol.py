#!/usr/bin/env python3
"""Evaluate a directory of weak-model outputs and recommend a capability tier.

Usage:
    python scripts/evaluate_ai_protocol.py docs/ai/evals/weak-model/good-runs
    python scripts/evaluate_ai_protocol.py outputs/dsv4pro-2026-06-15 --json
    python scripts/evaluate_ai_protocol.py outputs/dsv4pro --output report.md
"""

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from run_ai_protocol_check import infer_mode


ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "scripts" / "check_ai_protocol.py"


def candidate_files(directory):
    files = []
    for path in sorted(directory.rglob("*.md")):
        if infer_mode(path):
            files.append(path)
    return files


def check_file(path):
    mode = infer_mode(path)
    result = subprocess.run(
        [sys.executable, str(CHECK), "--mode", mode, str(path), "--json"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {"pass": False, "mode": mode, "errors": ["invalid checker output"]}
    return {
        "file": str(path),
        "mode": mode,
        "pass": result.returncode == 0 and payload.get("pass") is True,
        "errors": payload.get("errors", []),
    }


def recommend_tier(results):
    if not results:
        return "T0"

    by_mode = Counter(item["mode"] for item in results if item["pass"])
    failed = [item for item in results if not item["pass"]]

    if failed:
        if by_mode.get("plan", 0) > 0:
            return "T1"
        return "T0"

    modes = {item["mode"] for item in results}
    if {"plan", "patch", "review", "verification"}.issubset(modes):
        return "T2"
    if "plan" in modes:
        return "T1"
    return "T0"


def markdown_report(results, tier):
    total = len(results)
    passed = sum(1 for item in results if item["pass"])
    failed = total - passed
    lines = [
        "# AI Protocol Evaluation Report",
        "",
        f"- Total cases: {total}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        f"- Recommended tier: {tier}",
        "",
        "| File | Mode | Result | Errors |",
        "|------|------|--------|--------|",
    ]
    for item in results:
        status = "pass" if item["pass"] else "fail"
        errors = "; ".join(item["errors"]) if item["errors"] else ""
        lines.append(f"| {item['file']} | {item['mode']} | {status} | {errors} |")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Evaluate weak-model AI outputs")
    parser.add_argument("directory", help="Directory containing AI output markdown files")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", help="Write report to this file")
    args = parser.parse_args()

    directory = Path(args.directory)
    files = candidate_files(directory)
    results = [check_file(path) for path in files]
    tier = recommend_tier(results)

    payload = {"recommended_tier": tier, "results": results}
    rendered = json.dumps(payload, indent=2) if args.json else markdown_report(results, tier)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    sys.exit(1 if any(not item["pass"] for item in results) else 0)


if __name__ == "__main__":
    main()
