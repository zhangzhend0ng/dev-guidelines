---
type: harness
id: "cpp-abi-compatibility"
title: "C++ ABI Compatibility Checklist"
language: "cpp"
category: "api"
tier: "C"
scope: "Preserve binary compatibility for C++ libraries across releases, compiler settings, symbol visibility, public headers, and exported interfaces"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [abi, api, binary-compatibility, shared-library, symbol-visibility]
based_on:
  - "[C] C++ Core Guidelines"
  - "[C] Itanium C++ ABI"
  - "[A] GCC/Clang/MSVC visibility and ABI documentation"
  - "[A] Large-Scale C++ Vol. I"
related:
  - "cpp/build/toolchain-and-compiler-flags.md"
  - "cpp/correctness/interface-contracts.md"
  - "cpp/correctness/class-hierarchies.md"
  - "cpp/memory/ownership.md"
  - "cpp/design/feature-design-prerequisites.md"
  - "cpp/architecture/module-boundaries.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ ABI Compatibility Checklist

**Based on:** C++ Core Guidelines ([C]), Itanium C++ ABI ([C]), compiler ABI/visibility docs ([A]), Large-Scale C++ ([A]).
**Scope:** Applies to published C++ libraries where downstream users may link without recompiling.

---

## Checklist

### 1. ABI Surface Identification

- [ ] Library exposes headers, shared objects, plugins, or C++ interfaces to external consumers -> **(C)** define the ABI surface before release. [R1][R2]
- [ ] ABI surface is unclear -> **(A)** treat all exported symbols and public headers as ABI until proven otherwise. [R3]

### 2. Layout-Stable Types

- [ ] Public class layout changes -> **(C)** treat as ABI breaking unless the type is header-only and all consumers rebuild. [R2][R3]
- [ ] Public data members, virtual functions, base classes, or inline functions change -> **(C)** require ABI review. [R2][R3]
- [ ] Long-lived ABI required -> **(A)** use pimpl, opaque handles, or C-compatible boundaries where appropriate. [R4]

### 3. Symbol Visibility

- [ ] Building shared libraries -> **(C)** explicitly control exported symbols. [R3]
- [ ] Internal symbols are exported -> **(A)** hide them by default and export only the documented API. [R3]
- [ ] Visibility differs by compiler/platform -> **(A)** document macros and CI matrix behavior. [R3]

### 4. Toolchain Consistency

- [ ] Compiler, standard library, runtime, exception model, RTTI, or build flags change -> **(C)** run ABI compatibility checks or require downstream rebuild. [R2][R3]
- [ ] Public API uses STL types across binary boundaries -> **(A)** document compiler/runtime compatibility requirements. [R3]

### 5. Release Gate

- [ ] ABI promise exists -> **(C)** compare exported symbols and public headers against the previous release. [R2][R3]
- [ ] ABI break is intentional -> **(C)** bump major version or document required rebuild. [R1][R4]

---

## Decision Tree

```
Published C++ library?
  -> Identify ABI surface
  -> Check layout/symbol/toolchain changes
  -> Run ABI comparison or require rebuild
  -> Version and document breakage
```

---

## Anti-Patterns

### Anti-Pattern 1: Header Change Assumed Source-Only

- **Appearance:** Public class changes are treated as source compatibility only.
- **Trap:** The code still compiles when rebuilt.
- **Consequence:** Existing binaries crash or misbehave.
- **Fix:** Review ABI for layout, vtable, inline, and symbol changes.

### Anti-Pattern 2: Export Everything

- **Appearance:** All symbols are visible from a shared library.
- **Trap:** It avoids writing export macros.
- **Consequence:** Accidental ABI surface becomes permanent.
- **Fix:** Hide by default and export the documented API.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C1] C++ Core Guidelines | Interface design and encapsulation | verified-2026 | 2026-06 |
| R2 | C | Itanium C++ ABI | Object layout, vtables, name mangling | verified-2026 | 2026-06 |
| R3 | A | GCC/Clang/MSVC Documentation | ABI and symbol visibility | verified-2026 | 2026-06 |
| R4 | A | Large-Scale C++ Vol. I | Physical design and binary boundaries | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
