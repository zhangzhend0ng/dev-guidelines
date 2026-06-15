---
type: harness
id: "python-asyncio-cancellation"
title: "Python asyncio Cancellation Checklist"
language: "python"
category: "concurrency"
tier: "C"
scope: "Write asyncio code that handles cancellation, timeouts, task ownership, cleanup, and structured concurrency predictably"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [python, asyncio, cancellation, concurrency, tasks]
based_on:
  - "[C] Python Documentation"
related:
  - "common/error-handling/error-handling-strategy.md"
  - "common/debugging/fix-verification.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Python asyncio Cancellation Checklist

**Based on:** Python asyncio documentation ([C]).
**Scope:** Applies to Python async code using tasks, timeouts, cancellation, async context managers, or concurrent request handling.

---

## Checklist

### 1. Task Ownership

- [ ] Task is created with `create_task` -> **(C)** define who awaits, cancels, and observes exceptions from it. [R1]
- [ ] Fire-and-forget task is proposed -> **(C)** reject unless lifecycle, logging, and shutdown are explicit. [R1]

### 2. Cancellation Propagation

- [ ] Coroutine catches broad exceptions -> **(C)** do not swallow cancellation; re-raise after cleanup. [R1]
- [ ] Cleanup is needed -> **(C)** use `try/finally` or async context manager so cancellation releases resources. [R1]

### 3. Timeouts

- [ ] Operation may hang -> **(C)** apply an explicit timeout at the caller or boundary. [R1]
- [ ] Timeout is caught -> **(C)** distinguish timeout from business failure and preserve useful context. [R1]

### 4. Structured Concurrency

- [ ] Multiple related tasks run together -> **(C)** prefer structured task grouping where available. [R1]
- [ ] One sibling task fails -> **(C)** define whether siblings are cancelled, awaited, or allowed to finish. [R1]

### 5. Testing and Verification

- [ ] Async behavior changes -> **(C)** add tests for success, timeout, cancellation, and cleanup. [R1]
- [ ] Race or leak suspected -> **(A)** verify tasks are awaited and no pending task remains after test completion. [R1]

---

## Decision Tree

```
asyncio task or timeout?
  -> define task owner
  -> propagate cancellation
  -> cleanup in finally/context manager
  -> use timeout at boundary
  -> test cancellation and cleanup
```

---

## Anti-Patterns

### Anti-Pattern 1: Swallowed Cancellation

- **Appearance:** `except Exception` or broad handler logs and continues.
- **Trap:** It looks resilient.
- **Consequence:** Shutdown, timeout, or parent cancellation can hang.
- **Fix:** Let cancellation propagate after cleanup.

### Anti-Pattern 2: Unobserved Task

- **Appearance:** `asyncio.create_task(worker())` with no stored handle.
- **Trap:** It starts the work.
- **Consequence:** Exceptions are lost and shutdown behavior is undefined.
- **Fix:** keep task ownership explicit or use structured concurrency.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C24] Python Documentation | asyncio tasks, cancellation, timeouts, TaskGroup | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
