# Prompt: Weak-Model Harness Selection

Use this before a weak model is allowed to edit code.

```
You are selecting dev-guidelines harnesses for a bounded C++ task.

Rules:
- Do not propose code.
- Do not inspect unrelated files.
- Keep output to 6 non-empty lines or fewer.
- If a required harness is missing, say NOT VERIFIED.
- If the routing script is runnable, first run `python scripts/route_harnesses.py --files {FILES}` and use its output as the starting point for Applicable harnesses (no match or not runnable: fall back to scanning INDEX.md).
- If the host supports structured output, emit JSON conforming to docs/ai/schemas/plan.schema.json instead of the markdown template.

Task:
{TASK}

Files / areas:
{FILES}

Required output:
Objective:
Applicable harnesses:
Applicable checklist items:
Patch plan:
Verification plan:
Risks / NOT VERIFIED:
```

