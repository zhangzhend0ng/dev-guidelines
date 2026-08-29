#!/usr/bin/env python3
"""Check concise task plans for required harness-driven planning fields."""

import argparse
import json
import sys
from pathlib import Path


REQUIRED_SECTIONS = [
    "Goal:",
    "Harnesses:",
    "Scope:",
    "Steps:",
    "Verification:",
    "Stop / escalate:",
]

# Design intent: plans are ≤8-line minimal documents
# (docs/ai-evaluation-research-2026-08-04.md). The acceptance check is
# stricter — check_exact_shape enforces exactly len(REQUIRED_SECTIONS)
# lines — so no budget check exists in main() (iter 21 m1).
LINE_BUDGET = 8
FORBIDDEN_PATTERNS = [
    "chain of thought",
    "hidden reasoning",
    "let me think",
    "everything in the repo",
    "full rewrite",
]


def read_input(path):
    if path:
        return Path(path).read_text(encoding="utf-8-sig")  # utf-8-sig: strip BOM if present - a BOM breaks pos-0 anchors/parsers (iter 15/19)
    return sys.stdin.read()


def section_value(text, section):
    # strip: shape checks operate on stripped lines (meaningful_lines); using
    # raw lines here made "  Harnesses: x" pass the shape check yet report
    # "empty required section" — a self-contradiction (iter 21 m2).
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
            f"plan must contain exactly {len(REQUIRED_SECTIONS)} non-empty field lines"
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


def main():
    parser = argparse.ArgumentParser(description="Check planning protocol output")
    parser.add_argument("file", nargs="?", help="Plan file; stdin if omitted")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    text = read_input(args.file)
    lowered = text.lower()
    errors = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"missing required section: {section}")

    lines = meaningful_lines(text)
    # NOTE: no length-budget check here. LINE_BUDGET (8) is design intent,
    # but check_exact_shape below enforces exactly 6 non-empty field lines
    # and dominates any larger count — a budget error could never change the
    # verdict, only add noise (iter 21 m1).

    errors.extend(check_exact_shape(lines))

    for pattern in FORBIDDEN_PATTERNS:
        if pattern in lowered:
            errors.append(f"forbidden planning pattern: {pattern}")

    if not section_value(text, "Harnesses:"):
        errors.append("empty required section: Harnesses:")
    if not section_value(text, "Verification:"):
        errors.append("empty required section: Verification:")
    if not section_value(text, "Stop / escalate:"):
        errors.append("empty required section: Stop / escalate:")

    result = {"pass": not errors, "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}")
    else:
        print("Planning protocol check passed.")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
