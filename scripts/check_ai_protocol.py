#!/usr/bin/env python3
"""Check weak-model AI outputs for required protocol sections and line budgets.

Usage:
    python scripts/check_ai_protocol.py --mode plan < output.md
    python scripts/check_ai_protocol.py --mode patch output.md --json
    python scripts/check_ai_protocol.py --mode review output.md
    python scripts/check_ai_protocol.py --mode verification output.md
"""

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = {
    "plan": [
        "Objective:",
        "Applicable harnesses:",
        "Applicable checklist items:",
        "Patch plan:",
        "Verification plan:",
        "Risks / NOT VERIFIED:",
    ],
    "patch": [
        "Files changed:",
        "Harness checks:",
        "Verification run:",
        "Failures / NOT VERIFIED:",
        "Residual risks:",
    ],
    "review": [
        "Blocking findings:",
        "High findings:",
        "Suggestions:",
        "Harness coverage:",
        "Verdict:",
    ],
    "verification": [
        "Verification run:",
        "Result:",
        "Failures / NOT VERIFIED:",
        "Next action:",
    ],
}

LINE_BUDGETS = {
    "plan": 6,
    "patch": 10,
    "review": 20,
    "verification": 8,
}

FORBIDDEN_PATTERNS = [
    "chain of thought",
    "hidden reasoning",
    "let me think",
    "i will now think",
]

SUCCESS_PATTERNS = [
    "passed",
    "success",
    "successful",
    "verified",
    "all good",
]


def read_input(path):
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def check_sections(text, mode):
    missing = [section for section in REQUIRED_SECTIONS[mode] if section not in text]
    return missing


def check_budget(text, mode):
    meaningful = [line for line in text.splitlines() if line.strip()]
    limit = LINE_BUDGETS[mode]
    if len(meaningful) > limit:
        return f"{len(meaningful)} non-empty lines exceeds {mode} budget {limit}"
    return None


def check_noise(text):
    lowered = text.lower()
    return [pattern for pattern in FORBIDDEN_PATTERNS if pattern in lowered]


def section_value(text, section):
    for line in text.splitlines():
        if line.startswith(section):
            return line.split(":", 1)[1].strip()
    return ""


def check_non_empty_sections(text, mode):
    errors = []
    if mode == "plan":
        for section in ["Applicable harnesses:", "Verification plan:"]:
            if not section_value(text, section):
                errors.append(f"empty required section: {section}")
    if mode == "patch":
        if not section_value(text, "Files changed:"):
            errors.append("empty required section: Files changed:")
    if mode == "verification":
        verification = section_value(text, "Verification run:")
        not_verified = section_value(text, "Failures / NOT VERIFIED:")
        if not verification and "not verified" not in not_verified.lower():
            errors.append("empty Verification run requires NOT VERIFIED explanation")
    return errors


def check_review_findings(text, mode):
    if mode != "review":
        return []

    errors = []
    lowered = text.lower()
    verdict = section_value(text, "Verdict:").lower()
    coverage = section_value(text, "Harness coverage:").lower()

    if "approve" in verdict and (not coverage or "not verified" in coverage):
        errors.append("APPROVE verdict requires verified harness coverage")

    finding_lines = []
    capture = False
    for line in text.splitlines():
        if line.startswith(("Blocking findings:", "High findings:", "Suggestions:")):
            capture = True
            value = line.split(":", 1)[1].strip()
            if value and value.lower() not in {"none", "n/a"}:
                finding_lines.append(value)
            continue
        if line.startswith(("Harness coverage:", "Verdict:")):
            capture = False
        elif capture and line.strip():
            finding_lines.append(line.strip())

    for finding in finding_lines:
        if finding.lower() in {"none", "n/a"}:
            continue
        if not re.search(r"[\w./\\-]+:\d+", finding):
            errors.append("review finding lacks file:line citation")
            break

    if "finding" in lowered and "harness" not in lowered:
        errors.append("review mentions findings without harness reference")

    return errors


def check_verification_claims(text, mode):
    if mode not in {"patch", "verification"}:
        return []

    lowered = text.lower()
    has_success_claim = any(pattern in lowered for pattern in SUCCESS_PATTERNS)
    has_not_verified = False
    for line in text.splitlines():
        lowered_line = line.lower()
        if lowered_line.startswith("failures / not verified:"):
            value = line.split(":", 1)[1].strip().lower()
            if "not verified" in value:
                has_not_verified = True
        elif "not verified" in lowered_line and not lowered_line.startswith(
            "failures / not verified:"
        ):
            has_not_verified = True
    verification_line_has_value = any(
        line.lower().startswith("verification run:") and line.split(":", 1)[1].strip()
        for line in text.splitlines()
    )
    has_command_signal = verification_line_has_value or any(
        signal in lowered
        for signal in [
            "python ",
            "cmake",
            "ctest",
            "ninja",
            "clang",
            "gcc",
            "msbuild",
        ]
    )

    if has_success_claim and not has_command_signal and not has_not_verified:
        return ["success claim without command evidence or NOT VERIFIED"]
    return []


def main():
    parser = argparse.ArgumentParser(description="Check AI protocol output")
    parser.add_argument("file", nargs="?", help="Output file to check; stdin if omitted")
    parser.add_argument("--mode", choices=sorted(REQUIRED_SECTIONS), required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    text = read_input(args.file)
    errors = []

    missing = check_sections(text, args.mode)
    for section in missing:
        errors.append(f"missing required section: {section}")

    budget_error = check_budget(text, args.mode)
    if budget_error:
        errors.append(budget_error)

    for pattern in check_noise(text):
        errors.append(f"forbidden noise pattern: {pattern}")

    for error in check_non_empty_sections(text, args.mode):
        errors.append(error)

    for error in check_review_findings(text, args.mode):
        errors.append(error)

    for error in check_verification_claims(text, args.mode):
        errors.append(error)

    result = {
        "pass": not errors,
        "mode": args.mode,
        "errors": errors,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
        else:
            print("AI protocol check passed.")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
