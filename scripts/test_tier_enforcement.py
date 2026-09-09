#!/usr/bin/env python3
"""Regression tests for update_model_registry.py --emit-enforcement (Phase 4).

Covers:
- registry rows drive the generated matrix: adding a model at a tier makes
  that tier's row list the model (fixture A vs fixture B differ)
- AUTO-GENERATED marker and generation date are present
- every tier T0-T4 has an enforcement row
- the printed AGENTS.md snippet mirrors the same tier mapping
- CLI smoke on the real registry via a temp output (never touches the
  tracked docs/ai/tier-enforcement.md from the test)
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from update_model_registry import emit_enforcement, parse_registry  # noqa: E402, E501

SCRIPT = ROOT / "scripts" / "update_model_registry.py"

REGISTRY_A = """# Model Registry

| Model | Version | Default Tier | Approved Tasks | Blocked Tasks | Last Eval | Notes |
|-------|---------|--------------|----------------|---------------|-----------|-------|
| unknown / unevaluated | n/a | T0/T1 | summarize | everything | n/a | weak-model workflow |
| dsv4pro | TBD | T1 | plans | edits | TBD | promote only after eval |
"""

REGISTRY_B = REGISTRY_A.replace(
    "| dsv4pro | TBD | T1 |",
    "| dsv4pro | TBD | T1 |\n| qwen3 | 2026-09 | T2 | patches | autonomous tools | 2026-09-01 | promoted by eval |",
)


def main():
    errors = []

    doc_a, snippet_a = emit_enforcement(REGISTRY_A, "2026-09-10")
    doc_b, snippet_b = emit_enforcement(REGISTRY_B, "2026-09-10")

    # AUTO-GENERATED marker + date.
    for name, doc in (("doc", doc_a), ("snippet", snippet_a)):
        if "AUTO-GENERATED" not in doc:
            errors.append(f"{name}: missing AUTO-GENERATED marker")
    if "2026-09-10" not in doc_a:
        errors.append("doc: missing generation date")

    # Every tier has a row.
    for tier in ("T0", "T1", "T2", "T3", "T4"):
        if f"| {tier} |" not in doc_a:
            errors.append(f"doc: missing tier row {tier}")

    # Registry change -> emit output change (consistency).
    if "qwen3" in doc_a or doc_a == doc_b:
        errors.append("consistency: fixture B (adds qwen3@T2) did not change the matrix")
    if "| T2 | qwen3 (2026-09) |" not in doc_b:
        errors.append("consistency: T2 row does not list the new qwen3 model")

    # unknown/unevaluated row covers both T0 and T1.
    if "unknown / unevaluated (n/a)" not in doc_a:
        errors.append("doc: combined T0/T1 registry row not reflected")

    # Snippet mirrors tiers.
    for tier in ("T0", "T1", "T2", "T3", "T4"):
        if f"- **{tier}**:" not in snippet_b:
            errors.append(f"snippet: missing tier bullet {tier}")
    if "route_harnesses" not in snippet_b or "block_destructive_git" not in snippet_b:
        errors.append("snippet: enforcement wording lost runtime-layer references")

    # parse_registry on the real registry must find dsv4pro@T1 without crashing.
    real_rows = parse_registry(
        (ROOT / "docs" / "ai" / "model-registry.md").read_text(encoding="utf-8-sig")
    )
    if not any(m == "dsv4pro" and "T1" in tiers for m, _, tiers, _ in real_rows):
        errors.append(f"real registry parse lost dsv4pro/T1: {real_rows}")

    # CLI smoke: real registry -> temp output (tracked file untouched).
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "tier-enforcement.md"
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--emit-enforcement",
             "--registry", str(ROOT / "docs" / "ai" / "model-registry.md"),
             "--out", str(out)],
            capture_output=True, text=True, check=False,
        )
        if result.returncode != 0:
            errors.append(f"CLI --emit-enforcement failed rc={result.returncode}: "
                          f"{result.stderr[:200]}")
        if not out.exists() or "AUTO-GENERATED" not in out.read_text(encoding="utf-8"):
            errors.append("CLI: temp output missing or unmarked")
        if "dsv4pro" not in out.read_text(encoding="utf-8"):
            errors.append("CLI: generated doc missing registry model dsv4pro")
        if "Model Tier Enforcement" not in result.stdout:
            errors.append("CLI: stdout paste-ready snippet missing")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        sys.exit(1)

    print("Tier enforcement emit tests passed.")


if __name__ == "__main__":
    main()
