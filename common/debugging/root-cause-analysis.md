---
type: harness
id: "common-root-cause-analysis"
title: "Root Cause Analysis Checklist"
language: "common"
category: "debugging"
tier: "A"
scope: "Establish evidence-backed root cause before implementing or accepting a bug fix"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "24m"
tags: [debugging, root-cause, evidence, rca]
based_on:
  - "[A] The Pragmatic Programmer"
  - "[A] Release It!"
  - "[C] NIST SP 800-218 SSDF"
related:
  - "common/debugging/bug-report-triage.md"
  - "common/debugging/reproduction-and-minimization.md"
  - "common/debugging/fix-verification.md"
  - "cpp/debugging/sanitizer-triage.md"
  - "common/planning/requirements-gap-analysis.md"
  - "common/ai/model-capability-and-instruction-adherence.md"
  - "cpp/debugging/crash-dump-analysis.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Root Cause Analysis Checklist

**Based on:** Pragmatic Programmer ([A]), Release It! ([A]), NIST SSDF ([C]).
**Scope:** Applies after reproduction exists and before fix acceptance.

---

## Checklist

### 1. Evidence

- [ ] Root cause is claimed without reproduction or trace evidence -> **(A)** reject as hypothesis. [R1]
- [ ] Evidence points to multiple causes -> **(A)** isolate with experiment or instrumentation. [R1][R2]

### 2. Fault Model

- [ ] Cause is "bad input" -> **(A)** identify why validation or handling failed. [R3]
- [ ] Cause is "race/flaky" -> **(A)** identify synchronization, timing, environment, or test isolation failure. [R2]

### 3. Fix Link

- [ ] Proposed fix does not directly address root cause -> **(C)** require explanation or reject. [R3]
- [ ] Fix only masks symptom -> **(A)** document residual risk and follow-up. [R2]

### 4. Human Work Reduction

- [ ] AI summarizes debugging -> **(A)** require symptom, evidence, root cause, fix, verification; no raw log dump. [R1]

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | The Pragmatic Programmer | Debugging discipline | verified-2026 | 2026-06 |
| R2 | A | Release It! | Stability failure analysis | verified-2026 | 2026-06 |
| R3 | C | [C6] NIST SP 800-218 SSDF | Response and verification | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
