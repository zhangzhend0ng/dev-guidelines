---
type: harness
id: "cpp-template-best-practices"
title: "Template Best Practices and Concepts Checklist"
language: "cpp"
category: "templates"
tier: "N"
scope: "Write constrained, readable templates using C++20 Concepts and minimize instantiation bloat"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [templates, concepts, cpp20, generics]
based_on:
  - "[N] ISO C++ [temp], [temp.concept]"
  - "[C] C++ Core Guidelines T.1-T.84"
  - "[A] C++ Templates: The Complete Guide 2/e (Vandevoorde et al., 2017)"
  - "[A] Effective Modern C++ Items 1, 2, 9, 33 (Meyers)"
related: []
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Template Best Practices and Concepts Checklist

**Based on:** ISO C++ [temp]/[temp.concept] ([N]), C++ Core Guidelines T ([C]), C++ Templates 2/e ([A]), Effective Modern C++ ([A]).
**Scope:** Modern C++ template design: C++20 Concepts, `if constexpr`, bloat minimization.

---

## Concepts

| Feature | Use When |
|---------|----------|
| `concept` (C++20) | Constrain template parameters; replaces SFINAE |
| `requires` | Inline constraint |
| `if constexpr` | Compile-time branching in template body |
| Non-template base | Factor type-independent logic out |

---

## Checklist

### 1. Concepts Over SFINAE  **(C)** [R1][R2]

- [ ] C++20: `concept` to constrain templates → **(C)** [R1]
- [ ] `requires` clause for inline constraints → **(C)** [R1]
- [ ] SFINAE only pre-C++20 → **(A)** [R3]

### 2. Readable Error Messages  **(C)** [R2]

- [ ] Concept name communicates constraint: `Sortable`, `Hashable` → **(C)** [R2]
- [ ] Failed constraint → readable error at constraint boundary → **(C)** [R1]

### 3. Minimize Bloat  **(C)** [R2][R3]

- [ ] Non-template base for type-independent logic → **(C)** [R2]
- [ ] `if constexpr` over full specialization → **(C)** [R2]
- [ ] Explicit instantiation in `.cpp` for known types → **(A)** [R3]

### 4. `if constexpr`  **(C)** [R1]

- [ ] Over tag dispatch/SFINAE for compile-time branches → **(C)** [R1]
- [ ] Discarded branch checked but not instantiated → **(C)** [R1]

### 5. Auto Return Deduction  **(C)** [R2][R4]

- [ ] `auto` return where return follows from implementation → **(C)** [R2]
- [ ] Document return type contract → **(C)** [R2]
- [ ] `decltype(auto)` only for perfect-forwarding → **(A)** [R4]

### 6. ODR Compliance  **(N)** [R1]

- [ ] Template definitions in headers → **(N)** [R1]
- [ ] Full specializations: declare in header, define in one `.cpp` → **(C)** [R1]

### 7. Variadic Hygiene  **(C)** [R2][R3]

- [ ] Fold expressions (C++17) over recursive unpacking → **(C)** [R2]
- [ ] `sizeof...(Args)` for variadic count → **(C)** [R2]

---

## Decision Tree

```
Template?
  → Constraint? → concept [1]
  → Error readability? → named concepts [2]
  → Bloat? → non-template base + explicit instantiation [3]
  → Compile-time branch? → if constexpr [4]
  → Return type? → auto [5]
  → ODR? → header definition [6]
  → Variadic? → fold expression [7]
```

---

## Anti-Patterns

### 1. SFINAE Spaghetti

- **Appearance:** `std::enable_if` chains + `decltype` + `std::declval`.
- **Trap:** Worked pre-C++20; lots of examples.
- **Consequence:** Error messages are pages of overload resolution. Intent buried.
- **Fix:** C++20 `concept` + `requires`. Pre-C++20: named alias with `enable_if_t`.

### 2. Full Specialization Bloat

- **Appearance:** Full specialization for every type variant.
- **Trap:** Clean per-type handling.
- **Consequence:** Binary explosion. Compile time degrades per specialization.
- **Fix:** Non-template base + `if constexpr` per-type branches.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ | [temp], [temp.concept] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | T.1-T.84 | verified-2026 | 2026-06 |
| R3 | A | C++ Templates 2/e | Full text | verified-2026 | 2026-06 |
| R4 | A | Effective Modern C++ | Items 1,2,9,33 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
