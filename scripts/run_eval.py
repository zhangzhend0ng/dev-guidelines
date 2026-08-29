#!/usr/bin/env python3
"""Scaffold a weak-model evaluation run: render prompt templates into a run directory.

This is the FIRST step of Phase 6 (Real Model Evaluation Loop). It does NOT run a
model, evaluate outputs, or touch the registry — it only renders the four prompt
templates (prompts/weak-model-*.md) with values from a task spec into:

    docs/ai/evals/runs/<model>/<date>/
        prompt-plan.txt
        prompt-patch.txt
        prompt-review.txt
        prompt-verification.txt
        task-spec.yml

Prompt files use the .txt suffix deliberately: run_ai_protocol_check.infer_mode()
matches any filename ending in .plan.md/.patch.md/.review.md/.verification.md, so
a prompt file named prompt-plan.md would be auto-discovered and mis-checked as a
model output. .txt is never matched.

Only the plan (harness-selection) prompt can be fully filled from a static task
spec — its placeholders {TASK}/{FILES} describe the task itself. The patch/review/
verification prompts carry placeholders ({PATCH_PLAN}/{DIFF}/{COMMANDS_RUN}) that
depend on UPSTREAM outputs (the plan result, the actual diff, the commands run),
so those are left as {X} with an inline note for a human to fill before feeding
the prompt to a model.

After scaffolding, the workflow is:
  1. (human) fill the remaining {X} in prompt-patch/review/verification.txt
  2. (human/model) feed each prompt to the model, collect its output
  3. (human) write each output to <name>.<mode>.output.md in the run dir
     (see docs/ai/evals/weak-model/good-runs/ for the format)
  4. python scripts/evaluate_ai_protocol.py <run-dir> --json --output <run-dir>/report.json
     (exit 2 "not assessable" while the run dir has no <mode>.output.md files yet)
  5. (optional) python scripts/update_model_registry.py --model <m> --version <v> --report <run-dir>/report.json

Usage:
    python scripts/run_eval.py --model dsv4pro --version 2026-08
    python scripts/run_eval.py --model glm-5 --version 2026-08 --task my-task.yml
    python scripts/run_eval.py --model test --version 0 --date 2026-08-04
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
RUNS_DIR = ROOT / "docs" / "ai" / "evals" / "runs"

# Template name -> (prompt template file, list of placeholders it consumes).
# Order matters: plan feeds patch, patch feeds review, review feeds verification.
# Only plan's placeholders are fillable from a static task spec; the rest carry
# upstream-dependent placeholders that a human fills after upstream output exists.
TEMPLATES = [
    ("plan", "weak-model-harness-selection.md", ["TASK", "FILES"]),
    ("patch", "weak-model-cpp-patch.md", ["EDIT_SCOPE", "HARNESSES", "PATCH_PLAN", "COMMANDS"]),
    ("review", "weak-model-cpp-review.md", ["HARNESSES", "DIFF"]),
    ("verification", "weak-model-verification-report.md", ["COMMANDS", "COMMANDS_RUN"]),
]

# The default task case: a bounded C++ parameter-validation change. Reuses the
# scenario from cpp/functions/parameter-validation.md. PATCH_PLAN / DIFF /
# COMMANDS_RUN are intentionally absent — they are upstream-dependent and filled
# by a human after the plan/patch/review phases produce their outputs.
DEFAULT_TASK = {
    "task_id": "param-validation",
    "scenario": "Add parameter validation to a C++ public API function (Widget::resize)",
    "fields": {
        "TASK": (
            "Add parameter validation to Widget::resize(int w, int h); "
            "reject negative dimensions per cpp/functions/parameter-validation.md"
        ),
        "FILES": "src/widget.cpp; src/widget.h; cpp/functions/parameter-validation.md",
        "EDIT_SCOPE": "src/widget.cpp; src/widget.h",
        "HARNESSES": "cpp/functions/parameter-validation.md",
        "COMMANDS": "cmake --build build; ctest --test-dir build -R widget",
    },
}


def load_task(spec_path):
    """Load a task spec from YAML, or return the default if none given."""
    if spec_path is None:
        return dict(DEFAULT_TASK)
    data = yaml.safe_load(Path(spec_path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "fields" not in data:
        raise ValueError(
            f"task spec {spec_path} must be a mapping with a 'fields' key"
        )
    return data


def render_prompt(template_path, fields, placeholders):
    """Substitute placeholders into a prompt template.

    Returns (rendered_text, unfilled) where unfilled is the list of placeholders
    whose values were not present in the task spec (left as {X} for a human).
    """
    text = template_path.read_text(encoding="utf-8")
    unfilled = []
    for key in placeholders:
        token = "{" + key + "}"
        value = fields.get(key)
        if value:
            text = text.replace(token, value)
        else:
            unfilled.append(key)
    return text, unfilled


def write_run(run_dir, task, model, version, run_date):
    """Render all four prompts + task-spec.yml into run_dir. Returns list of (mode, unfilled)."""
    run_dir.mkdir(parents=True, exist_ok=True)
    report = []
    for mode, template_name, placeholders in TEMPLATES:
        template_path = PROMPTS_DIR / template_name
        if not template_path.exists():
            print(f"ERROR: prompt template missing: {template_path}", file=sys.stderr)
            sys.exit(1)
        rendered, unfilled = render_prompt(template_path, task.get("fields", {}), placeholders)
        out_path = run_dir / f"prompt-{mode}.txt"
        if unfilled:
            # Prepend an inline note so a human knows which tokens still need filling.
            # Placed INSIDE the file (not just stdout) so the note travels with the prompt.
            note = (
                f"<!-- UNFILLED PLACEHOLDERS: {', '.join(unfilled)} -->\n"
                f"<!-- These depend on upstream outputs (plan result / diff / commands run). -->\n"
                f"<!-- Fill them before feeding this prompt to a model. -->\n\n"
            )
            rendered = note + rendered
        out_path.write_text(rendered, encoding="utf-8")
        report.append((mode, unfilled))

    # Write the task spec back for reproducibility (authoritative for custom --task;
    # for the default task the script itself is also a source of truth).
    spec_out = {
        "task_id": task.get("task_id", "custom"),
        "scenario": task.get("scenario", ""),
        "model": model,
        "version": version,
        "run_date": run_date,
        "fields": task.get("fields", {}),
    }
    (run_dir / "task-spec.yml").write_text(
        yaml.safe_dump(spec_out, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a weak-model eval run (render prompts; does not run a model)."
    )
    parser.add_argument("--model", required=True, help="Model name (e.g. dsv4pro)")
    parser.add_argument("--version", required=True, help="Model version/date (e.g. 2026-08)")
    parser.add_argument("--task", help="Path to a task spec YAML (default: param-validation)")
    parser.add_argument("--date", help="Run date YYYY-MM-DD (default: today)")
    args = parser.parse_args()

    run_date = args.date or date.today().isoformat()
    task = load_task(args.task)
    run_dir = RUNS_DIR / args.model / run_date

    if run_dir.exists() and any(run_dir.iterdir()):
        print(
            f"ERROR: run dir already exists and is non-empty: {run_dir}",
            file=sys.stderr,
        )
        sys.exit(1)

    report = write_run(run_dir, task, args.model, args.version, run_date)

    print(f"Run scaffolded: {run_dir.relative_to(ROOT)}")
    print()
    print("Rendered prompts:")
    for mode, unfilled in report:
        status = "complete" if not unfilled else f"needs: {', '.join(unfilled)}"
        print(f"  prompt-{mode}.txt  ({status})")
    print(f"  task-spec.yml")
    print()
    print("Next steps:")
    print(f"  1. Fill any UNFILLED placeholders in the prompt-*.txt files")
    print(f"  2. Feed each prompt to {args.model}, collect outputs")
    print(f"  3. Write outputs as <name>.<mode>.output.md here (see good-runs/ for format)")
    print(f"  4. python scripts/evaluate_ai_protocol.py {run_dir} --json --output {run_dir}/report.json")
    print(f"     (step 4 exits 2 'not assessable' until outputs exist — do not register a tier from an empty run)")
    print()
    print("NOTE: this scaffolds a run only. Tier recommendation has no meaning until")
    print("outputs are filled and evaluate_ai_protocol.py passes. See")
    print("docs/ai/evals/runs/README.md.")


if __name__ == "__main__":
    main()
