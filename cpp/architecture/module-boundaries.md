---
type: harness
id: "cpp-module-boundaries"
title: "C++ Module Boundaries Checklist"
language: "cpp"
category: "architecture"
tier: "C"
scope: "Control C++ subsystem boundaries, dependency direction, public headers, internal APIs, and compile-time coupling"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [architecture, module-boundaries, dependencies, headers, layering]
based_on:
  - "[C] C++ Core Guidelines"
  - "[A] Large-Scale C++ Vol. I"
  - "[A] Lakos physical design principles"
related:
  - "cpp/build/cmake-include-hygiene.md"
  - "cpp/correctness/interface-contracts.md"
  - "cpp/api/abi-compatibility.md"
  - "common/api-design/restful-api-design.md"
  - "cpp/architecture/layering-and-dependency-inversion.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Module Boundaries Checklist

**Based on:** C++ Core Guidelines ([C]), Large-Scale C++ ([A]), physical design principles ([A]).
**Scope:** Applies to packages, libraries, subsystems, and public/internal header boundaries in C++ codebases.

---

## Checklist

### 1. Boundary Definition

- [ ] New subsystem, library, or package is introduced -> **(C)** define public API, internal API, ownership, and allowed dependencies. [R1]
- [ ] Boundary is unclear -> **(A)** document consumers and non-consumers before adding dependencies. [R2]

### 2. Dependency Direction

- [ ] Lower-level module depends on higher-level module -> **(C)** invert dependency or extract an interface. [R1][R2]
- [ ] Circular dependency appears -> **(C)** break the cycle before adding more code. [R2]

### 3. Header Discipline

- [ ] Public header includes internal details -> **(A)** hide implementation through forward declarations, pimpl, or private headers. [R2]
- [ ] Header change triggers broad rebuilds -> **(A)** reduce include fan-out and move implementation to `.cpp`. [R2]

### 4. API Stability

- [ ] Module is consumed outside its owning team/package -> **(C)** apply interface-contract and ABI compatibility harnesses. [R1]
- [ ] Internal API leaks into external use -> **(A)** rename, relocate, or mark as internal before consumers depend on it. [R2]

### 5. Build Enforcement

- [ ] Dependency rules are important -> **(A)** enforce with build targets, include paths, or dependency checks. [R2]
- [ ] AI proposes cross-layer include or dependency -> **(A)** reject unless the boundary rules allow it. [R1][R2]

---

## Decision Tree

```
New dependency or header exposure?
  -> Is boundary public/internal?
  -> Is dependency direction allowed?
  -> Does it increase rebuild/ABI surface?
  -> Enforce in build targets
```

---

## Anti-Patterns

### Anti-Pattern 1: Convenience Include

- **Appearance:** A low-level header includes a high-level subsystem for one helper.
- **Trap:** It is faster than extracting an interface.
- **Consequence:** Layering breaks and rebuilds spread.
- **Fix:** Move helper down, extract interface, or pass dependency in.

### Anti-Pattern 2: Internal API by Accident

- **Appearance:** Consumers include `detail/` headers because they are reachable.
- **Trap:** It works and avoids new API design.
- **Consequence:** Internal implementation becomes a de facto contract.
- **Fix:** Hide internal includes and expose a deliberate API.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C1] C++ Core Guidelines | Interfaces and source organization | verified-2026 | 2026-06 |
| R2 | A | Large-Scale C++ Vol. I | Physical design, packages, dependencies | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
