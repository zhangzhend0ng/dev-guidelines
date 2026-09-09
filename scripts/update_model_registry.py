#!/usr/bin/env python3
"""Update docs/ai/model-registry.md from an evaluation JSON report.

Usage:
    python scripts/evaluate_ai_protocol.py outputs/dsv4pro --json --output report.json
    python scripts/update_model_registry.py --model dsv4pro --version 2026-06 --report report.json
    python scripts/update_model_registry.py --emit-enforcement [--registry PATH] [--out PATH]

--emit-enforcement regenerates docs/ai/tier-enforcement.md from the current
registry rows: a tier -> enforcement-measures matrix (L6 governance layer).
It prints a paste-ready snippet for the repository AGENTS.md but never
edits any AGENTS.md itself. Promotion still requires eval evidence only
(Promotion Rule in the registry); this command never changes tiers.
"""

import argparse
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "docs" / "ai" / "model-registry.md"
ENFORCEMENT_DOC = ROOT / "docs" / "ai" / "tier-enforcement.md"

# The weak-model eval (evaluate_ai_protocol.py) only ever emits T0/T1/T2.
# T3/T4 are definitionally human-gated (strong-model scope + repo-specific eval
# + approval gates, per docs/ai/model-registry.md Tier Policy) and reach this
# script only via a manually-edited report JSON or a hand-authored registry row.
# The T3/T4 branches in approved_tasks()/blocked_tasks() render those manual
# assignments — they are forward-compat, not dead code; do not remove.
VALID_TIERS = {"T0", "T1", "T2", "T3", "T4"}


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


# L6: tier -> environment enforcement. Wording mirrors the Tier Policy in
# model-registry.md plus the runtime layers landed in this evolution
# (Phase 1 hook, Phase 2 router, Phase 3 schema checks).
ENFORCEMENT_MEASURES = {
    "T0": "hook config read-only (block all writes via PreToolUse, see docs/ai/hooks-setup.md); weak-model templates only (prompts/weak-model-*); no Edit/Bash write operations",
    "T1": "hook config read-only (see docs/ai/hooks-setup.md); weak-model templates only; no Edit/Bash write operations",
    "T2": "Edit allowed after plan approval; PostToolUse auto-runs run_ai_protocol_check; PreToolUse hook still blocks the destructive-git list (scripts/hooks/block_destructive_git.py)",
    "T3": "multi-file changes allowed; plan approval required first; scripts/route_harnesses.py output is the mandatory harness reading list",
    "T4": "shell unlocked; the destructive-git blocklist still applies (scripts/hooks/block_destructive_git.py)",
}


def parse_registry(content):
    """[(model, version, [tier, ...], last_eval)] from registry table rows."""
    rows = []
    for line in content.splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] == "Model" or set(cells[0]) <= {"-", " "}:
            continue
        tier_cell = cells[2]
        tiers = [t.strip() for t in tier_cell.split("/")
                 if t.strip() in VALID_TIERS]
        rows.append((cells[0], cells[1], tiers,
                     cells[5] if len(cells) > 5 else "n/a"))
    return rows


def emit_enforcement(registry_text, generated_on):
    """Return (enforcement_doc_text, agents_md_snippet_text)."""
    tiers_in_use = {t: [] for t in sorted(VALID_TIERS)}
    for model, version, tiers, _ in parse_registry(registry_text):
        for t in tiers:
            if t in tiers_in_use:
                tiers_in_use[t].append(f"{model} ({version})")

    lines = [
        "<!-- AUTO-GENERATED by scripts/update_model_registry.py --emit-enforcement. DO NOT EDIT BY HAND. -->",
        f"<!-- Generated: {generated_on} from docs/ai/model-registry.md -->",
        "",
        "# Tier Enforcement Matrix",
        "",
        "Maps each capability tier to the environment enforcement applied to",
        "agents running at that tier. Data source: docs/ai/model-registry.md.",
        "Regenerate with `python scripts/update_model_registry.py --emit-enforcement`.",
        "",
        "| Tier | Models at tier | Enforcement |",
        "|------|----------------|-------------|",
    ]
    for tier in sorted(VALID_TIERS):
        models = ", ".join(tiers_in_use[tier]) or "(none registered)"
        lines.append(f"| {tier} | {models} | {ENFORCEMENT_MEASURES[tier]} |")
    lines += [
        "",
        "Tier promotion is driven by eval evidence only (Promotion Rule in",
        "model-registry.md); this matrix never grants tiers by itself.",
        "",
    ]
    doc = "\n".join(lines)

    snippet_lines = [
        "<!-- AUTO-GENERATED: paste target for scripts/update_model_registry.py",
        "     --emit-enforcement. Regenerate instead of hand-editing. -->",
        "",
        "## Model Tier Enforcement",
        "",
    ]
    for tier in sorted(VALID_TIERS):
        snippet_lines.append(f"- **{tier}**: {ENFORCEMENT_MEASURES[tier]}")
    snippet = "\n".join(snippet_lines)
    return doc, snippet


def main():
    parser = argparse.ArgumentParser(description="Update AI model registry")
    parser.add_argument("--model")
    parser.add_argument("--version")
    parser.add_argument("--report")
    parser.add_argument("--notes", default="Updated from protocol evaluation")
    parser.add_argument("--emit-enforcement", action="store_true",
                        help="regenerate docs/ai/tier-enforcement.md from the registry")
    parser.add_argument("--registry", help="registry path override (emit-enforcement)")
    parser.add_argument("--out", help="output path override (emit-enforcement)")
    args = parser.parse_args()

    if args.emit_enforcement:
        registry_path = Path(args.registry) if args.registry else REGISTRY
        out_path = Path(args.out) if args.out else ENFORCEMENT_DOC
        doc, snippet = emit_enforcement(
            registry_path.read_text(encoding="utf-8-sig"), str(date.today())
        )
        out_path.write_text(doc, encoding="utf-8")
        print(f"Written {out_path}")
        print("\n--- snippet for repository AGENTS.md (paste manually) ---")
        print(snippet)
        return

    if not args.model or not args.version or not args.report:
        parser.error("--model, --version and --report are required "
                     "unless --emit-enforcement is used")

    report = json.loads(Path(args.report).read_text(encoding="utf-8-sig"))  # utf-8-sig: strip BOM if present - a BOM breaks pos-0 anchors/parsers (iter 15/19)
    # No default: a report without recommended_tier (e.g. an empty/not-
    # assessable eval) must be rejected, never silently recorded as T0.
    tier = report.get("recommended_tier")
    if tier not in VALID_TIERS:
        parser.error(
            f"recommended_tier {tier!r} is missing or not a valid tier "
            f"(expected one of {sorted(VALID_TIERS)}). "
            "An empty/not-assessable eval has no tier; weak-model eval emits "
            "at most T2; T3/T4 are manual promotions."
        )
    content = REGISTRY.read_text(encoding="utf-8")
    updated = upsert_row(content, args.model, args.version, tier, str(date.today()), args.notes)
    REGISTRY.write_text(updated, encoding="utf-8")
    print(f"Updated {REGISTRY} for {args.model} -> {tier}")


if __name__ == "__main__":
    main()
