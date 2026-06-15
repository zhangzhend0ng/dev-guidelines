---
type: harness
id: "cpp-runtime-observability"
title: "C++ Runtime Observability and Diagnostics Checklist"
language: "cpp"
category: "runtime"
tier: "C"
scope: "Design C++ runtime diagnostics, logging, assertions, crash reporting, metrics, and debug evidence without exposing sensitive data or overwhelming operators"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [observability, diagnostics, logging, crash-reporting, runtime]
based_on:
  - "[C] NIST SP 800-92 Log Management"
  - "[C] OpenTelemetry Logging Specification"
  - "[C] C++ Core Guidelines"
  - "[A] Google SRE Book"
related:
  - "common/logging/logging-standards.md"
  - "common/error-handling/error-handling-strategy.md"
  - "cpp/error-handling/result-vs-exception.md"
  - "cpp/testing/sanitizers.md"
  - "cpp/debugging/crash-dump-analysis.md"
  - "cpp/build/toolchain-and-compiler-flags.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Runtime Observability and Diagnostics Checklist

**Based on:** NIST log management ([C]), OpenTelemetry logging ([C]), C++ Core Guidelines ([C]), Google SRE Book ([A]).
**Scope:** Applies to C++ services, libraries, daemons, CLIs, and production binaries that need diagnosable failures.

---

## Checklist

### 1. Diagnostic Contract

- [ ] Runtime failure can occur in production -> **(C)** define what evidence is emitted: log, metric, status code, crash dump, or error object. [R1][R3]
- [ ] Failure is recoverable -> **(C)** include operation, component, and safe error context. [R1]
- [ ] Failure is fatal -> **(A)** emit final diagnostic before termination when feasible. [R4]

### 2. Sensitive Data

- [ ] Diagnostic may include input, file path, token, key, PII, or proprietary payload -> **(C)** redact or hash before logging. [R1]
- [ ] Parser/security error includes raw payload -> **(C)** summarize safely; do not log full attack input. [R1]

### 3. Assertions and Invariants

- [ ] Condition is programmer error -> **(C)** use assertion/contract-style diagnostic. [R3]
- [ ] Condition is user/runtime error -> **(C)** use recoverable error handling, not assertion. [R3]

### 4. Crash Diagnostics

- [ ] Binary may crash in production -> **(A)** preserve symbols, build ID, version, and crash collection path. [R4]
- [ ] Sanitizer/debug builds exist -> **(C)** keep symbolized output available in CI artifacts. [R3]

### 5. Noise Control

- [ ] Logging is high-volume -> **(C)** rate-limit, sample, or aggregate. [R1][R2]
- [ ] Weak AI summarizes diagnostics -> **(A)** require concise root error, affected component, and next action; no full log dump. [R2]

---

## Decision Tree

```
Runtime failure path?
  -> Recoverable or fatal?
  -> Emit safe diagnostic evidence
  -> Redact sensitive data
  -> Preserve symbols/build ID
  -> Control log volume
```

---

## Anti-Patterns

### Anti-Pattern 1: Log Everything

- **Appearance:** Raw inputs and full internal state are logged.
- **Trap:** More data feels easier to debug.
- **Consequence:** Sensitive data leaks and operators miss the signal.
- **Fix:** Log structured, minimal, redacted evidence.

### Anti-Pattern 2: Assert for User Input

- **Appearance:** Parser asserts on malformed input.
- **Trap:** It catches bugs during development.
- **Consequence:** Production can terminate on normal bad input.
- **Fix:** Use validation and recoverable error handling for external input.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | NIST SP 800-92 | Log management | verified-2026 | 2026-06 |
| R2 | C | OpenTelemetry Logging Specification | Structured telemetry | verified-2026 | 2026-06 |
| R3 | C | [C1] C++ Core Guidelines | Error handling and assertions | verified-2026 | 2026-06 |
| R4 | A | Google SRE Book | Monitoring and incident response | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
