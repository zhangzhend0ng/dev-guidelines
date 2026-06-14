---
type: harness
id: "cpp-parsing-validation"
title: "C++ Parsing and Validation Checklist"
language: "cpp"
category: "serialization"
tier: "C"
scope: "Parse and validate serialized, textual, binary, and protocol inputs in C++ without unsafe partial states or unchecked trust-boundary assumptions"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [parsing, serialization, validation, binary-format, protocol]
based_on:
  - "[C] SEI/CERT C++ Coding Standard"
  - "[C] CWE Top 25"
  - "[C] OWASP ASVS"
  - "[C] C++ Core Guidelines"
related:
  - "common/security/input-validation.md"
  - "cpp/security/secure-coding.md"
  - "cpp/correctness/integer-safety.md"
  - "cpp/correctness/type-safety.md"
  - "cpp/testing/fuzzing.md"
  - "cpp/testing/property-based-testing.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Parsing and Validation Checklist

**Based on:** SEI/CERT C++ ([C]), CWE Top 25 ([C]), OWASP ASVS ([C]), C++ Core Guidelines ([C]).
**Scope:** Applies to C++ parsers, deserializers, decoders, protocol handlers, config readers, and model/tool output consumers.

---

## Checklist

### 1. Trust Boundary

- [ ] Data comes from file, network, IPC, plugin, environment, user, dependency, or model output -> **(C)** treat it as untrusted until fully parsed and validated. [R1][R2][R3]
- [ ] Parser accepts multiple formats or versions -> **(C)** validate version and feature flags before dispatch. [R2]

### 2. Parse Then Validate

- [ ] Parser builds objects incrementally -> **(C)** avoid exposing partially valid objects. [R1][R4]
- [ ] Validation fails -> **(C)** reject and preserve no externally visible partial state. [R1][R3]
- [ ] Parser silently fixes malformed input -> **(C)** reject unless canonicalization is explicitly specified. [R3]

### 3. Size and Bounds

- [ ] Input controls length, count, index, offset, allocation, recursion depth, or nesting -> **(C)** validate limits before allocation or access. [R1][R2]
- [ ] Integer conversion or arithmetic is used -> **(C)** apply integer and type-safety harnesses. [R1][R4]

### 4. Error Reporting

- [ ] Parse error is user-visible -> **(A)** report enough context to fix input without leaking internals. [R3]
- [ ] Parse error is security-sensitive -> **(C)** avoid echoing raw attack payloads into logs. [R3]

### 5. Verification

- [ ] Parser handles untrusted input -> **(C)** add fuzzing and representative invalid cases. [R2]
- [ ] Format has round-trip semantics -> **(A)** add property-based round-trip tests. [R4]
- [ ] AI generates parser code -> **(A)** require static analysis, fuzz/property tests, and NOT VERIFIED if commands did not run. [R4]

---

## Decision Tree

```
Parsing untrusted input?
  -> Validate version/size/bounds
  -> Build no exposed partial state
  -> Reject malformed input
  -> Add fuzz + property tests
```

---

## Anti-Patterns

### Anti-Pattern 1: Allocation Before Bounds Check

- **Appearance:** Length field controls vector allocation before validation.
- **Trap:** The length is part of the format.
- **Consequence:** OOM, overflow, or denial of service.
- **Fix:** Validate length, count, nesting, and arithmetic before allocation.

### Anti-Pattern 2: Lenient Parser as Security Boundary

- **Appearance:** Parser accepts malformed input and guesses intent.
- **Trap:** It improves compatibility.
- **Consequence:** Ambiguous inputs bypass validation.
- **Fix:** Canonicalize only by specification; otherwise reject.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C2] SEI/CERT C++ Coding Standard | Input, memory, integer rules | verified-2026 | 2026-06 |
| R2 | C | [C3] CWE Top 25 | Bounds, integer, parser weaknesses | verified-2026 | 2026-06 |
| R3 | C | [C8] OWASP ASVS | Input validation, error handling, logging | verified-2026 | 2026-06 |
| R4 | C | [C1] C++ Core Guidelines | Type, bounds, interface rules | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
