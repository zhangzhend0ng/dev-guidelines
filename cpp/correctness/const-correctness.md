---
type: harness
id: "cpp-const-correctness"
title: "Const Correctness Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Ensure const is applied correctly to parameters, member functions, and return types in C++"
version: "2026.05"
status: "draft"
stable_since: ""
last_validated: "2026-05-31"
review_cycle: "12m"
tags: [const, correctness, immutability, type-safety]
based_on:
  - "[N] ISO C++ [dcl.type.cv], [class.this]"
  - "[C] C++ Core Guidelines Con.1-Con.5, F.15-F.17, F.20"
  - "[C] SEI/CERT EXP55-CPP"
  - "[A] Effective C++ Item 3 (Meyers)"
related: []
supersedes: []
changelog:
  - "2026.05: Initial draft"
---

# Const Correctness Checklist

**Based on:** ISO C++ [dcl.type.cv]/[class.this] ([N]), C++ Core Guidelines Con.1-Con.5 ([C]), SEI/CERT EXP55-CPP ([C]), Effective C++ Item 3 ([A]).
**Scope:** Verify const is used consistently on parameters, member functions, return types, and local variables.

---

## Concepts

| Concept | Definition |
|----------|-----------|
| **Bitwise const** | Object bytes don't change (compiler-enforced) |
| **Logical const** | Observable state unchanged; `mutable` for caching/mutexes |

---

## Checklist

### 1. Read-Only Parameters

- [ ] Large objects (`> 2*sizeof(void*)`) → **(C)** `const T&` [R2]
- [ ] Small/trivial → **(C)** Pass by value; const optional [R2]
- [ ] Out-parameter → **(C)** Prefer return value; else pointer for call-site visibility [R2]

### 2. Const Member Functions

- [ ] Not modifying observable state? → **(N)** Mark `const`. [R1]
- [ ] **(C)** Use `mutable` for caches/mutexes/lazy-init only — never to subvert const. [R2]
- [ ] **(C)** Const member function → read-only; must be thread-safe for concurrent reads. [R3]

### 3. Const Return Types

- [ ] Return by value? → **(C)** Never `const T` — inhibits move semantics. [R4]
- [ ] Return by reference to member? → **(C)** `const T&` for read-only; `T&` only if mutation intended. [R2]

### 4. Local Variable Constness

- [ ] **(A)** `const` (or `auto const`) by default for unmodified locals. [R4]
- [ ] **(C)** Loop counters/accumulators non-const is idiomatic. [R2]

### 5. Iterator Constness

- [ ] Read-only iteration → **(C)** `cbegin()`/`cend()` or `const auto&` in range-for. [R2]

### 6. Casting Away Const

- [ ] `const_cast` present? → **(N)** Almost always wrong. Valid only: legacy C APIs known to not modify (e.g., `strlen`). [R1]
- [ ] **(N)** Modifying genuinely-const object after `const_cast` = UB. [R1]

### 7. Const Overloads

- [ ] **(C)** Non-const overload should delegate to const overload + `const_cast`, not duplicate logic. [R2]

---

## Decision Tree

```
Read-only parameter?
  ├─ Large → const T& [1]
  └─ Small → by value [1]

Member function modifies state?
  ├─ No → const [2]
  └─ Yes → non-const

Return type?
  ├─ By value → no const qualifier [3]
  └─ By reference → const T& if read-only [3]

const_cast?
  └─ Only for legacy C interop [6]
```

---

## Anti-Patterns

### 1. Missing Const on Getters

- **Appearance:** `int size() { return count_; }`
- **Consequence:** Cannot call on const objects/refs. Propagates non-constness.
- **Fix:** Mark all non-mutating members `const`.

### 2. `const_cast` to Enable Mutation

- **Appearance:** `const_cast<T&>(obj).setX(5);`
- **Consequence:** UB if object is in read-only memory. Violates caller expectation.
- **Fix:** Fix the API. Don't pass as const if mutation is needed.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [dcl.type.cv], [class.this] | verified-2026 | 2026-05 |
| R2 | C | C++ Core Guidelines | Con.1-Con.5, F.15-F.20 | verified-2026 | 2026-05 |
| R3 | C | SEI/CERT C++ | EXP55-CPP | verified-2026 | 2026-05 |
| R4 | A | Effective C++ (Meyers) | Item 3 | verified-2026 | 2026-05 |

---

## Changelog

- 2026.05: Initial draft
