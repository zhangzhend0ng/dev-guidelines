---
type: harness
id: "cpp-build-system"
title: "C++ Build System and Include Hygiene Checklist"
language: "cpp"
category: "build"
tier: "C"
scope: "Maintain modern CMake targets, IWYU headers, and fast incremental builds in C++ projects"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [cmake, build, includes, iwyu, compile-time]
based_on:
  - "[C] C++ Core Guidelines SF.1-SF.11"
  - "[C] Modern CMake Best Practices (target-based design)"
  - "[A] Professional CMake (Craig Scott)"
  - "[A] Large-Scale C++ Vol. I (John Lakos, 2019)"
  - "[A] IWYU (Include What You Use)"
related: []
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Build System and Include Hygiene Checklist

**Based on:** C++ Core Guidelines SF ([C]), Modern CMake ([C]), Professional CMake ([A]), Large-Scale C++ ([A]), IWYU ([A]).
**Scope:** CMake target-based design, include hygiene, header guards, build performance.

---

## Concepts

| Practice | Principle |
|----------|-----------|
| Target-based CMake | `target_*` over global settings |
| PRIVATE/PUBLIC/INTERFACE | Correct dependency propagation |
| IWYU | Include what you directly use; no transitive reliance |
| Forward declare | Reduce header dependency chains |
| `#pragma once` | Universal; simpler than guards |

---

## Checklist

### 1. Target-Based CMake  **(C)** [R2][R3]

- [ ] `target_link_libraries(target PRIVATE dep)` over `link_libraries(dep)` → **(C)** [R2]
- [ ] `target_compile_options(target PRIVATE -Wall)` over `CMAKE_CXX_FLAGS` → **(C)** [R2]

### 2. PRIVATE/PUBLIC/INTERFACE  **(C)** [R2]

- [ ] PRIVATE: used only in `.cpp` → **(C)** [R2]
- [ ] PUBLIC: used in headers AND `.cpp` → **(C)** [R2]
- [ ] INTERFACE: header-only libs → **(C)** [R2]

### 3. Include What You Use  **(C)** [R1][R5]

- [ ] Every file includes what it directly uses → **(C)** [R1]
- [ ] No transitive include reliance → **(C)** [R1]
- [ ] IWYU tool in CI (warn) → **(A)** [R5]

### 4. Forward Declarations  **(C)** [R1][R4]

- [ ] Forward-declare in headers when only ptr/ref needed → **(C)** [R1]
- [ ] Full include in `.cpp` → **(C)** [R1]
- [ ] Reduces header dep chain → faster incremental builds → **(C)** [R4]

### 5. Header Guards  **(C)** [R1]

- [ ] `#pragma once` at top of every header → **(C)** [R1]
- [ ] Traditional `#ifndef` guards for strict ISO → **(A)** [R1]

### 6. No `using namespace` in Headers  **(N)** [R1]

- [ ] No `using namespace std;` or any `using namespace` in headers → **(N)** [R1]
- [ ] Pollutes every TU that includes the header → **(N)** [R1]

### 7. Precompiled Headers  **(A)** [R3][R4]

- [ ] PCH for stable, widely-used headers (stdlib, third-party) → **(A)** [R3]
- [ ] Do NOT put project headers in PCH → **(A)** [R3]

---

## Decision Tree

```
CMake project?
  → target-based? [1]
  → PRIVATE/PUBLIC/INTERFACE? [2]
  → Direct includes only (IWYU) [3]
  → Forward-declare in headers [4]
  → #pragma once [5]
  → No using namespace in headers [6]
  → PCH for stable libs only [7]
```

---

## Anti-Patterns

### 1. Global CMake

- **Appearance:** `include_directories(.)`, `link_libraries(pthread)`.
- **Trap:** Quick setup; one line works for everything.
- **Consequence:** All targets get same flags/libs. Cannot reason about individual deps.
- **Fix:** `target_include_directories(target PRIVATE .)`, `target_link_libraries(target PRIVATE pthread)`.

### 2. Transitive Include Reliance

- **Appearance:** Using `std::vector` without `#include <vector>`, relying on another header.
- **Trap:** Compiles today.
- **Consequence:** Upstream removes `<vector>` → downstream breaks with cryptic errors.
- **Fix:** Include what you directly use. Run IWYU periodically.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | C++ Core Guidelines | SF.1-SF.11 | verified-2026 | 2026-06 |
| R2 | C | Modern CMake | Target-based | verified-2026 | 2026-06 |
| R3 | A | Professional CMake (Scott) | Full text | verified-2026 | 2026-06 |
| R4 | A | Large-Scale C++ I (Lakos) | Physical design | verified-2026 | 2026-06 |
| R5 | A | IWYU Tool Docs | Include hygiene | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
