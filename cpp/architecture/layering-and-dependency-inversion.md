---
type: harness
id: "cpp-layering-and-dip"
title: "Layering and Dependency Inversion Checklist"
language: "cpp"
category: "architecture"
tier: "C"
scope: "Govern logical architectural layering and the SOLID principles that shape class/module boundaries (SRP, OCP, DIP): which layer may depend on which, who owns abstractions, and when a design decision is significant enough to record"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-26"
review_cycle: "12m"
tags: [architecture, layering, solid, srp, ocp, dip, dependency-inversion, abstraction-ownership, cross-cutting, adr]
based_on:
  - "[C] C++ Core Guidelines"
  - "[A] Large-Scale C++ Software Design Vol. I (Lakos, 2019)"
  - "[A] Clean Architecture (Martin, 2017)"
related:
  - "cpp/architecture/module-boundaries.md"
  - "cpp/correctness/interface-contracts.md"
  - "cpp/design/feature-design-prerequisites.md"
  - "common/documentation/documentation-standards.md"
supersedes: []
changelog:
  - "2026.07: Initial draft"
---

# Layering and Dependency Inversion Checklist

**Based on:** C++ Core Guidelines ([C]), Large-Scale C++ Vol. I ([A19]), Clean Architecture ([A20]).
**Scope:** Logical architectural design — SOLID principles at class and module level, dependency direction rules, abstraction ownership, cross-cutting concern consistency, and architectural-decision recording.

This harness owns **logical layering**. For **physical** boundary mechanics (header include hygiene, pimpl, build-target enforcement, ABI surface), apply `cpp/architecture/module-boundaries.md` — the two are complementary, not overlapping. For **per-interface contract expression** (precondition/postcondition, ISP/LSP mechanics, NVI), apply `cpp/correctness/interface-contracts.md`.

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|------------|
| Layer | A group of classes/modules at the same abstraction level that collaborate and share a dependency-direction policy |
| Dependency rule (Martin) | Dependencies point **inward** toward higher-level policy; inner layers know nothing of outer layers |
| Dependency Inversion (DIP) | High-level policy must not depend on low-level details; both depend on abstractions. **The abstraction is owned at the layer that consumes it** |
| Abstraction ownership | The interface header lives in the layer that *needs* the contract, not the layer that *implements* it |
| Single Responsibility (SRP) | A class has one reason to change — one actor whose requests force its evolution |
| Open-Closed (OCP) | Adding behavior does not require modifying existing source; extension points absorb change |
| Cross-cutting concern | A policy (logging, error propagation, configuration) that spans multiple layers and must be applied consistently |

---

## Checklist

### 1. Single Responsibility — One Reason to Change **(C)** [R1][R2]

SRP at class/module level (distinct from the function-size heuristic in `review-checklist.md`).

- [ ] Class or module has more than one actor whose requests force changes to the same source → **(C)** split by actor or responsibility, not by line count. [R1][R2]
- [ ] A "utility" or "helper" class accumulates methods serving unrelated callers → **(C)** split into role-cohesive units; do not let a god-class become the default dumping ground. [R2]
- [ ] The class name accurately reflects its single responsibility — if a truthful name would need "And" or "/", the class has more than one responsibility → **(C)** rename is a smell test, not a fix; split. [R1]

### 2. Open-Closed — Extend Without Modifying **(C)** [R1][R2]

Adding a new variant should not require editing existing tested code.

- [ ] A new subtype/variant requires modifying a switch/if-else chain over the existing set → **(C)** introduce a polymorphic interface, `std::variant`+visitor, or strategy template so the new variant is added by extension. [R1][R2]
- [ ] A new configuration case requires editing a function body rather than registering a new handler → **(C)** extract an extension point (callback, factory, or registration mechanism). [R2]
- [ ] OCP achieved via inheritance is weighed against template/variant alternatives — see `cpp/design/feature-design-prerequisites.md` for extension-point selection → **(A)** do not default to inheritance without considering composition. [R1]

### 3. Dependency Inversion — Abstraction Ownership and Direction **(C)** [R1][R2][R3]

High-level policy depends on abstractions; the abstraction header lives where it is consumed.

- [ ] A high-level module `#include`s a low-level concrete class header → **(C)** invert: define an interface in the high-level layer, inject the low-level implementation. [R1][R2]
- [ ] The interface header is co-located with the implementation rather than the consumer → **(C)** move the interface to the consuming layer; the low level implements it. [R3]
- [ ] A low-level module instantiates a high-level type → **(C)** this is an inverted dependency direction; refactor or document the exception. [R1]
- [ ] Dependency injection uses constructor injection for required collaborators and setter/parameter injection for optional ones → **(A)** do not hide required dependencies behind setters. [R2]

### 4. Layer Taxonomy and Dependency Direction **(C)** [R1][R2][R3]

Each class/module is assigned to a layer; dependencies respect the inward rule.

- [ ] A class cannot be placed in presentation / domain / infrastructure (or the project's chosen layering scheme) → **(C)** either it spans layers (split it) or the layering scheme is wrong (record an ADR). [R2][R3]
- [ ] An inner (domain) layer `#include`s or links against an outer (presentation/infrastructure) layer → **(C)** break the upward dependency. [R1]
- [ ] Infrastructure (database, network, filesystem, third-party adapter) is reached only through an interface defined by the domain layer, not by direct `#include` of the infra type → **(C)** wrap with an abstraction owned by the domain. [R2]
- [ ] The layering scheme is not the textbook three layers (e.g., a plugin host, an event pipeline) → **(A)** the dependency-direction rule still applies; document the scheme and its allowed edges in an ADR. [R3]

### 5. Cross-Cutting Concerns Consistency Across Layers **(C)** [R1][R2]

Logging, error propagation, and configuration must be applied uniformly across layers — not invented per layer.

- [ ] Different layers use different logging APIs, severity conventions, or correlation-ID propagation → **(C)** unify through a single logging abstraction; cross-link to `common/logging/logging-standards.md`. [R1]
- [ ] Error propagation crosses a layer boundary and is translated inconsistently (e.g., infrastructure exception caught and re-thrown as raw at domain, or swallowed silently) → **(C)** define a per-layer error-translation policy; cross-link to `cpp/error-handling/result-vs-exception.md` for mechanism selection. [R1][R2]
- [ ] Configuration is read directly from environment/registry at multiple layers rather than injected at a single boundary → **(C)** centralize configuration loading; inject values, do not let layers fetch their own. [R2]
- [ ] A project-level (P) policy constrains cross-cutting decisions (e.g., SnapmakerOrca disables exceptions) → **(P)** the project policy is the floor; this harness layers on top and must not contradict it. [R3]

### 6. Architectural Decision Recording Trigger **(A)** [R1][R3]

Not every design choice needs an ADR — but these do.

- [ ] A decision inverts or relaxes the dependency rule (e.g., a documented upward dependency for pragmatic reasons) → **(A)** record an ADR with context, alternatives considered, and consequences. [R3]
- [ ] A new layering scheme is introduced, or the existing scheme is materially altered → **(A)** record an ADR. [R2][R3]
- [ ] A cross-cutting concern policy is established or changed → **(A)** record an ADR or update the project convention doc. [R2]
- [ ] The decision is reversible and low-cost → **(A)** no ADR required; a code comment suffices. [R3]
- [ ] ADR format follows `common/documentation/documentation-standards.md` → **(A)** do not invent a parallel template. [R3]

### 7. AI / Reviewer Gate — Reject Cross-Layer Proposals Without Justification **(C)** [R1]

- [ ] AI proposes a cross-layer include or upward dependency and the boundary rules do not permit it → **(C)** reject unless accompanied by an ADR or an explicit documented exception. [R1]
- [ ] AI proposes a new abstraction without placing it in the consuming layer → **(C)** require the abstraction header to be relocated before approving. [R2]
- [ ] AI proposes a "convenience" logging/configuration call that bypasses the project's cross-cutting abstraction → **(C)** reject; route through the abstraction. [R1]

---

## Quick Decision Tree

```
New class or module introduced
  │
  ├─ Single responsibility? ─────── NO → split [1]
  │
  ├─ Will new variants need to extend it? ── YES → OCP: extension point [2]
  │                                            ↓ choose mechanism: see feature-design-prerequisites
  │
  ├─ Depends on a lower concrete layer? ── YES → DIP: invert, own abstraction at consumer [3]
  │
  ├─ Which layer does it belong to? ── unclear → ADR or split [4]
  │
  ├─ Does it cross a layer boundary for a cross-cutting concern?
  │     └─ YES → use the project's logging/error/config abstraction [5]
  │
  ├─ Is the decision significant / inverted / scheme-altering? ── YES → ADR [6]
  │
  └─ Reviewer: AI proposes cross-layer include or new abstraction placement?
        └─ reject unless ADR'd [7]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Abstraction Owned by the Implementer

- **Appearance:** `domain/IDataSource.hpp` is physically located under `infrastructure/database/`, and the domain layer `#include`s it via a relative path into infra.
- **Trap:** Co-location feels convenient — the interface and its implementation live together.
- **Consequence:** The high-level layer now physically depends on the low-level layer's directory, build target, and transitive includes. The "inversion" is in name only; the dependency arrow still points down. Build coupling and rebuild fan-out grow; the infra layer cannot be swapped without touching domain headers.
- **Fix:** Move the interface header to the consuming (domain) layer. The infrastructure layer implements it and depends upward on the domain abstraction — the correct direction.

### Anti-Pattern 2: Per-Layer Reinvention of a Cross-Cutting Concern

- **Appearance:** The domain layer returns `std::optional<T>` to signal "not found"; the infrastructure layer throws `std::runtime_error`; the presentation layer returns a HTTP 500. Each layer invents its own translation rule inline.
- **Trap:** Each layer's local choice is defensible in isolation.
- **Consequence:** Error semantics are lost across boundaries. "Not found" becomes a 500. Logs carry inconsistent severity. Operators cannot correlate. The system has no single source of truth for error policy.
- **Fix:** Define the cross-cutting error-translation policy once (cross-link `cpp/error-handling/result-vs-exception.md`). Apply it at every layer boundary as a mechanical translation, not an ad-hoc decision.

### Anti-Pattern 3: Documented Upward Dependency Without an ADR

- **Appearance:** A code comment says `// NOTE: domain depends on presentation here for pragmatic reasons — see TODO` with no ADR.
- **Trap:** The comment acknowledges the smell, which feels responsible.
- **Consequence:** The exception quietly becomes the rule as new contributors copy the pattern. There is no record of the alternatives considered, the conditions under which the exception should be revisited, or the cost of the deviation.
- **Fix:** An acknowledged deviation is exactly when an ADR is required. Record context, alternatives, consequences, and a revisit condition. Without it, the "exception" has no reviewable basis.

---

## See Also

- [Module Boundaries](module-boundaries.md) — physical boundary mechanics (headers, pimpl, build targets, ABI surface). This harness owns the logical rules; that one owns the physical mechanics.
- [Interface Contracts](../correctness/interface-contracts.md) — per-interface ISP/LSP/NVI mechanics. This harness decides layer placement and abstraction ownership; that one decides contract expression.
- [Feature Design Prerequisites](../design/feature-design-prerequisites.md) — what to design before writing a new class/module. Layer assignment is one of those prerequisites.
- [Documentation Standards](../../common/documentation/documentation-standards.md) — ADR format. This harness triggers when an ADR is needed; that one defines how to write it.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C1] C++ Core Guidelines | Interfaces, source organization, class design | verified-2026 | 2026-07 |
| R2 | A | [A20] Clean Architecture (Martin) | SOLID, dependency rule, component boundaries | verified-2026 | 2026-07 |
| R3 | A | [A19] Large-Scale C++ Vol. I (Lakos) | Packages, layering, physical/logical coupling | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft — 7 items covering SRP, OCP, DIP/abstraction ownership, layer taxonomy, cross-cutting consistency, ADR triggers, and AI/reviewer cross-layer gate
