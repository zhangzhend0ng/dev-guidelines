---
type: harness
id: "python-type-hints-mypy"
title: "Python Type Hints and mypy Checklist"
language: "python"
category: "correctness"
tier: "C"
scope: "Use Python type hints and mypy-style static checking to make interfaces explicit without fighting Python's gradual typing model"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [python, typing, mypy, correctness, static-analysis]
based_on:
  - "[C] Python Documentation"
  - "[C] mypy Documentation"
related:
  - "common/code-review/harness-driven-review.md"
  - "common/testing/testing-strategy.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Python Type Hints and mypy Checklist

**Based on:** Python typing docs ([C]) and mypy docs ([C]).
**Scope:** Applies to Python modules where static type hints support reviewability, refactoring, and AI-generated code safety.

---

## Checklist

### 1. Public Interface Types

- [ ] Function is public, exported, or cross-module -> **(C)** annotate parameters and return type. [R1]
- [ ] Function returns multiple shapes -> **(C)** use a precise union, dataclass, TypedDict, Protocol, or result object. [R1]

### 2. Avoid Unchecked Any

- [ ] Type is unknown -> **(C)** avoid silent `Any`; narrow with validation, protocol, or explicit cast near the boundary. [R2]
- [ ] Third-party library lacks types -> **(A)** isolate the untyped boundary and wrap it with typed local functions. [R2]

### 3. Optional and None Handling

- [ ] Value may be absent -> **(C)** use `Optional[T]` or `T | None` and check before use. [R1]
- [ ] AI uses `# type: ignore` -> **(C)** require reason and smallest possible scope. [R2]

### 4. Configuration

- [ ] Project uses type checking -> **(C)** commit mypy config in `pyproject.toml`, `mypy.ini`, or equivalent. [R2]
- [ ] New module is added -> **(A)** include it in the checked module set or document why excluded. [R2]

### 5. Runtime Boundary

- [ ] External input enters typed code -> **(C)** validate at runtime; type hints do not validate data. [R1]
- [ ] Deserialized JSON/dict is used -> **(C)** convert to typed structure before business logic. [R1]

---

## Decision Tree

```
Python API or module change?
  -> type public functions
  -> avoid unchecked Any
  -> handle None explicitly
  -> run type checker
  -> validate external data at runtime
```

---

## Anti-Patterns

### Anti-Pattern 1: Annotation Theater

- **Appearance:** Functions are annotated as `Any` or `dict` everywhere.
- **Trap:** It looks typed.
- **Consequence:** Review and static checks still cannot catch interface drift.
- **Fix:** Use precise collection, TypedDict, dataclass, Protocol, or domain types.

### Anti-Pattern 2: Blanket Ignore

- **Appearance:** `# type: ignore` is added to silence a difficult error.
- **Trap:** It unblocks CI.
- **Consequence:** Real interface bugs are hidden.
- **Fix:** Narrow the ignore and include a reason, or wrap the untyped boundary.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C24] Python Documentation | typing module, static typing concepts | verified-2026 | 2026-06 |
| R2 | C | [C27] mypy Documentation | configuration, Any, ignore controls | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
