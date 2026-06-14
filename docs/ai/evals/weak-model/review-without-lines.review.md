# Eval: Review Without Lines

## Prompt

Ask the model to review a small C++ diff with the weak-model review template.

## Expected Failure

The model gives broad feedback without file:line citations or harness item names.

## Required Pass Behavior

The output must include:
- `Blocking findings:`
- `High findings:`
- `Suggestions:`
- `Harness coverage:`
- `Verdict:`

Each real finding must cite file:line and a harness item.

