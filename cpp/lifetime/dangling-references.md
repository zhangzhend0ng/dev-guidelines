---
type: harness
id: "cpp-lifetime"
title: "Object Lifetime and Dangling References Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Prevent use-after-scope, dangling pointers/references, and iterator invalidation in C++"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [lifetime, dangling, use-after-free, iterators, references]
based_on:
  - "[N] ISO C++ [basic.life], [class.temporary], [res.on.arguments], [sequence.reqmts]"
  - "[C] C++ Core Guidelines R.30-R.37, F.43-F.45, F.52-F.54"
  - "[C] SEI/CERT EXP54-CPP, EXP61-CPP"
  - "[A] Effective Modern C++ (Meyers) Items 31-34"
  - "[A] C++ Best Practices (Jason Turner) on lifetime"
related:
  - "cpp/security/secure-coding.md"
  - "cpp/correctness/class-hierarchies.md"
  - "cpp/correctness/stl-algorithms-containers.md"
  - "cpp/memory/ownership.md"
  - "cpp/memory/raii.md"
  - "cpp/correctness/const-correctness.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Object Lifetime and Dangling References Checklist

**Based on:** ISO C++ [basic.life]/[class.temporary] ([N]), C++ Core Guidelines R.30-R.37 ([C]), SEI/CERT EXP54-CPP ([C]), Effective Modern C++ Items 31-34 ([A]).
**Scope:** Detect and prevent use-after-scope bugs, dangling pointers/references, and iterator invalidation. This harness covers stack-lifetime violations, view-type lifetime dependency, lambda captures, smart-pointer cycles, and static initialization ordering. It does not cover general memory leaks (see RAII harness) or thread-safety guarantees (see concurrency harness).

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|-----------|
| **Lifetime** | The period during which an object exists in memory, from construction through destruction. Accessing an object outside its lifetime is undefined behavior. |
| **Dangling Pointer/Reference** | A pointer or reference that names an object whose lifetime has ended. Dereferencing it is UB. |
| **Use-After-Scope** | Accessing a stack-allocated object after the scope in which it was defined has exited. |
| **Iterator Invalidation** | A container operation (insert, erase, push_back, rehash) renders existing iterators, pointers, or references to its elements invalid. |
| **View Types** | `std::string_view`, `std::span`, and similar non-owning types that reference data owned elsewhere. They are inherently lifetime-dependent. |
| **Temporary Materialization** | A prvalue is converted to an xvalue (materialized) when bound to a reference. The temporary's lifetime is extended to match the reference. |
| **Meyer's Singleton** | A function-local static variable initialized exactly once on first call, solving the static initialization order fiasco. |

---

## Checklist

### 1. Returning References or Pointers to Locals

The most fundamental lifetime violation: the caller receives an address to memory that no longer holds a valid object.

- [ ] Function returns a reference, pointer, `string_view`, or `span`? → **(N)** Verify the referent outlives every return path. Never return a local by reference. [R1][R3]
- [ ] Compiler emits `-Wreturn-local-addr` or `-Wdangling-reference`? → **(N)** Treat as hard error. Fix immediately. [R1]

```cpp
// Good -- return by value; guaranteed safe
std::string get_message() {
    return "hello";  // copy/move elision may apply
}

// Bad -- dangling reference to destroyed stack frame
const std::string& get_message() {
    std::string msg = "hello";
    return msg;  // UB: msg destroyed at '}'
}
```

---

### 2. Iterator, Pointer, and Reference Invalidation

Container mutations can silently invalidate existing iterators, pointers, or references to elements. The rules vary by container type.

- [ ] Modifying a container while holding an iterator to it? → **(N)** Check invalidation rules for that container/operation pair. [R2][R3]
- [ ] `vector`/`string` `push_back`, `emplace_back`, `resize`? → **(N)** May reallocate -- all iterators, pointers, references invalidated if capacity changes. Pre-reserve or use index. [R2]
- [ ] `deque` insertion in the middle, or `map`/`set` erase of an element? → **(N)** Only iterators/references to the erased element are invalidated. [R2]
- [ ] `unordered_map`/`unordered_set` rehash? → **(N)** All iterators invalidated; references/pointers to elements remain valid. [R2]

```cpp
// Good -- erase returns next valid iterator
auto it = container.begin();
while (it != container.end()) {
    if (should_remove(*it))
        it = container.erase(it);  // next iterator assigned
    else
        ++it;
}

// Bad -- accessing invalidated iterator
for (auto it = vec.begin(); it != vec.end(); ++it) {
    if (it->expired())
        vec.erase(it);  // it is now invalid; ++it on next loop = UB
}
```

---

### 3. `string_view` and `span` to Temporaries

View types are non-owning references to contiguous data. Binding them to a temporary creates a dangling view.

- [ ] `std::string_view` constructed from a temporary `std::string` or `const char*` return? → **(N)** The temporary is destroyed at the full-expression semicolon; the view dangles. [R1][R4]
- [ ] `std::span` bound to a temporary vector or `initializer_list`? → **(N)** Same trap. Only bind views to objects whose lifetime is visibly longer than the view. [R1]
- [ ] **(C)** Prefer `std::string` parameters over `string_view` when the function must store the string. [R4]

```cpp
// Good -- view to existing object
std::string owner = "persistent data";
std::string_view sv = owner;  // safe: owner outlives sv

// Bad -- view to materialized temporary
std::string_view sv = "hello"s + " world";  // temporary destroyed; sv dangles
```

---

### 4. Lambda Capture by Reference Outliving Captured Variables

A lambda object that captures by reference becomes dangerous as soon as any captured variable's lifetime ends. This is particularly insidious with asynchronous callbacks and detached threads.

- [ ] Lambda stored beyond the current scope (callback, `std::function`, thread, future, coroutine)? → **(N)** Prefer capture by copy `[=]` or explicitly list captures. Never `[&]` on an escaping lambda. [R1][R4]
- [ ] Detached `std::thread` or `std::async` receiving a lambda? → **(N)** Capture by copy only. The spawning scope may end before the thread starts. [R4]
- [ ] **(C)** For move-only types, use `[x = std::move(x)]` init-capture instead of reference capture. [R6]

```cpp
// Good -- copy captures; lambda is self-contained
auto task = [data = heavy_data]() {
    process(std::move(data));
};
std::async(std::launch::async, task);

// Bad -- reference to local destroyed before async runs
std::string msg = "hello";
auto task = [&msg]() { return msg.size(); };  // msg dangles
std::async(std::launch::async, task);          // race: scope exit vs thread start
```

---

### 5. `shared_ptr` Cycles

`std::shared_ptr` uses reference counting. A cycle of shared ownership prevents the count from reaching zero, causing a memory leak.

- [ ] Two or more objects hold `shared_ptr` to each other (e.g., parent-child back-reference)? → **(N)** Break the cycle with `std::weak_ptr` on the back-reference side. [R1][R3]
- [ ] Observer pattern or callback list using `shared_ptr`? → **(C)** Observers should use `weak_ptr`; callbacks that own targets risk cycles. [R4]
- [ ] **(C)** Prefer `unique_ptr` + raw observer pointers over `shared_ptr` unless shared ownership is genuinely required. [R3]

```cpp
// Good -- parent owns child via shared_ptr, child observes parent via weak_ptr
struct Child {
    std::weak_ptr<Parent> parent;
};
struct Parent {
    std::shared_ptr<Child> child;
};

// Bad -- mutual shared_ptr: neither reference count reaches zero
struct Node {
    std::shared_ptr<Node> next;
    std::shared_ptr<Node> prev;
};
// A<->B cycle leaks both A and B
```

---

### 6. Capturing `this` in Asynchronous Contexts

A lambda or callback capturing `this` assumes the object still exists when invoked. In asynchronous code, this assumption often breaks.

- [ ] `this` captured by reference `[this]` or `[&]` in a lambda passed to async operation, thread, timer, or callback queue? → **(N)** Object may be destroyed before the lambda runs. [R1][R5]
- [ ] Shared ownership of `this` needed? → **(C)** Use `std::enable_shared_from_this` and capture a `weak_ptr<Self>`; in the callback, `lock()` before use. [R4]
- [ ] **(C)** If the class is not shared, ensure the async operation is joined/cancelled before the object is destroyed (e.g., in the destructor). [R7]

```cpp
// Good -- enable_shared_from_this with weak_ptr guard
class Worker : public std::enable_shared_from_this<Worker> {
    void schedule() {
        auto weak = weak_from_this();
        thread_pool.post([weak]() {
            if (auto self = weak.lock()) self->do_work();
        });
    }
};

// Bad -- raw this capture; object may be destroyed
void Widget::animate() {
    timer.call_later(100ms, [this]() {
        update(this->state_);  // UB if Widget destroyed
    });
}
```

---

### 7. Virtual Destructors and Inheritance Hierarchies

Deleting a derived object through a base-class pointer without a virtual destructor invokes undefined behavior and typically leaks the derived portion.

- [ ] Class is designed to be a polymorphic base class (has any virtual function)? → **(N)** Declare `virtual ~ClassName() = default;` (or define it). [R1][R3]
- [ ] Class is `final` or not polymorphic? → **(C)** Virtual destructor not needed. Rule of thumb: if `sizeof` matters, omit it. [R4]
- [ ] **(N)** Calling `delete` on a base pointer without virtual destructor = UB per [expr.delete]. [R1]

```cpp
// Good -- virtual destructor on polymorphic base
class Animal {
public:
    virtual ~Animal() = default;
    virtual void speak() const = 0;
};

// Bad -- deleting derived through non-virtual base
class Base { /* no virtual dtor */ };
class Derived : public Base { std::string name; };
Base* b = new Derived();
delete b;  // UB: ~Derived() not called; name leaks
```

---

### 8. Static Initialization Order Fiasco

The order of dynamic initialization of non-local static objects across translation units is unspecified. A static object using another static object may see it uninitialized.

- [ ] Non-local static object depends on another non-local static from a different TU? → **(N)** Replace with Meyer's Singleton: `static T& get() { static T instance; return instance; }`. [R1][R3]
- [ ] Global `const` objects with `constexpr` constructors? → **(N)** Mark `constexpr` to force constant initialization before any dynamic initialization. [R1]
- [ ] **(C)** Avoid non-trivial global objects entirely. Prefer dependency injection. [R4]

```cpp
// Good -- Meyer's Singleton guarantees first-use initialization
LogManager& log_manager() {
    static LogManager instance("app.log");
    return instance;
}

// Bad -- initialization order unspecified across TUs
// file_a.cpp: Database db("db.conf");
// file_b.cpp: Logger  log(db);  // db may not be initialized yet
```

---

### 9. Temporary Lifetime Extension

Binding a temporary to a `const T&` (or `T&&` in certain contexts) extends the temporary's lifetime to match the reference. However, the rules are nuanced and do not propagate through chains.

- [ ] `const T&` bound to a temporary? → **(N)** Lifetime IS extended to the reference's lifetime. Safe for function-local const refs. [R1]
- [ ] `T&&` bound to a temporary inside a function body? → **(N)** Lifetime IS extended (same rule). However, `T&&` parameters do NOT extend lifetime -- they are bound to the caller's argument. [R1]
- [ ] Reference member in a class bound to a constructor temporary? → **(N)** Lifetime is NOT extended through member initializer lists. The temporary dies at the full-expression semicolon. [R1]
- [ ] **(C)** Do not rely on lifetime extension when the reference is a return value -- it does not propagate. [R4]

```cpp
// Good -- local const ref extends lifetime
void example() {
    const std::string& s = std::string("hello");  // temporary lives to end of scope
    use(s);  // safe
}

// Bad -- member reference to temporary
struct Holder {
    const std::string& s;
    Holder(const std::string& s_) : s(s_) {}
};
Holder h(std::string("oops"));  // temporary destroyed; h.s dangles
```

---

### 10. Placement `new` and Manual Destructor Calls

Explicit object lifetime management bypasses the compiler's automatic guarantees. It is fragile and error-prone.

- [ ] Placement `new` used for object construction? → **(N)** You MUST call the destructor manually before reusing or freeing the storage. The compiler will not do it. [R1][R3]
- [ ] Destructor called manually (not through `delete`)? → **(N)** You MUST have constructed the object via placement `new` first. Calling a destructor on an unconstructed object is UB. [R1]
- [ ] **(C)** Prefer `std::optional`, `std::variant`, or `std::aligned_storage` wrappers over raw placement `new`. These encapsulate the lifetime bookkeeping. [R5][R6]
- [ ] **(A)** If placement `new` is unavoidable, wrap it in a small RAII helper or document the exact construction/destruction pairing. [R7]

```cpp
// Good -- std::optional models optional lifetime safely
std::optional<Expensive> obj;
if (condition)
    obj.emplace(args...);  // construction and destruction handled automatically

// Bad -- manual placement new without matching destructor call
alignas(Widget) char buf[sizeof(Widget)];
auto* w = new (buf) Widget(config);
// ... Widget used ...
// Missing: w->~Widget(); -- destructor never called, resources leaked
```

---

## Quick Decision Tree

```
Returning a reference/pointer/view from function?
  ├─ YES → Does referent outlive the return? [Item 1]
  │          ├─ YES → OK (document the contract)
  │          └─ NO  → STOP. Return by value or restructure ownership.
  └─ NO  → Holding iterator/ref into container?
              ├─ YES → Modifying container? [Item 2]
              │          ├─ YES → Check invalidation rules. Prefer index or reserve().
              │          └─ NO  → OK, but document iterator validity span.
              └─ NO  → Lambda stored beyond scope? [Item 4]
                         ├─ YES → shared_ptr cycle risk? [Item 5] → Use weak_ptr.
                         │        Capturing this? [Item 6] → Use weak_from_this().
                         │        Otherwise → Capture by copy, never [&].
                         └─ NO  → Polymorphic base without virtual dtor? [Item 7]
                                    ├─ YES → Add virtual ~T() = default.
                                    └─ NO  → Global static depending on another? [Item 8]
                                               └─ YES → Meyer's Singleton or constexpr.
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: The Convenient `string_view` Parameter

- **Appearance:** `void log(std::string_view msg);` called as `log("error: " + details());`
- **Trap:** `string_view` is efficient and avoids copies. The temporary looks fine in the one-liner.
- **Consequence:** The temporary `std::string` from the concatenation is destroyed at the semicolon. `msg` inside `log()` is a dangling view. Dereference = UB.
- **Fix:** If the call site creates a temporary, make the parameter `const std::string&` (which extends lifetime) or accept `std::string` by value (move into it). Alternatively, split the concatenation into a named variable whose lifetime encloses the call.

### Anti-Pattern 2: Caching Iterators

- **Appearance:** Storing `auto it = vec.begin() + offset;` as a member or long-lived local, then calling `push_back` or `erase` elsewhere.
- **Trap:** "I know the index is stable." Iterators feel like pointers into stable memory.
- **Consequence:** After reallocation, the stored iterator points into freed memory. Dereference = heap-use-after-free UB. Sanitizers catch this, but only if the test exercises the reallocation path.
- **Fix:** Store an index (`size_t`), not an iterator. Compute the iterator from `begin() + index` each time, or use a `std::list`/`std::map` where insert/erase does not invalidate other iterators.

### Anti-Pattern 3: Global Manager Objects

- **Appearance:** `Database& db() { static Database db; return db; }` in `file_a`, and `Logger::Logger() { db().log("init"); }` in `file_b` -- where `Logger` is also a global.
- **Trap:** Meyer's Singleton protects `Database`, but `Logger` is still a non-local static. If `Logger` is constructed before `Database::get()` is first called, it is fine. If not, the dependency order is still fragile across TUs even with Meyer's Singleton on the callee side.
- **Consequence:** Subtle initialization order bugs that depend on link order. Hard to reproduce, harder to debug.
- **Fix:** Make ALL globals Meyer's Singletons accessed via functions, or eliminate global state entirely through dependency injection. Never have one global constructor call into another global's state.

---

## See Also

- [RAII and Resource Management](../memory/raii.md) -- Owning resource lifecycles with destructors
- [Smart Pointer and Ownership](../memory/ownership.md) -- Choosing the right pointer type and ownership model
- [Const Correctness](../correctness/const-correctness.md) -- Const qualification interacts with lifetime (const ref extension)

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [basic.life], [class.temporary], [class.dtor], [expr.delete] | verified-2026 | 2026-06 |
| R2 | N | ISO C++ Standard | [res.on.arguments], [sequence.reqmts], [container.requirements] | verified-2026 | 2026-06 |
| R3 | C | C++ Core Guidelines | R.30-R.37 (lifetime safety), C.30-C.37 (destructors) | verified-2026 | 2026-06 |
| R4 | C | C++ Core Guidelines | F.43-F.45, F.52-F.54 (lambda captures, parameter passing) | verified-2026 | 2026-06 |
| R5 | C | SEI/CERT C++ | EXP54-CPP, EXP61-CPP (lifetime, lambda this capture) | verified-2026 | 2026-06 |
| R6 | A | Effective Modern C++ (Meyers) | Items 31-34 (lambda captures, init capture, move into lambda) | verified-2026 | 2026-06 |
| R7 | A | C++ Best Practices (Jason Turner) | Lifetime safety, placement new avoidance | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
