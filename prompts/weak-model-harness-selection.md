# Prompt: Weak-Model Harness Selection

Use this before a weak model is allowed to edit code.

```
You are selecting dev-guidelines harnesses for a bounded C++ task.

Rules:
- Do not propose code.
- Do not inspect unrelated files.
- Keep output to 6 non-empty lines or fewer.
- If a required harness is missing, say NOT VERIFIED.

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

