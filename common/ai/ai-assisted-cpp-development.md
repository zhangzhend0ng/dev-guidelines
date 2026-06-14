---
type: harness
id: "common-ai-assisted-cpp-development"
title: "AI-Assisted C++ Development Checklist"
language: "common"
category: "ai"
tier: "C"
scope: "Use AI assistance for C++ software changes without bypassing C++ correctness, safety, testing, and review harnesses"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-14"
review_cycle: "12m"
tags:
  - ai
  - cpp
  - code-generation
  - review
  - verification
based_on:
  - "[C] C++ Core Guidelines"
  - "[C] SEI/CERT C++ Coding Standard"
  - "[C] NIST SP 800-218 SSDF"
  - "[A] dev-guidelines Harness-Driven Development Protocol"
related:
  - "common/ai/tool-calling-and-agent-control.md"
  - "common/ai/prompt-injection-and-llm-security.md"
  - "common/ai/ai-evaluation-and-regression-strategy.md"
  - "common/code-review/harness-driven-review.md"
  - "common/testing/testing-strategy.md"
  - "common/ci-cd/pipeline-patterns.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/memory/ownership.md"
  - "cpp/testing/sanitizers.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# AI-Assisted C++ Development Checklist

**Based on:** C++ Core Guidelines ([C]), SEI/CERT C++ ([C]), NIST SSDF ([C]), dev-guidelines harness protocol ([A]).
**Scope:** Applies when an AI agent writes, modifies, reviews, or explains C++ production code. This harness does not replace C++ topic harnesses; it gates how AI assistance is allowed to use them.

---

## Concepts

| Term | Meaning |
|------|---------|
| AI-authored change | Any code, config, test, or build change generated or materially edited by an AI tool |
| Applicable harness | A harness whose scope matches the changed code, build, dependency, test, or process concern |
| Verification evidence | Compiler, test, sanitizer, static-analysis, or review output that can be inspected after the AI change |

---

## Checklist

### 1. Harness Discovery Before Generation

- [ ] C++ code will be written or changed -> **(A)** Load [Harness-Driven Development](../code-review/harness-driven-review.md) before editing. [R4]
- [ ] The change touches ownership, lifetime, concurrency, templates, exceptions, or integer arithmetic -> **(C)** Load the matching C++ correctness/resource harness before generation. [R1][R2]
- [ ] No applicable harness exists -> **(A)** State the gap in the change notes; do not invent an uncited rule as if it were authoritative. [R4]

### 2. C++ Correctness Boundaries

- [ ] AI proposes raw ownership, pointer arithmetic, casts, or lifetime-sensitive references -> **(C)** Verify against ownership, lifetime, type-safety, and undefined-behavior harnesses before accepting. [R1][R2]
- [ ] AI proposes concurrency or async behavior -> **(C)** Verify data races, synchronization, cancellation, and object lifetime against the thread-safety harness. [R1][R2]
- [ ] AI proposes exception or error handling changes -> **(C)** Verify exception guarantees and error propagation against the relevant harnesses. [R1][R2]

### 3. Build and Toolchain Reality Check

- [ ] AI output changes CMake, include structure, compiler flags, or package config -> **(C)** Validate with the C++ build/package harnesses and a real configure/build run. [R1][R3]
- [ ] AI output uses a library, compiler feature, standard flag, or platform API -> **(C)** Confirm it exists in the target toolchain; do not trust plausible API names. [R1][R3]
- [ ] Target compiler or standard version is unknown -> **(A)** Inspect repository configuration before using newer C++ features. [R4]

### 4. Verification Evidence

- [ ] AI-authored production code compiles -> **(C)** Run the narrowest meaningful build target and record failures before final review. [R3]
- [ ] Behavior changed -> **(C)** Add or update tests that would fail on the previous bug or missing behavior. [R3]
- [ ] Memory, lifetime, undefined behavior, or threading risk exists -> **(C)** Run the applicable sanitizer or static-analysis path when available. [R1][R2][R3]

### 5. Dependency and Supply-Chain Restraint

- [ ] AI suggests a new dependency -> **(C)** Apply dependency-management and C++ package-management harnesses before adding it. [R3]
- [ ] The dependency is only needed for a small utility -> **(A)** Prefer local implementation if it is simpler and testable. [R3]
- [ ] AI suggests downloading code, copying snippets, or vendoring files -> **(C)** Check license, provenance, and maintainability before use. [R3]

### 6. Review Transparency

- [ ] AI made non-trivial design choices -> **(A)** Explain the chosen harnesses, tradeoffs, and verification commands in the review notes. [R4]
- [ ] AI could not run verification -> **(A)** State exactly what was not run and why; do not present the change as fully verified. [R4]
- [ ] Reviewer asks for source of a rule -> **(A)** Cite the harness and reference row, not the AI conversation. [R4]

### 7. No Hallucinated Authority

- [ ] AI cites a standard clause, API, compiler behavior, or security requirement -> **(C)** Verify it against an accepted source before using it as a blocking review claim. [R1][R2][R3]
- [ ] The claim is plausible but uncited -> **(A)** Treat it as a hypothesis until confirmed by source, build, test, or codebase evidence. [R4]

---

## Decision Tree

```
AI will change C++?
  -> Load harness-driven-review
  -> Select C++ topic harnesses
  -> Generate scoped change
  -> Build/test/static-check
  -> Record evidence
  -> Review by harness, not by AI confidence
```

---

## Anti-Patterns

### Anti-Pattern 1: Plausible C++ API

- **Appearance:** AI calls a standard-library or framework method that reads naturally but does not exist in the target version.
- **Trap:** The generated code looks idiomatic and compiles in the model's explanation.
- **Consequence:** Build failure or accidental fallback to a different overload/API.
- **Fix:** Verify against the repository toolchain and build before review.

### Anti-Pattern 2: Harness Laundering

- **Appearance:** The change says "follows best practices" without naming the actual harnesses used.
- **Trap:** The wording sounds authoritative.
- **Consequence:** Reviewers cannot distinguish verified rules from AI preference.
- **Fix:** List applicable harnesses and concrete verification evidence.

### Anti-Pattern 3: Test-After Approval

- **Appearance:** AI-generated code is approved because the diff is small, with tests deferred.
- **Trap:** Small C++ changes can still affect lifetime, ABI, or exception behavior.
- **Consequence:** Undefined behavior or regression reaches integration.
- **Fix:** Require the narrowest meaningful build/test/sanitizer evidence before approval.

---

## See Also

- [Tool Calling and Agent Control](tool-calling-and-agent-control.md) - controls AI tools that edit files, run builds, or call external systems
- [Harness-Driven Development Protocol](../code-review/harness-driven-review.md) - mandatory process for selecting and applying harnesses
- [Testing Strategy](../testing/testing-strategy.md) - test selection and coverage expectations
- [CI/CD Pipeline Patterns](../ci-cd/pipeline-patterns.md) - build and verification automation
- [Undefined Behavior Prevention](../../cpp/correctness/undefined-behavior.md) - C++ undefined behavior risks
- [Smart Pointer and Ownership Semantics](../../cpp/memory/ownership.md) - C++ ownership design
- [Sanitizer Integration and Usage](../../cpp/testing/sanitizers.md) - sanitizer verification paths

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C1] C++ Core Guidelines | General rules, ownership, lifetime, concurrency | verified-2026 | 2026-06 |
| R2 | C | [C2] SEI/CERT C++ Coding Standard | Secure C++ coding rules | verified-2026 | 2026-06 |
| R3 | C | [C6] NIST SP 800-218 SSDF | PW, RV, PS practices | verified-2026 | 2026-06 |
| R4 | A | dev-guidelines Harness-Driven Development Protocol | Part A and Part B | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
