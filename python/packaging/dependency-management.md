---
type: harness
id: "python-packaging-dependency-management"
title: "Python Packaging and Dependency Management Checklist"
language: "python"
category: "dependencies"
tier: "C"
scope: "Manage Python project metadata, dependency declarations, lockfiles, build backends, and package installation boundaries"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [python, packaging, dependencies, pyproject, lockfile]
based_on:
  - "[C] Python Packaging User Guide"
  - "[C] Python Documentation"
  - "[C] NIST SP 800-218 SSDF"
related:
  - "common/dependencies/dependency-management.md"
  - "common/ci-cd/pipeline-patterns.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Python Packaging and Dependency Management Checklist

**Based on:** Python Packaging User Guide ([C]), Python docs ([C]), NIST SSDF ([C]).
**Scope:** Applies to Python applications, libraries, CLIs, and automation scripts that declare or install dependencies.

---

## Checklist

### 1. Project Metadata

- [ ] Project is packaged or installed -> **(C)** declare metadata in `pyproject.toml`; do not rely on ad hoc setup commands. [R1]
- [ ] Build backend is used -> **(C)** declare it under `[build-system]` with explicit requirements. [R1]

### 2. Dependency Boundaries

- [ ] Runtime dependency is needed -> **(C)** declare it separately from dev/test dependencies. [R1]
- [ ] Optional feature dependency exists -> **(C)** expose it as an optional extra instead of forcing all users to install it. [R1]
- [ ] Dependency is only used for tooling -> **(A)** keep it out of runtime metadata. [R1]

### 3. Reproducible Installs

- [ ] Application or CI install must be reproducible -> **(C)** use a lockfile or pinned constraints and commit it. [R3]
- [ ] Library publishes broad compatibility -> **(A)** declare supported version ranges but test against the range in CI. [R1][R3]

### 4. Environment Isolation

- [ ] Installing project dependencies -> **(C)** use a virtual environment or isolated build environment. [R2]
- [ ] AI proposes global `pip install` -> **(A)** reject unless the task explicitly targets a disposable environment. [R2]

### 5. Supply-Chain Review

- [ ] New dependency is added -> **(C)** review license, maintenance status, transitive footprint, and vulnerability scan result. [R3]
- [ ] Dependency is imported for a small helper -> **(A)** prefer a local implementation when simpler and testable. [R3]

---

## Decision Tree

```
Python dependency change?
  -> pyproject metadata
  -> separate runtime/dev/optional deps
  -> lock or constraints for apps/CI
  -> isolated environment
  -> supply-chain review
```

---

## Anti-Patterns

### Anti-Pattern 1: Floating Tool Installs

- **Appearance:** CI runs `pip install tool` with no version or constraints.
- **Trap:** It is quick to write.
- **Consequence:** CI can break without a source change.
- **Fix:** Pin through lockfile, constraints, or tool-specific lock support.

### Anti-Pattern 2: Runtime Dependency Bloat

- **Appearance:** Test, lint, docs, and optional integration libraries are all runtime dependencies.
- **Trap:** One dependency list is easier to maintain.
- **Consequence:** Users install a larger attack surface and slower environment.
- **Fix:** Split runtime, dev, test, docs, and optional extras.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C25] Python Packaging User Guide | pyproject.toml, dependencies, optional dependencies | verified-2026 | 2026-06 |
| R2 | C | [C24] Python Documentation | venv, packaging and installation | verified-2026 | 2026-06 |
| R3 | C | [C6] NIST SP 800-218 SSDF | PS.2, PW.4, RV.1 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
