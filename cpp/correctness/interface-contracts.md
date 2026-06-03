---
type: harness
id: "cpp-interface-contracts"
title: "Interface Contracts and Design-by-Contract Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Design C++ interfaces with clear contracts: abstract base classes, precondition/postcondition boundaries, interface segregation, narrow/wide contracts, Liskov substitution, NVI, and noexcept commitments"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [interface-contracts, design-by-contract, abstract-base-class, lsp, nvi, noexcept, precondition, postcondition, interface-segregation]
based_on:
  - "[N] ISO C++ [class.abstract], [class.virtual]"
  - "[C] C++ Core Guidelines I.1-I.30"
  - "[C] Bloomberg BDE — Contracts and Defensive Programming"
  - "[A] Effective C++ Items 32-36 (Meyers)"
related:
  - "cpp/correctness/class-hierarchies.md"
  - "cpp/functions/parameter-validation.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Interface Contracts and Design-by-Contract Checklist

**Based on:** ISO C++ ([N]), C++ Core Guidelines ([C]), Bloomberg BDE Contracts ([A]), Effective C++ Items 32-36 ([A]).
**Scope:** Design C++ interfaces that communicate intent, enforce invariants, and respect substitutability. This harness covers the contractual design of interfaces -- what callers and callees promise each other. For mechanical virtual-dispatch correctness (destructors, slicing, override/final), see the Class Hierarchies harness.

---

## Concepts

| Concept | Principle |
|---------|-----------|
| Abstract base class (ABC) | Pure virtual functions, no data members -- defines a contract, not storage |
| Precondition | What must be true before the call -- caller's obligation |
| Postcondition | What is guaranteed after the call -- callee's obligation |
| Narrow contract | Precondition exists; caller must satisfy it; undefined behavior if violated |
| Wide contract | No precondition beyond type system; every input has defined behavior |
| Interface segregation | Many small, focused interfaces over one fat interface |
| Liskov Substitution (LSP) | Derived must be usable wherever Base is expected -- preconditions cannot strengthen, postconditions cannot weaken |
| NVI (Non-Virtual Interface) | Public non-virtual wrapper enforces invariants; private virtual `do_*` implements behavior |
| noexcept contract | A commitment that this function will not throw -- changing it breaks callers |

---

## Checklist

### 1. Abstract Base Classes as Interfaces **(N)** [R1][R2]

Use a pure-virtual class with no data members as the canonical way to define a C++ interface contract.

- [ ] The class contains only pure virtual functions (`= 0`) and a virtual destructor → **(N)** [R1]
- [ ] The class holds zero data members -- it defines a contract, not storage → **(N)** [R1][R2]
- [ ] The destructor is `virtual` and either `= default` or has an empty out-of-line body → **(N)** [R1]
- [ ] Constructors are `protected` (or `= default` public is acceptable for stateless interfaces) → **(C)** [R2]
- [ ] If the ABC has a pure virtual destructor, it MUST have an out-of-line empty body (`Base::~Base() {}`) -- otherwise linking fails → **(N)** [R1]
- [ ] Concrete base classes (with data + virtual) are NOT used as interface definitions -- separate interface from implementation inheritance → **(C)** [R2]

### 2. Precondition and Postcondition Documentation **(C)** [R2][R3]

Every non-trivial function documents its contract explicitly. The mechanism varies by maturity of tooling.

- [ ] Preconditions are documented in prose at minimum (doxygen `\pre` / `@pre`) → **(C)** [R2]
- [ ] Postconditions are documented (`\post` / `@post`) for non-obvious guarantees → **(C)** [R2]
- [ ] Where GSL is used: `Expects(cond)` for preconditions, `Ensures(cond)` for postconditions → **(C)** [R2]
- [ ] C++26 contracts (proposed, P2900): `pre(cond)` / `post(cond)` — track WG21 progress → **(A)** [R2]
- [ ] Preconditions are checked at the narrowest scope possible -- at the interface boundary, not deep in implementation → **(C)** [R2]
- [ ] Postconditions that depend on `this` state are documented on the class invariants, not repeated per-method → **(A)** [R2]

### 3. Interface Segregation -- Narrow Over Fat **(C)** [R2][R4]

A client should not depend on methods it does not call. Split fat interfaces into cohesive role-based interfaces.

- [ ] An interface exposes 7 or more public pure-virtual methods → split into 2+ role interfaces → **(C)** [R2]
- [ ] A client takes a pointer/reference to an interface whose methods it only partially calls → extract the subset into a narrower interface → **(C)** [R2]
- [ ] Concrete classes implement multiple narrow interfaces rather than one fat one → **(C)** [R2]
- [ ] Interface methods are at a consistent abstraction level -- no mix of high-level (process) and low-level (setMode) in one interface → **(C)** [R2]
- [ ] If splitting is impractical (e.g., stable ABI), document which methods a given client role is expected to call → **(A)** [R2]

### 4. Narrow vs. Wide Contracts -- Caller vs. Callee Responsibility **(C)** [R2][R3]

Decide per function whether the contract is narrow (caller guarantees) or wide (callee handles everything).

- [ ] Wide contract: the function accepts all values of its parameter types and produces defined behavior → **(C)** [R2]
- [ ] Narrow contract: the function has preconditions beyond the type system (e.g., `ptr != nullptr`, `index < size`) → **(C)** [R2]
- [ ] Narrow contract: preconditions are documented and checked via `assert()` / `Expects()` in debug builds → **(C)** [R3]
- [ ] Wide contract: never `assert()` on user input -- return error or throw → **(C)** [R3]
- [ ] A function that silently returns "success" for invalid input hides bugs -- prefer a narrow contract → **(C)** [R2]
- [ ] The contract type (narrow/wide) is stable: changing narrow to wide is backward-compatible; changing wide to narrow is a breaking API change → **(C)** [R2]
- [ ] For detailed validation mechanism selection (security boundaries, public vs internal), see Parameter Validation → **(A)** Cross-reference to `cpp/functions/parameter-validation.md`

### 5. Liskov Substitution Principle (LSP) in C++ **(N)** [R1][R2][R4]

A derived class must be usable through a base class pointer/reference without the caller knowing the difference.

- [ ] Derived overrides do NOT add new preconditions (strengthening) -- e.g., base accepts any `int`, derived rejects negative values → violation → **(N)** [R1][R2]
- [ ] Derived overrides do NOT weaken postconditions -- e.g., base guarantees sorted output, derived returns unsorted → violation → **(N)** [R1][R2]
- [ ] Derived overrides maintain the base's exception specification -- a `noexcept` virtual cannot be overridden with a throwing function → **(N)** [R1]
- [ ] Derived overrides respect the base's return-type contract -- covariant return types are fine, but the returned object must satisfy the base's postconditions → **(N)** [R1]
- [ ] Derived does NOT change the semantics of an inherited non-virtual function -- prefer NVI (Item 6) to prevent this → **(C)** [R2][R4]
- [ ] If LSP violation is intentional (e.g., `Circle` is NOT substitutable for `Ellipse`), the inheritance relationship itself is wrong -- remove it, do not document it away → **(C)** [R2]

### 6. NVI (Non-Virtual Interface) Idiom **(C)** [R2][R4]

Public methods are non-virtual wrappers. Virtual dispatch is private. The wrapper enforces invariants.

- [ ] Public interface methods are declared non-virtual → **(C)** [R2]
- [ ] Virtual behavior is implemented in `private` (or `protected` when derived needs to chain) virtual methods, conventionally named `do_<operation>` → **(C)** [R2]
- [ ] The public non-virtual method is the single point for: invariant checks, lock acquisition, logging, precondition/postcondition validation → **(C)** [R2]
- [ ] Derived classes override the private `do_*`, never the public wrapper → **(C)** [R2]
- [ ] The NVI wrapper cannot be overridden, so the invariant enforcement is guaranteed regardless of derivation depth → **(C)** [R4]
- [ ] NVI is preferred over public virtual for any interface intended to be subclassed by external code → **(C)** [R2]

### 7. noexcept in Interface Contracts **(C)** [R2][R4]

A `noexcept` specifier is a contract commitment. Breaking it terminates the program. Commit carefully.

- [ ] `noexcept` on move constructors and move assignment operators (enables `std::vector` optimization) → **(C)** [R2]
- [ ] `noexcept` on `swap` (required by many generic algorithms) → **(C)** [R2]
- [ ] `noexcept` on simple accessors that cannot fail (e.g., `size()`, `empty()`, getters returning by value for primitive types) → **(C)** [R2]
- [ ] `noexcept` on destructors (implicitly noexcept since C++11; do NOT mark `noexcept(false)` except for rare, documented cases) → **(N)** [R1]
- [ ] Do NOT mark a virtual function `noexcept` unless ALL overrides (present and future) are guaranteed non-throwing → **(C)** [R2]
- [ ] If a function allocates memory, calls user-provided callbacks, or performs I/O, do NOT mark it `noexcept` -- the operation may fail → **(C)** [R2]
- [ ] Wide-contract functions (Item 4) that validate input and throw on error are NOT `noexcept` → **(C)** [R2][R3]

---

## Decision Tree

```
Interface design:
  → Defining a pure contract? → ABC: pure virtual + no data [1]
  → Non-trivial function? → document pre/post [2]
  → Interface >7 methods or clients use subset? → segregate [3]
  → All inputs have defined behavior? → wide contract
    Else → narrow contract (document + debug-check) [4]
  → Inheritance relationship? → check LSP: no stronger pre, no weaker post [5]
  → External subclassing expected? → NVI: public non-virtual → private virtual do_* [6]
  → Function can never fail? → noexcept; else leave flexible [7]
```

---

## Anti-Patterns

### 1. Fat Interface with Empty Defaults

- **Appearance:** `class IWidget { virtual void draw() = 0; virtual void serialize() = 0; virtual void validate() = 0; virtual void animate() = 0; ... };` (10+ methods). Concrete classes override 2-3 methods, the rest get empty no-op bodies.
- **Trap:** "One interface is simpler than many." Adding a default empty body to pure virtuals seems to let clients opt in selectively.
- **Consequence:** A client calling `widget->animate()` on a static-rendering widget silently does nothing. The interface lies about what is supported. Testing must cover every permutation of supported/unsupported operations.
- **Fix:** Split into `IDrawable`, `ISerializable`, `IValidatable`, `IAnimatable`. Client requests only the interfaces it needs. Use `dynamic_cast` or `std::optional<IRef>` to query capability at runtime when truly dynamic.

### 2. LSP Violation via "Documented Exception"

- **Appearance:** `class Rectangle { virtual void setWidth(int w); }; class Square : public Rectangle { void setWidth(int w) override { if (w != height) throw std::logic_error("must be square"); } };`.
- **Trap:** "The precondition is documented in the Square's header. Callers who read the docs will know." Inheritance models IS-A; Square IS-A Rectangle with an invariant the base does not have.
- **Consequence:** Code written against `Rectangle&` breaks when given a `Square&`. The exception is a runtime surprise that static typing promised would not happen. Every caller must either catch `logic_error` (defeating the purpose) or avoid `Square` (defeating inheritance).
- **Fix:** Do not model Square as a subclass of mutable Rectangle. Either make them immutable value types, or remove the inheritance and use a free function `bool is_square(const Rectangle&)`.

### 3. noexcept on Virtual Functions

- **Appearance:** `class Base { virtual void process() noexcept = 0; };`. A future derived class needs to allocate memory or call a callback that may throw.
- **Trap:** "This function should never fail in our current implementation." The `noexcept` is a contract, not an optimization hint. Virtual functions are extension points -- you cannot predict what overrides will need.
- **Consequence:** The overriding function must wrap its body in `try { ... } catch(...) { std::terminate(); }` or risk `std::terminate` on the first exception. If the author misses this, the program terminates with no recovery. Changing the base to remove `noexcept` is a breaking change -- all callers that relied on `noexcept` for optimization or `std::move_if_noexcept` behavior are affected.
- **Fix:** Leave virtual functions `noexcept`-free unless the contract absolutely requires it (e.g., destructors, swap). Use NVI: the public non-virtual can document "does not throw under these conditions" without constraining overrides with a `noexcept` specifier.

---

## See Also

- [Class Hierarchies and Virtual Dispatch](class-hierarchies.md) -- Mechanical correctness: virtual destructors, override/final, slicing, downcasting. Apply both harnesses: this one for design, that one for mechanics.
- [Parameter Validation](../functions/parameter-validation.md) -- Narrow vs. wide contract validation mechanism selection (assert vs. if+throw vs. type system). This harness decides the contract; that harness implements it.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [class.abstract], [class.virtual] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | I.1-I.30 | verified-2026 | 2026-06 |
| R3 | C | Bloomberg BDE | Contracts and Defensive Programming | verified-2026 | 2026-06 |
| R4 | A | Effective C++ (Meyers) | Items 32-36 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft -- 7 items covering abstract base classes, pre/post conditions, interface segregation, narrow/wide contracts, LSP, NVI, and noexcept contracts
