---
type: harness
id: "cpp-secure-coding"
title: "C++ Secure Coding Checklist"
language: "cpp"
category: "security"
tier: "N"
scope: "Apply C++ secure coding gates across input validation, memory safety, integer safety, undefined behavior, concurrency, dependencies, and verification"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [security, secure-coding, cpp, memory-safety, ub, input-validation]
based_on:
  - "[N] ISO C++"
  - "[C] SEI/CERT C++ Coding Standard"
  - "[C] C++ Core Guidelines"
  - "[C] CWE Top 25"
  - "[C] OWASP ASVS"
related:
  - "common/security/input-validation.md"
  - "common/dependencies/dependency-management.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/correctness/integer-safety.md"
  - "cpp/correctness/type-safety.md"
  - "cpp/memory/ownership.md"
  - "cpp/lifetime/dangling-references.md"
  - "cpp/concurrency/thread-safety.md"
  - "cpp/serialization/parsing-and-validation.md"
  - "cpp/testing/fuzzing.md"
  - "cpp/testing/static-analysis.md"
  - "cpp/testing/sanitizers.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Secure Coding Checklist

**Based on:** ISO C++ ([N]), SEI/CERT C++ ([C]), C++ Core Guidelines ([C]), CWE Top 25 ([C]), OWASP ASVS ([C]).
**Scope:** Security entry point for C++ code changes. This harness routes to the detailed C++ correctness, memory, input, dependency, static-analysis, and sanitizer harnesses.

---

## Checklist

### 1. Trust Boundary

- [ ] Code accepts input from user, file, network, environment, IPC, plugin, dependency, or model output -> **(C)** apply input validation before parsing or acting. [R4][R5]
- [ ] Input controls size, index, count, allocation, path, command, or format -> **(C)** validate type, range, length, canonical form, and ownership. [R2][R4]

### 2. Memory and Lifetime

- [ ] Code owns resources -> **(N)** use RAII and explicit ownership; avoid naked owning pointers. [R1][R3]
- [ ] Code stores references, views, iterators, spans, or callbacks -> **(C)** verify lifetime and invalidation rules. [R2][R3]
- [ ] Code crosses C API boundaries -> **(C)** document ownership transfer and error handling. [R2]

### 3. Integer and Type Safety

- [ ] Code performs arithmetic on sizes, offsets, indexes, lengths, or serialized values -> **(N)** apply integer-safety checks. [R1][R2]
- [ ] Code converts between signed/unsigned, wide/narrow, enum/integer, or pointer/integer -> **(C)** apply type-safety checks. [R2][R3]
- [ ] Overflow or truncation affects allocation or bounds -> **(C)** treat as security-relevant. [R2][R4]

### 4. Undefined Behavior

- [ ] Code uses casts, aliasing, object lifetime tricks, uninitialized data, shifts, pointer arithmetic, or concurrency -> **(N)** apply undefined-behavior prevention. [R1][R2]
- [ ] Code depends on compiler extension or optimization-sensitive behavior -> **(C)** document and verify against the supported toolchain. [R1][R3]

### 5. Concurrency

- [ ] Code shares mutable state across threads -> **(C)** define synchronization, ownership, and lifetime. [R2][R3]
- [ ] Code uses atomics, lock-free structures, callbacks, or async cancellation -> **(C)** require thread-safety review and sanitizer/static-analysis coverage where available. [R2]

### 6. Dependencies and Build Surface

- [ ] Code adds or upgrades a dependency -> **(C)** apply dependency and package-management harnesses. [R4][R5]
- [ ] Build flags, compiler version, or platform assumptions change -> **(C)** apply toolchain and compiler-flags harness. [R3]

### 7. Verification Gate

- [ ] Security-sensitive C++ changed -> **(C)** run relevant tests plus static analysis and sanitizer checks when feasible. [R2][R4]
- [ ] Verification cannot be run -> **(A)** mark NOT VERIFIED and require human approval or follow-up before release. [R4]
- [ ] Weak AI model produced the change -> **(A)** require concise evidence summary, not raw logs. [R4]

---

## Decision Tree

```
C++ security-sensitive change?
  -> Trust boundary?
  -> Memory/lifetime?
  -> Integer/type conversion?
  -> UB/concurrency?
  -> Dependency/toolchain?
  -> Static analysis + sanitizer/test evidence
```

---

## Anti-Patterns

### Anti-Pattern 1: Security as Input Validation Only

- **Appearance:** External input is checked, but size arithmetic or ownership is unchecked.
- **Trap:** Input validation feels like the security boundary.
- **Consequence:** Valid-looking input still triggers overflow, UB, or lifetime bugs.
- **Fix:** Route through integer, type, ownership, lifetime, and UB harnesses.

### Anti-Pattern 2: "Compiler Would Catch It"

- **Appearance:** Review relies on compilation alone for C++ security.
- **Trap:** Many dangerous C++ bugs compile cleanly.
- **Consequence:** UB, data races, and ownership bugs reach production.
- **Fix:** Add static analysis, sanitizers, and targeted tests.

---

## See Also

- [Input Validation](../../common/security/input-validation.md) - trust boundary validation
- [Dependency Management](../../common/dependencies/dependency-management.md) - supply-chain controls
- [Undefined Behavior Prevention](../correctness/undefined-behavior.md) - UB security risks
- [Integer Safety](../correctness/integer-safety.md) - overflow and size bugs
- [Type Safety and Implicit Conversions](../correctness/type-safety.md) - conversion hazards
- [Smart Pointer and Ownership Semantics](../memory/ownership.md) - ownership design
- [Object Lifetime and Dangling References](../lifetime/dangling-references.md) - lifetime hazards
- [Concurrency and Thread Safety](../concurrency/thread-safety.md) - data races and synchronization
- [C++ Static Analysis](../testing/static-analysis.md) - static security gates
- [Sanitizer Integration and Usage](../testing/sanitizers.md) - runtime security gates

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | [N1] ISO C++ Standard | Core language rules | verified-2026 | 2026-06 |
| R2 | C | [C2] SEI/CERT C++ Coding Standard | Secure C++ rules | verified-2026 | 2026-06 |
| R3 | C | [C1] C++ Core Guidelines | Resource, lifetime, type, concurrency guidance | verified-2026 | 2026-06 |
| R4 | C | [C3] CWE Top 25 | Memory, integer, injection, race weaknesses | verified-2026 | 2026-06 |
| R5 | C | [C8] OWASP ASVS | Validation, dependency, logging, access control | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
