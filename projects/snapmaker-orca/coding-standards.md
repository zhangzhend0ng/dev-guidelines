---
type: harness
id: "snapmaker-orca-coding-standards"
title: "SnapmakerOrca C++ Coding Standards"
language: "cpp"
category: "project-specific"
tier: "P"
scope: "Enforce SnapmakerOrca C++ coding standards — superset of dev-guidelines C++ harnesses with additional restrictions"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-04"
review_cycle: "12m"
tags: [snapmaker-orca, coding-standards, cpp17]
based_on:
  - "[C] SnapmakerOrca 切片部门代码规范文档 v1.0 (2026-06-04)"
  - "[C] C++ Core Guidelines"
  - "[C] SEI/CERT C++ Coding Standard"
related:
  - "cpp/memory/raii.md"
  - "cpp/memory/ownership.md"
  - "cpp/correctness/const-correctness.md"
  - "cpp/correctness/type-safety.md"
  - "cpp/correctness/integer-safety.md"
  - "cpp/concurrency/thread-safety.md"
  - "cpp/functions/parameter-validation.md"
  - "common/security/input-validation.md"
  - "projects/snapmaker-orca/workflow-standards.md"
supersedes: []
changelog:
  - "2026.06: Initial draft from 切片部门代码规范文档 v1.0"
  - "2026.06.22: Language baseline updated from C++11/14 to C++17. Prohibited C++17 features retained: structured bindings, CTAD, if-init, constexpr new. All other C++17 features allowed."
---

# SnapmakerOrca C++ Coding Standards

**Based on:** SnapmakerOrca 切片部门代码规范文档 v1.0 ([C]), C++ Core Guidelines ([C]), SEI/CERT ([C]).
**Scope:** Project-specific coding standards. Enforce rules beyond dev-guidelines shared harnesses.

---

## Prerequisites

**Language baseline:** C++17 (build sets `CMAKE_CXX_STANDARD 17`). Prohibited C++17 features: structured bindings (`auto [a,b] = …`), CTAD (class template argument deduction without `<T>`), if-init (`if (init; cond)`), and `constexpr new`. All other C++17 features (`std::optional`, `std::variant`, `std::string_view`, `if constexpr`, `[[nodiscard]]`/`[[fallthrough]]`/`[[maybe_unused]]`, inline variables) are allowed.
**Exception policy:** Exceptions (throw/try/catch) disabled. All error handling uses return codes.
**Encoding:** UTF-8 with BOM. No Chinese in source code.

---

## Checklist

### 1. Language Baseline  **(C)** [R1]

- [ ] C++17 baseline; prohibited C++17 features: structured bindings (`auto [a,b]`), CTAD, if-init (`if (init; cond)`), `constexpr new` → **(C)** [R1]
- [ ] No exceptions (throw/try/catch); error handling via bool/int return codes → **(C)** [R1]
- [ ] No Chinese in source code; UTF-8 BOM encoding → **(C)** [R1]

### 2. Format Standards  **(C)** [R1]

- [ ] 4-space indentation; no hard tabs → **(C)** [R1]
- [ ] Line width: 80-120 characters → **(C)** [R1]
- [ ] Allman brace style (each brace on its own line) → **(C)** [R1]
- [ ] Spaces around operators and after commas; no space between function name and `(` → **(C)** [R1]

### 3. Syntax — Required  **(C)** [R1][R2]

- [ ] `std::vector`/`std::string` over raw arrays → **(C)** [R1]
- [ ] `std::unique_ptr` preferred, `std::shared_ptr` only when shared needed → **(C)** [R1]
- [ ] `const` on immutable variables, parameters, member functions → **(C)** [R1]
- [ ] `enum class` for all enums → **(C)** [R1]
- [ ] `nullptr` over `NULL` → **(C)** [R1]
- [ ] Explicit types; avoid `auto` where it obscures intent → **(C)** [R1]

### 4. Syntax — Forbidden  **(P)** [R1][R2]

- [ ] No C-style casts `(Type)value`; use `static_cast<>` → **(P)** [R1]
- [ ] No macros for constants/functions; use `const`/`constexpr`/`inline` → **(C)** [R1]
- [ ] No `goto` → **(P)** [R1]
- [ ] No multiple inheritance / virtual inheritance (except sanctioned) → **(C)** [R1]
- [ ] No C-style varargs (`printf` family) → **(C)** [R1]

### 5. Type Safety  **(C)** [R1]

- [ ] No implicit conversions; all conversions explicit → **(C)** [R1]
- [ ] No implicit int→bool, pointer→bool, narrowing conversions → **(C)** [R1]
- [ ] No `auto` abuse where type is unclear → **(C)** [R1]

```cpp
// Bad
if (ptr) {}       // pointer→bool; use if (ptr != nullptr)
int a = 3.14;     // narrowing; use static_cast<int>(3.14)
if (x = 10) {}    // assignment-as-condition
```

### 6. Memory & Resource Safety  **(C)** [R1][R2]

- [ ] No raw `new`/`delete`; use `std::make_unique`/`std::make_shared` → **(C)** [R1]
- [ ] No `malloc`/`free` in application code → **(P)** [R1]
- [ ] `std::vector` over fixed-length C arrays → **(C)** [R1]
- [ ] All resources (handles, locks, sockets, files) RAII-managed → **(C)** [R1]
- [ ] Pointer null check before dereference → **(C)** [R1]

### 7. Function & Interface  **(C)** [R1]

- [ ] Functions ≤ 150 lines; single responsibility → **(C)** [R1]
- [ ] Parameters ≤ 5; group excess into struct → **(C)** [R1]
- [ ] All incoming parameters validated: null, range, legality → **(C)** [R1]
- [ ] No hidden side effects; no implicit global state modification → **(C)** [R1]
- [ ] Error handling: bool/int error code; never throw → **(C)** [R1]

### 8. Header Files & Dependencies  **(C)** [R1]

- [ ] `#pragma once` at top of every header → **(C)** [R1]
- [ ] No global variables or function definitions in headers (inline excepted) → **(C)** [R1]
- [ ] Minimize header dependencies; prefer forward declarations → **(C)** [R1]
- [ ] Include order: project → third-party → system → **(C)** [R1]

### 9. Concurrency & Thread Safety  **(C)** [R1]

- [ ] All shared mutable data mutex-protected → **(C)** [R1]
- [ ] `std::mutex` + `std::lock_guard` only; no manual lock/unlock → **(C)** [R1]
- [ ] Consistent global lock ordering → **(C)** [R1]
- [ ] No heavy ops (I/O, compute, sleep) inside locked sections → **(C)** [R1]

### 10. Security Development  **(P)** [R1][R2]

- [ ] All external input (network, file, user) validated → **(C)** [R1]
- [ ] No `strcpy`/`sprintf`/`memcpy` without length checks → **(P)** [R1]
- [ ] Prefer `strcpy_s`/`sprintf_s`/`memcpy_s` → **(C)** [R1]
- [ ] No credentials/keys/sensitive data in plaintext or logs → **(P)** [R1]

### 11. Comments & Documentation  **(C)** [R1]

- [ ] Doxygen-style on all functions/classes: purpose, params, return → **(C)** [R1]
- [ ] Complex logic annotated with `//` (no `/* */` nesting) → **(C)** [R1]
- [ ] `TODO`/`FIXME`/`XXX` with explanation → **(C)** [R1]

---

## Decision Tree

```
SnapmakerOrca C++ code?
  → C++17 baseline, no exceptions, no prohibited C++17 features (structured bindings/CTAD/if-init/constexpr new)? [1]
  → 4-space, Allman, 80-120? [2]
  → vector, unique_ptr, const, enum class? [3]
  → No C casts, macros, goto? [4]
  → No implicit conversions? [5]
  → RAII, smart pointers? [6]
  → ≤150 lines, ≤5 params? [7]
  → pragma once, forward decl? [8]
  → lock_guard, lock order? [9]
  → Validated input, safe strings? [10]
  → Doxygen comments? [11]
```

---

## Anti-Patterns

### 1. Exception-Based Error Handling

- **Appearance:** `throw std::runtime_error("...")`.
- **Trap:** Standard C++ practice — taught everywhere.
- **Consequence:** Overhead unacceptable for slicing code. Complicates RAII.
- **Fix:** Return bool/int error codes.

### 2. C-Style Casts

- **Appearance:** `(int)value`, `(Widget*)ptr`.
- **Trap:** Shorter; works in most cases.
- **Consequence:** `(int*)&floatVar` compiles silently.
- **Fix:** `static_cast<T>()`.

### 3. Raw new/delete

- **Appearance:** `Widget* w = new Widget(); ... delete w;`
- **Trap:** Familiar pre-C++11 pattern.
- **Consequence:** Early return leaks. Double-delete on copy.
- **Fix:** `auto w = std::make_unique<Widget>();`.

---

## See Also

- [RAII](../../cpp/memory/raii.md)
- [Smart Pointers](../../cpp/memory/ownership.md)
- [Const Correctness](../../cpp/correctness/const-correctness.md)
- [Type Safety](../../cpp/correctness/type-safety.md)
- [Thread Safety](../../cpp/concurrency/thread-safety.md)
- [Parameter Validation](../../cpp/functions/parameter-validation.md)
- [Input Validation](../../common/security/input-validation.md)

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | SnapmakerOrca 切片部门代码规范文档 | v1.0 (2026-06-04) | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | C, ES, F, SL sections | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft from 切片部门代码规范文档 v1.0
- 2026.06.22: Language baseline updated from C++11/14 to C++17 (build already sets `CMAKE_CXX_STANDARD 17`). Prohibited C++17 features retained: structured bindings, CTAD, if-init, constexpr new. All other C++17 features (std::optional/variant/string_view, if constexpr, [[attributes]], inline variables) are allowed.
