---
type: harness
id: "common-naming-conventions"
title: "Naming Conventions Checklist"
language: "common"
category: "naming"
tier: "C"
scope: "Write self-documenting identifiers that communicate intent without requiring comments"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [naming, readability, conventions]
based_on:
  - "[C] ISO/IEC 29110:2018 — Naming in Software Engineering"
  - "[C] PEP 8 — Python Naming Conventions"
  - "[C] C++ Core Guidelines NL.1-NL.10"
  - "[A] Clean Code Ch.1-2 (Martin, 2008)"
  - "[A] Code Complete Ch.11 (McConnell, 2004)"
related: []
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Naming Conventions Checklist

**Based on:** ISO/IEC 29110 ([C]), PEP 8 ([C]), C++ Core Guidelines NL ([C]), Clean Code ([A]), Code Complete ([A]).
**Scope:** Identifiers that communicate intent. Language-agnostic; language harnesses cover ecosystem case conventions.

---

## Concepts

| Principle | Rule |
|-----------|------|
| Intent-revealing | Name answers "what does this do?" |
| Scope drives length | 1-2 chars loops; 8-20 locals; longer globals |
| No type encoding | No Hungarian: `strName`, `iCount` |
| Booleans as questions | `isEmpty`, `hasToken`, `isDone` |

---

## Checklist

### 1. Intent-Revealing  **(A)** [R4]

- [ ] Identifier communicates purpose without a comment → **(A)** [R4]
- [ ] Not `d`/`theList` but `elapsedDays`/`activeCustomers` → **(A)** [R4]

### 2. Scope Proportional Length  **(A)** [R5]

- [ ] Loop counters: 1-2 chars → **(A)** [R5]
- [ ] Locals: 8-20 chars, descriptive → **(A)** [R5]
- [ ] Public/global: longer, unambiguous → **(A)** [R5]

### 3. No Type Encoding  **(C)** [R2][R3]

- [ ] No `strName`, `iCount`, `m_member` → **(C)** [R3]
- [ ] No type prefix/suffix in identifier → **(C)** [R2]

### 4. Boolean Question Form  **(A)** [R5]

- [ ] `isEmpty`, `hasValue`, `isDone` → **(A)** [R5]
- [ ] Avoid negated: `isEnabled` over `isNotDisabled` → **(A)** [R5]

### 5. Avoid Disinformation  **(A)** [R4]

- [ ] No ambiguous abbreviations → **(A)** [R4]
- [ ] No visually ambiguous: `O0`, `l1` → **(A)** [R4]
- [ ] Distinguish clearly: `XYZController` vs `XYZManager` → **(A)** [R4]

### 6. Case Convention  **(C)** [R1][R2][R3]

- [ ] Follow ecosystem: Python=`snake_case`, JS=`camelCase`, C#=`PascalCase` → **(C)** [R2]
- [ ] Document project convention → **(C)** [R1]
- [ ] Enforce via linter → **(C)** [R2]

### 7. Project Glossary  **(C)** [R1]

- [ ] Domain abbreviations in project glossary → **(C)** [R1]
- [ ] New abbreviations reviewed, not improvised → **(C)** [R1]

---

## Decision Tree

```
Naming:
  → Intent clear? [1]
  → Length matches scope? [2]
  → No type encoding? [3]
  → Boolean? → question form [4]
  → No ambiguous abbreviations? [5]
  → Ecosystem case convention? [6]
  → Glossary entry? [7]
```

---

## Anti-Patterns

### 1. Hungarian Notation

- **Appearance:** `strName`, `iCount`, `bFlag`.
- **Trap:** Type in the name seems like documentation.
- **Consequence:** Renaming on type change. IDEs show types. Noise without value.
- **Fix:** Remove prefix: `name`, `count`, `flag`.

### 2. Single-Letter Globals

- **Appearance:** `int x = 0;` at file scope.
- **Trap:** Short names are convenient.
- **Consequence:** Search for `x` hits hundreds. Meaning depends on reading all surrounding code.
- **Fix:** Descriptive names at any scope broader than a 5-line loop.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | ISO/IEC 29110:2018 | Section 7.3 | verified-2026 | 2026-06 |
| R2 | C | PEP 8 | Naming | verified-2026 | 2026-06 |
| R3 | C | C++ Core Guidelines | NL.1-NL.10 | verified-2026 | 2026-06 |
| R4 | A | Clean Code (Martin) | Ch.1-2 | verified-2026 | 2026-06 |
| R5 | A | Code Complete (McConnell) | Ch.11 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
