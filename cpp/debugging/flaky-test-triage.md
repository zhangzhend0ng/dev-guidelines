---
type: harness
id: "cpp-debugging-flaky-test-triage"
title: "C++ Flaky Test Triage Checklist"
language: "cpp"
category: "debugging"
tier: "C"
scope: "Diagnose and stabilize intermittent C++ test failures caused by timing, concurrency, shared state, randomness, environment, or undefined behavior"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags:
  - debugging
  - flaky-tests
  - testing
  - concurrency
  - ci
based_on:
  - "[C] Google Testing Blog Test Sizes"
  - "[C] C++ Core Guidelines"
  - "[A] Software Engineering at Google"
related:
  - "common/testing/testing-strategy.md"
  - "common/debugging/reproduction-and-minimization.md"
  - "common/debugging/fix-verification.md"
  - "cpp/testing/googletest-patterns.md"
  - "cpp/testing/catch2-patterns.md"
  - "cpp/testing/sanitizers.md"
  - "cpp/concurrency/thread-safety.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Flaky Test Triage Checklist

**Based on:** Google test sizing guidance ([C]), C++ Core Guidelines ([C]), Software Engineering at Google ([A]).
**Scope:** Applies when a C++ test passes and fails without intentional source changes. This covers triage and stabilization, not general test design.

---

## Checklist

### 1. Confirm Flakiness

- [ ] Test failed once in CI -> **(C)** preserve failing log, seed, platform, compiler, and commit before rerunning. [R1][R3]
- [ ] Failure disappears on rerun -> **(C)** mark as flaky candidate, not fixed. [R3]
- [ ] Same test fails repeatedly under same input -> **(A)** treat as deterministic failure and use normal debugging. [R3]

### 2. Classify the Flake Source

- [ ] Test uses time, sleep, thread scheduling, or async callbacks -> **(C)** suspect timing/concurrency first. [R2]
- [ ] Test uses random data -> **(C)** print and replay seed. [R3]
- [ ] Test touches filesystem, environment, global state, locale, network, or singleton state -> **(C)** isolate or reset that state. [R1]
- [ ] Test fails only under sanitizer/optimized build -> **(N)** investigate undefined behavior or data race. [R2]

### 3. Reproduce Under Stress

- [ ] Flake is rare -> **(A)** run repeated iterations, shuffled order, parallel execution, and target platform. [R3]
- [ ] Failure may depend on test order -> **(C)** run the test alone and after suspected preceding tests. [R1]
- [ ] Failure may depend on concurrency -> **(C)** run under TSan or stress scheduler where available. [R2]

### 4. Stabilize the Test or Product

- [ ] Product bug found -> **(C)** fix product code and keep the test as regression coverage. [R2]
- [ ] Test race or timing assumption found -> **(C)** replace sleeps with deterministic synchronization or controllable clocks. [R1][R2]
- [ ] Shared state leak found -> **(C)** reset fixture state and remove order dependence. [R1]
- [ ] Flake blocks delivery before fix -> **(A)** quarantine with owner, issue, and expiry; do not silently disable. [R3]

### 5. Verify Stability

- [ ] Fix is proposed -> **(C)** run the formerly flaky test repeatedly with the failing seed/order/platform. [R3]
- [ ] Concurrency was involved -> **(C)** include sanitizer or stress verification. [R2]
- [ ] Quarantine remains -> **(A)** track expiration and restore merge gate after fix. [R3]

---

## Decision Tree

```
Intermittent C++ test?
  -> Preserve failure context
  -> Classify timing/random/state/environment/UB/concurrency
  -> Reproduce with seed, order, stress, platform
  -> Fix product or deterministic test control
  -> Verify repeated stability
  -> Quarantine only with owner and expiry
```

---

## Anti-Patterns

### Anti-Pattern 1: Rerun Until Green

- **Appearance:** CI is restarted until the test passes.
- **Trap:** Delivery unblocks quickly.
- **Consequence:** The flaky signal becomes invisible and regressions accumulate.
- **Fix:** Track the flake, preserve evidence, and require stabilization work.

### Anti-Pattern 2: Sleeping Longer

- **Appearance:** A timeout or sleep is increased after intermittent failure.
- **Trap:** The local test becomes less likely to fail.
- **Consequence:** CI gets slower while the race remains.
- **Fix:** Use deterministic synchronization, fake clocks, or explicit readiness signals.

---

## See Also

- [Testing Strategy](../../common/testing/testing-strategy.md) - flaky test management
- [Sanitizer Integration and Usage](../testing/sanitizers.md) - sanitizer evidence for UB and races
- [Concurrency and Thread Safety](../concurrency/thread-safety.md) - C++ data race prevention

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Google Testing Blog | test sizes and hermetic tests | verified-2026 | 2026-06 |
| R2 | C | [C1] C++ Core Guidelines | concurrency, lifetime, undefined behavior | verified-2026 | 2026-06 |
| R3 | A | Software Engineering at Google | flaky tests and CI practice | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
