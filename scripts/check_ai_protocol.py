#!/usr/bin/env python3
"""Check weak-model AI outputs for required protocol sections and line budgets.

Usage:
    python scripts/check_ai_protocol.py --mode plan < output.md
    python scripts/check_ai_protocol.py --mode patch output.md --json
    python scripts/check_ai_protocol.py --mode review output.md
    python scripts/check_ai_protocol.py --mode verification output.md
    python scripts/check_ai_protocol.py --mode plan --schema docs/ai/schemas/plan.schema.json output.json

--schema switches to the JSON contract mode: the input must be a pure JSON
document (or markdown with a ```json fenced block) conforming to
docs/ai/schemas/<mode>.schema.json. The markdown checks above are unchanged
and remain the default.
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

# Command evidence: a tool name must look like an INVOCATION, not a prose
# mention or a line-ending name-drop. Require the tool to be followed on
# the SAME LINE by an argument/path char ( '/', '.', '=', or a space then
# more non-space content). This blocks "will use cmake" (name-drop at end
# of a residual-risk line) and "the cmake build" (bare prose mention) while
# accepting "python scripts/validate.py", "cmake --build", "ctest --test-dir".
# Note: \s in lookahead would match the trailing newline, so we require a
# space followed by at least one more character on the same line.
COMMAND_EVIDENCE_RE = re.compile(
    r"\b(python|python3|pytest|cmake|ctest|ninja|clang|gcc|g\+\+|msbuild|lldb|gdb)"
    r"(?=(?:[/.=]| +\S))"
)


def read_input(path):
    if path:
        return Path(path).read_text(encoding="utf-8-sig")  # utf-8-sig: strip BOM if present - a BOM breaks pos-0 anchors/parsers (iter 15/19)
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
    # strip: presence checks are substring-based; raw-line startswith made an
    # indented section "present but empty" (iter 21 m2 family, third site)
    for line in text.splitlines():
        if line.strip().startswith(section):
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
    # Command evidence regex is module-level COMMAND_EVIDENCE_RE (shared with
    # the --schema JSON mode).
    has_command_signal = verification_line_has_value or bool(
        COMMAND_EVIDENCE_RE.search(lowered)
    )

    if has_success_claim and not has_command_signal and not has_not_verified:
        return ["success claim without command evidence or NOT VERIFIED"]
    return []


def extract_json(text):
    """Pure JSON document, or the first ```json fenced block inside markdown."""
    fence = re.search(r"```(?:json)?\s*\n(.*?)```", text, re.DOTALL)
    candidates = ([fence.group(1)] if fence else []) + [text]
    last = None
    for candidate in candidates:
        try:
            return json.loads(candidate), None
        except json.JSONDecodeError as e:
            last = e
    return None, (
        "no parsable JSON (expected a ```json fenced block or a pure JSON "
        f"document): {last}"
    )


def _resolve_ref(root, ref):
    node = root
    for part in ref[2:].split("/"):
        node = node.get(part, {})
    return node


def validate_against_schema(obj, schema, root, path="$"):
    """Minimal JSON Schema validator: only the keyword subset used by
    docs/ai/schemas/ (type, properties, required, additionalProperties,
    items, minItems, pattern, $ref). Deliberately stdlib-only - adding a
    jsonschema dependency needs separate approval (change-scope-control 3)."""
    if "$ref" in schema:
        return validate_against_schema(obj, _resolve_ref(root, schema["$ref"]), root, path)
    t = schema.get("type")
    if t == "object":
        if not isinstance(obj, dict):
            return [f"{path}: expected object"]
        errors = []
        for req in schema.get("required", []):
            if req not in obj:
                errors.append(f"{path}: missing required property '{req}'")
        if schema.get("additionalProperties") is False:
            for key in obj:
                if key not in schema.get("properties", {}):
                    errors.append(f"{path}: unexpected property '{key}'")
        for key, sub in schema.get("properties", {}).items():
            if key in obj:
                errors.extend(validate_against_schema(obj[key], sub, root, f"{path}.{key}"))
        return errors
    if t == "array":
        if not isinstance(obj, list):
            return [f"{path}: expected array"]
        errors = []
        if "minItems" in schema and len(obj) < schema["minItems"]:
            errors.append(
                f"{path}: needs at least {schema['minItems']} item(s), got {len(obj)}"
            )
        items = schema.get("items")
        if items:
            for i, v in enumerate(obj):
                errors.extend(validate_against_schema(v, items, root, f"{path}[{i}]"))
        return errors
    if t == "string":
        if not isinstance(obj, str):
            return [f"{path}: expected string"]
        if "pattern" in schema and not re.search(schema["pattern"], obj):
            return [f"{path}: {obj!r} does not match pattern {schema['pattern']!r}"]
        return []
    return []


def _iter_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _iter_strings(v)


def _count_contract_lines(payload):
    total = 0
    for v in payload.values():
        if isinstance(v, list):
            total += len(v)
        elif isinstance(v, str) and v.strip():
            total += 1
    return total


def schema_mode_errors(text, mode, schema_path):
    """JSON contract checks: schema conformance + budget + ported semantics."""
    errors = []
    try:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"unreadable schema {schema_path}: {e}"]

    payload, err = extract_json(text)
    if err:
        return [err]

    errors.extend(validate_against_schema(payload, schema, schema))

    budget = LINE_BUDGETS[mode]
    lines = _count_contract_lines(payload)
    if lines > budget:
        errors.append(f"{lines} contract lines exceeds {mode} budget {budget}")

    lowered = "\n".join(_iter_strings(payload)).lower()
    for pattern in check_noise(lowered):
        errors.append(f"forbidden noise pattern: {pattern}")

    if mode in ("patch", "verification"):
        has_success = any(p in lowered for p in SUCCESS_PATTERNS)
        has_not_verified = "not verified" in "\n".join(
            _iter_strings(payload.get("failures_not_verified", []))
        ).lower()
        has_signal = bool(payload.get("verification_run")) or bool(
            COMMAND_EVIDENCE_RE.search(lowered)
        )
        if has_success and not has_signal and not has_not_verified:
            errors.append("success claim without command evidence or NOT VERIFIED")

    if mode == "verification":
        run = payload.get("verification_run", [])
        not_verified = "not verified" in "\n".join(
            _iter_strings(payload.get("failures_not_verified", []))
        ).lower()
        if not run and not not_verified:
            errors.append(
                "empty verification_run requires a 'not verified' entry in "
                "failures_not_verified"
            )

    if mode == "review":
        verdict = str(payload.get("verdict", ""))
        coverage = payload.get("harness_coverage", [])
        cov = "\n".join(_iter_strings(coverage)).lower()
        if "approve" in verdict.lower() and (not cov or "not verified" in cov):
            errors.append("APPROVE verdict requires verified harness coverage")
        if any(payload.get(k) for k in ("blocking_findings", "high_findings",
                                        "suggestions")) and not coverage:
            errors.append("findings require harness coverage")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Check AI protocol output")
    parser.add_argument("file", nargs="?", help="Output file to check; stdin if omitted")
    parser.add_argument("--mode", choices=sorted(REQUIRED_SECTIONS), required=True)
    parser.add_argument("--schema",
                        help="JSON contract mode: validate against this schema "
                             "(docs/ai/schemas/<mode>.schema.json) instead of the markdown checks")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    text = read_input(args.file)
    errors = []

    if args.schema:
        errors = schema_mode_errors(text, args.mode, args.schema)
    else:
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
    if args.schema:
        result["schema"] = args.schema

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
