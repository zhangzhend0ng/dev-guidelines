---
type: harness
id: "common-risk-verification-plan"
title: "Risk and Verification Plan Checklist"
language: "common"
category: "planning"
tier: "C"
scope: "Define risk, verification commands, evidence, and NOT VERIFIED states before accepting engineering changes"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [planning, risk, verification, testing, ai]
based_on:
  - "[C] NIST SP 800-218 SSDF"
  - "[C] Google Testing Blog"
  - "[A] dev-guidelines Harness-Driven Development Protocol"
related:
  - "common/planning/task-decomposition.md"
  - "common/planning/change-scope-control.md"
  - "common/planning/rollback-and-migration-plan.md"
  - "common/debugging/fix-verification.md"
  - "common/testing/testing-strategy.md"
  - "common/ci-cd/pipeline-patterns.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Risk and Verification Plan Checklist

**Based on:** NIST SSDF ([C]), Google Testing guidance ([C]), dev-guidelines protocol ([A]).
**Scope:** Applies before accepting code, config, dependency, build, security, or AI-generated changes.

---

## Checklist

### 1. Risk Classification

- [ ] Change affects security, data, build, dependency, public API, concurrency, or production behavior -> **(C)** mark as high-risk and require stronger verification. [R1]
- [ ] Risk is unknown -> **(A)** treat as medium/high until clarified. [R3]

### 2. Verification Command

- [ ] Plan lacks concrete verification command or check -> **(C)** add one or mark NOT VERIFIED. [R1][R2]
- [ ] Command is unavailable -> **(A)** explain why and define next action. [R3]

### 3. Evidence

- [ ] Model or developer claims success -> **(C)** require command output summary or deterministic evidence. [R1]
- [ ] Evidence is long -> **(A)** summarize result and include raw logs only on request or failure diagnosis. [R3]

### 4. Regression

- [ ] Bug fix or security fix -> **(C)** add regression test or documented reason not to. [R1][R2]
- [ ] No regression path exists -> **(A)** add monitoring, static check, or manual verification note. [R1]

### 5. Approval Gate

- [ ] High-risk action cannot be verified automatically -> **(C)** require human approval before release. [R1]
- [ ] Weak model is used -> **(A)** protocol output must pass automated checks before human review. [R3]

---

## Decision Tree

```
Change planned
  -> classify risk
  -> name verification command
  -> define evidence
  -> add regression path
  -> mark NOT VERIFIED if evidence missing
```

---

## Anti-Patterns

### Anti-Pattern 1: Looks Correct

- **Appearance:** Patch is accepted because it is small and plausible.
- **Trap:** Small changes can break contracts.
- **Consequence:** Missing verification becomes production risk.
- **Fix:** Require command evidence or NOT VERIFIED.

### Anti-Pattern 2: Log Dump Verification

- **Appearance:** Full command output is pasted as proof.
- **Trap:** It contains evidence somewhere.
- **Consequence:** Reviewers miss the actual result.
- **Fix:** Summarize command, result, failures, and next action.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C6] NIST SP 800-218 SSDF | Verification and release practices | verified-2026 | 2026-06 |
| R2 | C | [C12] Google Testing Blog | Regression and test quality | verified-2026 | 2026-06 |
| R3 | A | dev-guidelines Harness-Driven Development Protocol | Evidence and NOT VERIFIED states | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
