---
type: harness
id: "cpp-param-validation"
title: "Parameter Validation Checklist"
language: "cpp"
category: "functions"
tier: "C"
scope: "Select validation mechanism for function parameters in public and internal APIs"
version: "2026.05"
status: "draft"
stable_since: ""
last_validated: "2025-12-01"
review_cycle: "12m"
tags:
  - validation
  - parameters
  - contracts
  - security
based_on:
  - "[C] C++ Core Guidelines I.6, I.12, I.13"
  - "[C] SEI/CERT C Coding Standard API00-C"
  - "[A] Bloomberg BDE — Contracts and Defensive Programming"
related:
  - "common/security/input-validation.md"
  - "cpp/correctness/interface-contracts.md"
  - "projects/snapmaker-orca/coding-standards.md"
supersedes: []
changelog:
  - "2026.05: Migrated from root; added frontmatter per harness template"
---

# Function Design Harness — Parameter Validation Checklist

**Based on:** C++ Core Guidelines (I.6/I.12/I.13) ([C]), SEI/CERT API00-C (v2025) ([C]), ISO P1743R0 (Bloomberg BDE) ([C]).
**Scope:** Decision framework for function parameter validation — when, where, and how to check inputs.

---

## Prerequisites / Concepts

### Function Contract Types

| Contract | Definition | Who Validates |
|----------|-----------|---------------|
| **Narrow** | Function has preconditions; caller MUST satisfy them | Caller responsible; Callee uses `assert()` / `Expects()` |
| **Wide** | Accepts all legal inputs; every input has defined behavior | Callee responsible; `if` + return/throw |

**Core principle: Validation happens on exactly one side — never both, never neither.**

---

## Checklist

### 1. Security Boundary Assessment

Input from an untrusted source (network, file, user input, cross-process)?

- [ ] YES → **(C)** Callee-side `if` + return/throw validation, all build modes [R1]
- [ ] NO → Proceed to Item 2

### 2. Public API Determination

Is the function a public library/module interface (non-static, non-anonymous namespace)?

- [ ] YES → **(C)** Callee-side validation; cannot control all callers [R1]
- [ ] NO → Proceed to Item 3

### 3. Validation Cost Assessment

Are the preconditions runtime-checkable at reasonable cost (no O-complexity change)?

- [ ] YES → **(C)** Proceed to Item 4 for mechanism selection [R3]
- [ ] NO (e.g., `is_sorted()` O(log N)→O(N)) → **(C)** Do NOT check. Document as narrow contract. [R2][R3]

### 4. Validation Mechanism Selection

| Mechanism | When | Build Modes |
|-----------|------|-------------|
| `if` + return/throw | External / Public API / Recoverable errors | Always |
| `assert()` / `Expects()` | Internal boundaries; catch programmer bugs | Debug/Assert only |
| Type system (`not_null<T>`) | Compile-time provable constraints | Compile-time |

- [ ] External input or public API → **(C)** `if` + return/throw [R2]
- [ ] Internal boundary → **(C)** `assert()` / `Expects()` [R2]
- [ ] Compile-time provable → **(C)** Type system [R2]

### 5. Null/Empty Value Handling

| Parameter Type | Strategy |
|----------------|----------|
| Raw pointer (nullable) | **(C)** MUST validate before dereference [R1] |
| Reference | **(N)** Caller responsible; null ref is UB at call site |
| `std::vector` / containers | **(C)** Empty is usually valid; define behavior |
| `std::optional` | **(C)** Use `.has_value()` / `.value_or()` |

### 6. Silent Pass-through Prevention

Does the function define a "harmless" default for invalid input?

- [ ] YES → **(C)** STOP. Hides caller bugs. Use `assert()` or explicit error. [R3]
- [ ] NO → OK

### 7. Error Handling Consistency

- [ ] **(C)** Validation failure handling matches existing project patterns

---

## Quick Decision Tree

```
External/untrusted input?
  ├─ YES → [Item 1] if + return/throw, always active
  └─ NO  → Public API?
              ├─ YES → [Item 2] if + return/throw
              └─ NO  → Preconditions checkable at low cost?
                          ├─ YES → [Item 4] assert() / Expects()
                          └─ NO  → [Item 3] Narrow contract, document

All branches: [Item 6] No silent pass-through + [Item 7] Style consistency
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Double Validation

- **Appearance:** Both caller and callee validate the same precondition.
- **Trap:** Seems "defensive" — more checks feel safer.
- **Consequence:** Performance overhead, code bloat, masks real contract ownership.
- **Fix:** One responsible side per contract type. Wide → callee. Narrow → caller (+ callee assert in debug).

### Anti-Pattern 2: Validating the Uncheckable

- **Appearance:** Code verifying "range is sorted" before binary search, or "comparator is strict weak ordering" before `std::sort`.
- **Trap:** Check has same/higher complexity than the operation — feels like safety.
- **Consequence:** O(N) check before O(log N) op defeats the purpose. False confidence.
- **Fix:** Document narrow precondition. `assert()` only O(1) checks. Use type system for semantic properties.

---

## See Also

- [Input Validation (Common)](../../common/security/input-validation.md) — Security-focused input validation for all languages

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | SEI/CERT C Coding Standard | API00-C | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | I.6, I.12, I.13 | verified-2026 | 2026-05 |
| R3 | A | Bloomberg BDE | Contracts and Defensive Programming | verified-2026 | 2026-06 |

---

## Changelog

- 2026.05: Migrated from root; added frontmatter, anti-patterns, reference table per harness template
