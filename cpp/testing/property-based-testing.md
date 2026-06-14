---
type: harness
id: "cpp-property-based-testing"
title: "C++ Property-Based Testing Checklist"
language: "cpp"
category: "testing"
tier: "C"
scope: "Use property-based tests to verify C++ invariants, round trips, parser behavior, and algorithm laws across generated input spaces"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [property-based-testing, invariants, generators, shrinking, testing]
based_on:
  - "[C] Google Testing Blog"
  - "[A] RapidCheck Documentation"
  - "[A] Catch2 Generators Documentation"
  - "[A] Hypothesis property-based testing concepts"
related:
  - "common/testing/testing-strategy.md"
  - "cpp/testing/mutation-testing.md"
  - "cpp/testing/fuzzing.md"
  - "cpp/testing/googletest-patterns.md"
  - "cpp/testing/catch2-patterns.md"
  - "cpp/serialization/parsing-and-validation.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Property-Based Testing Checklist

**Based on:** Google Testing guidance ([C]), RapidCheck ([A]), Catch2 generators ([A]), Hypothesis concepts ([A]).
**Scope:** Applies when behavior can be expressed as invariants over many inputs rather than a few examples.

---

## Checklist

### 1. Property Selection

- [ ] Function has algebraic laws, invariants, idempotence, ordering, serialization round trips, or parser acceptance rules -> **(C)** define properties in addition to examples. [R1]
- [ ] Only one hand-picked example exists for broad input behavior -> **(A)** add generated cases. [R1]

### 2. Generator Design

- [ ] Inputs have constraints -> **(A)** encode valid and invalid generators separately. [R2][R3]
- [ ] Generator cannot produce edge cases -> **(A)** add boundary values explicitly. [R2]
- [ ] Generated values are too large or slow -> **(A)** bound size and complexity. [R2]

### 3. Shrinking and Reproducibility

- [ ] Property fails -> **(A)** preserve seed and minimized counterexample. [R2]
- [ ] Test is flaky -> **(C)** pin seed in CI or fix nondeterminism before gating. [R1]

### 4. Oracles

- [ ] Exact output is hard to specify -> **(A)** compare against invariant, reference implementation, round trip, or metamorphic relation. [R1]
- [ ] Reference implementation differs -> **(A)** minimize and review before assuming test bug. [R1]

### 5. CI Gate

- [ ] Property test is fast and deterministic -> **(C)** run in PR CI. [R1]
- [ ] Property test is expensive -> **(A)** run smaller PR budget and larger scheduled budget. [R1]

---

## Decision Tree

```
Behavior spans many inputs?
  -> State invariant/property
  -> Build valid/invalid generators
  -> Preserve failing seed
  -> Gate fast properties in CI
```

---

## Anti-Patterns

### Anti-Pattern 1: Random Examples Without Properties

- **Appearance:** Test generates random inputs but asserts only "does not crash."
- **Trap:** It feels broad.
- **Consequence:** Wrong outputs pass.
- **Fix:** Assert invariants, round trips, or metamorphic relations.

### Anti-Pattern 2: Unreproducible Failure

- **Appearance:** CI fails with a random case but no seed.
- **Trap:** Randomness found the bug.
- **Consequence:** Developers cannot reproduce or fix it.
- **Fix:** Print seed and minimized counterexample.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C12] Google Testing Blog | Test quality and reliability | verified-2026 | 2026-06 |
| R2 | A | RapidCheck Documentation | Generators, shrinking, properties | verified-2026 | 2026-06 |
| R3 | A | Catch2 Generators Documentation | Generator-based tests | verified-2026 | 2026-06 |
| R4 | A | Hypothesis Concepts | Property testing concepts | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
