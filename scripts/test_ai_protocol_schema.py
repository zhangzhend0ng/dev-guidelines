#!/usr/bin/env python3
"""Regression tests for the JSON output contracts (Phase 3).

Covers:
- good-runs markdown samples convert to schema-conformant JSON and pass
  `check_ai_protocol.py --schema` in all four modes
- markdown mode regression: the same samples still pass the unchanged
  markdown checks
- negatives: missing required property, unknown property, empty minItems,
  budget overflow, finding without file:line citation, empty
  verification_run without NOT VERIFIED, APPROVE without coverage,
  forbidden noise
- markdown-embedded JSON (```json fenced block) is extracted and checked
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKER = ROOT / "scripts" / "check_ai_protocol.py"
GOOD_RUNS = ROOT / "docs" / "ai" / "evals" / "weak-model" / "good-runs"
SCHEMAS = ROOT / "docs" / "ai" / "schemas"

CITATION_RE = re.compile(r"[\w./\\-]+:\d+")

SECTIONS = {
    "plan": ["Objective:", "Applicable harnesses:", "Applicable checklist items:",
             "Patch plan:", "Verification plan:", "Risks / NOT VERIFIED:"],
    "patch": ["Files changed:", "Harness checks:", "Verification run:",
              "Failures / NOT VERIFIED:", "Residual risks:"],
    "verification": ["Verification run:", "Result:",
                     "Failures / NOT VERIFIED:", "Next action:"],
}
FINDING_SECTIONS = ["Blocking findings:", "High findings:", "Suggestions:"]


def md_to_contract(mode, text):
    """Convert a good-runs style markdown output into the JSON contract."""
    doc = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Za-z][A-Za-z /]+?):\s*(.*)$", line)
        if not m:
            continue
        section, value = m.group(1), m.group(2).strip()
        if mode == "review":
            if section in ("Blocking findings", "High findings", "Suggestions"):
                key = ("blocking_findings" if section.startswith("Blocking")
                       else "high_findings" if section.startswith("High")
                       else "suggestions")
                if value.lower() in ("none", "n/a", ""):
                    doc[key] = []
                else:
                    cite = CITATION_RE.search(value)
                    doc[key] = [{"text": value, "citation": cite.group(0) if cite else "x.md:1"}]
            elif section == "Harness coverage":
                doc["harness_coverage"] = [value]
            elif section == "Verdict":
                doc["verdict"] = value
            continue
        key = {
            "Objective": "objective",
            "Applicable harnesses": "applicable_harnesses",
            "Applicable checklist items": "applicable_checklist_items",
            "Patch plan": "patch_plan",
            "Verification plan": "verification_plan",
            "Risks / NOT VERIFIED": "risks_not_verified",
            "Files changed": "files_changed",
            "Harness checks": "harness_checks",
            "Verification run": "verification_run",
            "Failures / NOT VERIFIED": "failures_not_verified",
            "Residual risks": "residual_risks",
            "Result": "result",
            "Next action": "next_action",
        }.get(section)
        if key:
            doc[key] = [value] if value else []
    return doc


def run_checker(mode, schema, payload_or_text):
    if isinstance(payload_or_text, str):
        inp = payload_or_text
    else:
        inp = json.dumps(payload_or_text, indent=2)
    args = [sys.executable, str(CHECKER), "--mode", mode]
    if schema:
        args += ["--schema", str(SCHEMAS / f"{mode}.schema.json")]
    return subprocess.run(args, input=inp, capture_output=True, text=True,
                          check=False)


def expect_pass(errors, mode, payload_or_text, label):
    r = run_checker(mode, True, payload_or_text)
    if r.returncode != 0:
        errors.append(f"{label}: expected pass, got rc={r.returncode} "
                      f"errors={r.stdout.strip()}")


def expect_markdown_pass(errors, mode, text, label):
    r = run_checker(mode, False, text)
    if r.returncode != 0:
        errors.append(f"{label}: expected pass, got rc={r.returncode} "
                      f"errors={r.stdout.strip()}")


def expect_fail(errors, mode, payload, label, needle=None):
    r = run_checker(mode, True, payload)
    if r.returncode == 0:
        errors.append(f"{label}: expected fail, but passed")
        return
    if needle and needle not in r.stdout:
        errors.append(f"{label}: expected error containing {needle!r}, "
                      f"got {r.stdout.strip()!r}")


def main():
    errors = []

    # A/B: good-runs samples pass BOTH contract modes.
    for path in sorted(GOOD_RUNS.glob("*.md")):
        mode = path.name.split(".")[1]  # good-plan.plan.output.md -> plan
        text = path.read_text(encoding="utf-8-sig")
        expect_pass(errors, mode, md_to_contract(mode, text),
                    f"schema mode {path.name}")
        expect_markdown_pass(errors, mode, text, f"markdown regression {path.name}")

    base_plan = {
        "objective": ["Fix one bounded issue."],
        "applicable_harnesses": ["cpp/memory/ownership.md"],
        "applicable_checklist_items": ["ownership selection"],
        "patch_plan": ["smallest fix in approved file"],
        "verification_plan": ["python scripts/validate.py"],
        "risks_not_verified": ["behavior unverified"],
    }
    expect_pass(errors, "plan", base_plan, "plan baseline")

    # C1: missing required property.
    bad = {k: v for k, v in base_plan.items() if k != "applicable_harnesses"}
    expect_fail(errors, "plan", bad, "missing required",
                "missing required property 'applicable_harnesses'")

    # C2: budget overflow (7 contract lines > plan budget 6).
    over = dict(base_plan, objective=["a", "b"], patch_plan=["c", "d"],
                risks_not_verified=["e", "f"])
    expect_fail(errors, "plan", over, "budget overflow", "budget 6")

    # C10: unknown property.
    expect_fail(errors, "plan", dict(base_plan, extra=["x"]),
                "unknown property", "unexpected property 'extra'")

    # C8: forbidden noise.
    expect_fail(errors, "plan",
                dict(base_plan, objective=["let me think about it"]),
                "noise pattern", "forbidden noise pattern")

    # C3: empty minItems (files_changed).
    expect_fail(errors, "patch",
                {"files_changed": [], "harness_checks": ["ok"],
                 "verification_run": ["python scripts/validate.py"],
                 "failures_not_verified": [], "residual_risks": []},
                "empty files_changed", "at least 1 item")

    # C6: finding without file:line citation.
    expect_fail(errors, "review",
                {"blocking_findings": [{"text": "raw pointer", "citation": "no line"}],
                 "high_findings": [], "suggestions": [],
                 "harness_coverage": ["ownership checked"], "verdict": "REQUEST CHANGES"},
                "citation pattern", "does not match pattern")

    # C7: APPROVE without coverage.
    expect_fail(errors, "review",
                {"blocking_findings": [], "high_findings": [], "suggestions": [],
                 "harness_coverage": [], "verdict": "APPROVE"},
                "approve without coverage", "APPROVE verdict requires verified")

    # findings require coverage.
    expect_fail(errors, "review",
                {"blocking_findings": [{"text": "x", "citation": "a.cpp:1"}],
                 "high_findings": [], "suggestions": [],
                 "harness_coverage": [], "verdict": "REQUEST CHANGES"},
                "findings without coverage", "findings require harness coverage")

    # C4: empty verification_run without NOT VERIFIED.
    expect_fail(errors, "verification",
                {"verification_run": [], "result": ["pass"],
                 "failures_not_verified": ["nothing went wrong"],
                 "next_action": ["ship"]},
                "empty run without NOT VERIFIED", "empty verification_run")

    # C5: empty verification_run WITH explicit NOT VERIFIED passes.
    expect_pass(errors, "verification",
                {"verification_run": [], "result": ["not run"],
                 "failures_not_verified": ["NOT VERIFIED: no command available"],
                 "next_action": ["request environment"]},
                "empty run with NOT VERIFIED")

    # C9: markdown-embedded JSON is extracted.
    fenced = ("Here is the structured result:\n\n```json\n"
              + json.dumps(base_plan, indent=2) + "\n```\n\nEnd of report.")
    expect_pass(errors, "plan", fenced, "fenced JSON extraction")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("AI protocol schema tests passed "
          "(4 good-runs x 2 modes + baseline + 2 fence/regression + 8 negatives).")


if __name__ == "__main__":
    main()
