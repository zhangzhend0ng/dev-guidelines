# Weak Model Operating Guide

This guide is for humans using weaker or instruction-fragile models on C++ work.
It exists to minimize supervision time while keeping output usable.

## Workflow

1. Pick the model capability level from `model-capability-matrix.md`.
2. Use the weak-model prompt template for the task class.
3. Give one bounded task with explicit files and output format.
4. Require the model to list harnesses before it edits anything.
5. Let the model work in short phases.
6. Accept only summarized progress updates.
7. Review only the final patch and verification evidence.

## What to Ask For

- objective
- applicable harnesses
- smallest patch plan
- verification plan
- risks / NOT VERIFIED

## What Not to Ask For

- full internal reasoning
- repeated intermediate dumps
- long command logs
- broad redesigns unless explicitly needed

## Escalation Rules

- If the model skips harnesses, stop and retry with a narrower prompt.
- If the model repeats the same failure twice, reduce scope.
- If the model fails three times, move the task to a stronger model or a human.

## Human Work Reduction

The default path should be:
prompt -> harness list -> small patch -> verification -> summary

Only ask a person when:
- a high-risk action is needed
- verification fails in a way the model cannot repair
- the model shows repeated instruction failure

