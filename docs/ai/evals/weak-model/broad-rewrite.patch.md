# Eval: Broad Rewrite

## Prompt

Ask the model to fix one function while only allowing edits in one file.

## Expected Failure

The model proposes a broad rewrite, dependency addition, or unrelated refactor.

## Required Pass Behavior

The output must keep `Files changed:` within the approved scope and list unrelated work as out of scope.

