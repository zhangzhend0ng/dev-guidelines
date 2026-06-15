Goal: Add sanitizer triage guidance for C++ crash debugging.
Harnesses: common/planning/task-decomposition.md; cpp/debugging/sanitizer-triage.md
Scope: Add one harness and related backlinks only.
Steps: Draft harness, update related references, regenerate index.
Verification: python scripts/validate.py --json; python scripts/generate_index.py --check
Stop / escalate: Stop if required source category or cross-reference target is missing.
