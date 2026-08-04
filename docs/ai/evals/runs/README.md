# Evaluation Runs

This directory holds per-model evaluation runs for Phase 6 (Real Model Evaluation
Loop). Each run scaffolds the four weak-model protocol prompts for one model on
one date, ready for a human or external tool to fill in model outputs and evaluate
them.

**This is not a harness.** It carries no frontmatter. Do not run `validate.py`
against it.

## Directory layout

```
docs/ai/evals/runs/<model>/<date>/
    prompt-plan.txt            # rendered harness-selection prompt
    prompt-patch.txt           # rendered cpp-patch prompt (may have unfilled placeholders)
    prompt-review.txt          # rendered cpp-review prompt (may have unfilled placeholders)
    prompt-verification.txt    # rendered verification prompt (may have unfilled placeholders)
    task-spec.yml              # the task spec this run was built from (reproducibility)
    # added by the user after the model produces outputs:
    <name>.plan.output.md
    <name>.patch.output.md
    <name>.review.output.md
    <name>.verification.output.md
```

## File naming rules (critical)

`scripts/run_ai_protocol_check.py` infers a file's check mode from its suffix.
It matches any filename ending in `.plan.md`, `.patch.md`, `.review.md`,
`.verification.md`, or the `.output.md` variants.

- **Prompt files MUST use the `.txt` suffix.** A file named `prompt-plan.md`
  ends in `.plan.md` and would be auto-discovered and mis-checked as a model
  output — corrupting the run's evaluation. `run_eval.py` enforces this.
- **Output files MUST use `<name>.<mode>.output.md`** (e.g. `case1.plan.output.md`)
  so they are discovered and checked by the correct mode.
- `task-spec.yml` is safe — discovery only walks `*.md`.

## How to run an evaluation

```bash
# 1. Scaffold the run (renders prompts; does NOT run a model)
python scripts/run_eval.py --model <name> --version <ver> [--task <spec.yml>]

# 2. Fill any UNFILLED placeholders noted at the top of prompt-patch/review/verification.txt
#    (these depend on upstream outputs: the plan result, the actual diff, commands run)

# 3. Feed each prompt to the model and collect its output. Write each output to
#    <name>.<mode>.output.md in the run dir. Use docs/ai/evals/weak-model/good-runs/
#    as a format reference.

# 4. Evaluate the filled outputs (reuses the existing evaluator)
python scripts/evaluate_ai_protocol.py docs/ai/evals/runs/<model>/<date> \
    --json --output docs/ai/evals/runs/<model>/<date>/report.json

# 5. (optional) update the registry from the report
python scripts/update_model_registry.py --model <name> --version <ver> \
    --report docs/ai/evals/runs/<model>/<date>/report.json
```

## What this directory is NOT

- **It is not evidence on its own.** A scaffolded run with unfilled outputs proves
  nothing about model capability. The tier recommendation from
  `evaluate_ai_protocol.py` has meaning only after real model outputs are filled
  in and the evaluation passes.
- **The checker is structural, not semantic.** `check_ai_protocol.py` verifies
  required sections, line budgets, command evidence, and citation format — it
  cannot tell a *correct* parameter-validation patch from a *plausible but wrong*
  one. `good-runs/` is a format reference, not a semantic rubric. Semantic
  correctness remains a human judgment.
- **Debug mode is out of scope here.** Phase 6 also lists debug outputs
  (`check_debug_report.py`); this scaffolder covers plan/patch/review/verification
  only. Debug support is a follow-up.
