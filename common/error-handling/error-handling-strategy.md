---
type: harness
id: "common-error-handling"
title: "Error Handling Strategy Checklist"
language: "common"
category: "design"
tier: "C"
scope: "Choose consistent error handling mechanisms and propagation patterns for any codebase"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-09"
review_cycle: "12m"
tags: [error-handling, exceptions, error-codes, robustness]
based_on:
  - "[C] Google Error Handling Guide"
  - "[C] NIST SP 800-64"
  - "[A] Release It! (Michael Nygard)"
  - "[A] The Pragmatic Programmer (Hunt & Thomas)"
related:
  - "cpp/runtime/observability-and-diagnostics.md"
  - "cpp/error-handling/result-vs-exception.md"
  - "cpp/correctness/exception-safety.md"
  - "python/concurrency/asyncio-cancellation.md"
  - "common/logging/logging-standards.md"
  - "dart/error-handling.md"
supersedes: []
changelog:
  - "2026.05: Initial draft"
  - "2026.09: Items 8-9 and anti-patterns 4-5 added — identify errors by typed exceptions/error codes, never by message text; UI error-text desensitization must land as generic copy or a log line, never as commented-out silent swallowing. Distilled from the lava monorepo dual-diff review."
---

# Error Handling Strategy Checklist

**Based on:** Google Error Handling Guide ([C]), NIST SP 800-64 ([C]), Release It! (Nygard) ([A]), The Pragmatic Programmer ([A]).
**Scope:** Establish consistent error handling across a codebase. Language-agnostic; language harnesses define concrete mechanisms.

---

## Concepts

| Mechanism | Characteristics |
|-----------|----------------|
| **Exceptions** | Unwind stack; separate error/happy path; requires RAII |
| **Result<T,E>** | Explicit return; no hidden control flow; caller must check |
| **Assertions/Panics** | Programmer errors only; terminate; not for recoverable errors |

**One codebase = one primary strategy.**

---

## Checklist

### 1. Strategy Selection

- [ ] **(C)** Choose one: exceptions OR `Result<T,E>` OR error codes. Document it. [R1]
- [ ] **(C)** Assertions/panics ONLY for programmer bugs, never for runtime errors. [R2]

### 2. Error Information

- [ ] **(C)** Every error: what failed + relevant context + unique ID for log search. [R1]
- [ ] **(C)** Error messages for operators/developers, not end users. Be specific. [R3]
- [ ] **(C)** Include correlation/trace ID for distributed systems. [R1]

### 3. Error Propagation

- [ ] **(C)** Never silently swallow. Propagate to handler that can respond. [R1]
- [ ] **(C)** Can't handle? Propagate upward. Wrap with context at each layer boundary. [R2]
- [ ] **(C)** Top-level handler: log full error, return appropriate status. [R3]

### 4. Error Handling Boundaries

- [ ] **(C)** Module/library edges: translate internal errors to public error types. [R1]
- [ ] **(C)** Trust boundaries: convert to user-appropriate response. Never leak stack traces. [R2]

### 5. Log or Throw — Not Both

- [ ] **(C)** Log ONCE. Prefer outermost handler — it has the most context. [R1]
- [ ] **(C)** Intermediate layers add context via wrapping, not logging. [R3]

### 6. Retry and Resilience

- [ ] **(C)** Transient errors (network, deadlock) → exponential backoff + jitter + max retries. [R3]
- [ ] **(C)** Persistent errors (validation, auth) → fail fast. Do NOT retry. [R1]

### 7. Graceful Degradation

- [ ] **(C)** Non-critical component fails → degrade, don't crash. [R3]
- [ ] **(C)** Circuit breaker: N consecutive failures → cooldown before retry. [R3]

### 8. Error Identification — Never Branch on Message Text

- [ ] An error branch or classification matches the exception's message string (`e.toString().contains("Request expired")`) → **(C)** identify errors by typed exceptions or structured error codes. Message copy is display-layer content and is **not a contract**; upstream rewording silently breaks the match. [R1][R5]
- [ ] A message string has been stable long enough to "trust" it → **(C)** treat that as an accident of copy, not a guarantee; add a typed error/error code at the source and branch on that. [R5]

### 9. UI Error-Text Desensitization Must Land Somewhere

- [ ] A user-facing message that exposed a raw exception (`e.toString()`) is being removed (PII/technical-leak cleanup) → **(C)** replace every removed occurrence with either a generic user-facing message **or** a log line — never comment the call out and leave production code dead. [R5]
- [ ] Desensitization leaves commented-out code behind → **(C)** commented-out production code silently swallows the error and violates the review-checklist dead-code item; delete the line or land the copy/log replacement. [R5]

---

## Decision Tree

```
Programmer error? → Assert. Fail fast. [1]
Runtime error?
  ├─ Can handle? → Handle + log ONCE [5]
  └─ Can't → Propagate with context [3]
              └─ At boundary → translate + log [4]

Transient? → Retry with backoff [6]
Persistent? → Fail fast
Non-critical? → Degrade [7]
```

---

## Anti-Patterns

### 1. Empty Catch

- **Appearance:** `try { ... } catch (...) { }`
- **Fix:** At minimum, log. If truly non-critical, document why and monitor.

### 2. Log and Re-throw

- **Appearance:** Every stack frame catches, logs, re-throws.
- **Fix:** Log once at outermost handler. Intermediate layers wrap context, don't log.

### 3. Exceptions for Control Flow

- **Appearance:** `throw NotFound()` → catch → return 404 for expected conditions.
- **Fix:** Use `optional<T>` or `Result<T,E>` for expected failures. Exceptions for truly unexpected.

### 4. String-Matching an Exception Message to Branch

- **Appearance:** A client decides what to do next with `if (e.toString().contains("Request expired")) { ... }` — branching on a substring of an exception/log message.
- **Trap:** The message is human-readable, stable in practice, and the string arrives *with* the exception, so no error-code plumbing seems needed. Matching a substring feels like a pragmatic version of classification.
- **Consequence:** The upstream rewords its copy (e.g. `"Request expired (cleaned up after 60s)"` becomes something else), and the client's branch silently stops matching — the error is now misclassified or unhandled, with no compile error and no failing test to point at the change. Message text is also subject to localization, truncation, and log-format decoration, which makes substring matches doubly fragile.
- **Fix:** Item 8 — identify errors by typed exception classes or structured error codes; message text is display-layer and non-contractual. If you don't control the source, wrap it at the boundary into a typed error (see section 4).

### 5. Desensitization by Commenting Out

- **Appearance:** A sweep to remove raw `e.toString()` from user-facing dialogs "fixes" each site by commenting out the error-display call — no replacement message, no log line.
- **Trap:** Removing the raw text is the visible goal (PII/technical-leak cleanup), and commenting out is the minimal diff that makes the compiler and the security reviewer happy.
- **Consequence:** The error path now does nothing: the user sees no message and the failure is not logged. That is silent swallowing — the exact anti-pattern this harness forbids — and the commented-out production code is dead code that review-checklist flags. The user is left staring at an unresponsive dialog with no explanation.
- **Fix:** Item 9 — each removed `e.toString()` lands as *either* a generic user-facing message *or* a log line. If the site genuinely needs no user message, the log line is mandatory; never leave a commented-out call.

---

## See Also

- [Exception Safety (C++)](../../cpp/correctness/exception-safety.md) — Basic/strong/nothrow guarantees
- [Logging Standards](../../common/logging/logging-standards.md) — What NOT to log; item 8 here (message text is not a contract) pairs with keeping message copy out of programmatic use
- [Dart Asynchronous Error and Exception Safety Checklist](../../dart/error-handling.md) — the Dart concrete form of this harness

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Google Error Handling Guide | General | verified-2026 | 2026-05 |
| R2 | C | NIST SP 800-64 | Security in SDLC | verified-2026 | 2026-05 |
| R3 | A | Release It! (Nygard) | Stability patterns | verified-2026 | 2026-05 |
| R4 | A | The Pragmatic Programmer | Ch. 4 | verified-2026 | 2026-05 |
| R5 | A | dev-guidelines engineering experience (lava monorepo dual-diff review) | Message-string branching (`e.toString().contains("Request expired")`); desensitization must land as copy or log | verified-2026 | 2026-09 |

---

## Changelog

- 2026.05: Initial draft
- 2026.09: Items 8–9 and anti-patterns 4–5 added — error identification by typed exceptions/error codes rather than message text, and UI error-text desensitization that must land as generic copy or a log line (never commented-out dead code). Distilled from the lava monorepo dual-diff review.
