#!/usr/bin/env python3
"""Regression tests for AI protocol checking.

Good fixtures must pass. Bad fixtures must fail.
"""

import json
import subprocess
import sys
import tempfile
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


EVALUATE = ROOT / "scripts" / "evaluate_ai_protocol.py"
REGISTRY_TOOL = ROOT / "scripts" / "update_model_registry.py"
GOOD_RUNS = EVALS / "good-runs"


def run_eval(*args):
    return subprocess.run(
        [sys.executable, str(EVALUATE), *[str(a) for a in args]],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_evaluate(errors):
    """evaluate_ai_protocol exit contract (iter 16).

    0 = all pass; 1 = some fail; 2 = not assessable (empty/missing dir).
    Empty input must NOT yield a fake "T0" + exit 0 (misleading success
    that could flow into the persisted model registry).
    """
    ok = run_eval(GOOD_RUNS, "--json")
    if ok.returncode != 0 or '"recommended_tier": "T2"' not in ok.stdout:
        errors.append(f"good-runs eval expected T2/exit 0, got exit {ok.returncode}")

    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp) / "empty"
        empty.mkdir()
        result = run_eval(empty, "--json")
        if result.returncode != 2:
            errors.append(f"empty-dir eval expected exit 2 (not assessable), got {result.returncode}")
        if '"recommended_tier": null' not in result.stdout:
            errors.append("empty-dir eval JSON must carry recommended_tier: null (no fake T0)")
        if "not assessable" not in result.stderr:
            errors.append("empty-dir eval stderr must explain not-assessable")

        missing = run_eval(Path(tmp) / "does-not-exist", "--json")
        if missing.returncode != 2:
            errors.append(f"missing-dir eval expected exit 2, got {missing.returncode}")
        if "not a directory" not in missing.stderr:
            errors.append("missing-dir eval stderr must say 'not a directory or does not exist'")

        # update_model_registry: report missing recommended_tier must be
        # rejected (old code silently defaulted to T0 and wrote a row).
        # parser.error fires before REGISTRY is touched, so no cleanup needed.
        report = Path(tmp) / "report.json"
        report.write_text('{"results": []}', encoding="utf-8")
        reg = subprocess.run(
            [sys.executable, str(REGISTRY_TOOL), "--model", "t", "--version", "0", "--report", str(report)],
            check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        if reg.returncode != 2 or "recommended_tier" not in reg.stderr:
            errors.append(f"registry update with tier-less report expected exit 2, got {reg.returncode}")

    # exit 1 = cases evaluated, at least one failed (documented contract,
    # iter 29 item-3 audit found it untested). Copy one bad fixture into an
    # otherwise-empty dir so evaluate has exactly one case, which fails.
    with tempfile.TemporaryDirectory() as tmp:
        case_dir = Path(tmp) / "cases"
        case_dir.mkdir()
        (case_dir / BAD[0].name).write_bytes(BAD[0].read_bytes())
        failing = run_eval(case_dir, "--json")
        if failing.returncode != 1:
            errors.append(f"eval with a failing case expected exit 1, got {failing.returncode}")
        if '"pass": false' not in failing.stdout:
            errors.append("eval JSON must carry the failing case (pass: false)")


def test_bom(errors):
    """A UTF-8 BOM before the content must not fail protocol checks (iter 19).

    Windows editors emit BOMs; a BOM before "Goal:" broke the pos-0 anchor
    and false-failed a perfectly good plan (iter 15 fixed harness parsers,
    this covers the AI-output reader path).
    """
    with tempfile.TemporaryDirectory() as tmp:
        bom_file = Path(tmp) / "bom-plan.plan.output.md"
        bom_file.write_bytes(
            bytes([0xef, 0xbb, 0xbf]) + GOOD[0].read_bytes()
        )
        result = run([bom_file])
        if result.returncode != 0:
            errors.append("BOM'd good plan fixture failed protocol checks")


WRAPPER = ROOT / "scripts" / "run_ai_protocol_check.py"


def test_wrapper_json(errors):
    """run_ai_protocol_check --json contract (iter 21 m3).

    One file -> single JSON object (back-compat). Multiple files -> one
    JSON array (concatenated objects were unparseable).
    """
    one = subprocess.run(
        [sys.executable, str(WRAPPER), str(GOOD[0]), "--json"],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    try:
        payload = json.loads(one.stdout)
    except json.JSONDecodeError:
        errors.append("single-file --json is not a valid JSON object")
    else:
        if not isinstance(payload, dict):
            errors.append("single-file --json must stay a single object")

    many = subprocess.run(
        [sys.executable, str(WRAPPER), *[str(p) for p in GOOD[:3]], "--json"],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    try:
        payload = json.loads(many.stdout)
    except json.JSONDecodeError:
        errors.append("multi-file --json is not a valid JSON document")
    else:
        if not (isinstance(payload, list) and len(payload) == 3):
            errors.append("multi-file --json must be an array of 3 objects")

    # aggregate mode must still count failures into the exit code
    mixed = subprocess.run(
        [sys.executable, str(WRAPPER), str(GOOD[0]), str(BAD[0]), "--json"],
        check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    if mixed.returncode != 1:
        errors.append(f"aggregate --json with a bad fixture expected exit 1, got {mixed.returncode}")


def test_leading_space_section(errors):
    """m2 family, third site (iter 25): an indented field line must not be
    'present but empty' - presence is substring-based, extraction now strips.
    """
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "ls.plan.output.md"
        lines = [
            b"Objective: Fix one bug",
            b" Applicable harnesses: common/planning/task-decomposition.md",
            b"Applicable checklist items: item 1",
            b"Patch plan: edit one file",
            b"Verification plan: run tests",
            b"Risks / NOT VERIFIED: none",
        ]
        p.write_bytes(b"\r\n".join(lines) + b"\r\n")
        result = run([p])
        if result.returncode != 0:
            errors.append(f"leading-space plan section rejected: {result.stdout.strip()}")


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

    test_evaluate(errors)
    test_bom(errors)
    test_wrapper_json(errors)
    test_leading_space_section(errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("AI protocol regression tests passed.")


if __name__ == "__main__":
    main()
