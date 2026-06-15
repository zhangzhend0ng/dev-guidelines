# Prompt: Weak-Model C++ Patch

Use this only after the harness-selection output has been approved.

```
Proceed with the approved C++ patch only.

Rules:
- Touch only these files: {EDIT_SCOPE}
- Do not add dependencies.
- Do not rewrite unrelated code.
- Do not change public API unless explicitly approved.
- Use concise phase updates only if blocked or verification finishes.
- Summarize command output; do not paste full logs unless needed to explain failure.

Approved harnesses:
{HARNESSES}

Approved patch plan:
{PATCH_PLAN}

Available verification commands:
{COMMANDS}

Required final output:
Files changed:
Harness checks:
Verification run:
Failures / NOT VERIFIED:
Residual risks:
```

