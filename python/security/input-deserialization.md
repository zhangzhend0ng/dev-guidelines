---
type: harness
id: "python-input-deserialization"
title: "Python Input Deserialization Checklist"
language: "python"
category: "security"
tier: "N"
scope: "Safely parse JSON, YAML, pickle, and other serialized Python inputs at trust boundaries"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [python, security, deserialization, pickle, yaml, json]
based_on:
  - "[C] Python Documentation"
  - "[N] OWASP Top 10"
  - "[C] NIST SP 800-218 SSDF"
related:
  - "common/security/input-validation.md"
  - "common/logging/logging-standards.md"
  - "python/correctness/type-hints-and-mypy.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Python Input Deserialization Checklist

**Based on:** Python docs ([C]), OWASP Top 10 ([N]), NIST SSDF ([C]).
**Scope:** Applies whenever Python code parses serialized data from files, HTTP, queues, CLIs, environment variables, or model/tool outputs.

---

## Checklist

### 1. Trust Boundary

- [ ] Serialized data is external or user-controlled -> **(N)** treat it as untrusted input and validate before use. [R2]
- [ ] Parser output feeds business logic -> **(C)** convert to a typed/validated structure at the boundary. [R1][R3]

### 2. Unsafe Formats

- [ ] Data may be untrusted -> **(N)** do not use `pickle`, `marshal`, or object-construction deserializers. [R1][R2]
- [ ] Existing code uses pickle for trusted internal data -> **(C)** document trust boundary and reject external exposure. [R1]

### 3. JSON and YAML

- [ ] JSON input is parsed -> **(C)** validate schema, required fields, types, ranges, and unknown fields. [R2][R3]
- [ ] YAML input is parsed -> **(N)** use a safe loader and disable arbitrary object construction. [R2]

### 4. Resource Limits

- [ ] Input size or nesting can be large -> **(C)** enforce size, depth, timeout, and memory limits where feasible. [R2][R3]
- [ ] Parser errors are logged -> **(C)** summarize safely; do not log full sensitive payloads. [R3]

### 5. AI and Tool Outputs

- [ ] LLM/tool output is parsed -> **(C)** treat it as untrusted external input and validate exactly like user input. [R2]
- [ ] Output schema is required -> **(A)** reject unknown fields unless explicitly allowed. [R3]

---

## Decision Tree

```
Serialized input?
  -> untrusted by default
  -> avoid object deserialization
  -> parse with safe loader
  -> validate schema/types/ranges
  -> enforce resource limits
```

---

## Anti-Patterns

### Anti-Pattern 1: Pickle From Upload

- **Appearance:** Uploaded or API-provided data is loaded with `pickle.load`.
- **Trap:** It restores Python objects conveniently.
- **Consequence:** Arbitrary code execution risk.
- **Fix:** Use JSON or another data-only format plus validation.

### Anti-Pattern 2: Parsed Means Valid

- **Appearance:** JSON parse success is treated as validation success.
- **Trap:** The syntax is valid.
- **Consequence:** Missing fields, wrong types, and hostile values reach logic.
- **Fix:** Validate schema and domain constraints after parsing.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C24] Python Documentation | pickle security warning, json | verified-2026 | 2026-06 |
| R2 | N | [N5] OWASP Top 10 | A03 Injection, A08 Software and Data Integrity Failures | verified-2026 | 2026-06 |
| R3 | C | [C6] NIST SP 800-218 SSDF | PW.5, RV.1 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
