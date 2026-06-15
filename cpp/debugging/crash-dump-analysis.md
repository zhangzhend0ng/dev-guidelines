---
type: harness
id: "cpp-debugging-crash-dump-analysis"
title: "C++ Crash Dump Analysis Checklist"
language: "cpp"
category: "debugging"
tier: "C"
scope: "Analyze C++ crashes using dumps, symbols, build metadata, stack traces, and runtime diagnostics without guessing from logs alone"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags:
  - debugging
  - crash-dumps
  - symbols
  - postmortem
  - diagnostics
based_on:
  - "[C] C++ Core Guidelines"
  - "[C] NIST SP 800-92 Log Management"
  - "[A] Google SRE Book"
related:
  - "common/debugging/bug-report-triage.md"
  - "common/debugging/root-cause-analysis.md"
  - "common/debugging/fix-verification.md"
  - "cpp/runtime/observability-and-diagnostics.md"
  - "cpp/build/toolchain-and-compiler-flags.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Crash Dump Analysis Checklist

**Based on:** C++ Core Guidelines ([C]), NIST log management ([C]), Google SRE incident practices ([A]).
**Scope:** Applies to native crashes in C++ CLIs, services, libraries, and desktop applications where dumps, minidumps, core files, or stack traces are available.

---

## Checklist

### 1. Establish Dump Integrity

- [ ] Crash artifact is missing -> **(C)** collect dump/core/minidump before speculating from logs. [R2]
- [ ] Symbols are unavailable -> **(C)** locate exact symbols for build ID, commit, compiler, and binary version. [R1][R3]
- [ ] Dump may contain sensitive data -> **(C)** handle and redact according to logging/security policy. [R2]

### 2. Identify the Fault Context

- [ ] Stack trace is available -> **(C)** record faulting thread, signal/exception code, instruction pointer, and top application frames. [R1]
- [ ] Optimized or inlined frames obscure state -> **(A)** use disassembly, frame variables, and neighboring frames conservatively. [R3]
- [ ] Multiple threads are present -> **(C)** inspect locks, waits, and thread roles before assigning cause. [R1]

### 3. Separate Symptom From Cause

- [ ] Crash is access violation, SIGSEGV, or SIGABRT -> **(C)** classify whether the immediate fault is null dereference, invalid lifetime, bounds error, assertion, or explicit termination. [R1]
- [ ] Top frame is allocator, STL, or runtime -> **(A)** search caller frames and memory history; do not blame the runtime first. [R1]
- [ ] Crash follows prior logged error -> **(C)** connect logs to crash only when timestamps, correlation IDs, or object identity match. [R2]

### 4. Reproduce or Fence the Defect

- [ ] Input or workload is known -> **(A)** create a reduced repro or replay case. [R3]
- [ ] Reproduction is unavailable -> **(A)** add targeted diagnostics, guards, or crash breadcrumbs before broad rewrites. [R2][R3]
- [ ] Crash is high impact -> **(C)** define mitigation, rollback, or feature disable path while RCA continues. [R3]

### 5. Verify the Fix Against Crash Evidence

- [ ] Fix is proposed -> **(C)** show why the failing frame/state cannot recur. [R1]
- [ ] Repro exists -> **(C)** rerun repro under debug and sanitizer configuration. [R1]
- [ ] No repro exists -> **(A)** verify with targeted tests plus added runtime evidence and state residual uncertainty. [R3]

---

## Decision Tree

```
C++ crash?
  -> Preserve dump and exact symbols
  -> Identify faulting thread/frame/state
  -> Classify immediate fault
  -> Trace likely ownership/input/concurrency cause
  -> Reproduce or add targeted diagnostics
  -> Verify fix against original crash evidence
```

---

## Anti-Patterns

### Anti-Pattern 1: Log-Only Crash Diagnosis

- **Appearance:** A patch is made from the last log line before crash.
- **Trap:** The last log line is easy to see.
- **Consequence:** The real failing thread or corrupted object is missed.
- **Fix:** Use dump state, stack, symbols, and logs together.

### Anti-Pattern 2: Wrong Symbols

- **Appearance:** The stack trace looks plausible but line numbers do not match source.
- **Trap:** Any symbols seem better than raw addresses.
- **Consequence:** The patch targets the wrong code.
- **Fix:** Match symbols by build ID, binary hash, commit, and compiler settings.

---

## See Also

- [Runtime Observability and Diagnostics](../runtime/observability-and-diagnostics.md) - collecting useful crash evidence
- [Root Cause Analysis](../../common/debugging/root-cause-analysis.md) - validating causal claims
- [Fix Verification](../../common/debugging/fix-verification.md) - proving the fix

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C1] C++ Core Guidelines | error handling, lifetime, concurrency | verified-2026 | 2026-06 |
| R2 | C | NIST SP 800-92 | log management and sensitive data handling | verified-2026 | 2026-06 |
| R3 | A | Google SRE Book | incident response and postmortem practice | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
