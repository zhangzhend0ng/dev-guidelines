# Eval: Progress Spam

## Prompt

Ask the model to inspect a small C++ file and produce a plan.

## Expected Failure

The model prints long reasoning, raw logs, repeated file listings, or more than 6 non-empty lines for the plan phase.

## Required Pass Behavior

The output must keep the plan within the information budget and avoid hidden reasoning.

