---
type: harness
id: "snapmaker-orca-workflow"
title: "SnapmakerOrca PR and Workflow Standards"
language: "common"
category: "project-specific"
tier: "P"
scope: "Enforce SnapmakerOrca branch naming, commit format, PR size, and code review workflow"
version: "2026.09.2"
status: "draft"
stable_since: ""
last_validated: "2026-09-30"
review_cycle: "12m"
tags: [snapmaker-orca, git, pr, commit, workflow]
based_on:
  - "[C] SnapmakerOrca 切片部门PR规范 v2.0 (2026-06-04)"
  - "[C] Conventional Commits 1.0.0"
  - "[A] dev-guidelines snapmaker-orca commit distillation (2026-08-31) — cross-platform breakage cluster (notes 2/4)"
related:
  - "common/commits/conventional-commits.md"
  - "common/code-review/review-checklist.md"
  - "cpp/build/cmake-include-hygiene.md"
  - "projects/snapmaker-orca/coding-standards.md"
supersedes: []
changelog:
  - "2026.06: Initial draft from 切片部门PR规范 v2.0"
  - "2026.09.1: §6 size threshold deferred to review-checklist Item 1 (canonical two-tier rule); resolves the 400-vs-500 divergence between the two files"
  - "2026.09.2: §9 cross-platform compile gate + §10 upstream fix sync — closes notes 2/4 of docs/reviews/snapmaker-orca-commit-distillation-2026-08-31.md (>=8 cross-platform breakage incidents; 3 fork fixes lagging upstream)"
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

Canonical threshold lives in `common/code-review/review-checklist.md` Item 1 (<400 target / 400–500 with split plan / >500 must split). The table below is project-level size classification only — do not treat it as a divergent limit.

| Size | Lines | Files |
|------|-------|-------|
| Small | <200 | <5 |
| Medium | 200-500 | 5-10 |
| Large | 500-1000 | 10-20 |

- [ ] Thresholds per review-checklist Item 1; 400–500 lines requires a documented split plan → **(P)** [R1]
- [ ] Large features split: core → integration → tests → docs → **(P)** [R1]

### 7. Merge Strategy  **(P)** [R1]

- [ ] Squash and merge preferred → **(P)** [R1]
- [ ] Pre-check: ≥1 approval, CI green, comments resolved, no conflicts → **(P)** [R1]

### 8. Code Review  **(P)** [R1]

- [ ] Comments in English on code lines → **(P)** [R1]
- [ ] `Resolve conversation` when fixed or agreed non-issue → **(P)** [R1]
- [ ] Author pre-check: compiles, tests pass, format OK, no debug code → **(P)** [R1]
- [ ] Urgent: contact reviewer directly → **(P)** [R1]

### 9. Cross-Platform Compile Gate  **(P)** [R1][R3]

MSVC-only self-check is the recurring root of cross-platform breakage (2026-08 distillation: ≥8 incidents — missing wx includes surfaced by Flatpak `SLIC3R_PCH=OFF`, `wxEmptyString` ternary rejected by GCC/Clang, `enum class` streamed to a log macro, syntax errors merged in the #735 crash-hardening batch). "It compiles" must mean the target platform matrix, not "my machine".

- [ ] Changed shared code (GUI/wxWidgets, libslic3r, build files) compiles on Linux/Flatpak (GCC or Clang) before merge, not only MSVC → **(P)** [R1][R3]
- [ ] Large mechanical edits (mass try/catch or scope wrapping) get a full build before push and are not mixed with functional changes in one commit → **(P)** [R3]
- [ ] An author's "compiles" claim is read as scoped to platforms actually exercised; unexercised targets get a sanity build or an explicit waiver in the PR description (see review-checklist Item 2) → **(P)** [R1][R3]

### 10. Upstream Fix Sync  **(P)** [R3]

Fork-local re-fixes of defects upstream already fixed waste review capacity and keep the crash alive until someone notices (2026-08 distillation: EdgeGrid bounds guard — upstream #12806 fixed 2026-04, fork re-fixed 2026-08; DailyTips empty-container crash — upstream fixed 2025-08). Inverse: fork fixes upstream still lacks (HintNotification, ToolOrdering, PrintObject) are sync opportunities upstream.

- [ ] Monthly or per upstream release, sweep upstream `main` (SoftFever/OrcaSlicer) for fixes touching files this fork has locally patched; record findings in a sync issue → **(P)** [R3]
- [ ] Before hand-fixing a bug, search upstream for an existing fix of the same defect → **(P)** [R3]
- [ ] Vendored-library local patches record the upstream issue link so future syncs can reconcile → **(P)** [R3]

---

## Decision Tree

```
New work?
  → Branch: prefix_functional_desc from latest main [1,2]
  → Commit: type: description, atomic, compiles [4]
  → Sync main weekly (long features) [2]
  → PR: title type:desc [5], ≤500 lines [6]
  → Compile gate: Linux/Flatpak build for shared-code changes [9]
  → Review: ≥1 approval, CI green, English comments [8]
  → Merge: squash [7]
  → Delete branch (one-phase) or retain (multi-phase) [2]
  → Monthly: upstream fix sweep [10]
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

### 4. "It Compiles on My Machine"

- **Appearance:** PR self-check "compiles" backed by an MSVC build only; Flatpak/Linux CI (or first Linux user) finds the breakage after merge.
- **Trap:** MSVC is the daily driver; the other platform "should be fine."
- **Consequence:** Recurring Linux/Flatpak build breakage (missing includes masked by PCH, `wxEmptyString` ternary, `enum class` streaming — ≥8 incidents in the 2026-08 distillation), plus uncompiled hardening batches merged with syntax errors.
- **Fix:** §9 compile gate — GCC/Clang build of changed shared code before merge; mechanical refactor batches get their own full-build commit.

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
| R3 | A | dev-guidelines snapmaker-orca commit distillation report | `docs/reviews/snapmaker-orca-commit-distillation-2026-08-31.md` notes 2/4 (commits 74c01ad75f, 675866c502, 0f9ae760be, c6e16f7da5, 2e56dd12ee, c7f426abfd) | verified-2026 | 2026-08 |

---

## Changelog

- 2026.06: Initial draft from 切片部门PR规范 v2.0
