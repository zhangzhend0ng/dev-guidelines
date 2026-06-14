---
type: harness
id: "cpp-class-hierarchies"
title: "Class Hierarchies and Virtual Dispatch Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Ensure correct virtual dispatch, safe inheritance design, and prevention of slicing, dangling, and diamond issues in C++ class hierarchies"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [class-hierarchies, virtual, polymorphism, inheritance, slicing, downcasting, nvi, abstract-base, multiple-inheritance]
based_on:
  - "[N] ISO C++ [class], [class.derived], [class.virtual], [class.abstract], [class.slice]"
  - "[C] C++ Core Guidelines C.1-C.168, C.35, C.121-C.139"
  - "[C] SEI/CERT OOP50-OOP58"
  - "[A] Effective C++ Items 7, 9, 20, 32-40 (Meyers)"
  - "[A] Effective Modern C++ Items 7-9 (Meyers)"
related:
  - "cpp/api/abi-compatibility.md"
  - "cpp/correctness/interface-contracts.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/lifetime/dangling-references.md"
  - "cpp/memory/raii.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Class Hierarchies and Virtual Dispatch Checklist

**Based on:** ISO C++ ([N]), C++ Core Guidelines ([C]), SEI/CERT ([C]), Effective C++/Modern C++ ([A]).
**Scope:** Prevent slicing, dangling references to polymorphic objects, incorrect virtual dispatch, unsafe downcasting, and diamond inheritance bugs.

---

## Concepts

| Hazard | Safe Alternative |
|--------|-----------------|
| Non-virtual base destructor | `virtual ~Base() = default;` |
| Unmarked override | `override` on every virtual override |
| Pass-by-value polymorphic | Pass by `const&` or pointer; delete copy in base |
| C-style downcast | `dynamic_cast<T*>(ptr)` + null check |
| Public virtual interface | NVI: public non-virtual calls private virtual |
| Concrete "interface" base | Pure virtual destructor with empty body |
| Diamond MI with duplication | `virtual` base class inheritance |

---

## Checklist

### 1. Virtual Destructors in Polymorphic Bases **(N)** [R1][R2][R4]

- [ ] Every base class with virtual functions declares a `virtual` destructor → **(N)** [R1][R2]
- [ ] Destructor is either `= default` (preferred) or has an empty body → **(N)** [R1]
- [ ] Destructor is `public virtual` for bases deleted through base pointers, or `protected` (non-virtual) if deletion through base is forbidden → **(C)** [R2]
- [ ] `delete` through base pointer without `virtual ~Base()` → undefined behavior; fix immediately → **(N)** [R1]

### 2. override and final **(C)** [R2][R4]

- [ ] Every virtual function override in a derived class is marked `override` → **(C)** [R2]
- [ ] `final` on a class when no further derivation is intended (leaf class) → **(C)** [R2]
- [ ] `final` on a virtual method when overriding must stop at this level → **(C)** [R2]
- [ ] `override` and `final` are mutually exclusive in intent but can be combined (`override final`) when both apply → **(A)** [R2]

### 3. Slicing Prevention **(N)** [R1][R2]

- [ ] Polymorphic types are never passed by value — use `const T&` or `T*` → **(N)** [R1]
- [ ] Copy constructor and copy assignment are `= delete` in polymorphic base classes, or a virtual `clone()` method is provided instead → **(C)** [R2]
- [ ] Containers of polymorphic objects store `std::unique_ptr<Base>`, never `std::vector<Base>` → **(N)** [R1][R2]
- [ ] `auto x = someFuncReturningDerived();` — verify `x` has the intended type, not the sliced base → **(C)** [R2]

### 4. Downcasting Safety **(C)** [R2][R3][R4]

- [ ] Pointer downcasts use `dynamic_cast<Derived*>(basePtr)` → **(C)** [R2]
- [ ] Result of pointer `dynamic_cast` is null-checked before dereference → **(N)** [R1][R2]
- [ ] Reference downcasts use `dynamic_cast<Derived&>(baseRef)` and catch `std::bad_cast` → **(C)** [R2]
- [ ] `static_cast` downcast is used only when the dynamic type is provably known (e.g., CRTP, visitor pattern with known type) → **(C)** [R2]
- [ ] Prefer `std::variant` + `std::visit` over manual downcasting when the set of types is known and closed → **(A)** [R2]

### 5. Pure Virtual vs. Default Implementation **(C)** [R2][R4]

- [ ] Pure virtual functions (`= 0`) are used when every derived class must provide its own implementation → **(C)** [R2]
- [ ] Pure virtual with a body is provided when a default behavior exists but derived classes must explicitly opt-in → **(C)** [R2]
- [ ] Non-pure virtual with a default body is used when derived classes may override but are not required to → **(C)** [R2]
- [ ] Do not call pure virtual functions from constructors or destructors — results in undefined behavior → **(N)** [R1][R2]

### 6. NVI (Non-Virtual Interface) Idiom **(C)** [R2][R4]

- [ ] Public interface methods are non-virtual → **(C)** [R2]
- [ ] Virtual dispatch is delegated to private (or protected) virtual methods → **(C)** [R2]
- [ ] Pre- and post-condition checks (e.g., invariants, locking) live in the public non-virtual wrapper → **(C)** [R2]
- [ ] Override the private virtual `do_*` method, not the public non-virtual → **(C)** [R2]

### 7. Abstract Base Classes **(N)** [R1][R2]

- [ ] A class with at least one pure virtual function is abstract and cannot be instantiated → **(N)** [R1]
- [ ] Pure virtual destructor MUST have a body (`Base::~Base() {}`) — otherwise linkage errors at destruction of derived objects → **(N)** [R1]
- [ ] Abstract base classes hold no data members (pure interface) or minimal shared state only → **(C)** [R2]
- [ ] Abstract base constructors are `protected` to reinforce non-instantiability → **(C)** [R2]

### 8. Multiple Inheritance **(C)** [R2][R4]

- [ ] Multiple inheritance is used only for interface classes (pure virtual, no data) — avoid MI with stateful bases → **(C)** [R2]
- [ ] Diamond hierarchy uses `virtual` inheritance from the common base → **(C)** [R2]
- [ ] Most-derived class is responsible for initializing the virtual base → **(C)** [R2]
- [ ] Non-virtual MI of stateful classes is flagged for design review — prefer composition → **(C)** [R2]
- [ ] `static_cast` (not `dynamic_cast`) is used when navigating within a known MI hierarchy where the relationship is unambiguous at compile time → **(A)** [R2]

### 9. Inheriting Constructors and Deleted Special Members **(C)** [R2][R5]

- [ ] `using Base::Base` is used to inherit constructors when the derived class adds no new data members requiring initialization → **(C)** [R2]
- [ ] Inherited constructors do not copy move constructors — declare move operations explicitly if needed → **(C)** [R2]
- [ ] When a base class deletes copy/move (e.g., `= delete`), verify derived class intent — default-generated special members respect base accessibility → **(C)** [R2]
- [ ] Destructor, copy/move assignment are not inherited and must be declared explicitly in derived if non-default behavior is needed → **(C)** [R2]

---

## Decision Tree

```
Class hierarchy safety:
  → Base class with virtual functions? → virtual destructor [1]
  → Virtual function override? → mark override [2]
  → Passing polymorphic type? → const& or pointer, never by value [3]
  → Downcasting? → dynamic_cast + null check (ptr) or catch bad_cast (ref) [4]
  → Pure virtual? → decide: body or not; never call from ctor/dtor [5]
  → Public virtual API? → NVI: public non-virtual → private virtual [6]
  → Abstract base? → pure virtual destructor with body [7]
  → Multiple inheritance? → interfaces only; virtual base for diamond [8]
  → Inheriting constructors? → using Base::Base; mind deleted special members [9]
```

---

## Anti-Patterns

### 1. Non-Virtual Base Destructor

- **Appearance:** `class Base { virtual void foo(); };` with no virtual destructor. `delete` called through `Base*`.
- **Trap:** Compiler does not warn. Code appears to work in simple cases.
- **Consequence:** Undefined behavior. Derived destructor never runs. Resource leaks, dangling state.
- **Fix:** `virtual ~Base() = default;`. If polymorphic deletion through base is not intended, document why and make destructor `protected`.

### 2. Pass-by-Value Slicing

- **Appearance:** `void process(Shape s);` where `Circle : public Shape`. Called with `Circle c; process(c);`.
- **Trap:** "It's simpler. No reference/pointer syntax." The compiler implicitly copies, but only the `Shape` sub-object survives.
- **Consequence:** Derived data sliced away. Overridden virtual functions resolve to base. Silent data loss.
- **Fix:** `void process(const Shape& s);`. If copy semantics are needed, provide `virtual std::unique_ptr<Shape> clone() const;`.

### 3. C-Style or static_cast Downcast Without Proof

- **Appearance:** `Derived* d = (Derived*)basePtr;` or `static_cast<Derived*>(basePtr)` where the dynamic type is uncertain.
- **Trap:** "I know it's always a `Derived` here." But refactoring, new callers, or edge cases invalidate the assumption.
- **Consequence:** Invalid pointer dereference. Memory corruption if the cast succeeds but the layout is wrong.
- **Fix:** `dynamic_cast<Derived*>(basePtr)` with a null check. Use `std::variant` + `std::visit` when the type set is closed.

---

## See Also

- [Undefined Behavior](undefined-behavior.md) — UB from calling pure virtual in ctor/dtor, deleting through non-virtual destructor
- [Dangling References](../lifetime/dangling-references.md) — Dangling references to polymorphic temporaries
- [RAII and Resource Management](../memory/raii.md) — Virtual destructor ensures derived resources are released

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [class], [class.derived], [class.virtual], [class.abstract], [class.slice] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | C.1-C.168, C.35, C.121-C.139 | verified-2026 | 2026-06 |
| R3 | C | SEI/CERT C++ | OOP50-OOP58 | verified-2026 | 2026-06 |
| R4 | A | Effective C++ (Meyers) | Items 7, 9, 20, 32-40 | verified-2026 | 2026-06 |
| R5 | A | Effective Modern C++ (Meyers) | Items 7-9 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft — 9 items covering virtual destructors, override/final, slicing, downcasting, pure virtual, NVI, abstract base classes, multiple inheritance, and inheriting constructors
