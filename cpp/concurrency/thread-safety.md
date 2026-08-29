---
type: harness
id: "cpp-thread-safety"
title: "Concurrency and Thread Safety Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Ensure correct synchronization and freedom from data races in concurrent C++ code"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [concurrency, threading, atomics, mutex, data-race, tsan, condition-variable, deadlock, thread-local, synchronization]
based_on:
  - "[N] ISO C++ [thread], [atomics], [intro.races]"
  - "[C] C++ Core Guidelines CP.1-CP.50, CP.100-CP.112, CP.200-CP.202"
  - "[C] SEI/CERT CON40-CPP through CON56-CPP"
  - "[A] C++ Concurrency in Action 2/e (Williams)"
  - "[A] Effective Modern C++ Items 35-40 (Meyers)"
related:
  - "cpp/security/secure-coding.md"
  - "cpp/memory/ownership.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/memory/raii.md"
  - "cpp/debugging/flaky-test-triage.md"
  - "cpp/testing/sanitizers.md"
  - "cpp/third-party/wxwidgets-3-1-5.md"
  - "cpp/debugging/sanitizer-triage.md"
  - "cpp/third-party/qt6-core.md"
  - "cpp/third-party/qt6-qml.md"
  - "projects/snapmaker-orca/coding-standards.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Concurrency and Thread Safety Checklist

**Based on:** ISO C++ [thread]/[atomics]/[intro.races] ([N]), C++ Core Guidelines CP.1-CP.50, CP.100-CP.112, CP.200-CP.202 ([C]), SEI/CERT CON40-CPP through CON56-CPP ([C]), C++ Concurrency in Action 2/e (Williams) ([A]), Effective Modern C++ Items 35-40 (Meyers) ([A]).
**Scope:** Verify that every concurrent C++ program correctly synchronizes access to shared mutable state, avoids data races, and is free of deadlocks and livelocks.

---

## Prerequisites / Concepts

### The C++ Memory Model

| Concept | Definition |
|----------|-----------|
| **Data race** | Two or more threads access the same memory location concurrently, at least one is a write, and at least one is not an atomic operation. Data races are **undefined behavior** -- the optimizer may produce impossible results. |
| **Happens-before** | The fundamental ordering relationship. If A happens-before B, then A's side effects are visible to B. Established by: program order (same thread), synchronizes-with (mutex unlock to lock, atomic release to acquire), and dependency-ordered-before (memory_order_consume). |
| **Sequenced-before** | Within a single thread, evaluation A is sequenced-before B if A occurs earlier in program order. |
| **Synchronizes-with** | Inter-thread ordering: a release operation on atomic M synchronizes-with an acquire operation on M that reads the value written. A mutex unlock synchronizes-with the next lock. |

### Synchronization Primitives at a Glance

| Primitive | Purpose | Key Property |
|-----------|---------|--------------|
| `std::mutex` | Exclusive access to shared state | unlock() synchronizes-with lock() |
| `std::shared_mutex` | Reader-writer lock | Multiple readers OR one writer |
| `std::atomic<T>` | Lock-free atomic operations | Every operation is indivisible; configurable memory ordering |
| `std::condition_variable` | Wait for a state change | Always paired with a mutex; predicate protects against spurious wakeups |
| `std::lock_guard` / `std::scoped_lock` | RAII mutex ownership | Never manual lock/unlock |
| `std::once_flag` / `std::call_once` | One-time initialization | Thread-safe lazy init without double-checked locking |
| `thread_local` | Per-thread state | No synchronization needed for thread-private data |

---

## Checklist

### 1. Data Race Freedom

Every shared mutable state accessed from multiple threads must be protected.

- [ ] Compile with `-fsanitize=thread` (Clang/GCC) or `/fsanitize=thread` (MSVC) and run tests ([Item 6]). If TSan reports a race: **(N)** treat as a bug -- a data race is undefined behavior, not a "benign" anomaly. [R1][R2]
- [ ] **(N)** Either (a) protect shared mutable state with a mutex, or (b) use `std::atomic<T>`, or (c) restructure to avoid sharing. No other options exist. [R1][R2]
- [ ] **(C)** Immutable state (`const` objects, data initialized before thread creation) can be shared without synchronization. [R1]
- [ ] **(A)** If a synchronization-free design is claimed (e.g., "it's fine, only one thread writes"), challenge it: the C++ memory model does not recognize intent, only happens-before. Without a synchronizes-with edge, the compiler may reorder or elide the write entirely. [R2]

### 2. Mutex: RAII Locking Only

Never call `mutex::lock()` / `mutex::unlock()` manually.

- [ ] **(N)** Use `std::lock_guard<std::mutex>` for simple scope-based locking. [R1][R2]
- [ ] **(C)** Use `std::scoped_lock` (C++17) when locking one or more mutexes -- it is a strict superset of `lock_guard` with deadlock-avoidance for multiple locks. [R1][R2]
- [ ] **(N)** Manual `lock()` / `unlock()` is a bug magnet: early return, exception, or `continue` skips `unlock()`. Every such occurrence must be replaced with an RAII guard. [R1][R2]
- [ ] **(C)** `std::unique_lock` is acceptable when deferred locking or early unlock is genuinely needed (e.g., paired with `std::condition_variable`, or `std::try_to_lock`). [R2]

### 3. Deadlock Prevention

Every code path that acquires multiple locks must be verified deadlock-free.

- [ ] **(N)** Acquire multiple locks in a consistent global order. Document the order as a project-wide convention. [R1][R2]
- [ ] **(C)** Use `std::lock(l1, l2, ...)` (or `std::scoped_lock` with multiple mutexes) to atomically acquire all locks without deadlock risk. [R1][R2]
- [ ] **(C)** If consistent ordering is infeasible (e.g., hierarchical lock graph with cycles), use `std::try_lock` with back-off and retry. Document the fallback strategy. [R2]
- [ ] **(C)** Never call user code (callbacks, virtual functions, lambdas, `std::function`) while holding a lock -- the callee may acquire another lock and invert the ordering. [R2]
- [ ] **(A)** Hold locks for the minimum duration necessary. Extract non-critical computation outside the critical section. [R3]

### 4. Atomics: Correct Memory Ordering

Use `std::atomic<T>` with explicit, documented memory ordering.

- [ ] **(C)** Default to `std::memory_order_seq_cst` (sequential consistency) -- it is the safest and most intuitive ordering. Relax only with benchmarks proving the performance gain. [R1][R2]
- [ ] **(C)** Acquire-release ordering (`memory_order_acquire` / `memory_order_release`) is sufficient for mutex-like patterns (publish/consume, flags, simple state machines). Document the pairing. [R1][R2]
- [ ] **(N)** `memory_order_relaxed` is for counters and statistics only. It provides atomicity without ordering -- no happens-before relationship is established. Using it for synchronization is a latent data race. [R1][R2]
- [ ] **(C)** `std::memory_order_consume` is essentially unusable in practice (compilers treat it as acquire). Prefer `memory_order_acquire`. [R1]
- [ ] **(A)** For lock-free data structures: validate with TSan, model with CDSChecker or Relacy Race Detector, and have a second reviewer sign off. Lock-free code is the hardest concurrency code to get right. [R4]

### 5. Volatile is Not Atomic

`volatile` has exactly zero concurrency semantics in standard C++.

- [ ] **(N)** `volatile` does **not** provide: atomicity, mutual exclusion, memory ordering, or happens-before. Its only standard purpose is signal handlers, memory-mapped I/O, and setjmp/longjmp. [R1]
- [ ] **(N)** Every occurrence of `volatile` in a multi-threading context must be replaced with `std::atomic<T>`. [R1][R2]
- [ ] **(C)** In pre-C++11 codebases ported forward: audit all uses of `volatile` against the threading model. Legacy code often used `volatile` as a fake mutex. [R1]

### 6. Thread Sanitizer in CI

TSan must be a mandatory CI gate for any project using threads.

- [ ] **(C)** Add a CI build configuration with `-fsanitize=thread` (Clang/GCC) or `/fsanitize=thread` (MSVC). Run the full test suite under TSan. [R2][R4]
- [ ] **(C)** TSan runtime overhead is 5x-15x; test timeouts may need adjustment. Do **not** disable TSan due to slowness -- extend timeouts or use a smaller-but-representative test corpus. [R4]
- [ ] **(C)** Suppress false positives with `TSAN_OPTIONS="suppressions=tsan.supp"`, not by removing TSan from CI. File a comment referencing the suppression rationale. [R4]
- [ ] **(A)** For CI acceleration, run TSan on a scheduled (nightly) pipeline if per-commit is too slow -- but never omit it entirely. [R3]

### 7. Detached Thread Lifetime Safety

A detached thread (`std::thread::detach()`) must not access any stack-allocated variable of its creating scope.

- [ ] **(N)** `detach()` is a code smell. Prefer `std::jthread` (C++20) which automatically joins on destruction, or explicitly `join()` in a destructor. [R1][R2]
- [ ] **(N)** If `detach()` is unavoidable: capture by **value only** in the thread lambda. Never capture by reference or capture `[&]` -- the stack frame may be destroyed before the thread runs. [R1][R2]
- [ ] **(C)** Use `std::shared_ptr` to extend the lifetime of shared data that outlives the creating scope -- the detached thread holds a copy of the `shared_ptr`. [R2]

### 8. Condition Variables: Predicate Loop

Always test the condition in a `while` loop, never an `if`.

- [ ] **(N)** Every `cv.wait(lock)` must be wrapped as `while (!predicate()) { cv.wait(lock); }`, or use the predicate overload: `cv.wait(lock, predicate)`. [R1][R2]
- [ ] **(C)** Spurious wakeups are real and permitted by the standard. The `while` loop is the only defense. An `if` that skips re-checking the predicate after wakeup will proceed under a false condition. [R1]
- [ ] **(C)** Lost wakeup prevention: modify the shared state under the mutex before calling `cv.notify_one()` / `cv.notify_all()`. Otherwise, the waiting thread may check the predicate, see no change, and sleep through the notification. [R2]
- [ ] **(C)** Prefer `cv.notify_all()` unless there is a proven invariant that exactly one waiter can proceed. `notify_one()` may wake the wrong thread, starving others. [R2]

### 9. No Mutex Locking in Signal Handlers

A signal handler runs in a constrained context and must be async-signal-safe.

- [ ] **(N)** A signal handler must not call `lock()`, `unlock()`, or any function that may acquire a mutex. The signal may have interrupted the same thread while it held that mutex, producing a self-deadlock. [R1][R2]
- [ ] **(C)** The only safe synchronization in a signal handler: `std::atomic<T>` with `std::memory_order_relaxed` for flag-setting, or `volatile sig_atomic_t` (the one legitimate use of volatile for signaling). [R1]
- [ ] **(C)** For anything beyond flag-setting, use `sigaction` with `SA_SIGINFO` and a dedicated signal-processing thread via `signalfd` (Linux) or self-pipe trick. [R2]
- [ ] **(C)** Design the signal handler to set an atomic flag, then return. The main thread polls (or is notified via `signalfd`) and handles the event outside signal context. [R2]

### 10. Thread-Local Storage vs. Global State

`thread_local` eliminates races but introduces its own trade-offs.

- [ ] **(C)** Use `thread_local` when each thread genuinely needs its own copy of the data and there is no sharing requirement. Examples: thread-local random-number generators, per-thread caches, stack-depth counters. [R2][R5:Item 37]
- [ ] **(C)** `thread_local` has non-trivial initialization cost: each thread pays the initialization on first access. Avoid `thread_local` for large objects that may not be used by every thread -- use lazy wrappers or `std::optional`. [R5:Item 40]
- [ ] **(C)** `thread_local` can mask design problems. If two threads "don't share" data but their behavior must be coordinated, `thread_local` is the wrong answer -- use explicit synchronization or message-passing instead. [R2]
- [ ] **(C)** Beware of `thread_local` in dynamically loaded libraries (DLLs/shared objects): the C++ standard is under-specified on when thread_local destructors run during `dlclose`. Prefer a singleton with `std::shared_ptr` and explicit shutdown for library interfaces. [R4]

---

## Quick Decision Tree

```
Shared mutable state accessed from multiple threads?
├─ NO → No synchronization needed (immutable / thread-private)
└─ YES → Choose protection mechanism:

    Mutex (exclusive access):
    ├─ Single mutex → std::lock_guard / std::scoped_lock [Item 2]
    ├─ Multiple mutexes → std::scoped_lock or std::lock [Item 3]
    │     └─ Consistent lock order documented? [Item 3]
    └─ Don't call user code while holding lock [Item 3]

    Atomic (lock-free):
    ├─ Simple flag/counter → std::atomic<T>, seq_cst [Item 4]
    ├─ Publish/consume pattern → acquire/release [Item 4]
    └─ Lock-free data structure → benchmark + TSan + second review [Item 4]

    Condition variable (wait for state change):
    ├─ while(!predicate()) cv.wait(lock) [Item 8]
    ├─ Modify state under mutex before notify [Item 8]
    └─ Prefer notify_all() [Item 8]

    Thread management:
    ├─ Prefer jthread (C++20) or join() over detach() [Item 7]
    └─ Detach() → capture by value, use shared_ptr for lifetime [Item 7]

Signal handler?
└─ std::atomic flag only — no mutex, no lock [Item 9]

Thread-local? → No sharing needed and OK with init cost? [Item 10]

TSan CI gate → mandatory [Item 6]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Volatile as Thread Synchronization

- **Appearance:** `volatile bool ready;` shared between threads; writer sets it to `true`, reader spins on `while (!ready);`.
- **Trap:** Volatile prevents the compiler from optimizing away repeated reads of the same variable -- it "looks like" synchronization to engineers familiar with Java (where `volatile` has acquire-release semantics). In C++ it has no such semantics.
- **Consequence:** The compiler and CPU may reorder the write to `ready` relative to writes to the data it is supposed to guard. The reader may see `ready == true` but stale data (or partially constructed objects). The reader's spin-loop is a data race and undefined behavior. The optimizer may even hoist the read out of the loop.
- **Fix:** Replace with `std::atomic<bool> ready;` using at least `memory_order_acquire` (writer) / `memory_order_release` (reader), or default `seq_cst`.

### Anti-Pattern 2: Double-Checked Locking Without Atomic

- **Appearance:**
  ```cpp
  if (!ptr) {           // first check (no lock)
      std::lock_guard lk(mtx);
      if (!ptr) {       // second check (under lock)
          ptr = new T(); // init
      }
  }
  // use ptr
  ```
- **Trap:** The pattern is widely known and "works in Java." The first check reduces lock contention for the common case (already initialized).
- **Consequence:** Without `std::atomic` on the pointer, the write to `ptr` in the constructor and the write to `ptr` (the pointer assignment) may be reordered. A second thread can see a non-null `ptr` pointing to uninitialized memory. This is a data race and undefined behavior -- it can and does crash in production.
- **Fix:** Use `std::atomic<T*>` with acquire/release ordering, or better, use `std::call_once` / `std::once_flag`, or a function-local `static` (which is thread-safe since C++11).

### Anti-Pattern 3: Manual Mutex Lock/Unlock

- **Appearance:** `mtx.lock();` at function entry, `mtx.unlock();` before each return. Multiple return paths, some of which are conditional or exception-driven.
- **Trap:** Manual locking seems "explicit and clear" -- you can see exactly where the lock is held.
- **Consequence:** An early return, uncaught exception, or `continue`/`break` skips `unlock()`. The mutex remains locked forever. Every subsequent thread blocks. The program deadlocks or hangs. Even if correct today, a future maintainer adding a new return path will likely miss it.
- **Fix:** Replace every manual `lock()`/`unlock()` pair with `std::lock_guard`, `std::scoped_lock`, or `std::unique_lock`. RAII guarantees unlock on every exit path.

---

## See Also

- [Smart Pointer and Ownership](../memory/ownership.md) -- `shared_ptr` control block thread safety and pointee synchronization
- [RAII and Resource Management](../memory/raii.md) -- Foundation: mutex guards are RAII types
- [Undefined Behavior](../correctness/undefined-behavior.md) -- Data races are one category of UB; other forms interact with concurrency (e.g., object lifetime issues)

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [intro.races], [thread], [atomics] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | CP.1-CP.50, CP.100-CP.112, CP.200-CP.202 | verified-2026 | 2026-06 |
| R3 | C | SEI/CERT C++ Coding Standard | CON40-CPP through CON56-CPP | verified-2026 | 2026-06 |
| R4 | A | C++ Concurrency in Action 2/e (Williams) | Chapters 2-9 | verified-2026 | 2026-06 |
| R5 | A | Effective Modern C++ (Meyers) | Items 35-40 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft -- full checklist covering data races, mutex RAII, deadlock prevention, atomics memory ordering, volatile vs atomic, TSan CI, detached threads, condition variables, signal handlers, and thread-local storage
