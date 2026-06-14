# Prompt: Weak-Model Workflow Router

Use this as the default entry point for weaker, local, domestic, instruction-fragile, or unproven models.

## Route Selection

Pick exactly one route:

| Need | Use |
|------|-----|
| Choose harnesses before work | [weak-model-harness-selection.md](weak-model-harness-selection.md) |
| Produce a small approved C++ patch | [weak-model-cpp-patch.md](weak-model-cpp-patch.md) |
| Review a bounded C++ diff | [weak-model-cpp-review.md](weak-model-cpp-review.md) |
| Report verification evidence | [weak-model-verification-report.md](weak-model-verification-report.md) |

## Default Rules

- Start at T1 unless a capability matrix explicitly promotes the model.
- Do not edit code before harness selection is approved.
- Keep output within the template budget.
- Do not print hidden reasoning, raw logs, or repeated file listings.
- If verification did not run, say NOT VERIFIED.
- If the model fails the same instruction twice, narrow the task.
- If it fails three times, escalate to a stronger model or human review.

## Minimal User Prompt

```
Use the weak-model workflow router.

Goal:
{GOAL}

Task type:
{harness-selection|cpp-patch|cpp-review|verification}

Allowed files:
{FILES}

Available commands:
{COMMANDS}

Use the matching template and keep output concise.
```

