---
type: harness
id: "lava-login-logout-state-machine"
title: "Lava Login/Logout State Machine Pre-Check"
language: "dart"
category: "project-specific"
tier: "P"
scope: "Before changing any login/logout session-flow code in the lava monorepo (lava-orca / lava-app / lava-shared): enumerate every trigger and re-entry path across the WCP (machine), Orca, and cloud session states, and prove the transition sequence is idempotent and loop-free"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-09"
review_cycle: "12m"
tags: [lava, login, logout, session, state-machine, wcp, orca, flutter]
based_on:
  - "[P] lava monorepo dual-diff review (2026-08) — login/logout state machine findings"
  - "[A] dev-guidelines engineering experience"
related:
  - "dart/error-handling.md"
  - "common/planning/change-scope-control.md"
supersedes: []
changelog:
  - "2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)"
---

# Lava Login/Logout State Machine Pre-Check

**Based on:** lava monorepo dual-diff review findings ([P]), dev-guidelines engineering experience ([A]).
**Scope:** Project-level (**P**) checklist for the lava Flutter apps' session flows. A login/logout change touches three parties that must stay consistent — the **WCP machine** (the physical device/transport), **Orca** (the app's own session/UI), and the **cloud** account state. This checklist runs **before** writing the change (design gate) and again in review.

---

## Concepts

| Party | Role in a logout |
|-------|------------------|
| Cloud token | Expires/invalidates first (token-expiry callback, or a 401-style signal). |
| WCP machine | Owns the physical-channel session; a logout over WCP is a *remote operation with real side effects* on the device. |
| Orca (local app) | Owns the local session, `TokenInvalidation` bookkeeping, and the login dialog state machine. |

**Sequence that must hold:** token invalidation → local (Orca) logout cleanup → machine (WCP) logout → login dialog. Any step can throw or be re-entered; see `dart/error-handling.md` for the async rules this depends on.

---

## Checklist

### 1. Enumerate All Triggers and Re-Entry Paths Before Editing **(P)** [R1]

- [ ] Every source that can enter the logout flow is listed: token-expiry callback, manual logout UI action, remote/device-initiated logout, and error-driven logout (e.g. a failed request that forces re-login) → **(P)** a change that handles only one trigger is incomplete; the others are untested paths. [R1]
- [ ] Re-entry is checked: can a logout handler observe a user-state change that re-enters the same handler? → **(P)** guard with an explicit phase (e.g. `_loggingOut`) and prove the flow cannot loop or double-run. [R1]

### 2. Sequence, Idempotency, and Cleanup Across the Three Parties **(P)** [R1]

- [ ] The transition order (token invalidation → local cleanup → WCP logout → dialog) is stated and followed; a logout issued twice for one logical event is prevented (single issuer or in-flight guard) → **(P)** duplicate WCP logout messages are a real device side effect, not a harmless retry. [R1]
- [ ] Any step that can throw still lets required cleanup run: e.g. `TokenInvalidation.instance.reset()` and dialog progression are not skipped when the WCP call fails (see `dart/error-handling.md` item 3) → **(P)** a stranded cleanup that freezes the session state machine is a release blocker for this flow. [R1]

### 3. Three-Party State Stays Consistent **(C)** [R2]

- [ ] A state change on one party (token gone, WCP disconnected, cloud session dead) is reflected in the others within the flow, and the flow does not assume a party's state it never verified → **(C)** verify each transition's preconditions before acting. [R2]

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Single-Trigger Design

- **Appearance:** The logout flow is designed and tested from the manual logout button only; the token-expiry callback and the error-driven re-login path reuse it incidentally.
- **Trap:** Manual logout is the path you can click in a demo, so it becomes the "real" flow.
- **Consequence:** A token invalidation that arrives mid-session walks an untested path, skips the machine logout or the local cleanup, and leaves the device channel or the dialog state inconsistent.
- **Fix:** Item 1 — list every trigger before writing the change and give each one at least one transition test.

### Anti-Pattern 2: Cleanup That Depends on a "Can't Fail" Branch

- **Appearance:** `TokenInvalidation.instance.reset()` is placed after an awaited WCP logout call in a branch believed unreachable-by-failure (transport already dead), with no `try`/`finally`.
- **Trap:** In the dead-transport scenario the awaited call does throw — exactly the case the "can't fail" label was meant to cover — and the branch unwinds before the reset.
- **Consequence:** The session state machine is stuck: stale token, no dialog, no error surfaced. Reproduction requires the dead-transport timing, so it escapes normal testing.
- **Fix:** Item 2 — run required cleanup in `finally` or a catch that proceeds; see `dart/error-handling.md` Anti-Pattern 1 for the full write-up.

---

## See Also

- [Dart Asynchronous Error and Exception Safety Checklist](../../dart/error-handling.md) — the async/exception rules (items 3, 5, 7) this project checklist depends on; its Anti-Patterns 1–2 document the source incidents.
- [Change Scope Control Checklist (common)](../../common/planning/change-scope-control.md) — why a login/logout state-machine change must not be batched with unrelated fixes, and that this pre-check runs before the change is scheduled.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | P | lava monorepo dual-diff review (2026-08) | Login/logout trigger enumeration, three-party sequence, stranded `TokenInvalidation.reset()`, re-entry loop | verified-2026 | 2026-09 |
| R2 | C | [C29] Dart and Flutter Official Documentation | Futures/async error propagation (the mechanism under item 2's cleanup rule) | verified-2026 | 2026-09 |

---

## Changelog

- 2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)
