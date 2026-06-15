---
type: harness
id: "common-input-validation"
title: "Input Validation Checklist"
language: "common"
category: "security"
tier: "N"
scope: "Validate all input at trust boundaries to prevent injection, overflow, and data corruption"
version: "2026.05"
status: "draft"
stable_since: ""
last_validated: "2026-05-31"
review_cycle: "12m"
tags: [security, validation, input, injection, owasp]
based_on:
  - "[N] OWASP Top 10 A03:2021"
  - "[N] NIST SP 800-53 SA-11"
  - "[C] CWE Top 25 (CWE-20, CWE-89, CWE-79)"
  - "[C] SEI/CERT API00-C"
related:
  - "common/ai/prompt-injection-and-llm-security.md"
  - "common/ai/tool-calling-and-agent-control.md"
  - "common/dependencies/dependency-management.md"
  - "common/logging/logging-standards.md"
  - "cpp/functions/parameter-validation.md"
  - "cpp/security/secure-coding.md"
  - "cpp/serialization/parsing-and-validation.md"
  - "cpp/testing/fuzzing.md"
  - "common/ci-cd/pipeline-patterns.md"
  - "projects/snapmaker-orca/coding-standards.md"
supersedes: []
changelog:
  - "2026.05: Initial draft"
---

# Input Validation Checklist

**Based on:** OWASP Top 10 A03:2021 ([N]), NIST SP 800-53 SA-11 ([N]), CWE Top 25 ([C]), SEI/CERT API00-C ([C]).
**Scope:** Ensure all input crossing a trust boundary is validated before use. Applies to HTTP requests, file uploads, CLI args, env vars, API responses.

---

## Concepts

**Trust boundary:** Data crosses from less-trusted to more-trusted context. **Whitelist always preferred over blacklist.** Blacklists are trivially bypassed.

---

## Checklist

### 1. Trust Boundary Identification

- [ ] External input? → **(N)** MUST validate before ANY use (parse, process, store, display). [R1]

### 2. Validation Strategy

- [ ] **(N)** Whitelist: define what IS allowed, reject everything else. [R1][R2]
- [ ] **(C)** Free-text fallback: length limits + charset restriction + format check at minimum. [R3]
- [ ] **(C)** Canonicalize (Unicode NFC, path resolution) BEFORE validation. [R4]

### 3. Injection Prevention

- [ ] Reaches interpreter (SQL, shell, HTML, LDAP)? → **(N)** Parameterized queries/prepared statements. NEVER string-concatenate into commands. [R1]
- [ ] **(C)** If parameterization impossible → context-specific escaping. [R1]

### 4. Type and Range

- [ ] **(N)** Validate type: int is int, string is string. [R2]
- [ ] **(C)** Validate range: numeric min/max, string min/max length. [R3]
- [ ] **(C)** Validate format: email, URL, date, UUID patterns. [R3]

### 5. File Upload Validation

- [ ] **(C)** Check file type by MAGIC BYTES, not extension or Content-Type. [R1]
- [ ] **(C)** Max file size enforced. Store outside web root; generated filenames only. [R1]

### 6. Error Handling on Validation Failure

- [ ] **(C)** Reject. Do NOT silently fix/sanitize. [R1]
- [ ] **(C)** Log failure for monitoring (sanitize the log entry — no raw attack payloads). [R3]
- [ ] **(C)** User-facing error: generic ("Invalid input"). Never reveal expected format. [R2]

### 7. Output Encoding

- [ ] **(C)** Context-dependent encoding at render point, not at validation time. [R1]

---

## Decision Tree

```
Trust boundary? → Whitelist
  ├─ Type check [4]
  ├─ Range/length [4]
  ├─ Format [4]
  ├─ Interpreter? → Parameterize [3]
  └─ File upload? → Magic bytes + size [5]

On failure: reject + safe-log + generic error [6]
Output: encode at render point [7]
```

---

## Anti-Patterns

### 1. Client-Side Only Validation

- **Appearance:** JS form validation, no server check.
- **Fix:** Always validate server-side. Client validation = UX only.

### 2. Silent Input Fixing

- **Appearance:** Strip "dangerous" chars, continue processing.
- **Fix:** Reject invalid input. Let the user fix it.

---

## See Also

- [Parameter Validation (C++)](../../cpp/functions/parameter-validation.md) — C++ contract types, assert vs. if/throw

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | OWASP Top 10 (2021) | A03 Injection | verified-2026 | 2026-05 |
| R2 | N | NIST SP 800-53 | SA-11 | verified-2026 | 2026-05 |
| R3 | C | CWE Top 25 | CWE-20, CWE-89, CWE-79 | verified-2026 | 2026-05 |
| R4 | C | SEI/CERT | API00-C | verified-2026 | 2026-05 |

---

## Changelog

- 2026.05: Initial draft
