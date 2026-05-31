# Harness Methodology

## What Is a Harness?

A harness is a **reusable, checklist-based decision document** for code review and code generation. It transforms scattered best practices into a structured workflow: condition → action, backed by authoritative sources at verifiable tiers.

A harness is NOT:
- A tutorial or how-to guide
- A style guide (though it may reference style rules)
- A static rulebook (it has a lifecycle, version, and review cycle)

## Why Checklists?

Checklists are the most reliable tool for reducing human error in complex, repetitive tasks — proven in aviation, surgery, and construction. Software code review is no different.

Each item is a **single, independent decision point**. The reviewer processes items sequentially, marking each done. This transforms code review from "read and hope you notice problems" to "verify each condition systematically."

## The Harness Document Structure

1. **Frontmatter** — machine-readable metadata (tier, version, status, sources)
2. **Prerequisites** — concepts needed to understand the checklist
3. **Checklist** — 5-10 items: condition → action + **(N)**/**(C)**/**(A)** tag + [Rx] reference
4. **Decision Tree** — visual summary of the checklist flow
5. **Anti-Patterns** — Appearance → Trap → Consequence → Fix
6. **See Also** — cross-references (bidirectional)
7. **Reference Sources** — annotated source table with timeliness tags

## Authority Tiers (N/C/A)

Every action is tagged with its source's authority level:

| Tier | Name | Meaning |
|------|------|---------|
| **(N)** | Normative | Formal standard (ISO, IETF, WG21). Non-negotiable. |
| **(C)** | Consensus | Industry-wide guideline (C++ Core Guidelines, SEI/CERT). Strong default. |
| **(A)** | Advisory | Expert literature (Effective C++, Google Style Guide). Context-dependent. |

## Timeliness

Sources decay. Every citation carries a `verified-YYYY` tag and `last_validated` date. Expired → `needs-review`. Obsolete → `deprecated`. This prevents the repo from accumulating outdated advice.

## Harness Lifecycle

```
draft → reviewed → stable → deprecated → archived
```

- **draft**: initial proposal
- **reviewed**: CODEOWNER-approved
- **stable**: used in ≥1 real project for ≥1 month
- **deprecated**: superseded; 12-month grace period
- **archived**: retained for historical reference

## Design Philosophy

1. **Authority over opinion.** Every recommendation traces to a verifiable source.
2. **Mechanical over memory.** Checklists processed systematically, not recalled.
3. **Fresh over frozen.** Review cycles prevent rot.
4. **Specific over vague.** "Use RAII" is vague. "Bind every acquired resource to an owning object in the constructor; release in the destructor; destructor must not throw; mark move operations noexcept" is specific.
