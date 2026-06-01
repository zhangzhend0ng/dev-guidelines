---
type: harness
id: "common-error-handling"
title: "Error Handling Strategy Checklist"
language: "common"
category: "design"
tier: "C"
scope: "Choose consistent error handling mechanisms and propagation patterns for any codebase"
version: "2026.05"
status: "draft"
stable_since: ""
last_validated: "2026-05-31"
review_cycle: "12m"
tags: [error-handling, exceptions, error-codes, robustness]
based_on:
  - "[C] Google Error Handling Guide"
  - "[C] NIST SP 800-64"
  - "[A] Release It! (Michael Nygard)"
  - "[A] The Pragmatic Programmer (Hunt & Thomas)"
related: []
supersedes: []
changelog:
  - "2026.05: Initial draft"
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

---

## See Also

- [Exception Safety (C++)](../../cpp/correctness/exception-safety.md) — Basic/strong/nothrow guarantees

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Google Error Handling Guide | General | verified-2026 | 2026-05 |
| R2 | C | NIST SP 800-64 | Security in SDLC | verified-2026 | 2026-05 |
| R3 | A | Release It! (Nygard) | Stability patterns | verified-2026 | 2026-05 |
| R4 | A | The Pragmatic Programmer | Ch. 4 | verified-2026 | 2026-05 |

---

## Changelog

- 2026.05: Initial draft
