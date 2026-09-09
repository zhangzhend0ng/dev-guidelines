---
type: harness
id: "dart-error-handling"
title: "Dart Asynchronous Error and Exception Safety Checklist"
language: "dart"
category: "correctness"
tier: "C"
scope: "Ensure every Dart/Flutter async error reaches exactly one handler and that cleanup, finalization, and single-flight side effects survive awaited calls, unawaited futures, stream callbacks, rethrows, and Completers"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-09"
review_cycle: "12m"
tags: [dart, flutter, async, futures, streams, exceptions, error-handling, state-machine]
based_on:
  - "[C] Dart and Flutter Official Documentation (dart.dev / flutter.dev)"
  - "[C] Effective Dart"
  - "[A] dev-guidelines engineering experience (lava monorepo dual-diff review)"
related:
  - "common/error-handling/error-handling-strategy.md"
  - "projects/lava/login-logout-state-machine.md"
supersedes: []
changelog:
  - "2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)"
---

# Dart Asynchronous Error and Exception Safety Checklist

**Based on:** Dart/Flutter official docs ([C]), Effective Dart ([C]), dev-guidelines engineering experience from the lava monorepo dual-diff review ([A]).
**Scope:** The Dart-language concrete rules for `common/error-handling/error-handling-strategy.md`: where async errors escape, how they must be caught/wrapped/logged, and how cleanup and remote side effects must survive them. This harness does **not** re-state the general strategy checklist — it pins down the Dart-specific failure modes (unawaited futures, `stream.listen` async callbacks, `Completer` dangling, double-send races). C++ exception-safety guarantees have no direct Dart `noexcept` equivalent; the analogue is *finalization must not be skipped* and *errors must not be dropped or doubled*.

---

## Prerequisites / Concepts

| Concept | Dart behavior |
|---------|---------------|
| Async error propagation | An `async` function never throws synchronously; it returns a `Future` that completes with the error. `await` rethrows that error in the awaiting zone. |
| Unhandled async error | A `Future` whose error is never observed surfaces as an **unhandled error** in the enclosing zone (`Zone.current.handleUnhandledError`) — it does *not* propagate to the `try` around the code that *started* the future. |
| `unawaited()` | `package:async`'s `unawaited(future)` marks a deliberate fire-and-forget and satisfies the `unawaited_futures` lint. It suppresses the *warning*; it does **not** add an error handler. |
| `stream.listen` async callback | The callback `(event) async { ... }` returns a `Future` that `listen` discards. An exception thrown inside it becomes an unhandled async error unless caught inside the callback or handled by `onError`/`cancelOnError`. |
| Error `Zone` | `runZonedGuarded`/`PlatformDispatcher.onError` catch *unhandled* errors globally. A last-resort net, not a substitute for per-call handling. |
| `Completer` | The owner must complete the future exactly once — with a value or an error — on every path. A never-completed `Completer` leaves awaiters hanging forever. |

**Guiding principle (mirrors exception-safety):** the weakest link decides the outcome. A cleanup step placed *after* an `await` that can throw is only as reliable as the exception handling around that `await`; a fire-and-forget call is only as safe as its error path; a remote operation issued twice is a real side effect, not a test artifact.

---

## Checklist

### 1. Async Callback Exceptions Are Handled Where the Callback Lives

An exception from an `async` callback passed to `stream.listen` (or an event bus, socket, or platform-channel handler) does not reach a `try` around the `listen` call — it becomes an unhandled async error.

- [ ] Callback is `(event) async { ... }` and can throw → **(C)** catch inside the callback, or attach `onError`, so the error is handled where the listener can still react. [R1][R2]
- [ ] The async error is only noticed via a global zone handler → **(A)** acceptable as a last-resort net (telemetry + crash reporting); do not rely on it for flow correctness. [R1][R3]

### 2. Fire-and-Forget Futures Carry an Error Path

- [ ] A future is started without `await` and intentionally ignored → **(C)** give it an error path: `unawaited(f.catchError(...))`, an `async` wrapper with `try`, or a deliberately scoped zone; `unawaited(f)` alone only silences the lint. [R1][R2]
- [ ] The un-awaited future mutates process/remote state and its failure matters → **(C)** do not fire-and-forget it at all; await it in a handler that owns the outcome. [R1][R3]

```dart
// Good — the fire-and-forget future cannot die silently.
unawaited(_syncPrefs().catchError((Object e, StackTrace s) {
  log.warning('prefs sync failed', e, s);   // handled here, exactly once
}));

// Bad — suppresses the lint, drops the error.
unawaited(_syncPrefs());
```

### 3. Mandatory Finalization After a Possibly-Throwing Await

If code after an `await` must run for the feature to keep working (state reset, `TokenInvalidation.reset()`, dialog continuation), an exception in the awaited call must not skip it.

- [ ] An `await`ed call that can throw precedes required cleanup/state progression → **(C)** run the required step in `finally` or in the catch handler of a `catch` that still proceeds; never leave it as the unprotected next statement. [R1][R3]
- [ ] The awaited branch "is the transport already dead" so errors are assumed impossible → **(C)** that assumption does not protect the finalization after it; a rethrown error there still unwinds past your cleanup. [R3]

```dart
// Good — reset runs whether logout succeeded or threw.
try {
  await Wcp.instance.userLogout();
} catch (e, s) {
  log.warning('wcp logout failed; still clearing local session', e, s);
} finally {
  TokenInvalidation.instance.reset();   // state machine can always move on
  _navigateToLogin();
}
```

### 4. Rethrow With Context; Log Once at the Edge

- [ ] An intermediate layer catches an error only to propagate it → **(C)** wrap it in a typed error / error code that adds context and rethrow that; do not log-and-rethrow the same error at every layer. [R1][R3]
- [ ] The outermost handler that can respond logs the full error (message + stack) once → **(C)** it may also translate to a user-facing message, but that translation is a separate concern from logging (see common error-handling and logging harnesses). [R3]

### 5. One Logical Event → One Remote/State Operation (No Awaited + Fire-and-Forgotten Pair)

- [ ] The same operation (logout, sync, flag apply) can be triggered both un-awaited and awaited for one logical event → **(C)** make the call sites converge on a single issuer, or guard with single-flight/in-flight state; two paths that each send the operation produce duplicate remote side effects. [R3]
- [ ] Two such paths are believed harmless because "the server treats it as idempotent" → **(C)** do not rely on peer-side idempotency for ordering guarantees; the duplicate is still a real message on the wire and can interleave with other transitions. [R3]

```dart
// Bad — two issuers for one logout: both send a logout over the same WCP channel.
void onUserInitiated() {
  logout();                      // fire-and-forget issuer
  await Wcp.instance.userLogout();  // second issuer, same logical event
}
```

### 6. Owned Completers Complete Exactly Once on Every Path

- [ ] Code creates and completes a `Completer` → **(C)** every path (including early returns and exceptions inside the guarded `try`) completes it once, with `completeError` for failures; never leave it pending. [R1]
- [ ] A completion is at risk of running twice (callback + error path both fire) → **(C)** complete only once (`if (!_done)`) or restructure so exactly one path owns completion; double-complete throws `StateError`. [R1]
- [ ] Callers cannot afford to wait forever on an external source → **(A)** add `Future.timeout` as a documented backstop when the API contract permits a bounded wait. [R1][R3]

### 7. Login/Logout State Flows Are Treated as State Machines, Not Scripts

A session flow has multiple triggers (token-expiry callback, manual logout, remote/device logout, error-driven logout) and can re-enter itself.

- [ ] A session-state change can be triggered from several sources → **(C)** enumerate the triggers and re-entry paths up front (see the lava project checklist) and make each transition idempotent. [R3]
- [ ] A logout handler observes a user-state change that itself re-enters the logout handler → **(C)** guard with an explicit phase/state (e.g., `_loggingOut`) so the re-entry does not loop or double-run. [R3]

---

## Quick Decision Tree

```
async function / callback
  ├─ error escapes a stream/event callback?        → handle inside callback or onError  [1]
  ├─ future started but never awaited?             → attach error path; don't just unawaited() [2]
  │     └─ it mutates remote/state?                → await it where the outcome is owned [2]
  ├─ required cleanup after a possibly-throwing await? → finally / catch-that-proceeds  [3]
  ├─ intermediate layer rethrowing?                → wrap with context, log once at edge  [4]
  ├─ same op issuable awaited AND un-awaited?      → single issuer or single-flight guard  [5]
  ├─ you own a Completer?                          → complete exactly once, error or value  [6]
  └─ login/logout flow?                            → state machine: enumerate triggers, guard re-entry  [7]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Cleanup Stranded After a Throwing Await

- **Appearance:** A logout branch calls `await Wcp.instance.userLogout()` (which rethrows internally) with no `try`/`catch`, and places `TokenInvalidation.instance.reset()` after it — in a branch that "is only reached when the transport is already dead," so the author assumed the call could not fail.
- **Trap:** In a dead-transport scenario the awaited call *does* throw, and the branch looks unreachable-by-failure, so no guard seems needed. The code compiles and passes happy-path tests.
- **Consequence:** The exception escapes `showLoginDialog`, skipping `TokenInvalidation.instance.reset()` and the dialog continuation. The client's session state machine is stuck: the token is stale, nobody observed the error, and no later login/dialog path fires.
- **Fix:** Item 3 — run the reset (and dialog progression) in `finally` or in a catch that still proceeds, and log the failure once. Cleanup that must happen cannot be left to the unprotected next statement.

### Anti-Pattern 2: Awaited + Fire-and-Forgotten Calls to the Same Operation

- **Appearance:** One logout flow calls `logout();` (un-awaited, fire-and-forget) and later `await Wcp.instance.userLogout();` — two code paths, both issuing the same logout over the same WCP channel, in overlapping order.
- **Trap:** "The first one is just a local trigger; the server logout is idempotent." Each line looks reasonable in isolation and the duplicate is invisible in a single-path trace.
- **Consequence:** Two logout messages go out for one logical event. The second can arrive after the channel/state has already transitioned, re-entering the login/logout state machine out of order or canceling the first logout's cleanup — a race that only shows up under real timing.
- **Fix:** Item 5 — converge on one issuer per logical event, or guard with an in-flight flag; never pair an awaited and an un-awaited call to the same remote operation.

### Anti-Pattern 3: Dangling Completer on the Error Path

- **Appearance:** A `Completer` is completed on the success path but an early `return` or a `throw` in the guarded `try` skips `complete`/`completeError`.
- **Trap:** The success path is the one that was written and tested; the error path "just returns."
- **Consequence:** The awaiter hangs forever — no timeout fires because none exists, no error surfaces, and the surrounding state machine stalls waiting on a future that never completes.
- **Fix:** Item 6 — complete exactly once on every path, using `try/finally` or a single completion point, with `completeError` carrying the exception.

---

## See Also

- [Error Handling Strategy Checklist (common)](../common/error-handling/error-handling-strategy.md) — the language-agnostic strategy this harness instantiates for Dart; log-once, wrap-with-context, and never-silently-swallow rules apply here.
- [Lava Login/Logout State Machine Pre-Check (P)](../projects/lava/login-logout-state-machine.md) — the project-level checklist for session flows; item 7 of this harness is its general rule.
- [Logging Standards Checklist (common)](../common/logging/logging-standards.md) — what the single log line at the edge may and may not contain.
- [Exception Safety Guarantees (C++)](../cpp/correctness/exception-safety.md) — the C++ cousin of this harness; its "finalization must survive unwinding" thinking maps to Dart items 3 and 6.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C29] Dart and Flutter Official Documentation | Futures, streams, async error propagation, unhandled-error zones, `Completer` | verified-2026 | 2026-09 |
| R2 | C | [C30] Effective Dart | Async usage guidance, `unawaited_futures` discipline | verified-2026 | 2026-09 |
| R3 | A | dev-guidelines engineering experience (lava monorepo dual-diff review) | Login/logout re-entry, fire-and-forget ordering, duplicate logout, stranded `TokenInvalidation.reset()` | verified-2026 | 2026-09 |

> **Tier honesty note:** The mechanism rules — where an async error lands, that `unawaited()` does not handle errors, that a `Completer` must complete once — are backed by the official Dart/Flutter documentation and are tagged (C). The *flow-level* rules (items 3, 5, 7: cleanup-after-throw, single-issuer, state-machine re-entry) are distilled from one real review and carry engineering experience as (A)-tier evidence; they are stated as (C) at the harness level because they are the Dart concrete form of long-standing error-handling consensus, but reviewers should read the item-level tags honestly.

---

## Changelog

- 2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)
