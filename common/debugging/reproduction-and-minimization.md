---
type: harness
id: "common-reproduction-minimization"
title: "Reproduction and Minimization Checklist"
language: "common"
category: "debugging"
tier: "A"
scope: "Create reliable, minimal reproductions before debugging, fixing, or claiming root cause"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "24m"
tags: [debugging, reproduction, minimization, test-case]
based_on:
  - "[A] The Pragmatic Programmer"
  - "[A] Software Engineering at Google"
  - "[C] Google Testing Blog"
related:
  - "common/debugging/bug-report-triage.md"
  - "common/debugging/root-cause-analysis.md"
  - "common/debugging/fix-verification.md"
  - "common/testing/testing-strategy.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Reproduction and Minimization Checklist

**Based on:** Pragmatic Programmer ([A]), Software Engineering at Google ([A]), Google Testing guidance ([C]).
**Scope:** Applies before root cause analysis and fix acceptance.

---

## Checklist

### 1. Reproduction Command

- [ ] Bug lacks command, input, or scenario -> **(A)** define one before debugging. [R1]
- [ ] Reproduction depends on hidden state -> **(A)** capture environment and setup. [R2]

### 2. Reliability

- [ ] Reproduction is flaky -> **(A)** run repeated attempts and record rate. [R2]
- [ ] Reproduction cannot be made reliable -> **(A)** mark NOT VERIFIED and avoid root cause claims. [R1]

### 3. Minimization

- [ ] Reproduction is large -> **(A)** reduce to smallest input, test, or scenario that still fails. [R1][R3]
- [ ] Minimization changes behavior -> **(A)** keep both original and minimized cases. [R3]

### 4. Regression Candidate

- [ ] Reproduction is reliable -> **(C)** convert it into regression test, fixture, or documented manual check. [R3]

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | The Pragmatic Programmer | Debugging discipline | verified-2026 | 2026-06 |
| R2 | A | Software Engineering at Google | Flaky tests and reproducibility | verified-2026 | 2026-06 |
| R3 | C | [C12] Google Testing Blog | Regression and test quality | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
