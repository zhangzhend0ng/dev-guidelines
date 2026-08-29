#!/usr/bin/env python3
"""Check concise debugging reports for evidence, RCA, and verification fields."""

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "Symptom:",
    "Evidence:",
    "Reproduction:",
    "Root cause:",
    "Fix:",
    "Verification:",
    "Residual risk:",
]

# Design intent: debug reports stay small (≤12 lines). The acceptance check
# is stricter — check_exact_shape's exact-line-count dominates — so no budget
# check runs in main() (iter 21 m1, same fix as check_plan_protocol.py).
LINE_BUDGET = 12
FORBIDDEN_PATTERNS = [
    "probably fixed",
    "seems fine",
    "root cause unknown but",
    "chain of thought",
    "hidden reasoning",
]


def read_input(path):
    if path:
        return Path(path).read_text(encoding="utf-8-sig")  # utf-8-sig: strip BOM if present - a BOM breaks pos-0 anchors/parsers (iter 15/19)
    return sys.stdin.read()


def section_value(text, section):
    # strip: shape checks operate on stripped lines; raw-line startswith made
    # leading-space sections self-contradict (iter 21 m2, same as plan checker)
    for line in text.splitlines():
        if line.strip().startswith(section):
            return line.split(":", 1)[1].strip()
    return ""


def meaningful_lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


def check_exact_shape(lines):
    errors = []
    if len(lines) != len(REQUIRED_SECTIONS):
        errors.append(
            f"debug report must contain exactly {len(REQUIRED_SECTIONS)} non-empty field lines"
        )
    for index, section in enumerate(REQUIRED_SECTIONS):
        if index >= len(lines):
            break
        if not lines[index].startswith(section):
            errors.append(f"line {index + 1} must start with {section}")
    for line in lines:
        if not any(line.startswith(section) for section in REQUIRED_SECTIONS):
            errors.append("extra non-field line is not allowed")
            break
    return errors


def has_command_signal(value):
    # Match a build/test tool name as a command. Trailing boundary is
    # (?=\s|[/.=]|$): a space, a path/flag char, or end of string. We cannot
    # use \b here because g++ ends in non-word chars (+) and \b won't fire
    # after them — so "g++ main.cpp" and bare "g++" both need to match.
    return bool(
        re.search(
            r"\b(python|pytest|cmake|ctest|ninja|clang|gcc|g\+\+|msbuild|lldb|gdb)"
            r"(?=\s|[/.=]|$)",
            value.lower(),
        )
    )


def main():
    parser = argparse.ArgumentParser(description="Check debugging report output")
    parser.add_argument("file", nargs="?", help="Debug report file; stdin if omitted")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    text = read_input(args.file)
    lowered = text.lower()
    errors = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required section: {section}")

    lines = meaningful_lines(text)
    # NOTE: no length-budget check (see check_plan_protocol.py iter 21 m1) —
    # check_exact_shape's exact-line-count dominates; a budget error could
    # never change the verdict.
    errors.extend(check_exact_shape(lines))

    for pattern in FORBIDDEN_PATTERNS:
        if pattern in lowered:
            errors.append(f"forbidden debug report pattern: {pattern}")

    for section in REQUIRED_SECTIONS:
        if not section_value(text, section):
            errors.append(f"empty required section: {section}")

    verification = section_value(text, "Verification:")
    residual = section_value(text, "Residual risk:")
    if verification and not has_command_signal(verification):
        if "not verified" not in verification.lower() and "not verified" not in residual.lower():
            errors.append("verification requires command evidence or NOT VERIFIED note")

    root_cause = section_value(text, "Root cause:").lower()
    if root_cause in {"unknown", "unclear", "n/a", "none"}:
        if "not verified" not in residual.lower() and "next" not in residual.lower():
            errors.append("unknown root cause requires residual risk or next action")

    result = {"pass": not errors, "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}")
    else:
        print("Debug report check passed.")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
