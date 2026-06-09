---
type: harness
id: "snapmaker-orca-workflow"
title: "SnapmakerOrca PR and Workflow Standards"
language: "common"
category: "project-specific"
tier: "P"
scope: "Enforce SnapmakerOrca branch naming, commit format, PR size, and code review workflow"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-04"
review_cycle: "12m"
tags: [snapmaker-orca, git, pr, commit, workflow]
based_on:
  - "[C] SnapmakerOrca 切片部门PR规范 v2.0 (2026-06-04)"
  - "[C] Conventional Commits 1.0.0"
related:
  - "common/commits/conventional-commits.md"
  - "common/code-review/review-checklist.md"
  - "projects/snapmaker-orca/coding-standards.md"
supersedes: []
changelog:
  - "2026.06: Initial draft from 切片部门PR规范 v2.0"
---

# SnapmakerOrca PR and Workflow Standards

**Based on:** SnapmakerOrca 切片部门PR规范 v2.0 ([C]), Conventional Commits 1.0.0 ([C]).
**Scope:** Git workflow, branch naming, commit format, and code review for SnapmakerOrca.

---

## Concepts

| Aspect | Standard |
|--------|----------|
| Branch model | GitHub Flow — `main` is the only long-term branch |
| Feature branches | `prefix_functional_description` (kebab_case, no `/`) |
| Commit format | `type: description` (Conventional Commits variant) |
| PR merge | Squash and merge preferred |
| Review | ≥1 approval, CI green, no conflicts |

---

## Checklist

### 1. Branch Naming  **(P)** [R1]

| Prefix | Use | Example |
|--------|-----|---------|
| `feature_` | New feature | `feature_wipe_tower_improvements` |
| `bugfix_` | Bug fix | `bugfix_fix_support_overlap` |
| `hotfix_` | Urgent fix | `hotfix_crash_on_startup` |
| `refactor_` | Code restructuring | `refactor_simplify_gcode_generator` |
| `docs_` | Documentation | `docs_update_build_instructions` |

- [ ] Lowercase, underscores (no `/` — filesystem ambiguity on Linux/Mac) → **(P)** [R1]
- [ ] Functional description mandatory; no personal names without description → **(P)** [R1]

### 2. Branch Lifecycle  **(P)** [R1]

- [ ] Create from latest `main` → **(P)** [R1]
- [ ] Dev branches PR to feature branch; feature branch PR to `main` → **(P)** [R1]
- [ ] Sync `main` into feature weekly for 1+ month branches → **(P)** [R1]
- [ ] Delete feature branch after merge (one-phase); retain (multi-phase) → **(P)** [R1]

### 3. Branch Protection (main)  **(P)** [R1]

- [ ] Require PR; no direct push → **(P)** [R1]
- [ ] ≥1 approving review; CI green; up to date; no force push → **(P)** [R1]

### 4. Commit Format  **(P)** [R1][R2]

- [ ] `type: description` — types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert` → **(P)** [R1]
- [ ] Body (optional): bullet list (`-` or `*` OK) → **(P)** [R1]
- [ ] Atomic commits: one logical change, must compile → **(P)** [R1]

```bash
# Good
git commit -m "feat: optimize erasure tower generation algorithm"
git commit -m "fix: render module crash on null pointer"
```

### 5. PR Title  **(P)** [R1]

- [ ] Title follows commit format: `type: description` → **(P)** [R1]

### 6. PR Size  **(P)** [R1]

| Size | Lines | Files |
|------|-------|-------|
| Small | <200 | <5 |
| Medium | 200-500 | 5-10 |
| Large | 500-1000 | 10-20 |

- [ ] ≤500 lines unless split plan documented → **(P)** [R1]
- [ ] Large features split: core → integration → tests → docs → **(P)** [R1]

### 7. Merge Strategy  **(P)** [R1]

- [ ] Squash and merge preferred → **(P)** [R1]
- [ ] Pre-check: ≥1 approval, CI green, comments resolved, no conflicts → **(P)** [R1]

### 8. Code Review  **(P)** [R1]

- [ ] Comments in English on code lines → **(P)** [R1]
- [ ] `Resolve conversation` when fixed or agreed non-issue → **(P)** [R1]
- [ ] Author pre-check: compiles, tests pass, format OK, no debug code → **(P)** [R1]
- [ ] Urgent: contact reviewer directly → **(P)** [R1]

---

## Decision Tree

```
New work?
  → Branch: prefix_functional_desc from latest main [1,2]
  → Commit: type: description, atomic, compiles [4]
  → Sync main weekly (long features) [2]
  → PR: title type:desc [5], ≤500 lines [6]
  → Review: ≥1 approval, CI green, English comments [8]
  → Merge: squash [7]
  → Delete branch (one-phase) or retain (multi-phase) [2]
```

---

## Anti-Patterns

### 1. Person-Named Branches

- **Appearance:** `feature_alves` — no functional description.
- **Trap:** Quick; author knows what it means.
- **Consequence:** `git branch` useless to everyone else.
- **Fix:** `bugfix_filament_lost_alves` — functional description first.

### 2. Mega PR

- **Appearance:** 2000+ lines, 30+ files, one PR.
- **Trap:** "One PR is easier."
- **Consequence:** Review takes hours. Skimming. Bugs.
- **Fix:** Split: core → integration → tests → docs.

### 3. "fix typo" Commits

- **Appearance:** Multiple tiny commits fixing same thing.
- **Trap:** Incremental fixes feel productive.
- **Consequence:** `git bisect` hits broken intermediate states.
- **Fix:** Squash before PR. Each commit must compile.

---

## See Also

- [Commit Conventions](../../common/commits/conventional-commits.md)
- [Code Review Checklist](../../common/code-review/review-checklist.md)
- [SnapmakerOrca Coding Standards](coding-standards.md)

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | SnapmakerOrca 切片部门PR规范 | v2.0 (2026-06-04) | verified-2026 | 2026-06 |
| R2 | C | Conventional Commits 1.0.0 | Sections 1-7 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft from 切片部门PR规范 v2.0
