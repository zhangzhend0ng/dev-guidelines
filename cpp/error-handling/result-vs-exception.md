---
type: harness
id: "cpp-result-vs-exception"
title: "C++ Result vs Exception Checklist"
language: "cpp"
category: "design"
tier: "C"
scope: "Choose between exceptions, result types, error codes, assertions, and termination for C++ error handling boundaries"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [error-handling, exceptions, result, expected, error-codes]
based_on:
  - "[C] C++ Core Guidelines E.1-E.31"
  - "[C] SEI/CERT C++ ERR rules"
  - "[A] Exceptional C++"
  - "[A] std::expected design guidance"
related:
  - "cpp/runtime/observability-and-diagnostics.md"
  - "common/error-handling/error-handling-strategy.md"
  - "cpp/correctness/exception-safety.md"
  - "cpp/correctness/interface-contracts.md"
  - "cpp/memory/raii.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Result vs Exception Checklist

**Based on:** C++ Core Guidelines ([C]), SEI/CERT C++ ERR rules ([C]), Exceptional C++ ([A]), `std::expected` design guidance ([A]).
**Scope:** Applies when selecting an error handling mechanism for C++ APIs and internal boundaries.

---

## Checklist

### 1. Error Category

- [ ] Programmer error or violated precondition -> **(C)** use assertion/contract mechanism, not recoverable error flow. [R1]
- [ ] Runtime failure caller can handle -> **(C)** use exception or result type consistently. [R1][R2]
- [ ] Fatal invariant failure -> **(A)** terminate with diagnostic rather than continuing in corrupted state. [R2]

### 2. Exceptions

- [ ] Codebase uses exceptions and RAII -> **(C)** prefer exceptions for failures that cannot be handled locally. [R1][R3]
- [ ] Function is destructor, move, swap, or low-level cleanup -> **(C)** respect `noexcept` and exception-safety harness. [R1][R2]

### 3. Result Types

- [ ] API boundary must make errors explicit, avoid exceptions, or cross ABI/language boundary -> **(A)** use result/expected/error-code style. [R1][R4]
- [ ] Caller may ignore result -> **(C)** use `[[nodiscard]]` or equivalent enforcement. [R1]

### 4. Error Codes

- [ ] Interop with C/system APIs -> **(A)** preserve native error information and convert at boundary. [R2]
- [ ] Error code lacks context -> **(A)** attach operation, resource, and recovery context. [R3]

### 5. Consistency Gate

- [ ] New API differs from module convention -> **(C)** document why and update caller expectations. [R1]
- [ ] AI suggests changing error style broadly -> **(A)** reject unless task explicitly includes migration. [R1]

---

## Decision Tree

```
Error condition?
  -> Programmer bug? assert/contract
  -> Recoverable and exceptions allowed? exception
  -> Boundary/no exceptions? result/expected/error_code
  -> Fatal invariant? terminate with diagnostic
```

---

## Anti-Patterns

### Anti-Pattern 1: Boolean Failure

- **Appearance:** Function returns `false` with no error context.
- **Trap:** It is simple.
- **Consequence:** Callers cannot diagnose or recover.
- **Fix:** Return structured error or throw meaningful exception.

### Anti-Pattern 2: Mixed Local Style

- **Appearance:** One module mixes exceptions, null returns, bools, and error codes.
- **Trap:** Each call site picked what was convenient.
- **Consequence:** Callers miss failures.
- **Fix:** Pick one convention per boundary and enforce it.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C1] C++ Core Guidelines | E.1-E.31 | verified-2026 | 2026-06 |
| R2 | C | [C2] SEI/CERT C++ Coding Standard | ERR rules | verified-2026 | 2026-06 |
| R3 | A | Exceptional C++ | Error and exception safety guidance | verified-2026 | 2026-06 |
| R4 | A | std::expected design guidance | Explicit result style | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
