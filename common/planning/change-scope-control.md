---
type: harness
id: "common-change-scope-control"
title: "Change Scope Control Checklist"
language: "common"
category: "planning"
tier: "A"
scope: "Keep engineering changes within explicit scope, non-goals, approved files, and reviewable boundaries"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-09"
review_cycle: "24m"
tags: [planning, scope-control, change-management, ai]
based_on:
  - "[A] dev-guidelines Harness-Driven Development Protocol"
  - "[C] NIST SP 800-218 SSDF"
  - "[A] Software Engineering at Google"
related:
  - "common/planning/task-decomposition.md"
  - "common/planning/risk-and-verification-plan.md"
  - "common/ai/model-capability-and-instruction-adherence.md"
  - "common/planning/requirements-gap-analysis.md"
  - "projects/lava/login-logout-state-machine.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
  - "2026.09: Item 6 (release-batch diffs) added — version bump + hotfix + small feature may share a release batch, but auth/login state-machine changes must not mix with unrelated remediation, and a login-flow change must enumerate all triggers and re-entry paths. Distilled from the lava monorepo dual-diff review."
---

# Change Scope Control Checklist

**Based on:** dev-guidelines protocol ([A]), NIST SSDF ([C]), Software Engineering at Google ([A]).
**Scope:** Applies to implementation, refactoring, debugging, and AI-generated patches.

---

## Checklist

### 1. Scope Statement

- [ ] Change lacks explicit in-scope files/areas -> **(A)** define them before edits. [R1]
- [ ] Task has likely adjacent cleanup -> **(A)** list non-goals. [R1][R3]

### 2. File Boundary

- [ ] Patch touches files outside approved scope -> **(A)** stop and request scope update. [R1]
- [ ] AI proposes broad rewrite -> **(A)** reduce to smallest behavior-preserving patch unless rewrite is approved. [R1]

### 3. Dependency Boundary

- [ ] Change adds dependency, tool, build flag, or package config -> **(C)** require explicit approval and dependency/build harness checks. [R2]
- [ ] Dependency is incidental -> **(A)** avoid it and keep change local. [R2]

### 4. Review Boundary

- [ ] Diff mixes behavior change with formatting/refactor -> **(A)** split into separate changes. [R3]
- [ ] Review cannot identify core behavior change -> **(A)** narrow or split. [R3]

### 5. Escape Hatch

- [ ] Out-of-scope issue blocks the task -> **(A)** record blocker and propose a new task; do not silently expand scope. [R1]

### 6. Release-Batch Diffs

A "release batch" diff ships several independently-reviewable items together because they are released as one unit. Its rules are more permissive than a single-purpose change but still have hard lines.

- [ ] Batch combines a version bump + hotfix + small feature for one coordinated release -> **(A)** acceptable when each item remains independently reviewable and the batch is cut/released together. [R3]
- [ ] Batch mixes an authentication/login state-machine change with unrelated remediation -> **(C)** split the auth change from the unrelated fixes; session-flow edits are security-sensitive and get isolated review. [R2]
- [ ] Change alters a login/logout state flow -> **(C)** enumerate every triggering source and re-entry path (token-expiry callback, manual logout, remote/device logout, error-driven logout), and verify idempotency and loop-freedom — see the lava project checklist. [R2][R4]

---

## Decision Tree

```
Before editing
  -> in-scope files
  -> non-goals
  -> dependency/build boundary
  -> stop on scope expansion
Release-batch diff?
  -> bump + hotfix + small feature: OK if coordinated  [6]
  -> auth/login state machine mixed with unrelated fixes: SPLIT  [6]
  -> login/logout flow change: enumerate triggers + re-entry paths first  [6]
```

---

## Anti-Patterns

### Anti-Pattern 1: Opportunistic Cleanup

- **Appearance:** Patch fixes a bug and reformats unrelated files.
- **Trap:** The file was already open.
- **Consequence:** Review cost rises and regressions hide.
- **Fix:** Split cleanup into a separate change.

### Anti-Pattern 2: Silent Scope Expansion

- **Appearance:** Agent fixes adjacent issues without asking.
- **Trap:** It looks helpful.
- **Consequence:** Unreviewed behavior changes enter the patch.
- **Fix:** Stop and create a new task.

---

## See Also

- [Lava Login/Logout State Machine Pre-Check](../../projects/lava/login-logout-state-machine.md) — the project-level checklist item 6 refers to; run it before a login/logout flow change is scoped.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines Harness-Driven Development Protocol | Scope and review gates | verified-2026 | 2026-06 |
| R2 | C | [C6] NIST SP 800-218 SSDF | Secure change and verification practices | verified-2026 | 2026-06 |
| R3 | A | Software Engineering at Google | Small changes and reviewability | verified-2026 | 2026-06 |
| R4 | A | dev-guidelines engineering experience (lava monorepo dual-diff review) | Release-batch composition; auth/login state-machine trigger and re-entry enumeration | verified-2026 | 2026-09 |

---

## Changelog

- 2026.06: Initial draft
- 2026.09: Item 6 (release-batch diffs) added — version bump + hotfix + small feature may share a coordinated release batch, but auth/login state-machine changes must not mix with unrelated remediation, and a login-flow change must enumerate all triggers and re-entry paths. Distilled from the lava monorepo dual-diff review.
