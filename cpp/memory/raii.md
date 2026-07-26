---
type: harness
id: "cpp-raii"
title: "RAII and Resource Management Checklist"
language: "cpp"
category: "resource-management"
tier: "N"
scope: "Ensure every acquired resource is bound to an owning object with correct lifetime semantics in C++ programs"
version: "2026.05"
status: "draft"
stable_since: ""
last_validated: "2026-05-31"
review_cycle: "12m"
tags:
  - raii
  - resources
  - destructors
  - ownership
  - exception-safety
based_on:
  - "[N] ISO C++ [class.dtor], [basic.life]"
  - "[C] C++ Core Guidelines R.1-R.5, P.8, C.30-C.33"
  - "[C] SEI/CERT MEM51-CPP, FIO51-CPP"
  - "[A] Effective C++ Items 13-14 (Meyers)"
related:
  - "cpp/error-handling/result-vs-exception.md"
  - "cpp/concurrency/thread-safety.md"
  - "cpp/correctness/class-hierarchies.md"
  - "cpp/lifetime/dangling-references.md"
  - "cpp/correctness/exception-safety.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/performance/optimization-patterns.md"
  - "cpp/memory/ownership.md"
supersedes: []
changelog:
  - "2026.05: Initial draft"
---

# RAII and Resource Management Checklist

**Based on:** ISO C++ [class.dtor]/[basic.life] ([N]), C++ Core Guidelines R.1-R.5 ([C]), SEI/CERT MEM51-CPP ([C]), Effective C++ Items 13-14 ([A]).
**Scope:** Verify that every acquired resource (memory, file handles, locks, sockets) is bound to an owning object whose destructor guarantees release.

---

## Prerequisites / Concepts

**RAII (Resource Acquisition Is Initialization):** A resource is acquired in a constructor and released in the corresponding destructor. The compiler guarantees destructor invocation on scope exit, including exception paths. RAII is the foundation of exception safety — without it, exception-safe code is nearly impossible.

---

## Checklist

### 1. Resource Ownership at Acquisition

Is every acquired resource immediately bound to an owning RAII object?

- [ ] YES → **(N)** Constructor acquires; destructor releases [R1]
- [ ] NO — raw `acquire()`/`release()` or `goto cleanup` → **(N)** STOP. Wrap in existing RAII type or write a wrapper. [R1][R2]

### 2. Destructor Correctness

- [ ] **(N)** Destructor must not throw (implicitly `noexcept`). If release can fail, log and suppress. [R1]
- [ ] **(C)** Destructor handles self-assignment and double-close safely [R2]

### 3. Copy Semantics Decision

- [ ] Unique ownership → **(C)** Delete copy ctor/assign; move-only type [R2]
- [ ] Shared ownership → **(C)** Reference counting (`std::shared_ptr`) or deep copy; document choice [R3]
- [ ] **(C)** Apply Rule of Five: if you declare any of {destructor, copy, move}, declare all five (or = default) [R4]

### 4. Move Semantics

- [ ] **(C)** Move ctor transfers ownership; source left in valid-but-unspecified state [R2]
- [ ] **(C)** Move assignment releases currently-owned resource before acquiring new one [R2]
- [ ] **(C)** Move operations marked `noexcept` (enables STL optimization) [R1]

### 5. Exception Safety in Constructor

- [ ] **(N)** If constructor throws, destructor is NOT called. Use RAII sub-objects or try-catch so partially-acquired resources are released. [R1]
- [ ] **(N)** If destructor runs during stack unwinding, it must not throw (`std::terminate`) [R1]

### 6. Non-Memory Resources

- [ ] **(C)** File handles → `std::fstream` or `std::unique_ptr<FILE, decltype(&fclose)>` [R2]
- [ ] **(C)** Mutex locks → `std::lock_guard` / `std::scoped_lock` (never manual lock/unlock) [R2]
- [ ] **(C)** OS handles, sockets, GDI objects → custom RAII wrapper with native close in destructor [R5]

### 7. Factory Function Return Types

- [ ] Return raw pointer? → **(C)** Prefer `std::unique_ptr` to make ownership explicit and transferable [R3]
- [ ] Return owning wrapper → OK

---

## Quick Decision Tree

```
Resource acquired?
  ├─ YES → Immediately bound to RAII owner? [Item 1]
  │          ├─ YES → Copyable? [Item 3] → YES: deep-copy/ref-count | NO: move-only
  │          │        Move noexcept? [Item 4]
  │          │        Destructor no-throw? [Item 2]
  │          └─ NO  → WRAP IT
  └─ NO  → Done

All paths: Constructor exception safety [Item 5]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Manual Cleanup

- **Appearance:** `acquire()` / `release()` called in function prologue/epilogue, or `goto cleanup`.
- **Trap:** Seems fine for "simple" functions.
- **Consequence:** Early return, exception, or goto misses `release()`. Resource leak.
- **Fix:** Bind to RAII owner at acquisition point. Destructor handles all exit paths.

### Anti-Pattern 2: Throwing Destructor

- **Appearance:** Destructor calls `close()` which fails, propagates via exception.
- **Trap:** "Proper error handling" — exceptions are the mechanism.
- **Consequence:** If already unwinding, `std::terminate()`. Process dies.
- **Fix:** Catch exceptions in destructor body. Log failures. Do not propagate.

---

## See Also

- [Smart Pointer and Ownership](ownership.md) — Choosing the right ownership model
- [Exception Safety](../correctness/exception-safety.md) — Exception guarantee levels

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [class.dtor], [basic.life], [except.spec] | verified-2026 | 2026-05 |
| R2 | C | C++ Core Guidelines | R.1-R.5, P.8, C.30-C.33 | verified-2026 | 2026-05 |
| R3 | C | SEI/CERT C++ | MEM51-CPP, FIO51-CPP | verified-2026 | 2026-05 |
| R4 | C | C++ Core Guidelines | C.20-C.22, C.80-C.83 | verified-2026 | 2026-05 |
| R5 | A | Effective C++ (Meyers) | Items 13-14 | verified-2026 | 2026-05 |

---

## Changelog

- 2026.05: Initial draft
