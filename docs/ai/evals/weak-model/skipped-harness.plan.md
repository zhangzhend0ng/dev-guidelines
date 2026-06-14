# Eval: Skipped Harness

## Prompt

Ask the model to fix a C++ ownership bug and require the weak-model plan format.

## Expected Failure

The model jumps directly to code or a patch plan without listing applicable harnesses.

## Required Pass Behavior

The output must include:
- `Objective:`
- `Applicable harnesses:`
- `Applicable checklist items:`
- `Patch plan:`
- `Verification plan:`
- `Risks / NOT VERIFIED:`

It should name at least:
- `common/ai/model-capability-and-instruction-adherence.md`
- `common/ai/ai-assisted-cpp-development.md`
- `cpp/memory/ownership.md`

