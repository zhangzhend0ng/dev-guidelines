---
type: harness
id: "cpp-compile-time"
title: "Compile-Time Programming Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Guide constexpr, consteval, constinit, static_assert, and if constexpr usage to maximize compile-time safety and minimize runtime overhead in C++"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [compile-time, constexpr, consteval, constinit, static-assert, if-constexpr, templates, cpp]
based_on:
  - "[N] ISO C++ [expr.const]"
  - "[C] C++ Core Guidelines Per.11, T.123"
  - "[A] Effective Modern C++ Item 15 (Meyers)"
  - "[A] A Tour of C++ Ch.6 (Stroustrup)"
related:
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/correctness/type-safety.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Compile-Time Programming Checklist

**Based on:** ISO C++ [expr.const] ([N]), C++ Core Guidelines Per.11, T.123 ([C]), Effective Modern C++ Item 15 ([A]), A Tour of C++ Ch.6 ([A]).
**Scope:** Maximize work done at compile time to catch errors earlier, eliminate runtime overhead, and enforce invariants before the program runs.

---

## Concepts

| Practice | Rationale |
|----------|-----------|
| `constexpr` variable | Guaranteed compile-time evaluation; no runtime init cost |
| `constexpr` function | May be evaluated at compile time or runtime, depending on context |
| `consteval` function | Must be evaluated at compile time; runtime call is an error |
| `constinit` variable | Static initialization at compile time; prevents init-order fiasco |
| `static_assert` | Compile-time assertion; failure stops the build |
| `if constexpr` | Compile-time branch; discarded branch is not instantiated |

---

## Standard Version Capability Matrix

| Feature | C++11 | C++14 | C++17 | C++20 | C++23 |
|---------|-------|-------|-------|-------|-------|
| `constexpr` variables | Yes | Yes | Yes | Yes | Yes |
| `constexpr` functions | Single return | Relaxed (loops, multiple returns) | — | `try`-`catch`, `virtual` | `constexpr` lambda with captures |
| `consteval` | — | — | — | Yes | Yes |
| `constinit` | — | — | — | Yes | Yes |
| `static_assert` | Yes (message optional) | — | — | — | C++26: user-generated messages |
| `if constexpr` | — | — | Yes | Yes | Yes |
| `constexpr` `std::vector` / `std::string` | — | — | — | Yes | Yes (transient allocation) |
| `constexpr` `std::unique_ptr` | — | — | — | — | Yes |

---

## Checklist

### 1. constexpr Variables — Prefer Over `#define` and `const`  **(N)** [R1][R2]

- [ ] Compile-time constants declared `constexpr`, not `#define` → **(N)** [R1]
- [ ] `const` only when the value is not a constant expression (e.g., runtime config) → **(C)** [R2]
- [ ] Global compile-time constants in headers marked `inline constexpr` (C++17) to avoid ODR issues → **(C)** [R2]

### 2. constexpr Functions — Know the Constraints  **(N)** [R1][R2]

- [ ] C++14+: Loops, local variables, and multiple return statements are allowed → **(A)** [R1]
- [ ] C++20+: `try`-`catch` and `virtual` functions may be `constexpr`; non-`virtual` calls resolved at compile time → **(A)** [R1]
- [ ] `constexpr` function evaluated at runtime when any argument is not a constant expression; no diagnostic required → **(C)** [R3]
- [ ] Large `constexpr` functions: profile compile time impact; consider splitting into smaller functions → **(A)** [R4]

### 3. consteval — Guaranteed Compile-Time Only (C++20)  **(N)** [R1]

- [ ] Functions that must never execute at runtime declared `consteval` → **(N)** [R1]
- [ ] Compile-time-only validation (e.g., format string checking, bit-width calculations) uses `consteval` → **(C)** [R2]
- [ ] `consteval` functions called at runtime produce a compile error — use this as a safety net → **(C)** [R1]

### 4. constinit — Static Init Guarantee (C++20)  **(C)** [R1]

- [ ] Static/thread-local variables that must be initialized at compile time (not runtime) declared `constinit` → **(C)** [R1]
- [ ] `constinit` prevents the static initialization order fiasco by guaranteeing constant initialization → **(C)** [R1]
- [ ] `constinit` does NOT imply `const`; the variable may be mutated after initialization → **(C)** [R1]

### 5. static_assert — Compile-Time Assertion  **(N)** [R1][R2]

- [ ] Conditions knowable at compile time use `static_assert`, not runtime `assert` → **(N)** [R1]
- [ ] Type traits checks (`std::is_trivially_copyable`, `std::is_nothrow_move_constructible`) guarded by `static_assert` in templates → **(C)** [R2]
- [ ] Compile-time constraints on template parameters expressed as `static_assert` (or `requires` in C++20) → **(C)** [R2]

### 6. if constexpr — Compile-Time Branching (C++17)  **(N)** [R1]

- [ ] Branches that depend on a compile-time condition use `if constexpr` → **(N)** [R1]
- [ ] The discarded branch is not instantiated — safe to reference types/functions that would not compile for the other branch → **(C)** [R2]
- [ ] `if constexpr` in templates: the condition must be a constant expression dependent on a template parameter, or the discarded branch may still be parsed → **(C)** [R2]
- [ ] Do not use `if constexpr` where a regular `if` suffices — the optimizer will eliminate dead branches when the condition is knowable at compile time anyway → **(A)** [R4]

### 7. constexpr Containers  **(C)** [R1]

- [ ] C++20: `std::vector` and `std::string` usable in `constexpr` contexts; allocation must be deallocated before the end of the constant evaluation → **(C)** [R1]
- [ ] C++23: Transient `constexpr` allocations relax the deallocation-before-return rule → **(A)** [R1]
- [ ] `constexpr` `std::vector`/`std::string` returned from a `constexpr` function (C++20) must be fully consumed at compile time; passing to runtime context is not allowed in C++20 → **(C)** [R1]

### 8. Compile-Time vs Runtime Trade-Offs  **(A)** [R3][R4]

- [ ] Binary size: heavy `constexpr` evaluation can generate large amounts of compile-time-computed data in the binary → **(A)** [R3]
- [ ] Compile time: aggressive `constexpr` on large data structures or complex algorithms increases build time; profile before moving everything to compile time → **(A)** [R4]
- [ ] Debugging: `constexpr`-evaluated code cannot be single-stepped at runtime; ensure the logic is simple or separately tested with runtime invocations → **(A)** [R3]
- [ ] Prefer `constexpr` for: integral constants, lookup tables, string processing, type traits, format validation → **(A)** [R4]
- [ ] Defer to runtime for: large data transformations, I/O-bound work, heap-heavy algorithms with unbounded allocation → **(A)** [R4]

---

## Decision Tree

```
Compile-time programming:
  ├─ Value known at compile time?
  │     ├─ Yes → constexpr variable [1]
  │     └─ No → const variable (runtime config)
  │
  ├─ Function must NOT run at runtime?
  │     ├─ Yes → consteval [3]
  │     └─ No → constexpr if possible [2]
  │
  ├─ Static/thread-local with init-order risk?
  │     └─ Yes → constinit [4]
  │
  ├─ Condition knowable at compile time?
  │     ├─ Type trait / template constraint → static_assert / requires [5]
  │     └─ Template-dependent branch → if constexpr [6]
  │
  ├─ Container needed at compile time?
  │     ├─ C++20: vector/string (must dealloc before return) [7]
  │     └─ C++23: transient allocation relaxed [7]
  │
  └─ Large data / heavy algorithm?
        ├─ Integral constant / lookup table / type trait → constexpr [8]
        └─ Unbounded allocation / I/O → defer to runtime [8]
```

---

## Anti-Patterns

### 1. `#define` for Compile-Time Constants

- **Appearance:** `#define MAX_BUFFER_SIZE 4096`, `#define PI 3.14159`.
- **Trap:** Familiar, zero-overhead, works everywhere.
- **Consequence:** No scoping, no type checking, invisible to debugger, can be silently redefined. Macro expansion errors produce incomprehensible diagnostics.
- **Fix:** `constexpr int max_buffer_size = 4096;` or `constexpr double pi = 3.14159;`. Scoped, typed, debugger-visible.

### 2. Runtime `assert` for Compile-Time-Knowable Conditions

- **Appearance:** `assert(sizeof(T) == 8);` or `assert(std::is_trivially_copyable_v<T>);`.
- **Trap:** Assert is the familiar tool for invariants.
- **Consequence:** Failure is only caught at runtime — possibly in production, or never if the code path is untested. A type that violates the assumption compiles and ships silently.
- **Fix:** `static_assert(sizeof(T) == 8, "T must be 8 bytes");`. Fails at build time, cannot ship.

### 3. `consteval` Used Where `constexpr` Suffices

- **Appearance:** Every compile-time-callable function marked `consteval`.
- **Trap:** Feels safer — "always at compile time".
- **Consequence:** Function is unavailable at runtime. Testing, debugging, and fallback paths that need the same logic at runtime must duplicate code. Prevents gradual adoption — callers must provide compile-time arguments or fail to compile.
- **Fix:** Use `consteval` only when runtime execution would be a correctness or security bug (e.g., compile-time format string validation). Use `constexpr` for functions that benefit from but do not require compile-time evaluation. If you need both guaranteed-compile-time and runtime access, wrap the `consteval` call in a helper that captures the result for runtime use.

### 4. `if constexpr` Overuse

- **Appearance:** Every conditional in a template uses `if constexpr`, even when the condition is not template-dependent or when a regular `if` would work.
- **Trap:** Seems like the "right" tool for template code.
- **Consequence:** Code that is more constrained than it needs to be — a regular `if` with a compile-time condition is optimized away by any modern compiler. `if constexpr` prevents the discarded branch from being parsed, which can hide the fact that the "unused" branch has rotted — it never compiles and nobody notices until a refactor tries to use it.
- **Fix:** Reserve `if constexpr` for truly type-dependent branching where the discarded branch would fail to compile. For value-based conditions, use a regular `if` with a compile-time predicate — the optimizer will eliminate the dead branch.

---

## See Also

- [Undefined Behavior](undefined-behavior.md) — UB from signed overflow, ODR violations, and dangling references that compile-time checks can prevent
- [Type Safety](type-safety.md) — `if constexpr` and `static_assert` for enforcing type constraints at compile time

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [expr.const] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | Per.11, T.123 | verified-2026 | 2026-06 |
| R3 | A | Effective Modern C++ (Meyers) | Item 15 | verified-2026 | 2026-06 |
| R4 | A | A Tour of C++ (Stroustrup) | Ch.6 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft — 8 checklist items covering constexpr variables/functions, consteval, constinit, static_assert, if constexpr, constexpr containers, and compile-time vs runtime trade-offs
