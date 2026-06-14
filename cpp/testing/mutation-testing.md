---
type: harness
id: "cpp-mutation-testing"
title: "C++ Mutation Testing Checklist"
language: "cpp"
category: "testing"
tier: "A"
scope: "Use mutation testing selectively to measure whether C++ tests detect meaningful behavioral changes"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "24m"
tags: [mutation-testing, test-quality, coverage, regression]
based_on:
  - "[A] Mull Mutation Testing Documentation"
  - "[A] PIT Mutation Testing Concepts"
  - "[C] Google Testing Blog"
related:
  - "common/testing/testing-strategy.md"
  - "cpp/testing/property-based-testing.md"
  - "cpp/testing/static-analysis.md"
  - "cpp/testing/fuzzing.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Mutation Testing Checklist

**Based on:** Mull mutation testing docs ([A]), PIT mutation testing concepts ([A]), Google Testing guidance ([C]).
**Scope:** Applies when line/branch coverage is not enough to show that tests detect behavioral changes.

---

## Checklist

### 1. Target Selection

- [ ] Code is high-value, algorithmic, parser-related, security-sensitive, or regression-prone -> **(A)** consider mutation testing. [R1][R3]
- [ ] Code is trivial glue or generated -> **(A)** do not spend mutation budget there. [R3]

### 2. Baseline

- [ ] Mutation testing is introduced into legacy code -> **(A)** baseline current mutation score and fail only regressions first. [R1]
- [ ] Mutants survive -> **(A)** classify as missing test, equivalent mutant, or intentional behavior gap. [R1][R2]

### 3. CI Budget

- [ ] Mutation run is fast enough -> **(A)** run on PRs for touched targets. [R1]
- [ ] Mutation run is expensive -> **(A)** run scheduled or on demand; gate only selected critical modules. [R1]

### 4. Test Quality Action

- [ ] Surviving mutant reveals missing assertion -> **(A)** add focused test or property. [R2][R3]
- [ ] Surviving mutant is equivalent -> **(A)** suppress with documented reason. [R1]

### 5. Human Work Reduction

- [ ] Mutation output is large -> **(A)** summarize surviving mutants by file, operator, and required action. [R1]
- [ ] Weak AI model reviews mutation output -> **(A)** require concise report; no raw mutant dump. [R3]

---

## Decision Tree

```
Need test-quality evidence?
  -> Choose high-value target
  -> Run mutation tool
  -> Classify survivors
  -> Add tests or suppress equivalents
  -> Track score trend
```

---

## Anti-Patterns

### Anti-Pattern 1: Mutation Score Theater

- **Appearance:** Team chases a global mutation percentage.
- **Trap:** One number looks objective.
- **Consequence:** Time is spent on low-risk code.
- **Fix:** Apply mutation testing to high-value targets and regressions.

### Anti-Pattern 2: Equivalent Mutant Churn

- **Appearance:** Developers repeatedly investigate mutants that cannot change behavior.
- **Trap:** Every survivor looks like missing coverage.
- **Consequence:** Review time is wasted.
- **Fix:** Suppress equivalent mutants with reason and review date.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | Mull Mutation Testing Documentation | C++ mutation workflow | verified-2026 | 2026-06 |
| R2 | A | PIT Mutation Testing Concepts | Survivor classification | verified-2026 | 2026-06 |
| R3 | C | [C12] Google Testing Blog | Test quality and reliability | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
