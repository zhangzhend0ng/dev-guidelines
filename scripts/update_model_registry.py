#!/usr/bin/env python3
"""Update docs/ai/model-registry.md from an evaluation JSON report.

Usage:
    python scripts/evaluate_ai_protocol.py outputs/dsv4pro --json --output report.json
    python scripts/update_model_registry.py --model dsv4pro --version 2026-06 --report report.json
"""

import argparse
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "ai" / "model-registry.md"


def approved_tasks(tier):
    if tier == "T0":
        return "summarize, classify"
    if tier == "T1":
        return "harness selection, short plans, bounded explanations"
    if tier == "T2":
        return "harness selection, small bounded patches, review drafts, verification reports"
    if tier == "T3":
        return "multi-file subsystem work with review gates"
    if tier == "T4":
        return "tool-using workflows with approval gates"
    return "summarize, classify"


def blocked_tasks(tier):
    if tier in {"T0", "T1"}:
        return "autonomous edits, approval verdicts, unverified patch claims"
    if tier == "T2":
        return "autonomous tools, broad rewrites, approval verdicts without human gate"
    if tier == "T3":
        return "production-affecting autonomous tools without approval"
    return "none beyond high-impact approval gates"


def upsert_row(content, model, version, tier, last_eval, notes):
    lines = content.splitlines()
    row = (
        f"| {model} | {version} | {tier} | {approved_tasks(tier)} | "
        f"{blocked_tasks(tier)} | {last_eval} | {notes} |"
    )
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith(f"| {model} |"):
            lines[i] = row
            replaced = True
            break
    if not replaced:
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith("| unknown / unevaluated |"):
                insert_at = i + 1
        lines.insert(insert_at, row)
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Update AI model registry")
    parser.add_argument("--model", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--notes", default="Updated from protocol evaluation")
    args = parser.parse_args()

    report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    tier = report.get("recommended_tier", "T0")
    content = REGISTRY.read_text(encoding="utf-8")
    updated = upsert_row(content, args.model, args.version, tier, str(date.today()), args.notes)
    REGISTRY.write_text(updated, encoding="utf-8")
    print(f"Updated {REGISTRY} for {args.model} -> {tier}")


if __name__ == "__main__":
    main()
