---
type: harness
id: "cpp-static-analysis"
title: "C++ Static Analysis Checklist"
language: "cpp"
category: "testing"
tier: "C"
scope: "Configure and gate C++ static analysis so warnings, clang-tidy, cppcheck, and include analysis catch defects before review"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [static-analysis, clang-tidy, cppcheck, iwyu, warnings, ci]
based_on:
  - "[C] C++ Core Guidelines"
  - "[C] SEI/CERT C++ Coding Standard"
  - "[C] LLVM clang-tidy Documentation"
  - "[A] Include What You Use Documentation"
related:
  - "common/ai/ai-assisted-cpp-development.md"
  - "cpp/testing/fuzzing.md"
  - "cpp/testing/mutation-testing.md"
  - "common/testing/testing-strategy.md"
  - "common/ci-cd/pipeline-patterns.md"
  - "cpp/build/cmake-include-hygiene.md"
  - "cpp/testing/sanitizers.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/correctness/type-safety.md"
  - "cpp/build/toolchain-and-compiler-flags.md"
  - "cpp/security/secure-coding.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Static Analysis Checklist

**Based on:** C++ Core Guidelines ([C]), SEI/CERT C++ ([C]), LLVM clang-tidy ([C]), IWYU ([A]).
**Scope:** Compiler warnings, clang-tidy, cppcheck-style analyzers, include analysis, and CI gating. Runtime sanitizers are covered separately.

---

## Concepts

| Signal | Best Use |
|--------|----------|
| Compiler warnings | Fast baseline; always-on in developer builds |
| clang-tidy | C++ Core Guidelines, bugprone, performance, readability checks |
| cppcheck / equivalent | Independent analyzer for missed paths |
| IWYU | Header dependency and transitive include control |
| Baseline suppressions | Legacy debt list with owner and expiration |

---

## Checklist

### 1. Warning Baseline

- [ ] New or touched C++ target -> **(C)** enable high-value warnings for the supported compilers. [R1]
- [ ] New code emits warnings -> **(C)** fail CI or block review unless there is a documented suppression. [R1][R2]
- [ ] Warning policy differs by compiler -> **(A)** document the matrix and avoid flags unsupported by target compilers. [R1]

### 2. clang-tidy Configuration

- [ ] Project uses clang-tidy -> **(C)** check in `.clang-tidy` with enabled check groups and explicit disabled noisy checks. [R1][R3]
- [ ] New checks are introduced into a legacy codebase -> **(A)** baseline existing findings and fail only new findings first. [R3]
- [ ] AI-authored C++ change -> **(C)** run relevant clang-tidy checks when available before approval. [R1][R3]

### 3. Include Analysis

- [ ] Header changes or include churn occurs -> **(A)** run IWYU or equivalent include analysis on affected targets. [R4]
- [ ] Code relies on transitive includes -> **(C)** include directly what the file uses. [R1][R4]
- [ ] Header adds heavy dependencies -> **(A)** consider forward declarations or implementation hiding. [R4]

### 4. Security and Correctness Checks

- [ ] Analyzer reports lifetime, null dereference, bounds, integer, cast, or concurrency risk -> **(C)** map the finding to the relevant correctness/security harness. [R1][R2]
- [ ] Finding is suppressed -> **(C)** document reason, owner, date, and review deadline. [R2]
- [ ] Analyzer result conflicts with reviewer intuition -> **(A)** prefer reproducing or minimizing the case before dismissal. [R2][R3]

### 5. CI Integration

- [ ] Static analysis is part of release or merge gates -> **(C)** run it in CI with stable versions and archived output. [R3]
- [ ] Static analysis is too slow for every PR -> **(A)** run changed-file checks per PR and full checks nightly. [R3]
- [ ] Tool versions float -> **(A)** pin versions or record analyzer version in CI output. [R3]

### 6. Human Work Reduction

- [ ] Static analysis output is large -> **(A)** report only new, changed, or blocking findings in review summaries. [R3]
- [ ] Weak AI model is used -> **(A)** require it to summarize analyzer findings by file, rule, and fix action; no raw log dumps. [R3]

---

## Decision Tree

```
C++ change?
  -> Compile warnings clean
  -> Run clang-tidy / configured analyzer
  -> Include analysis if headers changed
  -> Map findings to harnesses
  -> Suppress only with owner + expiry
```

---

## Anti-Patterns

### Anti-Pattern 1: Warning Flood

- **Appearance:** CI prints thousands of legacy warnings.
- **Trap:** "At least we are running analysis."
- **Consequence:** Reviewers ignore real new defects.
- **Fix:** Baseline legacy findings and fail only new or touched-code findings first.

### Anti-Pattern 2: Suppression Without Expiry

- **Appearance:** `NOLINT` comments with no reason.
- **Trap:** It unblocks the build quickly.
- **Consequence:** Suppressions become permanent blind spots.
- **Fix:** Add reason, owner, date, and review deadline.

---

## See Also

- [AI-Assisted C++ Development](../../common/ai/ai-assisted-cpp-development.md) - requires external verification for AI-authored C++ changes
- [Testing Strategy](../../common/testing/testing-strategy.md) - places static analysis in the verification strategy
- [CI/CD Pipeline Patterns](../../common/ci-cd/pipeline-patterns.md) - automates analysis gates
- [C++ Build System and Include Hygiene](../build/cmake-include-hygiene.md) - target and include structure
- [Sanitizer Integration and Usage](sanitizers.md) - runtime defect detection
- [Undefined Behavior Prevention](../correctness/undefined-behavior.md) - maps many analyzer findings to C++ UB
- [Type Safety and Implicit Conversions](../correctness/type-safety.md) - conversion and cast findings

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C1] C++ Core Guidelines | General, Type, ES, SF profiles | verified-2026 | 2026-06 |
| R2 | C | [C2] SEI/CERT C++ Coding Standard | Secure C++ rules | verified-2026 | 2026-06 |
| R3 | C | LLVM clang-tidy Documentation | Checks and CI usage | verified-2026 | 2026-06 |
| R4 | A | Include What You Use Documentation | Include analysis | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
