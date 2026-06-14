---
type: harness
id: "cpp-fuzzing"
title: "C++ Fuzzing Checklist"
language: "cpp"
category: "testing"
tier: "C"
scope: "Apply fuzz testing to C++ parsers, decoders, validators, protocol handlers, and security-sensitive input surfaces"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags: [fuzzing, libfuzzer, afl, honggfuzz, sanitizers, security]
based_on:
  - "[C] Google Fuzzing / OSS-Fuzz guidance"
  - "[C] LLVM libFuzzer Documentation"
  - "[C] CWE Top 25"
  - "[A] AFL++ Documentation"
related:
  - "common/security/input-validation.md"
  - "common/testing/testing-strategy.md"
  - "cpp/serialization/parsing-and-validation.md"
  - "cpp/testing/property-based-testing.md"
  - "cpp/testing/mutation-testing.md"
  - "cpp/testing/sanitizers.md"
  - "cpp/testing/static-analysis.md"
  - "cpp/security/secure-coding.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Fuzzing Checklist

**Based on:** Google fuzzing/OSS-Fuzz guidance ([C]), LLVM libFuzzer docs ([C]), CWE Top 25 ([C]), AFL++ docs ([A]).
**Scope:** Applies to C++ code that parses, decodes, validates, transforms, or executes behavior based on untrusted inputs.

---

## Checklist

### 1. Fuzz Target Selection

- [ ] Code parses files, network frames, serialized data, text protocols, compression, images, or model/tool output -> **(C)** create fuzz targets for the trust boundary. [R1][R3]
- [ ] Code has prior crash/security bugs -> **(C)** add minimized reproducers to the corpus. [R1]

### 2. Harness Design

- [ ] Fuzz target has global state or external I/O -> **(C)** isolate it and make each run deterministic. [R1][R2]
- [ ] Target accepts structured input -> **(A)** use dictionaries, seed corpus, or custom mutators. [R2][R4]

### 3. Sanitizer Pairing

- [ ] Fuzzing C++ memory-unsafe code -> **(C)** run with ASan/UBSan at minimum. [R1][R2]
- [ ] Target has concurrency -> **(A)** add separate stress or TSan coverage where practical. [R2]

### 4. Corpus and Regression

- [ ] Fuzzer finds a crash -> **(C)** minimize input and add it as regression test. [R1]
- [ ] Corpus grows large -> **(A)** minimize corpus and keep CI runtime bounded. [R1]

### 5. CI Gate

- [ ] Fuzz target is security-sensitive -> **(C)** run short fuzz smoke in PR and longer scheduled fuzzing. [R1]
- [ ] Fuzzing is too slow -> **(A)** gate on regression corpus in PR and fuzz continuously out of band. [R1]

---

## Decision Tree

```
Untrusted parser/decoder/validator?
  -> Create fuzz target
  -> Add seed corpus
  -> Run with sanitizers
  -> Minimize crashes
  -> Add regressions and scheduled fuzzing
```

---

## Anti-Patterns

### Anti-Pattern 1: Fuzzing Without Sanitizers

- **Appearance:** Fuzzer only detects crashes.
- **Trap:** It still finds some bugs.
- **Consequence:** UB and memory defects are missed.
- **Fix:** Pair fuzzing with ASan/UBSan.

### Anti-Pattern 2: Crash Fixed but Corpus Lost

- **Appearance:** Bug is fixed but the crashing input is not retained.
- **Trap:** The immediate issue is gone.
- **Consequence:** Regression can return silently.
- **Fix:** Minimize and commit regression input or generated test.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Google Fuzzing / OSS-Fuzz guidance | Targeting, corpus, regression | verified-2026 | 2026-06 |
| R2 | C | LLVM libFuzzer Documentation | Target design and sanitizer use | verified-2026 | 2026-06 |
| R3 | C | [C3] CWE Top 25 | Parser, bounds, memory weaknesses | verified-2026 | 2026-06 |
| R4 | A | AFL++ Documentation | Dictionaries and fuzzing strategy | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
