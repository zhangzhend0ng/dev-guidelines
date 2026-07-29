---
type: harness
id: "common-task-decomposition"
title: "Task Decomposition Checklist"
language: "common"
category: "planning"
tier: "A"
scope: "Decompose engineering work into bounded, reviewable, verifiable tasks before implementation"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "24m"
tags: [planning, task-decomposition, scope, ai]
based_on:
  - "[A] dev-guidelines Harness-Driven Development Protocol"
  - "[A] The Pragmatic Programmer"
  - "[A] Software Engineering at Google"
related:
  - "common/planning/change-scope-control.md"
  - "common/planning/risk-and-verification-plan.md"
  - "common/planning/rollback-and-migration-plan.md"
  - "common/debugging/bug-report-triage.md"
  - "common/ai/model-capability-and-instruction-adherence.md"
  - "cpp/design/feature-design-prerequisites.md"
  - "common/planning/requirements-gap-analysis.md"
  - "common/config/option-registration-and-dimension.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Task Decomposition Checklist

**Based on:** dev-guidelines harness protocol ([A]), Pragmatic Programmer ([A]), Software Engineering at Google ([A]).
**Scope:** Applies before coding, refactoring, debugging, migration, or AI-assisted work.

---

## Checklist

### 1. Objective

- [ ] Task has no one-sentence objective -> **(A)** write one before planning. [R1]
- [ ] Objective mixes multiple outcomes -> **(A)** split into separate tasks. [R1][R2]

### 2. Harness Selection

- [ ] Task changes code, tests, build, security, or process -> **(A)** list applicable harnesses before implementation. [R1]
- [ ] Applicable harness is unclear -> **(A)** select the closest harness and record the gap. [R1]

### 3. Work Units

- [ ] Task spans multiple files, components, or risk types -> **(A)** split into reviewable work units with independent verification. [R2][R3]
- [ ] A work unit cannot be tested or reviewed alone -> **(A)** split smaller or define an explicit integration gate. [R3]

### 4. Stop Conditions

- [ ] Task lacks completion criteria -> **(A)** define done, blocked, and not-verified states. [R1]
- [ ] AI agent is used -> **(A)** require short phase updates and stop on repeated instruction failure. [R1]

### 5. Human Gate Minimization

- [ ] Human approval is needed -> **(A)** restrict it to scope approval, high-risk action approval, or final review. [R1]
- [ ] Human is asked to inspect raw logs or broad plans -> **(A)** summarize decision-relevant evidence first. [R1]

---

## Decision Tree

```
Task received
  -> one-sentence objective
  -> applicable harnesses
  -> split work units
  -> define verification and stop conditions
```

---

## Anti-Patterns

### Anti-Pattern 1: One Big Task

- **Appearance:** "Refactor the module and fix bugs" as one work item.
- **Trap:** It feels efficient.
- **Consequence:** Review and rollback become hard.
- **Fix:** Split by behavior, file boundary, or risk class.

### Anti-Pattern 2: Plan Without Done

- **Appearance:** Steps exist, but no completion or blocked criteria.
- **Trap:** The plan looks actionable.
- **Consequence:** Work drifts or claims success without evidence.
- **Fix:** Define done, blocked, and NOT VERIFIED states.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines Harness-Driven Development Protocol | Planning and harness selection | verified-2026 | 2026-06 |
| R2 | A | The Pragmatic Programmer | Tracer bullets, orthogonality | verified-2026 | 2026-06 |
| R3 | A | Software Engineering at Google | Reviewability and maintainability | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
