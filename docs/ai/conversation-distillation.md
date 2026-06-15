# Conversation Distillation for Weak Models

This document distills the current Codex planning conversation into reusable assets for weaker models.

## Purpose

Use strong-model conversations as a source of decisions, patterns, and guardrails.
Do not feed the full conversation to weaker models.

Weak models should receive short, fixed contracts with:

- one goal
- applicable harnesses
- allowed files or directories
- required output format
- verification command
- stop condition

## Distilled Decisions

### 1. Harness First

Every implementation or review task starts by selecting applicable harnesses.

Weak-model rule:

```text
Before proposing code, list 1-5 applicable harnesses.
If no harness applies, say "HARNESS GAP" and stop.
```

### 2. Low-Freedom Output

Weaker models should not produce broad prose or open-ended plans.

Weak-model rule:

```text
Use the required fields only.
Do not add extra sections.
Do not include hidden reasoning or raw logs.
```

### 3. Short Planning

Plans must be compact and checkable.

Required plan shape:

```text
Goal:
Harnesses:
Scope:
Steps:
Verification:
Stop / escalate:
```

Validation:

```bash
python scripts/check_plan_protocol.py output.plan.md
```

### 4. Debugging Requires Evidence

Bug fixes are not accepted from symptom-only reasoning.

Required debug report shape:

```text
Symptom:
Evidence:
Reproduction:
Root cause:
Fix:
Verification:
Residual risk:
```

Validation:

```bash
python scripts/check_debug_report.py output.debug.md
```

### 5. Verification Beats Confidence

Weak models must not say a change is verified unless they can name the command or deterministic check.

Weak-model rule:

```text
If verification did not run, write NOT VERIFIED and the next concrete action.
```

### 6. Human Work Should Be Minimized

The user should see useful state, not process noise.

Weak-model rule:

```text
Progress update <= 3 lines.
Final response <= 10 lines unless reporting findings.
Summarize command results; do not paste full logs unless needed.
```

### 7. Escalation Is Automatic

Weak models should stop rather than continue accumulating wrong work.

Weak-model rule:

```text
Same instruction failed twice -> shrink task.
Same instruction failed three times -> escalate to stronger model or human.
High-risk action without approval -> stop.
```

## Distilled Task Types

### Harness Creation

Use when adding a new checklist document.

Input contract:

```text
Goal: create one harness for <topic>.
Allowed files: one harness file plus index/related updates.
Must include: YAML frontmatter, 5-10 checklist items, anti-patterns, references.
Verification: python scripts/validate.py --json; python scripts/generate_index.py --check
```

### C++ Small Patch

Use when editing production C++.

Input contract:

```text
Goal: fix one bounded C++ issue.
Harnesses: name C++ correctness/build/testing harnesses.
Allowed files: exact files only.
Verification: build/test/static-analysis command.
Stop: missing harness, broad rewrite needed, or verification unavailable.
```

### Debug Triage

Use when analyzing a failure before code changes.

Input contract:

```text
Goal: classify and minimize one failure.
Harnesses: debugging + relevant language/testing harnesses.
Allowed output: debug report only.
Verification: reproduction command or NOT VERIFIED.
Stop: no evidence, no reproduction, or conflicting symptoms.
```

### Pack Extension

Use when adding a language or feature pack.

Input contract:

```text
Goal: add or update one pack.
Allowed files: packs/<id>/pack.yml and referenced harnesses only.
Verification: validate.py --pack <id>; generate_index.py --check.
Stop: missing dependency, missing source, or invalid related link.
```

## Good Weak-Model Prompt Skeleton

```text
You are a constrained coding assistant.
Task: <one task>
Allowed files: <paths>
Applicable harnesses: <paths or "select first">

Output exactly:
Goal:
Harnesses:
Scope:
Steps:
Verification:
Stop / escalate:

Rules:
- Do not write code yet.
- Do not exceed 6 non-empty lines.
- If a required harness is missing, write HARNESS GAP and stop.
- If verification cannot be named, write NOT VERIFIED.
```

## Bad Patterns to Reject

- broad rewrite proposal
- missing harness list
- "looks good" without command evidence
- long reasoning transcript
- raw log dump without summary
- approval verdict without line-specific findings
- code edits before plan acceptance

## Conversion Process

When a strong-model conversation produces useful decisions:

1. Extract stable decisions.
2. Convert each decision into a rule, prompt, fixture, or harness item.
3. Add good and bad fixtures for weak-model behavior.
4. Add or update protocol checks when the failure can be detected mechanically.
5. Re-run AI protocol tests.

## Next Assets to Create

- [x] `prompts/weak-model-from-distilled-task.md`
- [ ] more fixtures from real dsv4pro runs
- [ ] per-model notes after eval evidence exists
- [ ] conversation-to-fixture checklist for future strong-model sessions
