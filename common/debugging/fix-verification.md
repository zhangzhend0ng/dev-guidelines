---
type: harness
id: "common-fix-verification"
title: "Fix Verification Checklist"
language: "common"
category: "debugging"
tier: "C"
scope: "Verify bug fixes with regression evidence, negative checks, and residual risk before closure"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [debugging, fix-verification, regression, evidence]
based_on:
  - "[C] NIST SP 800-218 SSDF"
  - "[C] Google Testing Blog"
  - "[A] Software Engineering at Google"
related:
  - "common/debugging/bug-report-triage.md"
  - "common/debugging/reproduction-and-minimization.md"
  - "common/debugging/root-cause-analysis.md"
  - "common/testing/testing-strategy.md"
  - "common/planning/risk-and-verification-plan.md"
  - "cpp/debugging/crash-dump-analysis.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Fix Verification Checklist

**Based on:** NIST SSDF ([C]), Google Testing guidance ([C]), Software Engineering at Google ([A]).
**Scope:** Applies before closing bugs or accepting AI-generated fixes.

---

## Checklist

### 1. Regression Evidence

- [ ] Bug had a reproduction -> **(C)** add regression test or documented manual check. [R1][R2]
- [ ] No regression test is possible -> **(A)** document reason and compensating check. [R3]

### 2. Before/After

- [ ] Fix lacks before/after evidence -> **(C)** show failure before and pass after, or explain why unavailable. [R1]
- [ ] AI claims fixed -> **(A)** require command evidence or NOT VERIFIED. [R1]

### 3. Side Effects

- [ ] Fix touches adjacent behavior -> **(C)** run targeted non-regression checks. [R2]
- [ ] Fix changes API, data, dependency, or config -> **(C)** apply planning rollback/verification harnesses. [R1]

### 4. Closure

- [ ] Verification incomplete -> **(C)** do not close; mark NOT VERIFIED and next action. [R1]
- [ ] Verification passes -> **(A)** record command, result, regression artifact, residual risk. [R3]

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C6] NIST SP 800-218 SSDF | Verification and response | verified-2026 | 2026-06 |
| R2 | C | [C12] Google Testing Blog | Regression testing | verified-2026 | 2026-06 |
| R3 | A | Software Engineering at Google | Bug fix reviewability | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
