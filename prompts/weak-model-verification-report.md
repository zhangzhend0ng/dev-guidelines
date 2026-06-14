# Prompt: Weak-Model Verification Report

Use this after a weak model has edited code or reviewed a patch.

```
Report verification status only.

Rules:
- Do not claim success unless a command or deterministic check was actually run.
- If no command was run, write NOT VERIFIED.
- Summarize failures; do not paste full logs unless needed to explain the next action.
- Keep output to 8 non-empty lines or fewer.

Commands available:
{COMMANDS}

Commands actually run:
{COMMANDS_RUN}

Required output:
Verification run:
Result:
Failures / NOT VERIFIED:
Next action:
```

