---
type: harness
id: "common-harness-driven-review"
title: "Harness-Driven Development Protocol"
language: "common"
category: "code-review"
tier: "A"
scope: "Enforce that harnesses are applied BEFORE writing code (pre-implementation checklist) AND during code review (verification checklist)"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-27"
review_cycle: "12m"
tags:
  - code-review
  - code-generation
  - meta-harness
  - process-enforcement
based_on:
  - "[A] dev-guidelines AGENTS.md — Code Review Entry Rules"
  - "[A] dev-guidelines CLAUDE.md — Harness Usage Protocol"
  - "[A] dev-guidelines Harness Methodology (concepts/01-harness-methodology.md)"
related:
  - "common/ai/model-capability-and-instruction-adherence.md"
  - "common/ai/ai-assisted-cpp-development.md"
  - "common/ai/tool-calling-and-agent-control.md"
  - "common/code-review/review-checklist.md"
  - "common/meta/harness-evolution.md"
  - "cpp/design/feature-design-prerequisites.md"
supersedes: []
changelog:
  - "2026.06: Initial draft, review-only"
  - "2026.06: Expanded to cover code generation (pre-implementation harness application)"
  - "2026.07: Added B6 — Feedback Signal Check. Conditional step after verdict: if the review produced a harness-improvement signal (gap/inoperable/misleading/under-coverage/tier-mismatch), append to common/meta/harness-feedback-log.md. Closes the review-side of the distillation->evolution bridge."
  - "2026.07.1: B6 mechanized for AI-only workflow. Instead of asking the reviewer to judge whether a signal occurred, B6 now runs scripts/check_review_signals.py which auto-detects gap/inoperable/tier-mismatch from the report and auto-appends to the log. misleading/under-coverage handled via inline HTML markers. Zero meta-cognition required."
---
# Harness-Driven Development Protocol

**This harness is the MANDATORY entry point for two scenarios:**

1. **Before writing code** — load relevant harnesses first, apply them as you implement
2. **During code review** — verify the code against all applicable harnesses

In both cases: no code should be written or approved without passing relevant harness checklists.

---

## Part A: Before Writing Code

### A1. Harness Discovery — BEFORE writing a single line

When asked to implement a feature, fix a bug, or write any code:

- [ ] Read [INDEX.md](../../INDEX.md), list all applicable harnesses by category and topic → **(A)** [R1]
- [ ] Match harness categories to the task:
  - Writing a new function → `cpp/functions/parameter-validation.md`
  - Managing memory/resources → `cpp/memory/raii.md`, `ownership.md`, `move-semantics.md`
  - Handling errors → `common/error-handling/error-handling-strategy.md`
  - Processing external input → `common/security/input-validation.md`
  - GUI/dialog logic → check error-handling, parameter-validation
  - Threading → `cpp/concurrency/thread-safety.md`
  - Any C++ work → `cpp/correctness/` harnesses (const, undefined-behavior, exception-safety)
- [ ] Include any harness that *might* apply → **(A)** False positives are cheap; missed issues are expensive [R1]

### A2. Harness Loading — Understand the rules before implementing

- [ ] Read each applicable harness in full → **(A)** Prerequisites, checklist items, anti-patterns, decision tree [R1]
- [ ] Note the tier tags: (N) items are non-negotiable, must be satisfied in implementation → **(A)** [R2]

### A3. Harness-Guided Implementation

- [ ] While writing code, satisfy each (N)-tier item first → **(A)** These are non-negotiable [R2]
- [ ] Then satisfy (C)-tier items — default to following them unless there is a documented reason not to → **(A)** [R2]
- [ ] Consider (A)-tier items as context-dependent suggestions → **(A)** [R2]
- [ ] After writing, self-check: run through each harness item and confirm PASS → **(A)** [R1]

---

## Part B: During Code Review

### B1. Harness Discovery — BEFORE reading the code

- [ ] Re-read [INDEX.md](../../INDEX.md), list all applicable harnesses → **(A)** [R1]
- [ ] Do NOT read the code before this step — avoid post-hoc rationalization → **(A)** [R1]

### B2. Harness Loading — Load all applicable harnesses

- [ ] Read each harness in full (prerequisites, items, anti-patterns, decision tree) → **(A)** [R1]

### B3. Harness Application — Execute every checklist item

- [ ] For each item: state condition, check code, cite file:line, report PASS or FAIL → **(A)** [R1]
- [ ] Tag each finding with authority tier → **(N)** = BLOCKING, **(C)** = HIGH (needs justification), **(A)** = suggestion [R2]

### B4. Verdict Gate

- [ ] All harnesses applied? If NO → **DO NOT ISSUE VERDICT** → **(A)** [R1]
- [ ] Any (N) failure? → **REQUEST CHANGES** → **(A)** [R2]
- [ ] Any unjustified (C) failure? → **REQUEST CHANGES** or **APPROVE with comments** → **(A)** [R2]
- [ ] All PASS or (A)-only? → **APPROVE** → **(A)** [R2]

### B5. Report Format

- [ ] List each harness by name, report items as PASS/FAIL with tier+line → **(A)** [R1]
- [ ] Include summary table → **(A)** [R1]

```
## Harness: Parameter Validation (cpp/functions/parameter-validation.md)
Item 1 — N/A (static internal)
Item 2 — PASS (line 1193, region checked)
...
## Verdict: APPROVE
```

### B6. Feedback Signal Check

After the verdict, mechanically scan the review report for harness-improvement signals. AI-only workflow: run one command, do not meta-cognitively judge.

- [ ] Run `python scripts/check_review_signals.py <this-review-report.md>` → **(A)** the script auto-detects: gap (orphan FAIL), inoperable (N/A + keyword), tier-mismatch (item tier exceeds harness source tier). It auto-appends to `common/meta/harness-feedback-log.md`. [R1]
- [ ] For misleading / under-coverage (not auto-detectable), if you judge one occurred, add an inline marker `<!-- signal: misleading -->` or `<!-- signal: under-coverage -->` at the relevant report line BEFORE running the script → **(A)** the script collects these markers. [R1]
- [ ] Script reports "No signals detected" → **(A)** done. Do not force a log entry — routine PASS/FAIL is not an improvement signal. [R1]

---

## Decision Tree

```
Task received (implement or review)
  │
  ├─ IMPLEMENT:   A1→A2→A3 (harnesses guide every line)
  │
  └─ REVIEW:      B1→B2→B3→B4→B5→B6 (harnesses verify every line)
                    │
                    ├─ B4 Gate: (N)=BLOCK (C)=HIGH (A)=suggestion
                    └─ B6: if signal, log to feedback-log; else skip
```

---

## Anti-Patterns

### Anti-Pattern 1: Write First, Harness Later

- **Appearance:** Implement the feature, then skim harnesses to "validate" what was already written.
- **Consequence:** Harnesses become a rubber stamp. (N)-tier violations are found too late, requiring rewrites.
- **Fix:** Harness discovery (A1) happens BEFORE any code is written.

### Anti-Pattern 2: Review Without Harnesses

- **Appearance:** Read diff → ad-hoc comments → verdict. No harness loaded.
- **Consequence:** Systematic gaps. Inconsistent coverage.
- **Fix:** Every review starts at B1.

### Anti-Pattern 3: Post-Hoc Harness Selection (Review)

- **Appearance:** Read code first, then pick harnesses that confirm the already-formed verdict.
- **Consequence:** Confirmation bias.
- **Fix:** B1 requires harness selection BEFORE reading the code.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines CLAUDE.md | Harness Usage Protocol, Report Format | verified-2026 | 2026-06 |
| R2 | A | dev-guidelines AGENTS.md | Key Rules, Tier-Based Severity | verified-2026 | 2026-06 |
