---
type: harness
id: "cpp-ownership"
title: "Smart Pointer and Ownership Semantics Checklist"
language: "cpp"
category: "resource-management"
tier: "N"
scope: "Choose correct ownership model and smart pointer type for dynamically allocated objects in C++"
version: "2026.05"
status: "draft"
stable_since: ""
last_validated: "2026-05-31"
review_cycle: "12m"
tags:
  - ownership
  - smart-pointers
  - unique_ptr
  - shared_ptr
  - memory
based_on:
  - "[N] ISO C++ [util.smartptr]"
  - "[C] C++ Core Guidelines R.20-R.37, F.7, F.26"
  - "[C] SEI/CERT MEM50-CPP"
  - "[A] Effective Modern C++ Items 18-22 (Meyers)"
related:
  - "common/ai/ai-assisted-cpp-development.md"
  - "cpp/concurrency/thread-safety.md"
  - "cpp/lifetime/dangling-references.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/memory/raii.md"
supersedes: []
changelog:
  - "2026.05: Initial draft"
---

# Smart Pointer and Ownership Semantics Checklist

**Based on:** ISO C++ [util.smartptr] ([N]), C++ Core Guidelines R.20-R.37 ([C]), SEI/CERT MEM50-CPP ([C]), Effective Modern C++ Items 18-22 ([A]).
**Scope:** Ensure correct choice of ownership model and smart pointer type. Raw pointers = non-owning observation only.

---

## Prerequisites / Concepts

| Pointer Type | Ownership | Use When |
|-------------|-----------|----------|
| `std::unique_ptr<T>` | Exclusive | One owner; move-only; default choice |
| `std::shared_ptr<T>` | Shared (ref-counted) | Multiple owners genuinely needed |
| `std::weak_ptr<T>` | Non-owning observer | Break cycles; cache-like patterns |
| `T*` (raw) | None | Non-owning observation; nullable |
| `T&` (reference) | None | Non-owning; non-null by convention |

---

## Checklist

### 1. Default Choice

- [ ] **(C)** Prefer `std::unique_ptr<T>` as the default owning pointer. Use `std::make_unique<T>()`. [R2][R4]

### 2. Shared Ownership Justification

- [ ] `shared_ptr` used? → **(C)** Document why shared ownership is genuinely needed. It's the most expensive model. [R2]
- [ ] **(C)** Use `std::make_shared<T>()` for single-allocation efficiency. [R4]

### 3. Raw Pointer Usage

- [ ] **(C)** Raw pointer = non-owning observation ONLY. Never `delete` a raw pointer. [R2]
- [ ] **(C)** If nullable observation → `T*`. If non-null → prefer `T&`. [R2]
- [ ] **(C)** Factory functions → return `std::unique_ptr<T>`, never raw owning pointer. [R3]

### 4. Shared Pointer Parameter Passing

- [ ] Function stores a copy → **(C)** Pass `shared_ptr` by value (increases ref count). [R2]
- [ ] Function uses but does not store → **(C)** Pass by const-ref to avoid atomic ref-count churn. [R2]
- [ ] **(A)** Never pass `shared_ptr` just to read the pointee — pass `const T&` instead. [R4]

### 5. Cycle Prevention

- [ ] **(C)** Parent→child via `unique_ptr`; child→parent via raw pointer or reference. [R2]
- [ ] **(C)** Peer-to-peer or graph → use `weak_ptr` to break cycles. [R2]
- [ ] **(C)** Ref count never reaches zero? → memory leak. Check for cycles. [R3]

### 6. `this` as Shared Pointer

- [ ] **(C)** Need `shared_ptr` to `this`? → inherit `std::enable_shared_from_this<T>`. Use `shared_from_this()`. [R2]
- [ ] **(N)** NEVER `shared_ptr<T>(this)` — second control block, double-delete, UB. [R1][R2]

### 7. Thread Safety

- [ ] **(C)** `shared_ptr` control block is thread-safe; pointee access is NOT. Protect with mutex. [R1]
- [ ] **(C)** `unique_ptr` has no thread safety — only one thread should own it. [R1]

---

## Quick Decision Tree

```
Dynamically allocated object?
  ├─ Exclusive owner → unique_ptr [Item 1]
  ├─ Shared (justified) → shared_ptr [Item 2]
  │     ├─ Cycle possible? → weak_ptr [Item 5]
  │     └─ shared_ptr to this? → enable_shared_from_this [Item 6]
  └─ Non-owning → T* or T& [Item 3]

Passing shared_ptr to function?
  ├─ Stores copy → by value
  └─ Uses only → const-ref (or skip shared_ptr entirely) [Item 4]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: `shared_ptr` by Default

- **Appearance:** All owning pointers are `shared_ptr` "just in case."
- **Trap:** GC-language habits; seems safer than thinking about ownership.
- **Consequence:** Atomic ref-count overhead everywhere; cycles cause leaks; unclear ownership.
- **Fix:** Default to `unique_ptr`. Upgrade to `shared_ptr` only with documented justification.

### Anti-Pattern 2: `shared_ptr` from `this`

- **Appearance:** `std::shared_ptr<T>(this)` in a member function.
- **Trap:** `this` is a valid pointer — seems like it should work.
- **Consequence:** Second control block. Double-delete. Undefined behavior.
- **Fix:** Inherit `std::enable_shared_from_this<T>`. Use `shared_from_this()`.

---

## See Also

- [RAII and Resource Management](raii.md) — Foundation: all smart pointers rely on RAII

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [util.smartptr] | verified-2026 | 2026-05 |
| R2 | C | C++ Core Guidelines | R.20-R.37, F.7, F.26 | verified-2026 | 2026-05 |
| R3 | C | SEI/CERT C++ | MEM50-CPP | verified-2026 | 2026-05 |
| R4 | A | Effective Modern C++ (Meyers) | Items 18-22 | verified-2026 | 2026-05 |

---

## Changelog

- 2026.05: Initial draft
