---
type: harness
id: "cpp-type-safety"
title: "Type Safety and Implicit Conversions Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Prevent narrowing, implicit conversions, signed/unsigned mismatch, and enum misuse in C++"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [type-safety, conversions, enums, explicit, cpp]
based_on:
  - "[N] ISO C++ [dcl.init.list], [conv], [expr.static.cast]"
  - "[C] C++ Core Guidelines C.46, ES.46-ES.49, Enum.3-Enum.7, Type.1-Type.5"
  - "[C] SEI/CERT INT02-C, INT05-C, EXP39-C"
  - "[A] Effective C++ Item 27 (Meyers)"
  - "[A] Effective Modern C++ Items 6-7 (Meyers)"
related:
  - "cpp/serialization/parsing-and-validation.md"
  - "cpp/security/secure-coding.md"
  - "cpp/testing/static-analysis.md"
  - "cpp/correctness/stl-algorithms-containers.md"
  - "cpp/correctness/undefined-behavior.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Type Safety and Implicit Conversions Checklist

**Based on:** ISO C++ ([N]), C++ Core Guidelines ([C]), SEI/CERT ([C]), Effective C++/Modern C++ ([A]).
**Scope:** Prevent implicit narrowing, signed/unsigned bugs, enum misuse, and C-style casts.

---

## Concepts

| Hazard | Safe Alternative |
|--------|-----------------|
| Narrowing | `{}` init catches at compile time |
| Signed/unsigned mismatch | `-Wsign-conversion` as error |
| Implicit bool | `explicit operator bool()` |
| Unscoped enum | `enum class` |
| C-style cast | `static_cast` / named casts |

---

## Checklist

### 1. Explicit Constructors  **(C)** [R2][R4]

- [ ] Single-argument ctors marked `explicit` → **(C)** [R2]
- [ ] C++20: `explicit(bool)` for conditional → **(A)** [R2]

### 2. Enum Class  **(C)** [R2]

- [ ] `enum class` for all new enums → **(C)** [R2]
- [ ] Unscoped `enum` only for C interop with documented reason → **(C)** [R2]

### 3. Avoid Narrowing  **(N)** [R1][R2]

- [ ] `{}` init catches narrowing → **(N)** [R1]
- [ ] `int x{3.14}` — error, not silent truncation → **(N)** [R1]

### 4. Signed/Unsigned  **(C)** [R2][R3]

- [ ] `-Wsign-conversion` as error → **(C)** [R2]
- [ ] Signed for arithmetic; unsigned only for bit manipulation → **(C)** [R3]

### 5. Bool Conversion  **(C)** [R2]

- [ ] `explicit operator bool()` → **(C)** [R2]
- [ ] No implicit non-bool→bool in conditionals → **(C)** [R2]

### 6. No C-Style Casts  **(C)** [R2][R5]

- [ ] `static_cast<T>(x)`, never `(T)x` → **(C)** [R2]
- [ ] `reinterpret_cast` flagged for review → **(A)** [R2]

### 7. Array/Function Pointer Decay  **(C)** [R1]

- [ ] `std::array<T,N>` over C arrays; `std::span<T>` over pointer+size → **(C)** [R2]
- [ ] `std::function` for type-erased callables → **(C)** [R2]

---

## Decision Tree

```
Type safety:
  → Single-arg ctor? → explicit [1]
  → Enum? → enum class [2]
  → Narrowing? → {} init [3]
  → Signed/unsigned? → signed for math [4]
  → Bool? → explicit [5]
  → (T)x? → static_cast<T> [6]
  → Array decay? → std::array/span [7]
```

---

## Anti-Patterns

### 1. C-Style Cast

- **Appearance:** `(int)value`, `(Widget*)ptr`.
- **Trap:** Shorter, works for most conversions.
- **Consequence:** `(int*)&floatVar` compiles silently. Reviewers can't assess safety.
- **Fix:** `static_cast` for compile-time, `reinterpret_cast` for raw bits (flagged).

### 2. Unscoped Enum

- **Appearance:** `enum Color { Red, Green, Blue }; int x = Red;`.
- **Trap:** Simpler than `enum class`.
- **Consequence:** Namespace pollution. Implicit int conversion. Values collide.
- **Fix:** `enum class Color { Red, Green, Blue };`.

---

## See Also

- [Undefined Behavior](undefined-behavior.md) — Type-based UB: strict aliasing, const modification

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ | [dcl.init.list], [conv] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | C.46, ES.46-ES.49, Enum, Type | verified-2026 | 2026-06 |
| R3 | C | SEI/CERT C++ | INT02-C, INT05-C | verified-2026 | 2026-06 |
| R4 | A | Effective C++ (Meyers) | Item 27 | verified-2026 | 2026-06 |
| R5 | A | Effective Modern C++ (Meyers) | Items 6-7 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
