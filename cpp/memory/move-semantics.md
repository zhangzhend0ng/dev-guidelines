---
type: harness
id: "cpp-move-semantics"
title: "Move Semantics and Rule of Five Checklist"
language: "cpp"
category: "resource-management"
tier: "N"
scope: "Ensure correct implementation of move semantics and special member functions in C++"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [move-semantics, rule-of-five, rule-of-zero, rvalue, noexcept, forwarding]
based_on:
  - "[N] ISO C++ [class.copy.elision], [class.copy.assign], [class.copy.ctor]"
  - "[C] C++ Core Guidelines C.20-C.22, C.66, C.80-C.83, C.87, F.18"
  - "[C] SEI/CERT OOP51-CPP"
  - "[A] Effective Modern C++ (Meyers) Items 14, 17, 23-30"
  - "[A] A Tour of C++ 3rd ed. (Stroustrup) Chapter 6"
related:
  - "cpp/performance/optimization-patterns.md"
  - "cpp/memory/raii.md"
  - "cpp/memory/ownership.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Move Semantics and Rule of Five Checklist

**Based on:** ISO C++ [class.copy.elision]/[class.copy.assign]/[class.copy.ctor] ([N]), C++ Core Guidelines C.20-C.22, C.80-C.87, F.18 ([C]), SEI/CERT OOP51-CPP ([C]), Effective Modern C++ Items 14, 17, 23-30 ([A]), A Tour of C++ 3rd ed. Chapter 6 ([A]).

**Scope:** Verify correct declaration and implementation of move constructors, move assignment operators, and all special member functions. Covers forwarding, copy elision, and the relationship between move semantics and STL optimizations. Does not cover smart pointer choice (see ownership.md) or basic RAII patterns (see raii.md).

---

## Prerequisites / Concepts

### Value Category Taxonomy

| Category | Description | Example |
|----------|------------|---------|
| **lvalue** | Has identity; cannot be moved from (unless `std::move`-cast) | named variable, `*ptr` |
| **prvalue** | Pure rvalue; no identity; can be moved from | literal, temporary, function return by value |
| **xvalue** | eXpiring value; has identity but can be moved from | `std::move(x)`, `static_cast<T&&>(x)` |
| **glvalue** | Generalized lvalue; either lvalue or xvalue | anything with identity |
| **rvalue** | Either prvalue or xvalue; can be moved from | anything that can bind to `T&&` |

### Special Member Functions (Rule of Five)

| Member Function | Signature | Compiler-Generated When |
|----------------|-----------|------------------------|
| Default ctor | `T()` | No other ctor declared |
| Destructor | `~T()` | Always if not user-declared |
| Copy ctor | `T(const T&)` | No move operations declared |
| Copy assign | `T& operator=(const T&)` | No move operations declared |
| Move ctor | `T(T&&)` | No copy/move/dtor user-declared |
| Move assign | `T& operator=(T&&)` | No copy/move/dtor user-declared |

**Rule of Five:** If any of {destructor, copy-ctor, copy-assign, move-ctor, move-assign} is user-declared, the compiler-generated move operations are suppressed. Declare all five (or `=default` them) to make intent explicit.

**Rule of Zero:** If no member manages a resource directly, declare none of the five -- let the compiler generate all of them. This is the ideal; it relies on RAII member types (e.g., `std::vector`, `std::unique_ptr`) to handle resources correctly.

### Reference Collapsing

When combining references in template instantiation or `auto&&` deduction:

| Outer & | Inner & | Result |
|---------|---------|--------|
| `&` | `&` | `&` |
| `&` | `&&` | `&` |
| `&&` | `&` | `&` |
| `&&` | `&&` | `&&` |

The only way to get an rvalue reference is `T&&` + `T&&`. This is what makes `std::forward<T>(x)` work: when `T = U&` the result collapses to `U&` (lvalue); when `T = U` (no ref) the result is `U&&` (rvalue).

---

## Checklist

### 1. Apply Rule of Five When Any Special Member Is Custom

If a class manually manages any resource (raw pointer, handle, file descriptor), it must declare all five special members (or explicitly default the inapplicable ones).

- [ ] Custom destructor present? → **(N)** Declare copy-ctor, copy-assign, move-ctor, move-assign -- or `=delete` them if the class is move-only. [R1][R2]
- [ ] Custom copy operations present? → **(N)** Declare destructor, move-ctor, move-assign -- the compiler silently suppresses move generation. [R1][R2]
- [ ] Custom move-to-self handling implemented in move-assign via guard clause or self-assignment-safe logic. → **(C)** [R2]

```cpp
// Good — all five declared explicitly
class Buffer {
    char* data_;
    size_t size_;
public:
    explicit Buffer(size_t n) : data_(new char[n]), size_(n) {}
    ~Buffer() { delete[] data_; }
    Buffer(const Buffer& other) : data_(new char[other.size_]), size_(other.size_) {
        std::copy(other.data_, other.data_ + size_, data_);
    }
    Buffer& operator=(const Buffer& other) {
        if (this != &other) {
            delete[] data_;
            size_ = other.size_;
            data_ = new char[size_];
            std::copy(other.data_, other.data_ + size_, data_);
        }
        return *this;
    }
    Buffer(Buffer&& other) noexcept
        : data_(std::exchange(other.data_, nullptr)), size_(std::exchange(other.size_, 0)) {}
    Buffer& operator=(Buffer&& other) noexcept {
        if (this != &other) {
            delete[] data_;
            data_ = std::exchange(other.data_, nullptr);
            size_ = std::exchange(other.size_, 0);
        }
        return *this;
    }
};

// Bad — custom destructor suppresses implicit move; only copy will compile
class LeakyBuffer {
    char* data_;
    ~LeakyBuffer() { delete[] data_; }
    // MOVES ARE SUPPRESSED — std::vector<LeakyBuffer> will copy instead of move
};
```

---

### 2. Prefer Rule of Zero

If no member manages a resource directly, allow the compiler to generate all special members.

- [ ] All data members are RAII types (`std::string`, `std::vector`, `std::unique_ptr`, etc.)? → **(C)** Do not declare any of the five. [R2][R4]
- [ ] Business-logic class wrapping standard library types? → **(C)** Trust the compiler-generated defaults. [R2]

```cpp
// Good — Rule of Zero: no special members declared
class Customer {
    std::string name_;
    std::vector<Order> orders_;
public:
    Customer(std::string name) : name_(std::move(name)) {}
    // Compiler generates: destructor, copy, move — all correct
};

// Bad — unnecessary special members
class Unnecessary {
    std::string name_;
public:
    ~Unnecessary() {}              // suppresses move
    Unnecessary(const Unnecessary&) = default;  // boilerplate
    // ...
};
```

---

### 3. std::move Is a Cast, Not a Move Operation

Calling `std::move(x)` does not perform any move. It is an unconditional cast to rvalue reference -- only the subsequent operation (constructor, assignment) actually moves.

- [ ] `std::move` used only as the last use of an object, right before passing into a move-capable context. → **(C)** [R4]
- [ ] `std::move` not applied in a context where no move-capable overload exists (e.g., passing to a function taking `const T&` only). → **(C)** [R4]
- [ ] **(A)** `std::move` on a `const T` is a silent copy -- never do it. [R4]

```cpp
// Good — std::move triggers move constructor
std::vector<int> make_data();
std::vector<int> v = make_data();  // RVO, no std::move needed
std::vector<int> sink;
sink = std::move(v);  // v is now moved-from; last use of v in this scope

// Bad — std::move does nothing here because no move occurs
const std::vector<int> cv = {1, 2, 3};
auto copy = std::move(cv);  // calls COPY ctor, not move — cv is const!
```

---

### 4. Moved-From Objects: Valid-but-Unspecified State

After a move, the source object must be in a state where destruction and assignment are safe. No other invariants are guaranteed.

- [ ] Destructor call on moved-from object is safe. → **(N)** Required by the standard. [R1]
- [ ] Assignment to moved-from object (copy or move) is safe. → **(N)** Required by the standard. [R1]
- [ ] No reliance on moved-from value beyond the above guarantees (e.g., `v.front()` after move is unspecified). → **(C)** [R2]
- [ ] Move constructor uses `std::exchange` or equivalent to null-out the source's resource pointer. → **(C)** [R4]

```cpp
// Good — source left in safe state
Buffer(Buffer&& other) noexcept
    : data_(std::exchange(other.data_, nullptr)),
      size_(std::exchange(other.size_, 0)) {}
// other can now be safely destroyed or assigned to

// Bad — source left with dangling pointer
Buffer(Buffer&& other) noexcept
    : data_(other.data_), size_(other.size_) {}
// other.data_ still points to the now-transferred buffer
// Destructor on 'other' will double-delete
```

---

### 5. Move Operations Must Be noexcept

Move constructors and move assignment operators should be marked `noexcept`. Without this, `std::vector` and other STL containers cannot use them during reallocation and will fall back to slower copy operations.

- [ ] Move constructor marked `noexcept`. → **(C)** Enables STL optimization (e.g., `vector::push_back` strong exception guarantee path). [R2][R4]
- [ ] Move assignment operator marked `noexcept`. → **(C)** Same rationale. [R2]
- [ ] Move operations can truly never throw (no allocations, no external calls that might throw). → **(C)** Design requirement. If a move can throw, document why. [R4]

```cpp
// Good — noexcept enables vector growth optimization
class Buffer {
public:
    Buffer(Buffer&& other) noexcept;            // STL can use this
    Buffer& operator=(Buffer&& other) noexcept; // STL can use this
};

// Bad — missing noexcept forces copy fallback in std::vector
class BadMove {
public:
    BadMove(BadMove&& other);            // NOT noexcept
    BadMove& operator=(BadMove&& other); // NOT noexcept
    // std::vector<BadMove> will copy on reallocation — 2x slower
};
```

---

### 6. Copy Elision and RVO -- Do Not std::move Return Values

Since C++17, return value optimization (RVO) is guaranteed for prvalues. Wrapping a local return in `std::move` defeats RVO and forces a move (or worse, inhibits elision and forces a copy when no move ctor exists).

- [ ] Local variable returned by value from a function → **(N)** NEVER `std::move` it. RVO is mandatory in C++17. [R1][R4]
- [ ] Function parameter returned by value → **(C)** `std::move` is required here (parameters are lvalues). [R4]
- [ ] Conditional return (e.g., from `if` branches) → **(C)** `std::move` may be needed because NRVO is not guaranteed across branches. [R4]

```cpp
// Good — trust RVO
Widget make_widget() {
    Widget w;          // local variable
    w.configure();
    return w;          // NRVO applies; no copy, no move
}

// Bad — std::move on return defeats RVO
Widget make_bad() {
    Widget w;
    w.configure();
    return std::move(w);  // forces move, prevents RVO
}

// Good — std::move parameter returns (parameters are lvalues)
Widget process(Widget w) {
    mutate(w);
    return std::move(w);  // correct: w is a parameter, not a local
}

// Good — conditional branches
Widget pick(bool flag) {
    Widget a, b;
    if (flag)
        return std::move(a);  // NRVO not guaranteed across branches
    return std::move(b);
}
```

---

### 7. Sink Parameters: Pass by Value, Then std::move

When a function needs to store a copy of an argument (a "sink" parameter), pass by value and `std::move` into the stored location. This amortizes the cost: lvalues get one copy, rvalues get one move.

- [ ] Function stores a copy of the argument (e.g., constructor initializer, setter). → **(C)** Pass by value + `std::move`. [R4]
- [ ] Function only reads the argument → **(C)** Pass by `const T&`. Do NOT use the sink pattern. [R2]
- [ ] Argument is a non-copyable move-only type → **(C)** Pass by `T&&` or by-value + `std::move` as appropriate. [R4]

```cpp
// Good — sink pattern
class Employee {
    std::string name_;
    std::vector<int> scores_;
public:
    Employee(std::string name, std::vector<int> scores)
        : name_(std::move(name)), scores_(std::move(scores)) {}
    // lvalue: 1 copy (parameter) + 1 move (into member) = amortized
    // rvalue: 1 move (parameter) + 1 move (into member) = optimal
};

// Bad — two overloads (boilerplate explosion)
class Boilerplate {
    std::string name_;
public:
    void setName(const std::string& s) { name_ = s; }  // 1 copy
    void setName(std::string&& s) { name_ = std::move(s); }  // 1 move
    // For N parameters, 2^N overloads. Use sink pattern instead.
};
```

---

### 8. Do Not std::move a const Object

`std::move` on a `const T` silently produces a `const T&&`, which binds to the copy constructor (not the move constructor). The result is a copy -- no compiler warning.

- [ ] `const` object in scope → **(N)** NEVER `std::move` it; it will copy. [R1][R4]
- [ ] Function returns `const T` by value → **(C)** Do not `std::move`; the `const` already inhibits move in C++11+. [R4]
- [ ] **(A)** Prefer not returning `const T` by value at all (inhibits move for callers). [R4]

```cpp
// Bad — const + std::move = silent copy
const std::string s = "hello";
auto x = std::move(s);   // calls string(const string&) — a COPY, not a move

// Good — non-const enables actual move
std::string s = "hello";
auto x = std::move(s);   // calls string(string&&) — actual move
```

---

### 9. Understand lvalue vs rvalue vs xvalue Distinctions

Correct use of move semantics depends on understanding which expressions bind to `T&` (lvalues) versus `T&&` (rvalues, including xvalues from `std::move`).

- [ ] Named variables are always lvalues (even if their type is rvalue reference). → **(C)** Use `std::move` to cast to xvalue. [R4]
- [ ] A function parameter of type `T&&` is an lvalue inside the function body. → **(C)** Must `std::forward<T>(x)` (in templates) or `std::move(x)` (concrete) to forward/pass on. [R4]
- [ ] **(A)** Understand: `decltype((x))` for named variable gives `T&` (always lvalue reference). [R4]

```cpp
// Demonstrates: rvalue-ref parameter IS an lvalue inside the function
void sink(std::string&& s) {
    // s is an lvalue here! Its type is rvalue-ref, but it's a named variable.
    std::string local = s;             // copies (s is lvalue)
    std::string local2 = std::move(s); // moves (std::move casts to xvalue)
}

// Template forwarding: use std::forward, not std::move
template <typename T>
void relay(T&& arg) {
    // arg is an lvalue. std::forward<T> preserves the original value category:
    target(std::forward<T>(arg));  // lvalue if T=U&, rvalue if T=U
}
```

---

### 10. std::forward for Perfect Forwarding in Templates

In forwarding references (`T&&` in a deduced context), use `std::forward<T>` to preserve the argument's original value category. Never use `std::move` for forwarding -- it unconditionally casts to rvalue.

- [ ] Template function taking `T&&` (forwarding/universal reference) → **(C)** Use `std::forward<T>(x)` to pass on, never `std::move(x)`. [R2][R4]
- [ ] `std::forward<T>` without valid T deduction → **(C)** Fails at compile time with confusing errors; ensure forwarding reference context. [R4]
- [ ] `std::forward<T>` used exactly once per forwarding reference -- same argument cannot be forwarded twice (use-after-move risk). → **(C)** [R2]

```cpp
// Good — perfect forwarding with variadic templates
template <typename T, typename... Args>
std::unique_ptr<T> make(Args&&... args) {
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}

// Bad — std::move destroys value category information
template <typename T>
void bad_forward(T&& arg) {
    target(std::move(arg));  // ALWAYS rvalue — even when caller passed lvalue
}

// Good — pair with decltype(auto) for return forwarding
template <typename F, typename... Args>
decltype(auto) invoke(F&& f, Args&&... args) {
    return std::forward<F>(f)(std::forward<Args>(args)...);
}
```

---

## Quick Decision Tree

```
Implementing a class?
  ├─ All members are RAII types?
  │     YES → Rule of Zero: declare nothing [Item 2]
  │     NO  → Rule of Five: declare all five [Item 1]
  │              ├─ Move ctor? → noexcept + valid-but-unspecified source [Items 4, 5]
  │              └─ Move assign? → noexcept + self-assignment guard [Items 4, 5]
  │
  ├─ Passing argument to store in member?
  │     ├─ Sink (store copy) → pass by value + std::move [Item 7]
  │     └─ Forward (template) → T&& + std::forward [Item 10]
  │
  └─ Returning value from function?
        ├─ Local variable → just return it (RVO) [Item 6]
        ├─ Parameter → std::move it [Item 6]
        ├─ Const object → NEVER std::move it [Item 8]
        └─ Conditional branches → std::move each branch [Item 6]

Using std::move?
  ├─ On non-const object in last use → OK [Item 3]
  ├─ On const object → BAD — silent copy [Item 8]
  ├─ On return value → BAD unless parameter [Item 6]
  └─ In template forwarding → BAD — use std::forward [Item 10]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Missing Move Semantics via Custom Destructor

- **Appearance:** Class has a custom destructor but no move constructor or move assignment operator declared.
- **Trap:** The code compiles and runs. No warning or error is emitted; the compiler silently falls back to copy semantics.
- **Consequence:** `std::vector<MyType>` reallocation copies every element instead of moving. O(n) overhead becomes O(n^2) in pathological cases. For large objects, this can be a dramatic performance regression.
- **Fix:** Declare move ctor and move assign as `=default` (if all members are movable) or implement them manually. Mark them `noexcept`.

### Anti-Pattern 2: std::move on Return Values (Preempting RVO)

- **Appearance:** `return std::move(local_variable);` at the end of a function.
- **Trap:** Intuition says "I want to move, not copy." The return statement already treats locals as rvalues for overload resolution and RVO eliminates the move entirely.
- **Consequence:** `std::move` here is strictly worse: (a) if RVO applied, it now does not -- a move (or copy) is forced; (b) if the type is not movable, the code may not compile or may silently copy.
- **Fix:** Simply `return local_variable;` -- no qualifier. Exceptions: returning a member of a local (e.g., `return w.widget_;`) or a parameter, where `std::move` is correct.

### Anti-Pattern 3: const T&& Misuse

- **Appearance:** `const T&&` as a function parameter or `std::move(const_obj)`.
- **Trap:** `const T&&` is a valid type in C++. It may seem like "I accept rvalues but promise not to modify them," which sounds useful.
- **Consequence:** `const T&&` almost never binds usefully. Move constructors take `T&&` (non-const), so `const T&&` resolves to the copy constructor. The parameter is practically useless -- it accepts rvalues but cannot move from them.
- **Fix:** Never write `const T&&` as a parameter type. Use `const T&` for read-only access or `T&&`/by-value for sink semantics.

---

## See Also

- [RAII and Resource Management](raii.md) -- Foundation: all move-semantics correctness depends on correct RAII destructors
- [Smart Pointer and Ownership Semantics](ownership.md) -- Choosing the right owning pointer type; `unique_ptr` is move-only

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [class.copy.elision], [class.copy.assign], [class.copy.ctor], [basic.lval] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | C.20-C.22, C.66, C.80-C.83, C.87, F.18 | verified-2026 | 2026-06 |
| R3 | C | SEI/CERT C++ | OOP51-CPP | verified-2026 | 2026-06 |
| R4 | A | Effective Modern C++ (Meyers) | Items 14, 17, 23-30 | verified-2026 | 2026-06 |
| R5 | A | A Tour of C++ 3rd ed. (Stroustrup) | Chapter 6 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
