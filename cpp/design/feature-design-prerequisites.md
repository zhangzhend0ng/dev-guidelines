---
type: harness
id: "cpp-feature-design-prerequisites"
title: "Feature Design Prerequisites Checklist"
language: "cpp"
category: "design"
tier: "C"
scope: "Decide what must be designed and documented BEFORE writing code for a new C++ class, module, or feature: responsibility, entity classification, state and invariants, extension-point mechanism, public surface, and failure modes"
version: "2026.07.2"
status: "draft"
stable_since: ""
last_validated: "2026-07-27"
review_cycle: "12m"
tags: [design, feature-design, prerequisites, domain-modeling, value-type, entity, state-machine, extension-point, public-api, failure-modes]
based_on:
  - "[C] C++ Core Guidelines"
  - "[A] Effective C++ (Meyers)"
  - "[A] C++ Templates: The Complete Guide (2/e)"
  - "[A] Clean Architecture (Martin, 2017)"
  - "[A] Domain-Driven Design (Evans, 2003)"
related:
  - "cpp/correctness/interface-contracts.md"
  - "cpp/architecture/layering-and-dependency-inversion.md"
  - "cpp/api/abi-compatibility.md"
  - "common/commits/conventional-commits.md"
  - "common/planning/task-decomposition.md"
  - "common/code-review/harness-driven-review.md"
supersedes: []
changelog:
  - "2026.07: Initial draft"
---

# Feature Design Prerequisites Checklist

**Based on:** C++ Core Guidelines ([C]), Effective C++ ([A1]), C++ Templates Complete Guide ([A4]), Clean Architecture ([A20]), Domain-Driven Design ([A21]).
**Scope:** The design-artifact gate before writing code for a new class, module, or non-trivial feature. This harness answers **what to design**; `cpp/correctness/interface-contracts.md` answers how to **express** contracts; `cpp/architecture/layering-and-dependency-inversion.md` answers where a class **belongs** in the architecture.

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|------------|
| Design artifact | A short written record (header comment, design note, ADR) capturing the decisions below before code is written |
| Value type | Immutable, identity-less; compared by value; cheap to copy (e.g., `Money`, `Point`) |
| Entity | Has identity and lifecycle; mutable state tracked over time (e.g., `Order`, `Session`) |
| Service / Policy | Stateless (or environment-bound) operation; behavior, not data (e.g., `TaxCalculator`) |
| Invariant | A condition that always holds for valid objects of the type, established by constructors and preserved by every method |
| Extension point | A deliberate seam where future variants can be added without modifying existing source |
| Public surface | The set of declarations a consumer may legitimately depend on (the API contract, not the implementation) |

**When this harness applies:** before writing any new class, struct, module, or non-trivial free-function group. **When it does NOT apply:** trivial one-liners, local lambdas inside a single function, generated code.

---

## Checklist

### 1. Design Artifact Exists Before Code **(A)** [R1][R2]

- [ ] New non-trivial class, module, or feature has no written design record → **(A)** produce one (header doc-comment block, design note, or ADR) before writing the body. Trivial helpers are exempt. [R1][R2]
- [ ] The design record is co-located with the code it governs (header doc-comment) or in a discoverable location (ADR under `docs/`) → **(A)** do not let design live only in chat or memory. [R2]
- [ ] The change is a refactor with no new behavior → **(A)** no new design artifact required; the existing one still applies. [R1]

### 2. Responsibility Statement (SRP) **(A)** [R1][R2]

- [ ] The type/module cannot be described in a single sentence of the form "An X that does Y" without using "and" → **(A)** it has more than one responsibility; split. [R1][R2]
- [ ] Two unrelated change-driving actors touch the same class → **(A)** split by actor. [R2]
- [ ] The responsibility statement is recorded in the design artifact → **(A)** a name alone is not enough; the *what it does* must be explicit. [R1]

### 3. Entity Classification — Value / Entity / Service **(A)** [R1][R3]

- [ ] The type is classified explicitly as value type, entity, or service/policy before its interface is drafted → **(A)** the classification drives copy semantics, equality, mutability, and lifetime. [R3]
- [ ] A value type is immutable, cheap to copy, and compared by value (no identity) → **(A)** if it needs identity or mutation, it is an entity, not a value. [R3]
- [ ] An entity has a defined identity, lifecycle, and persistence boundary → **(A)** document where its state lives and who owns its lifetime. [R3]
- [ ] A service/policy is stateless or environment-bound only (no per-instance mutable data) → **(A)** if it accumulates per-instance state, re-classify as entity. [R2]
- [ ] Classification is ambiguous (e.g., a value with identity) → **(A)** record the decision and rationale; do not leave it implicit. [R3]
- [ ] A value type carries a runtime status field (success/failure/cancel, e.g. `Result<T>`/`Outcome`/`BatchMatchResult.error_code`) → **(A)** the status field is a **value projection** of the runtime state whose single source of truth is the producer path/object. Document which path writes the status and that readers treat it as derived, not authoritative. Without this rule the status field and its producer drift (the original source mutates state but forgets to sync the value field). [R3]

### 4. State and Invariants Documented **(C)** [R1][R2]

- [ ] All class invariants are enumerated in the design artifact (e.g., "size_ <= capacity_", "host_ is non-empty when connected_") → **(C)** every method preserves them or the invariant list is incomplete. [R1]
- [ ] The type has ≥3 states (including initial/terminal) → **(C)** draw or describe the state machine: states, transitions, and the events that trigger them. [R1]
- [ ] A transition is reachable from multiple states with different outcomes → **(C)** the state machine must show this; implicit "we'll handle it" is a bug source. [R2]
- [ ] Concurrency touches the state → **(C)** cross-link to `cpp/concurrency/thread-safety.md`; document the synchronization contract. [R1]

### 5. Extension-Point Mechanism Chosen and Justified **(A)** [R1][R2][R4]

- [ ] A future variant or behavior swap is anticipated → **(A)** choose and record the extension-point mechanism: template/CRTP, runtime polymorphism, `std::function`/callback, or `std::variant`+visitor. [R1][R4]
- [ ] Runtime polymorphism chosen when the variant set is closed and known at compile time → **(A)** reconsider template or variant; runtime indirection has a cost that closed sets do not need to pay. [R4]
- [ ] `std::function` chosen for an extension point that is called in a hot path → **(A)** document the overhead or pick a template/lambda-based design. [R4]
- [ ] Inheritance chosen when the project (P) policy forbids multiple/virtual inheritance → **(P)** respect the project floor; prefer composition or variant. [R2]
- [ ] The chosen mechanism is recorded with a one-line rationale in the design artifact → **(A)** future maintainers must not have to reverse-engineer why. [R1]

### 6. Public Surface Minimized **(C)** [R1][R2]

- [ ] A method, friend, or data member is public without an identified consumer → **(C)** make it private/protected; expose only what is consumed. [R1]
- [ ] Getters/setters mirror every private field by default → **(C)** this is not encapsulation; expose behavior, not state. [R2]
- [ ] The type is intended for use outside its owning package → **(C)** cross-link to `cpp/architecture/module-boundaries.md` and `cpp/api/abi-compatibility.md`; the public surface is now a contract. [R1]
- [ ] Versioning implications exist (breaking change risk) → **(C)** cross-link to `common/commits/conventional-commits.md` for SemVer policy. [R2]

### 7. Failure Modes and Collaborators Declared **(C)** [R1][R2]

- [ ] Every operation that can fail has its failure mode declared: exception, `std::optional`, `std::expected`, error code, or precondition (narrow contract) → **(C)** cross-link to `cpp/error-handling/result-vs-exception.md` for mechanism; the design must commit to one. [R1]
- [ ] Collaborators (injected dependencies) are listed with their role and lifetime ownership → **(C)** unclear ownership is a use-after-free waiting to happen; cross-link to `cpp/memory/ownership.md`. [R1]
- [ ] Resource acquisition (file, socket, lock, memory) is identified → **(C)** RAII ownership must be specified at design time, not retrofitted; cross-link to `cpp/memory/raii.md`. [R1]
- [ ] Destructors release resources and the failure mode of release is considered → **(C)** destructors must not throw; cross-link to `cpp/correctness/exception-safety.md`. [R2]

---

## Quick Decision Tree

```
About to write a new class / module / feature?
  │
  ├─ Trivial (one-liner, local lambda)? ── YES → exempt; proceed
  │
  ├─ [1] Design artifact created? ── NO → write it first
  │
  ├─ [2] Single-sentence responsibility? ── NO → split (SRP)
  │
  ├─ [3] Value / Entity / Service? ── unclear → classify and record
  │
  ├─ [4] ≥3 states or non-trivial invariants? ── YES → state machine + invariant list
  │
  ├─ [5] Future variants expected? ── YES → pick extension-point mechanism + record rationale
  │
  ├─ [6] Public surface? ── minimize; cross-link module-boundaries/abi if cross-package
  │
  └─ [7] Failure modes + collaborators + ownership declared? ── NO → declare before coding
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Design Emerges From Implementation

- **Appearance:** The author writes the class, then derives the "design" by summarizing what they built.
- **Trap:** Writing code first feels productive; the design document feels like documentation overhead.
- **Consequence:** Invariants, entity classification, and extension-point choices are reverse-engineered from code that was never deliberately chosen. The resulting design encodes accidents, not decisions. Refactors later reveal that the "design" never justified the shape it has.
- **Fix:** The design artifact is a prerequisite (item 1), not a deliverable. Write responsibility, classification, state, and extension point before the body.

### Anti-Pattern 2: Default-to-Inheritance Extension Points

- **Appearance:** Every anticipated future variant gets a virtual function, "just in case."
- **Trap:** Inheritance is the most familiar extension mechanism; it feels safe and idiomatic.
- **Consequence:** The class accumulates virtual functions for variants that never come, paying indirection cost forever. When a real variant arrives, the inheritance hierarchy may be the wrong shape (see LSP in `interface-contracts.md`). Project policies that forbid multiple/virtual inheritance are silently violated.
- **Fix:** Choose the extension-point mechanism deliberately (item 5). Default to composition, template, or variant unless runtime polymorphism is genuinely required.

### Anti-Pattern 3: Public Surface Grows by Convenience

- **Appearance:** A private helper is made public "so another class can call it," then a third class starts depending on it.
- **Trap:** Making something public is a one-line change; restricting it later is a breaking change.
- **Consequence:** The public surface expands without design. Each addition becomes a de facto contract. Future refactors are blocked by consumers that materialized against accidental API.
- **Fix:** Public surface is minimized by default (item 6). Every public declaration has an identified consumer. Cross-package exposure triggers the module-boundaries and ABI harnesses.

---

## See Also

- [Interface Contracts](../correctness/interface-contracts.md) — precondition/postcondition, ISP/LSP, NVI, noexcept contracts. This harness decides *what* to design; that one decides how to *express* the contract.
- [Layering and Dependency Inversion](../architecture/layering-and-dependency-inversion.md) — where a class belongs and what it may depend on. Layer assignment is a prerequisite input to this harness.
- [ABI Compatibility](../api/abi-compatibility.md) — binary stability of public C++ APIs. This harness minimizes the public surface; that one keeps it binary-stable.
- [Conventional Commits](../../common/commits/conventional-commits.md) — SemVer policy when a public-surface change is a breaking change.
- [Task Decomposition](../../common/planning/task-decomposition.md) — splitting work into reviewable units. This harness is the design gate that task-decomposition's "harness selection" step invokes.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C1] C++ Core Guidelines | Class design, interfaces, resource management | verified-2026 | 2026-07 |
| R2 | A | [A1] Effective C++ (Meyers) | Items on interface design, minimal APIs | verified-2026 | 2026-07 |
| R3 | A | [A21] Domain-Driven Design (Evans) | Value object vs entity, ubiquitous language | verified-2026 | 2026-07 |
| R4 | A | [A4] C++ Templates: Complete Guide | Static vs dynamic polymorphism, extension mechanisms | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft — 7 items covering design artifact, SRP, entity classification, state/invariants, extension-point selection, public-surface minimization, and failure-mode/collaborator declaration
- 2026.07.1: Item-tier correction. Items 1 (design artifact), 2 (SRP), 3 (entity classification), 5 (extension-point mechanism) downgraded C→A. C++ Core Guidelines [C1] addresses interface/resource mechanics, not these design-process or DDD/SOLID-adjacent decisions as named principles. Items 4 (invariants — C1 I.x), 6 (minimal interface — C1 I.23), 7 (failure/ownership — C1 R.x/E.x) retain (C) with genuine C1 backing. Overall harness tier remains C. Per `harness-quality-standards.md` Anti-Pattern 2 (Tier Inflation).
- 2026.07.2: Item 3 (entity classification) — added bullet covering value types carrying runtime status fields (Result/Outcome pattern). First real-review feedback: status fields like `BatchMatchResult.error_code` drift from their producer path when the "value projection of runtime state" rule is left implicit.
