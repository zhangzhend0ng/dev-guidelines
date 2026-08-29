---
type: harness
id: "cpp-debugging-sanitizer-triage"
title: "C++ Sanitizer Report Triage Checklist"
language: "cpp"
category: "debugging"
tier: "C"
scope: "Triage ASan, UBSan, TSan, MSan, and LSan reports into reproducible root causes, suppressions, or verified fixes"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags:
  - debugging
  - sanitizers
  - triage
  - asan
  - ubsan
  - tsan
based_on:
  - "[N] ISO/IEC 14882 C++ Standard"
  - "[C] LLVM Compiler-RT Sanitizer Documentation"
  - "[A] Google Sanitizers Wiki"
related:
  - "common/debugging/reproduction-and-minimization.md"
  - "common/debugging/root-cause-analysis.md"
  - "common/debugging/fix-verification.md"
  - "cpp/testing/sanitizers.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/concurrency/thread-safety.md"
  - "common/ai/ai-assisted-cpp-development.md"
  - "cpp/testing/catch2-patterns.md"
  - "cpp/testing/googletest-patterns.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Sanitizer Report Triage Checklist

**Based on:** ISO C++ undefined behavior and race rules ([N]), LLVM sanitizer docs ([C]), Google sanitizer usage guidance ([A]).
**Scope:** Applies when sanitizer output appears in local development or CI. This harness covers triage and fix validation, not sanitizer build integration.

---

## Checklist

### 1. Preserve the Report

- [ ] Sanitizer output is unsymbolized -> **(C)** rerun or symbolize before root-cause analysis. [R2]
- [ ] Report came from CI -> **(C)** capture build ID, compiler, sanitizer flags, test name, and environment options. [R2]
- [ ] Multiple reports appear -> **(A)** triage the first fatal report first unless later reports have independent evidence. [R2]

### 2. Classify the Sanitizer Signal

- [ ] ASan/LSan report -> **(N)** treat use-after-free, overflow, double-free, and leak reports as real defects until disproven. [R1][R2]
- [ ] UBSan report -> **(N)** identify the C++ rule violated before changing code. [R1]
- [ ] TSan report -> **(N)** map both access stacks to the shared object and synchronization edge. [R1][R2]
- [ ] MSan report -> **(C)** trace the uninitialized origin, not only the read site. [R2]

### 3. Reproduce and Minimize

- [ ] Failure is nondeterministic -> **(C)** rerun with fixed seed, repeated iterations, and preserved sanitizer options. [R2]
- [ ] Failure needs large input -> **(A)** minimize the input or test case before editing broad logic. [R3]
- [ ] Report depends on optimization or platform -> **(A)** record that constraint in the bug note and verification plan. [R2]

### 4. Fix the Ownership or Synchronization Cause

- [ ] Memory lifetime bug -> **(N)** fix ownership, bounds, or object lifetime; do not mask the read/write site only. [R1]
- [ ] UB report -> **(N)** replace the undefined operation with defined behavior or explicit validation. [R1]
- [ ] Data race -> **(N)** add a correct happens-before relationship or remove shared mutable state. [R1]
- [ ] Third-party false positive suspected -> **(C)** prove it with upstream issue, minimal reproduction, or documented suppression. [R2]

### 5. Verify the Fix

- [ ] Fix is proposed -> **(C)** rerun the same sanitizer target that failed. [R2]
- [ ] Bug was nondeterministic -> **(A)** run repeated sanitizer iterations or stress schedule after the fix. [R2]
- [ ] Suppression is added -> **(C)** include reason, owner, date, and review deadline. [R2]

---

## Decision Tree

```
Sanitizer report?
  -> Preserve full symbolized report
  -> Classify ASan/UBSan/TSan/MSan/LSan
  -> Reproduce and minimize
  -> Fix root ownership/UB/synchronization cause
  -> Rerun the failing sanitizer target
  -> Suppress only with documented proof
```

---

## Anti-Patterns

### Anti-Pattern 1: Treating Sanitizers as Warnings

- **Appearance:** CI logs show sanitizer output, but the patch still passes review.
- **Trap:** The program continued far enough to print more logs.
- **Consequence:** Undefined behavior or memory corruption remains in the codebase.
- **Fix:** Sanitizer reports are hard failures unless a documented false positive is proven.

### Anti-Pattern 2: Fixing the Crash Site Only

- **Appearance:** A null check or bounds guard is added at the reported read site.
- **Trap:** The visible failure disappears.
- **Consequence:** The owner, lifetime, or synchronization bug persists elsewhere.
- **Fix:** Trace allocation, ownership transfer, invalidation, and concurrent access stacks.

---

## See Also

- [Sanitizer Integration and Usage](../testing/sanitizers.md) - build and CI setup
- [Reproduction and Minimization](../../common/debugging/reproduction-and-minimization.md) - reducing failing cases
- [Root Cause Analysis](../../common/debugging/root-cause-analysis.md) - evidence-based RCA

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | [N1] ISO/IEC 14882 C++ Standard | undefined behavior, memory model, data races | verified-2026 | 2026-06 |
| R2 | C | LLVM Compiler-RT Sanitizer Documentation | sanitizer reports, symbolization, runtime options | verified-2026 | 2026-06 |
| R3 | A | Google Sanitizers Wiki | triage patterns and suppressions | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
