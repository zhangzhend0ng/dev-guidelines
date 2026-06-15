---
type: harness
id: "common-bug-report-triage"
title: "Bug Report Triage Checklist"
language: "common"
category: "debugging"
tier: "A"
scope: "Triage bug reports into reproducible, prioritized, assigned debugging work with clear evidence requirements"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "24m"
tags: [debugging, triage, bug-report, severity]
based_on:
  - "[A] Software Engineering at Google"
  - "[A] The Pragmatic Programmer"
  - "[A] Release It!"
related:
  - "common/debugging/reproduction-and-minimization.md"
  - "common/debugging/root-cause-analysis.md"
  - "common/debugging/fix-verification.md"
  - "common/planning/risk-and-verification-plan.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Bug Report Triage Checklist

**Based on:** Software Engineering at Google ([A]), Pragmatic Programmer ([A]), Release It! ([A]).
**Scope:** Applies when a bug report, failing test, production issue, or AI-discovered defect enters the workflow.

---

## Checklist

### 1. Symptom

- [ ] Report lacks observed behavior -> **(A)** request symptom, expected behavior, and affected version. [R1]
- [ ] Symptom is ambiguous -> **(A)** classify as needs-info before debugging. [R1]

### 2. Impact

- [ ] Bug affects security, data loss, availability, correctness, or release blocking -> **(A)** mark high priority and require verification plan. [R3]
- [ ] Impact is unknown -> **(A)** record unknown and investigate before broad fix. [R1]

### 3. Reproduction

- [ ] No reproduction exists -> **(A)** route to reproduction/minimization before root cause claims. [R2]
- [ ] Reproduction is flaky -> **(A)** mark confidence and collect environment details. [R1]

### 4. Ownership

- [ ] Component owner is unclear -> **(A)** assign triage owner, not fix owner. [R1]
- [ ] AI agent is used -> **(A)** require concise status and NOT VERIFIED when reproduction is missing. [R1]

### 5. Exit Criteria

- [ ] Triage completes -> **(A)** report severity, owner, repro status, suspected component, and next step. [R1]

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | Software Engineering at Google | Bug tracking and maintenance | verified-2026 | 2026-06 |
| R2 | A | The Pragmatic Programmer | Debugging discipline | verified-2026 | 2026-06 |
| R3 | A | Release It! | Production impact and stability | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
