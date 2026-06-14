---
type: harness
id: "cpp-undefined-behavior"
title: "Undefined Behavior Prevention Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Identify and eliminate common sources of undefined behavior in C++ code"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [undefined-behavior, ub, safety, correctness]
based_on:
  - "[N] ISO C++ [intro.races], [basic.life], [dcl.type], [expr], [res.on.arguments]"
  - "[C] C++ Core Guidelines ES.100-ES.107, ES.40-ES.49, Type.1-Type.3"
  - "[C] SEI/CERT INT32-C, EXP34-C, ARR30-C"
  - "[A] Deep C++ series (John Regehr), UB Sanitizer documentation"
related:
  - "common/ai/ai-assisted-cpp-development.md"
  - "cpp/security/secure-coding.md"
  - "cpp/testing/static-analysis.md"
  - "cpp/concurrency/thread-safety.md"
  - "cpp/correctness/class-hierarchies.md"
  - "cpp/correctness/const-correctness.md"
  - "cpp/correctness/stl-algorithms-containers.md"
  - "cpp/correctness/type-safety.md"
  - "cpp/memory/raii.md"
  - "cpp/memory/ownership.md"
  - "cpp/testing/sanitizers.md"
  - "cpp/correctness/compile-time-programming.md"
  - "cpp/correctness/integer-safety.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Undefined Behavior Prevention Checklist

**Based on:** ISO C++ Standard [intro.races]/[basic.life]/[dcl.type]/[expr]/[res.on.arguments] ([N]), C++ Core Guidelines ES.100-ES.107, ES.40-ES.49, Type.1-Type.3 ([C]), SEI/CERT INT32-C, EXP34-C, ARR30-C ([C]), "Deep C++" series by John Regehr and UB Sanitizer documentation ([A]).

**Scope:** Identify and eliminate the most common and dangerous sources of undefined behavior in C++ code. Undefined behavior means the language standard imposes no requirements -- the program may appear to work, crash, produce wrong results, or silently corrupt data. UB is the root cause of the most intractable bugs and security vulnerabilities in C++.

---

## Prerequisites / Concepts

### What Is Undefined Behavior?

Undefined behavior (UB) is program behavior for which the C++ standard imposes no requirements. The compiler is permitted to assume UB never happens and may optimize accordingly -- meaning UB can cause time-travel effects where "impossible" code paths are eliminated, or a write past the end of an array corrupts a variable that the compiler already proved was initialized to a different value.

### UB Categories

| Category | Examples | Typical Consequence |
|----------|----------|-------------------|
| **Language UB** | Signed overflow, ODR violations, strict aliasing | Compiler may delete code, reorder "impossible" branches |
| **Library UB** | Passing invalid range to `std::sort`, using moved-from `std::unique_ptr` | Runtime crash, heap corruption, double-free |
| **Data-race UB** | Unsynchronized concurrent read/write | Tearing, lost updates, compiler-introduced speculative writes |
| **Lifetime UB** | Use-after-free, dangling reference, modifying const object | Use of freed memory, silent corruption |

### Tooling

| Tool | What It Detects |
|------|----------------|
| `-fsanitize=undefined` (UBSan) | Signed overflow, null deref, out-of-bounds, misaligned access, invalid vptr, float-cast-overflow |
| `-fsanitize=address` (ASan) | Use-after-free, heap/stack buffer overflow, memory leaks |
| `-fsanitize=thread` (TSan) | Data races |
| `-fsanitize=memory` (MSan) | Uninitialized reads |
| Static analysis (clang-tidy, Coverity) | ODR violations, use-after-move, dangling refs |

**Rule: All CI builds must enable at least UBSan + ASan for test binaries. Release builds should enable UBSan with `-fsanitize=undefined -fno-sanitize-recover` (trap-on-failure) unless profiling shows unacceptable overhead.**

---

## Checklist

### 1. Signed Integer Overflow

Signed integer overflow is UB. The compiler may assume `x + 1 > x` always holds for signed types and eliminate overflow checks accordingly.

- [ ] Arithmetic on signed integers whose operands could overflow? → **(N)** Replace with unsigned for wrapping semantics, or use compiler builtins (`__builtin_add_overflow`) to check. [R1][R2]
- [ ] Security-sensitive range check like `if (size + delta < size)`? → **(N)** UB if `size + delta` overflows before the check; use unsigned or `__builtin_add_overflow`. [R1]
- [ ] Narrowing cast from wider signed type? → **(C)** `gsl::narrow<T>()` or explicit range check before cast. [R2]
- [ ] Float-to-int conversion whose value exceeds the integer range? → **(N)** UB. Always range-check before conversion. [R1]
- [ ] Division by zero or `INT_MIN / -1`? → **(N)** Both are UB. Guard with an explicit check. [R1]

### 2. Null Pointer Dereference

Dereferencing a null pointer is UB. In practice, modern compilers exploit this to eliminate null checks that appear "after" a dereference.

- [ ] Raw pointer parameter that the function dereferences? → **(N)** Verify non-null before dereference. At public API boundaries, check explicitly; at internal boundaries, `assert(p != nullptr)`. [R1][R2]
- [ ] `this` pointer in member function called on `nullptr`? → **(N)** UB. Never call member functions (even non-virtual) on null pointers -- compilers may elide the call body entirely. [R1]
- [ ] Pointer returned from a function that may fail? → **(C)** Document nullable contract; caller checks before use. Prefer `std::optional<T&>` or `not_null<T*>` where the type system can help. [R3]
- [ ] Pointer arithmetic before dereference? → **(C)** Verify the resulting pointer is within bounds. `p + n` on null is UB even without dereference. [R1]

### 3. Out-of-Bounds Array/Container Access

Accessing an array or standard container outside its valid index range is UB (for `operator[]` on `std::vector` and arrays) or throws (`.at()`).

- [ ] Raw array indexing with computed index? → **(N)** Validate index `< size` before access. No bounds checking exists. [R1][R2]
- [ ] `std::vector<T>::operator[]` used? → **(C)** Prefer `.at()` for defensive code; `operator[]` only when the index is provably in bounds. [R2]
- [ ] Iterator arithmetic (`it + n`) that could exceed `end()`? → **(C)** Validate distance to end before advancing. Past-the-end iterator dereference is UB. [R1]
- [ ] `std::span<T>` with unchecked index? → **(C)** `.size()` check before indexing. Spans carry size but offer no bounds checking. [R2]
- [ ] Pointer from `data()` plus offset without bounds check? → **(N)** Validate offset `< size`. Same risk as raw array. [R1]

### 4. Use-After-Move / Use-After-Free

Accessing an object after its lifetime has ended is UB. This includes dereferencing a dangling pointer, calling methods on a moved-from object in an unspecified state, or accessing freed memory.

- [ ] Pointer/reference stored that outlives the referenced object? → **(N)** Document lifetime dependency. Use `std::unique_ptr` or `std::shared_ptr` to encode ownership in the type system. [R1][R2]
- [ ] Reference returned from function? → **(C)** Verify the referenced object lives at least as long as the caller's use. Never return a reference/pointer to a local. [R2]
- [ ] Moved-from `std::unique_ptr` or `std::shared_ptr` dereferenced? → **(C)** Moved-from unique_ptr is null; moved-from shared_ptr is empty. Check before use or re-assign. [R2]
- [ ] `std::move()` used on an object that is still needed? → **(C)** `std::move` is a cast, not an action. The object is still alive but may be in a valid-but-unspecified state. Do not reuse without re-assignment. [R4]
- [ ] Container element reference/iterator still used after mutation (`push_back`, `erase`)? → **(N)** Revalidation/invalidation rules apply. Never use iterators after container modification that invalidates them. [R1]

### 5. Data Races

Two or more threads accessing the same memory location, at least one is a write, without synchronization = data race = UB. The compiler is permitted to introduce speculative writes and reorder memory accesses around unsynchronized code.

- [ ] Shared mutable state accessed from multiple threads? → **(N)** Every access must be protected by a mutex, atomic, or other synchronization primitive. [R1]
- [ ] `const` member function called concurrently from multiple threads? → **(C)** const member functions must be safe for concurrent reads; if they mutate `mutable` state, that state must be synchronized. [R2]
- [ ] Lock-free code using `std::atomic`? → **(N)** Use the correct memory order. `memory_order_relaxed` is insufficient for anything beyond a simple counter without dependencies. [R1]
- [ ] Double-checked locking pattern? → **(C)** Use `std::atomic` with `memory_order_acquire`/`release` or `std::call_once`. Naive flag + mutex is UB. [R1][R4]
- [ ] Signal handler accessing global variables? → **(N)** Only `std::atomic<>` with `is_lock_free() == true` is safe. All other shared state access is UB. [R1]

### 6. Strict Aliasing Violations

Accessing an object through a pointer/reference of an incompatible type violates the strict aliasing rule and is UB (with narrow exceptions for `char*`, `unsigned char*`, and `std::byte*`).

- [ ] `reinterpret_cast<T*>(ptr)` where `T` is not the actual dynamic type? → **(N)** UB unless `T` is `char`, `unsigned char`, `std::byte`, or the actual type. [R1]
- [ ] Union member read from a different member than the last one written (type punning)? → **(N)** UB in C++ (unlike C). Use `std::bit_cast` (C++20) or `memcpy`. [R1]
- [ ] Cast between structs with different layout to access common initial sequence? → **(N)** Only valid if both are standard-layout and share a common initial member sequence, and only through the union type itself. Otherwise UB. [R1]
- [ ] `reinterpret_cast` used at all? → **(A)** Audit every occurrence. Legitimate uses are rare: serialization to byte buffers, low-level memory-mapped I/O. Document justification. [R4]

### 7. Modifying Const Objects

Modifying an object that was originally declared `const` is UB. This includes casting away constness and writing through the resulting pointer/reference, even if the memory appears writable.

- [ ] `const_cast` present in code? → **(N)** Nearly always wrong. Legitimate exceptions: calling legacy C APIs known not to modify; adapting to a C API that lacks const but does not write. Document every occurrence. [R1][R2]
- [ ] Const object stored in read-only memory (e.g., string literal, global const)? → **(N)** Any write attempt is a crash or silent corruption. `const_cast` on these is UB regardless of actual memory protection. [R1]
- [ ] `mutable` member used to modify logically-const state? → **(C)** Acceptable only for caching, mutexes, or lazy initialization where the observable state is unchanged. Never to bypass const-correctness for business logic. [R2]

### 8. Throwing Destructor During Stack Unwinding

If a destructor throws while the stack is already being unwound due to another exception, `std::terminate()` is called. This is an unrecoverable program termination.

- [ ] Destructor calls functions that could throw? → **(N)** Every destructor is implicitly `noexcept`. Wrap potentially-throwing calls in try-catch; log and suppress. Never let an exception escape a destructor. [R1][R2]
- [ ] Destructor releases a resource (e.g., flushes a buffer) that can fail? → **(C)** Separate close/flush into an explicit method. Destructor performs best-effort release only; swallows errors. [R2]
- [ ] `noexcept(false)` destructor explicitly declared? → **(C)** Strongly suspect. Requires exceptional justification and documentation. [R2]

### 9. ODR (One Definition Rule) Violations

The ODR requires that any symbol with external linkage (global variables, non-inline functions, class definitions) have exactly one definition across all translation units, and that all definitions be token-for-token identical. Violations are silently accepted by the linker with unpredictable results.

- [ ] Same function name defined in multiple `.cpp` files (not `static`, not in anonymous namespace)? → **(N)** ODR violation. Use `static`, anonymous namespace, or `inline`. [R1]
- [ ] Class definition with different member layouts in different translation units (e.g., `#ifdef`-gated members)? → **(N)** ODR violation. Same class must compile to the same layout everywhere. [R1]
- [ ] Template specialization that differs from the primary template in another TU? → **(N)** Explicit specializations must be declared before first use in every TU. [R1][R2]
- [ ] Header defines a non-`inline` function or variable (not a template)? → **(C)** Mark as `inline` or move definition to exactly one `.cpp` file. [R2]

### 10. Returning Reference/Pointer to Local

Returning a reference or pointer to a local (stack-allocated) variable produces a dangling reference -- the object is destroyed when the function returns.

- [ ] Function return type is `T&` or `const T&`? → **(N)** Verify the referenced object's lifetime extends beyond the return. Common traps: returning ref to local, ref to temporary, ref to `vector` element after `push_back`. [R1][R2]
- [ ] Function return type is `T*`? → **(N)** Same lifetime requirement as references. `nullptr` is acceptable for "not found" semantics. [R1]
- [ ] Returning `std::string_view` or `std::span`? → **(C)** Both are non-owning reference types. The underlying storage must outlive the view. Returning a `string_view` to a local `std::string` is UB. [R2]

---

## Decision Tree

```
Code review: potential UB?
  ├─ Arithmetic?
  │     ├─ Signed integer overflow possible? → [Item 1] unsigned / __builtin_add_overflow
  │     ├─ Division with variable divisor? → [Item 1] guard zero + INT_MIN/-1
  │     └─ Float-to-int conversion? → [Item 1] range-check before cast
  │
  ├─ Pointer/reference?
  │     ├─ Could be null? → [Item 2] check before dereference
  │     ├─ Returned from function? → [Item 10] verify lifetime extends past return
  │     ├─ reinterpret_cast involved? → [Item 6] strict aliasing audit
  │     └─ const_cast involved? → [Item 7] audit; likely wrong
  │
  ├─ Array/container access?
  │     └─ Index computed at runtime? → [Item 3] bounds check / .at()
  │
  ├─ Lifetime after free/move?
  │     ├─ Moved-from object reused? → [Item 4] re-assign before use
  │     └─ Iterator after container mutation? → [Item 4] assume invalidation
  │
  ├─ Concurrency?
  │     └─ Shared mutable state? → [Item 5] mutex / atomic / synchronization
  │
  ├─ Destructor?
  │     └─ Could throw? → [Item 8] wrap, log, suppress -- never propagate
  │
  ├─ Multiple translation units?
  │     └─ Same symbol defined differently? → [Item 9] static / anonymous / inline / one .cpp
  │
  └─ Tooling gate:
        └─ UBSan+ASan clean? → proceed; else → fix sanitizer reports FIRST
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: "It Works on My Machine"

- **Appearance:** Code with signed overflow, uninitialized reads, or data races that pass manual testing and CI. Developer dismisses sanitizer warnings as false positives.
- **Trap:** UB can produce "correct" output in one compiler version, optimization level, or platform, then silently produce wrong results after any toolchain change.
- **Consequence:** Heisenbugs that vanish under debugger. Security vulnerabilities from compiler optimizations exploiting UB to eliminate safety checks. Code that breaks on a different CPU architecture (e.g., x86 to ARM for signed overflow wrapping).
- **Fix:** Treat every UBSan/ASan/TSan report as a real bug until proven otherwise. Understand the specific UB before suppressing. Run sanitizers on every CI build for test targets.

### Anti-Pattern 2: Defensive Null Check After Dereference

- **Appearance:** `*ptr; if (!ptr) return;` or `ptr->method(); if (!ptr) { /* handle */ }` -- null check placed after the pointer has already been used.
- **Trap:** The compiler sees the dereference and concludes `ptr` is non-null. The subsequent null check is eliminated as dead code because the compiler is permitted to assume UB (null dereference) never occurs.
- **Consequence:** The null-check code is silently removed. The program crashes or continues with corrupt state exactly when the defensive check was meant to save it.
- **Fix:** Place null checks before any dereference. Use `-fno-delete-null-pointer-checks` only as a temporary mitigation, not a permanent fix. Consider `gsl::not_null<T*>` for non-nullable pointers.

### Anti-Pattern 3: Signed Size/Length Variables From API

- **Appearance:** A loop counter or buffer size stored as `int` because a third-party API returns `int`. Arithmetic operations like `int remaining = total - consumed` can overflow silently.
- **Trap:** Legacy C APIs (POSIX, Win32) often use `int` for sizes. Copying these types into arithmetic-intensive code without awareness of signed overflow UB.
- **Consequence:** Overflow wraps on some platforms (x86) but not others, leads to buffer overruns when a large size "wraps" to negative, and triggers UB that sanitizers will flag but developers may dismiss as "impossible" values.
- **Fix:** Convert API-returned sizes to `size_t` or `uint32_t` at the API boundary with explicit validation. Use unsigned types for sizes, offsets, and counts. If wraparound is intentional, use unsigned types (wrapping is well-defined for unsigned). If overflow would be a bug, check with `__builtin_add_overflow`.

---

## See Also

- [Const Correctness](const-correctness.md) -- Const-correctness prevents accidental writes to read-only objects ([Item 7])
- [RAII and Resource Management](../memory/raii.md) -- RAII is the primary defense against use-after-free and leaking-throwing-destructor UB ([Items 4, 8])
- [Smart Pointer and Ownership](../memory/ownership.md) -- Correct ownership modeling eliminates most lifetime UB ([Items 2, 4, 10])

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [intro.races], [basic.life], [dcl.type], [expr], [res.on.arguments], [basic.def.odr], [class.dtor], [dcl.type.cv] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | ES.100-ES.107, ES.40-ES.49, Type.1-Type.3, Con.1-Con.5 | verified-2026 | 2026-06 |
| R3 | C | SEI/CERT C Coding Standard | INT32-C, EXP34-C, ARR30-C, STR32-C | verified-2026 | 2026-06 |
| R4 | A | Deep C++ series (John Regehr); UB Sanitizer docs | Blog series, compiler-rt docs | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft -- 10 checklist items covering signed overflow, null deref, OOB access, lifetime, data races, strict aliasing, const modification, throwing destructors, ODR, and dangling references
