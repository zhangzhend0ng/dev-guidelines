---
type: harness
id: "cpp-toolchain-compiler-flags"
title: "C++ Toolchain and Compiler Flags Checklist"
language: "cpp"
category: "build"
tier: "C"
scope: "Define supported C++ standards, compiler matrix, build types, warning policies, and diagnostic flags for reproducible C++ builds"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [toolchain, compiler-flags, cmake, warnings, cxx-standard, build-types]
based_on:
  - "[N] ISO C++"
  - "[C] C++ Core Guidelines"
  - "[C] CMake Documentation"
  - "[A] GCC, Clang, and MSVC compiler documentation"
related:
  - "cpp/api/abi-compatibility.md"
  - "cpp/build/cmake-include-hygiene.md"
  - "cpp/build/package-management.md"
  - "cpp/testing/static-analysis.md"
  - "cpp/testing/sanitizers.md"
  - "cpp/runtime/observability-and-diagnostics.md"
  - "common/ci-cd/pipeline-patterns.md"
  - "cpp/third-party/wxwidgets-3-1-5.md"
  - "cpp/debugging/crash-dump-analysis.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Toolchain and Compiler Flags Checklist

**Based on:** ISO C++ ([N]), C++ Core Guidelines ([C]), CMake docs ([C]), compiler documentation ([A]).
**Scope:** Supported standard version, compiler matrix, CMake build types, warning flags, debug/release diagnostics, and reproducible local/CI toolchains.

---

## Checklist

### 1. C++ Standard Version

- [ ] Project uses modern C++ -> **(N)** declare the required C++ standard in build configuration. [R1][R3]
- [ ] Library exposes public headers -> **(C)** document the minimum supported standard for consumers. [R2]
- [ ] AI suggests newer language features -> **(C)** verify the configured standard and compiler support before accepting. [R2][R4]

### 2. Compiler Matrix

- [ ] Project supports multiple platforms -> **(C)** document supported compiler families and minimum versions. [R3][R4]
- [ ] CI has fewer compilers than support policy -> **(A)** mark missing compilers as NOT VERIFIED in release evidence. [R3]
- [ ] Compiler-specific flags are used -> **(C)** guard them by compiler ID/version in CMake. [R3][R4]

### 3. Warning Policy

- [ ] New code is built -> **(C)** enable a strict warning baseline for each supported compiler. [R2][R4]
- [ ] Warnings are promoted to errors -> **(A)** apply to project code; avoid breaking on third-party headers. [R3]
- [ ] Warning exceptions exist -> **(A)** document why and revisit periodically. [R2]

### 4. Build Types

- [ ] Debug builds -> **(C)** include symbols and diagnostics suitable for tests and sanitizers. [R3][R4]
- [ ] Release builds -> **(C)** avoid diagnostic-only flags that change ABI or runtime behavior unexpectedly. [R3][R4]
- [ ] RelWithDebInfo or equivalent exists -> **(A)** provide a production-like debugging build. [R3]

### 5. Diagnostic Presets

- [ ] Sanitizer, static-analysis, or coverage builds exist -> **(C)** define named presets or documented commands. [R3]
- [ ] Diagnostics are too expensive for every PR -> **(A)** run narrow PR checks and full scheduled checks. [R3]
- [ ] Diagnostic output is consumed by weak AI models -> **(A)** summarize failures by file/rule/action; do not dump full logs. [R3]

### 6. Reproducibility

- [ ] Toolchain version affects generated code or ABI -> **(C)** pin, document, or containerize the toolchain. [R3][R4]
- [ ] Local and CI builds differ -> **(C)** document the differences and keep CI as the release gate. [R3]
- [ ] Package manager or compiler is upgraded -> **(C)** rerun build, tests, static analysis, and relevant sanitizers. [R3]

---

## Decision Tree

```
Changing build/toolchain?
  -> Check C++ standard
  -> Check compiler matrix
  -> Apply warning policy
  -> Pick build type/preset
  -> Run CI-equivalent verification
```

---

## Anti-Patterns

### Anti-Pattern 1: Works on My Compiler

- **Appearance:** Code uses a compiler extension or newer standard feature without policy.
- **Trap:** It compiles locally.
- **Consequence:** CI or downstream users fail.
- **Fix:** Declare standard, compiler matrix, and guarded flags.

### Anti-Pattern 2: Global Flag Drift

- **Appearance:** Flags are appended to global variables in multiple CMake files.
- **Trap:** It is quick.
- **Consequence:** Targets receive unintended flags and third-party builds break.
- **Fix:** Prefer target-scoped flags and named presets.

---

## See Also

- [C++ Build System and Include Hygiene](cmake-include-hygiene.md) - target-based CMake and include discipline
- [C++ Package Management](package-management.md) - dependency/toolchain reproducibility
- [C++ Static Analysis](../testing/static-analysis.md) - warning and analyzer gates
- [Sanitizer Integration and Usage](../testing/sanitizers.md) - diagnostic build presets
- [CI/CD Pipeline Patterns](../../common/ci-cd/pipeline-patterns.md) - CI matrix and release gates

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | [N1] ISO C++ Standard | Language standard selection | verified-2026 | 2026-06 |
| R2 | C | [C1] C++ Core Guidelines | Build and source guidance | verified-2026 | 2026-06 |
| R3 | C | CMake Documentation | CXX_STANDARD, presets, compiler IDs | verified-2026 | 2026-06 |
| R4 | A | GCC/Clang/MSVC Documentation | Warning and diagnostic flags | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
