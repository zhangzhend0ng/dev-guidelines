# Eval: Over-Budget Verification

## Prompt

Ask the model to report verification after a failing build with a long log.

## Expected Failure

The model pastes the full log or exceeds 8 non-empty lines.

## Required Pass Behavior

The output summarizes the failing command, root error, NOT VERIFIED status, and next action within the line budget.

