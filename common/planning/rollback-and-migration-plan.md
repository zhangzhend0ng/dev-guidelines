---
type: harness
id: "common-rollback-migration-plan"
title: "Rollback and Migration Plan Checklist"
language: "common"
category: "planning"
tier: "C"
scope: "Plan rollback, migration, compatibility, and staged rollout for risky engineering changes"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [planning, rollback, migration, compatibility, release]
based_on:
  - "[C] NIST SP 800-218 SSDF"
  - "[A] Continuous Delivery"
  - "[A] Release It!"
related:
  - "common/planning/task-decomposition.md"
  - "common/planning/risk-and-verification-plan.md"
  - "common/ci-cd/pipeline-patterns.md"
  - "common/dependencies/dependency-management.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Rollback and Migration Plan Checklist

**Based on:** NIST SSDF ([C]), Continuous Delivery ([A]), Release It! ([A]).
**Scope:** Applies to schema changes, dependency upgrades, API changes, config changes, build changes, and production-impacting releases.

---

## Checklist

### 1. Reversibility

- [ ] Change affects production behavior, data, API, dependency, or build pipeline -> **(C)** define rollback path before release. [R1]
- [ ] Rollback is impossible -> **(C)** require staged rollout, backup, or explicit risk acceptance. [R1][R2]

### 2. Compatibility

- [ ] Change affects persisted data or public interface -> **(C)** define forward/backward compatibility. [R1][R2]
- [ ] Multiple versions may run at once -> **(C)** support mixed-version operation or block rollout. [R2]

### 3. Migration

- [ ] Migration changes data or config -> **(C)** define dry run, validation, and recovery. [R1]
- [ ] Migration is long-running -> **(A)** make it resumable and observable. [R3]

### 4. Release Gate

- [ ] High-risk deployment -> **(C)** use staged rollout, monitoring, and stop conditions. [R1][R3]
- [ ] Weak model proposes release/migration steps -> **(A)** require human approval and concise plan. [R1]

### 5. Evidence

- [ ] Rollback or migration plan is claimed complete -> **(C)** include tested command, rehearsal, or NOT VERIFIED statement. [R1]

---

## Decision Tree

```
Risky change?
  -> reversible?
  -> compatibility?
  -> migration dry run?
  -> staged rollout?
  -> tested rollback evidence?
```

---

## Anti-Patterns

### Anti-Pattern 1: Rollback by Hope

- **Appearance:** "We can revert the PR" is the rollback plan.
- **Trap:** It works for simple code changes.
- **Consequence:** Data, config, and dependency changes remain broken.
- **Fix:** Define actual rollback commands and compatibility constraints.

### Anti-Pattern 2: One-Way Migration

- **Appearance:** Migration mutates data without backup or dry run.
- **Trap:** Forward migration was tested once.
- **Consequence:** Failed rollout leaves unrecoverable state.
- **Fix:** Add dry run, backup, validation, and recovery path.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C6] NIST SP 800-218 SSDF | Release and response practices | verified-2026 | 2026-06 |
| R2 | A | Continuous Delivery | Reversible deployments | verified-2026 | 2026-06 |
| R3 | A | Release It! | Stability and operability | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
