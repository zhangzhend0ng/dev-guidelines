---
type: harness
id: "cpp-exception-safety"
title: "Exception Safety Guarantees Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Ensure every function and class satisfies the appropriate exception safety guarantee level in C++"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [exceptions, exception-safety, raii, noexcept]
based_on:
  - "[N] ISO C++ [except.ctor], [except.spec]"
  - "[C] C++ Core Guidelines E.1-E.31"
  - "[C] SEI/CERT ERR51-CPP, ERR55-CPP, ERR59-CPP"
  - "[A] Exceptional C++ (Sutter) Items 8-19"
  - "[A] Effective C++ (Meyers) Item 29"
related:
  - "cpp/memory/raii.md"
  - "common/error-handling/error-handling-strategy.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Exception Safety Guarantees Checklist

**Based on:** ISO C++ [except.ctor]/[except.spec] ([N]), C++ Core Guidelines E.1-E.31 ([C]), SEI/CERT ERR51-CPP/ERR55-CPP/ERR59-CPP ([C]), Exceptional C++ Items 8-19 ([A]), Effective C++ Item 29 ([A]).
**Scope:** Verify that every function and class satisfies the appropriate exception safety guarantee level, and that exception handling code is correct, efficient, and does not introduce new bugs.

---

## Prerequisites / Concepts

### The Three Exception Safety Guarantees

| Level | Definition | When Required |
|-------|-----------|---------------|
| **Nothrow** | Operation cannot fail. Never throws. | Destructors, move constructors, `swap`, release/close operations |
| **Strong** | Commit-or-rollback. On failure, program state is unchanged -- as if the operation never happened. | Mutating operations on complex data structures, transactions |
| **Basic** | No leaks, invariants preserved. State may have changed but is valid and destructible. | Minimum bar for every function that can throw |

**Core principle: Every function must satisfy at least the basic guarantee. The guarantee level of a composite operation is the weakest guarantee among its constituent operations.**

### Critical Language Rules

| Rule | Rationale |
|------|-----------|
| Destructors are implicitly `noexcept` | Throwing during stack unwinding calls `std::terminate()` |
| Constructors that throw do NOT invoke the destructor | Only fully-constructed sub-objects have their destructors run |
| `catch` by reference | Prevents slicing; required for polymorphic exception hierarchies |
| `noexcept` is part of the type system | Affects move vs. copy selection in standard containers |

---

## Checklist

### 1. Basic Guarantee: No Leaks, Invariants Preserved

Does every throwing function leave objects in a destructible state with no resource leaks?

- [ ] Every acquired resource bound to RAII owner before any throwing operation --> **(N)** Satisfies basic guarantee [R1]
- [ ] All class invariants hold after an exception -- no dangling pointers, no double-free, no invalid state --> **(N)** Required [R1]
- [ ] Raw `new`/`delete` present? --> **(N)** Replace with `std::unique_ptr` / `std::make_unique`. Raw allocation cannot be exception-safe without RAII. [R1][R3]

```cpp
// Good -- RAII ensures no leaks even if process() throws
void good(std::istream& in) {
    auto data = std::make_unique<Buffer>(read_header(in));  // owns resource
    data->process();  // if this throws, ~unique_ptr cleans up
}

// Bad -- leak if process() throws
void bad(std::istream& in) {
    auto* data = new Buffer(read_header(in));
    data->process();  // leak if this throws!
    delete data;
}
```

---

### 2. Strong Guarantee: Commit-or-Rollback Semantics

Does the operation either fully succeed or leave the object unchanged?

- [ ] Mutating operation on data structure --> **(C)** Implement via copy-and-swap idiom: copy whole state, mutate copy, swap (nothrow) with original. [R2][R5]
- [ ] Allocation or copy can fail --> **(C)** Ensure no side effects before the last throwing operation (Sutter's "do all the work off to the side, then commit using non-throwing operations only"). [R5]
- [ ] Cannot afford copy overhead --> **(C)** Document as basic-only guarantee. Strong guarantee is not free. [R5]

```cpp
// Good -- copy-and-swap: strong guarantee
class Widget {
public:
    Widget& operator=(const Widget& rhs) {
        Widget temp(rhs);       // copy -- may throw
        swap(temp);             // noexcept -- commit
        return *this;
    }                           // temp destroyed with old state
private:
    void swap(Widget&) noexcept;
};

// Bad -- partial mutation on failure
Widget& bad_assign(const Widget& rhs) {
    clear();                    // side effect 1
    for (auto& item : rhs.items_)
        items_.push_back(item); // may throw after partial clear!
    return *this;
}
```

---

### 3. Nothrow Guarantee: Destructors, Move Constructors, Swap

Do operations that must never fail guarantee they do not throw?

- [ ] Destructor --> **(N)** Must not throw. Implicitly `noexcept`. If release can fail, catch, log, and suppress. [R1]
- [ ] Move constructor --> **(C)** Mark `noexcept`. Enables `std::vector` to move elements on reallocation instead of copying. [R2][R3]
- [ ] Move assignment --> **(C)** Mark `noexcept` when possible. Prefer copy-and-swap for strong guarantee; mark `noexcept` only if truly non-throwing. [R2]
- [ ] `swap` function --> **(C)** Mark `noexcept`. Foundation of copy-and-swap and strong guarantee. [R2][R5]

```cpp
// Good -- noexcept on move and swap enables STL optimizations
class Good {
public:
    Good(Good&& other) noexcept;              // enables vector move-realloc
    Good& operator=(Good&& other) noexcept;
    friend void swap(Good& a, Good& b) noexcept;
};

// Bad -- missing noexcept blocks STL optimization
class Slow {
public:
    Slow(Slow&& other);                       // vector will copy, not move
    Slow& operator=(Slow&& other);
};
```

---

### 4. Never Throw from Destructors

Does any destructor propagate an exception?

- [ ] Destructor calls a function that may throw (e.g., `close()`, `flush()`, `commit()`) --> **(N)** Wrap in try-catch. Log failure. Do NOT propagate. [R1][R3]
- [ ] Destructor running during stack unwinding (another exception in flight) and throws --> **(N)** `std::terminate()` is called. Process dies. Never allow this. [R1]
- [ ] Destructor `noexcept(false)` --> **(N)** Justify in writing. Only acceptable: destructors of types used exclusively in non-unwinding contexts. [R3]

```cpp
// Good -- suppress exceptions from cleanup
~Connection() {
    try {
        close();  // may fail (network gone)
    } catch (const std::exception& e) {
        log_error("close failed in destructor: {}", e.what());
        // swallow -- cannot propagate from destructor
    }
}

// Bad -- exception escapes destructor
~BadConnection() {
    close();  // if this throws and we are already unwinding --> std::terminate()
}
```

---

### 5. Use RAII to Achieve Exception Safety

Are resources managed manually in try/catch blocks instead of RAII?

- [ ] Manual `try`/`catch` for resource cleanup --> **(N)** Replace with RAII owner. Manual cleanup is fragile: early return, exception, or missing catch path all leak. [R1][R2]
- [ ] `lock()`/`unlock()` --> **(C)** Use `std::lock_guard` / `std::scoped_lock`. [R2]
- [ ] `fopen()`/`fclose()` --> **(C)** Use `std::fstream` or `std::unique_ptr<FILE, decltype(&fclose)>`. [R2]
- [ ] Every `new` --> **(C)** `std::make_unique` / `std::make_shared` or container. [R2]

```cpp
// Good -- RAII handles all exit paths
void process_file(const char* path) {
    std::ifstream file(path);
    auto data = std::make_unique<Buffer>();
    std::scoped_lock lock(mutex_);
    file >> *data;  // may throw -- RAII cleans up file, data, lock
}

// Bad -- manual cleanup is fragile
void bad_process(const char* path) {
    std::FILE* f = std::fopen(path, "r");
    auto* data = new Buffer();
    mtx_.lock();
    try {
        read(f, data);
    } catch (...) {
        std::fclose(f);
        delete data;
        mtx_.unlock();
        throw;
    }
    std::fclose(f);
    delete data;
    mtx_.unlock();
}
```

---

### 6. Exception-Unsafe Composition: Chain Is Only as Strong as the Weakest Link

If a function calls multiple sub-operations, does the weakest guarantee propagate correctly?

- [ ] Composite operation calling N sub-operations --> **(C)** Overall guarantee = min(guarantee of each sub-op). If any sub-op is basic-only, composite is basic-only. [R2][R5]
- [ ] Mixing basic and nothrow operations --> **(C)** Composite is basic unless all mutation is done off to the side before commit. [R5]
- [ ] Calling third-party or legacy code --> **(C)** Assume basic guarantee unless documented otherwise. Wrap in try-catch if stronger guarantee needed. [R2]

```cpp
// Good -- explicit about guarantee level
/// Returns basic guarantee: on failure, `out` may have partial data but is valid.
void serialize(std::vector<Record>& out, const Input& in) {
    for (const auto& r : in.records())
        out.push_back(serialize_one(r));  // may throw; partial out is valid
}

// Bad -- silent degradation from strong to basic
void transfer_all(Account& a, Account& b) {
    // If second debit throws, first debit already happened -- only basic guarantee!
    a.debit(100);  // throws on insufficient funds
    b.debit(200);  // throws on insufficient funds
}
```

---

### 7. Catch by Reference, Not by Value

Are exception handlers catching polymorphic types by value, causing slicing?

- [ ] `catch (std::exception e)` --> **(N)** Must be `catch (const std::exception& e)`. Value catch slices derived exceptions, losing type information and data. [R1][R4]
- [ ] `catch (...)` followed by `throw;` --> **(C)** Correct for cleanup-and-rethrow. Use `throw;` (not `throw e;`) to preserve original exception type and stack trace. [R2]
- [ ] Multiple catch blocks --> **(C)** Order most-derived first. `catch (const std::runtime_error&)` must come before `catch (const std::exception&)`. [R4]

```cpp
// Good -- catch by const reference, ordered derived-to-base
try {
    risky_operation();
} catch (const std::out_of_range& e) {
    // handle specific
} catch (const std::runtime_error& e) {
    // handle runtime errors
} catch (const std::exception& e) {
    // handle generic
}

// Bad -- value catch slices
try {
    risky_operation();
} catch (std::exception e) {  // SLICES derived exception -- only std::exception part retained
    std::cerr << e.what();    // may lose derived-class what() message
}
```

---

### 8. Avoid `catch(...)` Without Rethrow

Does code swallow all exceptions indiscriminately?

- [ ] `catch (...) { }` with no action --> **(N)** Must rethrow or document (with rationale) why swallowing is safe. Swallowing masks critical errors (`std::bad_alloc`, thread cancellation). [R2][R3]
- [ ] `catch (...)` as scope guard --> **(C)** Must rethrow: `catch (...) { cleanup(); throw; }`. Prefer RAII or scope guard instead. [R2]
- [ ] `catch (...)` at thread boundary --> **(C)** Acceptable pattern: catch all, log, then `std::terminate()` or set `std::exception_ptr`. [R3]

```cpp
// Good -- catch-all at thread boundary with logging
void thread_main() noexcept {
    try {
        do_work();
    } catch (const std::exception& e) {
        log_fatal("Worker thread: {}", e.what());
        global_error = std::current_exception();
    } catch (...) {
        log_fatal("Worker thread: unknown exception");
        global_error = std::current_exception();
    }
}

// Bad -- silent swallow
void danger_zone() {
    try {
        process();
    } catch (...) {
        // Pretend nothing happened -- masks all errors including fatal ones
    }
}
```

---

### 9. `noexcept` Annotation on Functions That Cannot Fail

Are functions that never throw properly annotated?

- [ ] Function with no throwing operations and no call to throwing functions --> **(C)** Annotate `noexcept`. Enables compiler optimizations. [R2][R5]
- [ ] `noexcept` function calls a function that may throw --> **(N)** Compiler trusts the annotation. If it throws, `std::terminate()` is called. Fix by removing `noexcept` or wrapping the call. [R1]
- [ ] Conditional `noexcept(expr)` --> **(C)** Use for generic code: `noexcept(noexcept(T(std::declval<U>())))`. Documents that noexcept-ness depends on template parameters. [R5]

```cpp
// Good -- noexcept on truly non-throwing operations
class FixedBuffer {
public:
    size_t size() const noexcept { return size_; }     // trivial getter
    bool empty() const noexcept { return size_ == 0; } // trivial
    void clear() noexcept { size_ = 0; }               // no allocation
};

// Bad -- noexcept on potentially-throwing function
void bad_noexcept() noexcept {
    std::vector<int> v(1000000);  // may throw std::bad_alloc --> std::terminate()!
}
```

---

### 10. Move Constructors Marked `noexcept`

Is every move constructor annotated `noexcept` to enable STL container optimizations?

- [ ] Move constructor with default behavior --> **(C)** `= default` generates implicit `noexcept` when all members have `noexcept` moves. [R2]
- [ ] Move constructor implemented manually --> **(C)** Mark `noexcept` unless it genuinely must allocate or throw. If it must throw, document why and accept that `std::vector` will copy instead of move during reallocation. [R2][R5]
- [ ] Move constructor missing `noexcept` --> **(C)** `std::vector::push_back` and reallocation will call the copy constructor instead, degrading performance from O(1) to O(N). [R2]

```cpp
// Good -- noexcept move enables vector optimization
class Transferable {
    std::unique_ptr<Impl> impl_;
public:
    Transferable(Transferable&&) noexcept = default;  // unique_ptr move is noexcept
};

// Bad -- missing noexcept causes silent performance degradation
class Pessimized {
    std::unique_ptr<Impl> impl_;
public:
    Pessimized(Pessimized&& other)  // NOT noexcept -- vector will copy instead
        : impl_(std::move(other.impl_)) {}
};

static_assert(std::is_nothrow_move_constructible_v<Transferable>);  // true
static_assert(std::is_nothrow_move_constructible_v<Pessimized>);    // false -- costly!
```

---

## Quick Decision Tree

```
Exception thrown inside function?
  └─ YES --> Leaks possible? [Item 1]
              ├─ YES --> Add RAII owner. Retry.
              └─ NO  --> Invariants hold after throw? [Item 1]
                          ├─ NO  --> Restore invariants. Retry.
                          └─ YES --> Strong guarantee needed? [Item 2]
                                      ├─ YES --> Copy-and-swap or do-work-off-to-side [Item 2]
                                      └─ NO  --> Basic guarantee is sufficient. Document it.

Destructor?
  └─ Always: catch and suppress. Do NOT throw. [Item 4]

Move constructor?
  └─ Always: mark noexcept. [Item 3][Item 10]

Resource managed manually (new/delete, lock/unlock)?
  └─ Replace with RAII. [Item 5]

catch block?
  ├─ Catch by const reference. [Item 7]
  ├─ catch(...) must rethrow or log-and-terminate. [Item 8]
  └─ Order: most-derived first. [Item 7]

Function never throws?
  └─ Annotate noexcept. [Item 9]

Calling multiple sub-operations?
  └─ Composite guarantee = min(sub-operation guarantees). [Item 6]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Throwing Destructor

- **Appearance:** Destructor calls `close()`, `flush()`, `commit()`, or `cleanup()` without wrapping in try-catch.
- **Trap:** "Proper error handling means reporting failures." It feels wrong to silently ignore a failed close.
- **Consequence:** If an exception is already in flight (stack unwinding), a second exception from the destructor calls `std::terminate()`. The process dies immediately, with no recovery. If no exception is in flight, the exception propagates, but the caller cannot meaningfully respond since destruction is non-negotiable.
- **Fix:** Wrap fallible cleanup calls in `try { ... } catch (const std::exception&) { log(); }` inside the destructor body. Accept that destructors cannot report errors through exceptions. Provide a separate `close()` or `shutdown()` method for explicit error reporting when the object is still in active use.

### Anti-Pattern 2: Catching by Value (Slicing)

- **Appearance:** `catch (std::exception e)` instead of `catch (const std::exception& e)`.
- **Trap:** It compiles and works for the base-class slice. For simple cases throwing `std::runtime_error`, the `what()` message may even survive.
- **Consequence:** When a derived exception is thrown (e.g., `std::out_of_range`, `std::system_error`, custom exception hierarchies), the caught-by-value copy slices off all derived-class data. The `what()` string may change, error codes are lost, and `dynamic_cast` or `typeid` checks fail silently. The wrong catch handler may fire.
- **Fix:** Always `catch (const T&)`. No exceptions to this rule. Use `catch (...); throw;` only for rethrow-after-cleanup patterns.

### Anti-Pattern 3: Silent Exception Swallowing

- **Appearance:** `try { ... } catch (...) { }` or `catch (const std::exception&) { }` with an empty body.
- **Trap:** "This operation is non-critical." "It happens rarely." The code compiles cleanly and passes normal testing.
- **Consequence:** Critical failures (`std::bad_alloc`, corrupted state, logic errors manifesting as exceptions) are silently discarded. The program continues in an undefined or subtly wrong state. Debugging becomes extremely difficult because the original failure site has no trace. On some platforms, structured exceptions (SEH on Windows) can be caught by `catch(...)`, masking access violations.
- **Fix:** At minimum, log the exception with `e.what()` and context. If truly non-critical: document the rationale in a comment adjacent to the catch block. Prefer catching specific exception types over `catch(...)`. At thread boundaries: catch, log, store `std::current_exception()`, and either terminate or set an error flag.

---

## See Also

- [RAII and Resource Management](../memory/raii.md) -- RAII is the foundation of exception safety; this harness assumes RAII discipline
- [Error Handling Strategy (Common)](../../common/error-handling/error-handling-strategy.md) -- Language-agnostic error handling strategy; this harness provides the C++ concrete rules

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | [N1] ISO/IEC 14882 (C++ Standard) | [except.ctor], [except.spec], [except.terminate] | verified-2026 | 2026-06 |
| R2 | C | [C1] C++ Core Guidelines | E.1-E.31 | verified-2026 | 2026-06 |
| R3 | C | [C2] SEI/CERT C++ Coding Standard | ERR51-CPP, ERR55-CPP, ERR59-CPP | verified-2026 | 2026-06 |
| R4 | A | [A1] Effective C++ (Meyers) | Item 29 | verified-2026 | 2026-06 |
| R5 | A | [A6] Exceptional C++ (Sutter) | Items 8-19 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
