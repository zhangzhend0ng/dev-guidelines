# Prompt: Weak-Model C++ Task Protocol Index

Use these templates when the model is less capable, instruction-fragile, local, small, or unproven on this repository. The goal is to reduce autonomy and force harness use, not to ask for more free-form reasoning.

Prefer the specialized templates:

- [Harness Selection](weak-model-harness-selection.md) - before edits
- [C++ Patch](weak-model-cpp-patch.md) - after plan approval
- [C++ Review](weak-model-cpp-review.md) - bounded diff review
- [Verification Report](weak-model-verification-report.md) - final evidence summary

The combined template below is retained for tools that need a single prompt.

## Template

```
You are working in a C++ repository under dev-guidelines.

Capability mode:
- Start at T1 unless I explicitly promote you.
- Do not edit code until you list applicable harnesses and I approve the plan.
- If you cannot verify something, say NOT VERIFIED. Do not claim success.
- Keep user-facing output concise. Do not print hidden reasoning, raw logs, or repeated file listings.
- At the start, give a one-line goal and a one-line plan.

Task:
{TASK}

Repository context:
- Files you may inspect: {FILES}
- Files you may edit: {EDIT_SCOPE}
- Build/test command available: {COMMANDS}

Required process:
1. State the objective in one sentence.
2. List applicable harnesses from INDEX.md.
3. For each harness, list only the checklist items that apply.
4. Propose the smallest patch plan.
5. Stop and wait for approval before editing.

Required output format:
Objective:
Applicable harnesses:
Applicable checklist items:
Patch plan:
Verification plan:
Risks / NOT VERIFIED:

Information budget:
- Plan: maximum 6 lines.
- No implementation details until approval.
- Mention only decision-relevant risks.
- If work continues, give a one-line status update only at phase boundaries.
```

## Progress Update Template

Use this only at phase boundaries, when blocked, or when verification finishes.

```
Status: {planning|editing|verifying|blocked|done}
Done: {one short sentence}
Next: {one short sentence}
Issue / NOT VERIFIED: {one short sentence or "none"}
```

## Patch Phase Template

```
Proceed with the approved patch only.

Rules:
- Touch only the approved files.
- Make the smallest change that satisfies the harnesses.
- Do not add dependencies.
- Do not rewrite unrelated code.
- After editing, report exact files changed and verification results.
- During work, use the Progress Update Template only at phase boundaries or blockers.
- Summarize command output; include raw logs only if needed to explain a failure.

Final output format:
Files changed:
Harness checks:
Verification run:
Failures / NOT VERIFIED:
Residual risks:

Information budget:
- Final answer: maximum 10 lines unless there are blocking findings.
- Do not include full diffs or full logs unless requested.
```

## Review Phase Template

```
Review the following diff using the listed harnesses.

Rules:
- Findings must cite file:line.
- Each finding must name the harness and checklist item.
- Do not give a verdict unless every applicable harness item is processed.
- If evidence is missing, say NOT VERIFIED.

Harnesses:
{HARNESSES}

Diff:
{DIFF}

Output format:
Blocking findings:
High findings:
Suggestions:
Harness coverage:
Verdict:

Information budget:
- Findings first, ordered by severity.
- Omit pass-only checklist items unless needed for coverage.
- Do not include broad commentary when there are no findings.
```
