---
type: harness
id: "python-pytest-patterns"
title: "pytest Patterns Checklist"
language: "python"
category: "testing"
tier: "C"
scope: "Write maintainable pytest tests using fixtures, parametrization, assertions, markers, and deterministic isolation"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [python, pytest, testing, fixtures, parametrization]
based_on:
  - "[C] pytest Documentation"
  - "[C] Google Testing Blog"
related:
  - "common/testing/testing-strategy.md"
  - "common/debugging/fix-verification.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# pytest Patterns Checklist

**Based on:** pytest docs ([C]) and Google testing guidance ([C]).
**Scope:** Applies to Python tests written with pytest. General test strategy is covered by the common testing harness.

---

## Checklist

### 1. Test Names and Structure

- [ ] Test name is vague -> **(C)** name behavior and expected result, not implementation detail. [R1]
- [ ] Test has multiple independent behaviors -> **(A)** split into separate tests or parametrized cases. [R1]

### 2. Fixtures

- [ ] Setup is shared -> **(C)** use fixtures with explicit scope and dependencies. [R1]
- [ ] Fixture mutates global state, filesystem, env, or clock -> **(C)** restore state after the test. [R1][R2]
- [ ] Fixture scope is broader than needed -> **(A)** reduce scope to avoid order dependence. [R1]

### 3. Parametrization

- [ ] Same assertion applies to multiple inputs -> **(C)** use parametrization instead of manual loops. [R1]
- [ ] Failure needs context -> **(C)** give parametrized cases readable IDs. [R1]

### 4. Assertions and Exceptions

- [ ] Expected exception path -> **(C)** use pytest exception assertion and check the meaningful message or attribute. [R1]
- [ ] Assertion compares complex structures -> **(A)** assert directly on values so pytest can render useful diffs. [R1]

### 5. CI and Flakiness

- [ ] Test uses network, time, random, or concurrency -> **(C)** mark, isolate, seed, or fake the dependency. [R2]
- [ ] Test is known flaky -> **(C)** quarantine with owner and issue; do not silently skip. [R2]
- [ ] Bug fix has repro -> **(C)** add a regression test or document why not. [R2]

---

## Decision Tree

```
New pytest test?
  -> behavior name
  -> fixture for shared setup
  -> parametrize repeated cases
  -> direct assertions
  -> isolate time/random/io/global state
```

---

## Anti-Patterns

### Anti-Pattern 1: Hidden Global State

- **Appearance:** Tests pass alone but fail in a suite.
- **Trap:** Global mutation is easy in Python.
- **Consequence:** Order-dependent CI failures.
- **Fix:** Use fixtures that reset state and keep fixture scope narrow.

### Anti-Pattern 2: Manual Case Loop

- **Appearance:** A test loops over many inputs and stops at first failure.
- **Trap:** It is simple Python.
- **Consequence:** Only one failing case is reported.
- **Fix:** Use parametrization with case IDs.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C26] pytest Documentation | fixtures, parametrization, assertions | verified-2026 | 2026-06 |
| R2 | C | [C12] Google Testing Blog | test isolation, regression, flaky tests | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
