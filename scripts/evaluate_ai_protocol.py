#!/usr/bin/env python3
"""Evaluate a directory of weak-model outputs and recommend a capability tier.

Exit codes:
    0 = cases evaluated, all passed
    1 = cases evaluated, at least one failed
    2 = not assessable: directory missing / not a directory, or zero
        AI output files matched (argparse usage errors share exit 2;
        the stderr message distinguishes them). A report is still
        written with recommended_tier: null so humans can inspect it,
        but update_model_registry.py will refuse it.

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
    # NOTE: empty results cannot reach here from main() (it exits 2 first).
    # Returning "T0" for empty input would be a fake signal ("evaluated and
    # worst" vs "never assessed") — do not call this with [].
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
    tier_label = tier if tier is not None else "N/A (0 cases — not assessable)"
    lines = [
        "# AI Protocol Evaluation Report",
        "",
        f"- Total cases: {total}",
        f"- Passed: {passed}",
        f"- Failed: {failed}",
        f"- Recommended tier: {tier_label}",
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
    if not directory.is_dir():
        print(f"ERROR: not a directory or does not exist: {directory}", file=sys.stderr)
        sys.exit(2)
    files = candidate_files(directory)
    results = []
    tier = None
    if not files:
        # Two-state honesty (empty eval): zero matched cases is "not
        # assessable", NOT a scored T0. The old behavior (recommended_tier
        # "T0" + exit 0) was misleading-success and could flow into the
        # persisted model registry via update_model_registry.py.
        print(f"ERROR: no AI output files matched in {directory} (not assessable)", file=sys.stderr)
    else:
        results = [check_file(path) for path in files]
        tier = recommend_tier(results)

    payload = {"recommended_tier": tier, "results": results}
    rendered = json.dumps(payload, indent=2) if args.json else markdown_report(results, tier)

    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)

    if tier is None:
        sys.exit(2)
    sys.exit(1 if any(not item["pass"] for item in results) else 0)


if __name__ == "__main__":
    main()
