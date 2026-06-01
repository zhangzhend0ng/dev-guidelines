---
type: harness
id: "common-testing-strategy"
title: "Testing Strategy Checklist"
language: "common"
category: "testing"
tier: "C"
scope: "Establish test classification, pyramid proportions, mocking rules, and flaky test management for any codebase"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [testing, unit-tests, integration-tests, tdd, quality]
based_on:
  - "[C] Google Test Sizes (Small/Medium/Large)"
  - "[C] Martin Fowler — TestPyramid"
  - "[A] xUnit Test Patterns (Meszaros, 2007)"
  - "[A] Working Effectively with Legacy Code (Feathers, 2004)"
  - "[A] Software Engineering at Google Ch.11 (2020)"
related: []
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Testing Strategy Checklist

**Based on:** Google Test Sizes ([C]), Fowler TestPyramid ([C]), xUnit Test Patterns ([A]), Working Effectively with Legacy Code ([A]), SWE at Google Ch.11 ([A]).
**Scope:** Test classification and strategy decisions. Language-agnostic; language harnesses define specific frameworks.

---

## Concepts

| Size | Scope | Execution | I/O |
|------|-------|-----------|-----|
| Small (Unit) | Single function/class | <100ms | None |
| Medium (Integration) | Multiple classes/modules | <1s | Localhost |
| Large (E2E) | Full system | Variable | Real services |

**Target distribution:** ~70% Small, ~20% Medium, ~10% Large. Deviations require documented justification.

---

## Checklist

### 1. Test Size Classification  **(C)** [R1]

- [ ] Every test classified as Small, Medium, or Large per Google definitions → **(C)** [R1]
- [ ] Small tests: zero I/O, <100ms → **(C)** [R1]

### 2. Pyramid Proportion  **(C)** [R1][R2]

- [ ] Small ≥ 60%, Medium ≤ 30%, Large ≤ 10% → **(C)** [R2]
- [ ] Deviation >20% from target → documented justification → **(C)** [R2]

### 3. Test Naming Convention  **(C)** [R3]

- [ ] `Given<Context>_When<Action>_Then<ExpectedResult>` or equivalent documented convention → **(C)** [R3]
- [ ] Test name describes behavior, not implementation → **(C)** [R3]

### 4. Property-Based Testing  **(C)** [R1]

- [ ] Functions with algorithmic properties (roundtrip, idempotence, commutativity) → at least one property-based test → **(C)** [R1]

### 5. Mocking Rules  **(C)** [R4]

- [ ] Mock only at architectural boundaries: I/O, network, clock, external services → **(C)** [R4]
- [ ] Never mock SUT's own types or value objects → **(C)** [R4]
- [ ] Prefer real instances over mocks for in-process dependencies → **(C)** [R4]

### 6. Flaky Test Management  **(C)** [R1][R5]

- [ ] Any inconsistently failing test → quarantined (skipped + ticketed) within 24h → **(C)** [R5]
- [ ] Never commit a known-flaky test → **(C)** [R5]
- [ ] Same test fails 3 of 10 CI runs → auto-skip with alert → **(C)** [R1]

### 7. Coverage as Signal  **(A)** [R1][R5]

- [ ] Track coverage trends; do NOT gate on fixed percentage → **(A)** [R5]
- [ ] Sudden drop >5% → explain in PR → **(A)** [R1]

---

## Decision Tree

```
New test needed?
  ├─ Unit-level logic → Small (no I/O, <100ms)
  ├─ Cross-module → Medium (localhost)
  └─ Full-system → Large (sparingly)

Pyramid [2]: 70/20/10 maintained?
Naming [3]: Given/When/Then?
Algorithmic property? → Property-based [4]
Mock boundaries only [5]
Flaky? → Quarantine in 24h [6]
Coverage trend [7]
```

---

## Anti-Patterns

### 1. 100% Coverage Target

- **Appearance:** CI fails if coverage <90%. Teams write weak tests to pass.
- **Fix:** Track trend. Review uncovered paths, not just percentage.

### 2. Mock Everything

- **Appearance:** Every dependency mocked, including value objects.
- **Fix:** Mock architectural boundaries only. Use real objects for in-process deps.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Google Testing Blog | Test Sizes | verified-2026 | 2026-06 |
| R2 | C | Martin Fowler | TestPyramid | verified-2026 | 2026-06 |
| R3 | A | xUnit Test Patterns (Meszaros) | Test naming | verified-2026 | 2026-06 |
| R4 | A | Working Effectively with Legacy Code (Feathers) | Mocking | verified-2026 | 2026-06 |
| R5 | A | SWE at Google Ch.11 (Winters) | Testing | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
