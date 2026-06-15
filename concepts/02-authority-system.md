# Authority Tier System Design

## The Problem

Code guidelines cite many kinds of sources: ISO standards, community guidelines, expert books, blog posts. Without systematic weighting, all sources are treated equally — or cherry-picked to support preference.

## The Solution: N/C/A Tiers

Three tiers based on origin, maintenance model, and adoption breadth.

### Normative (N) — "The law"

**Definition:** Official standards from recognized bodies. Formally adopted. Versioned.

**Examples:** ISO 14882, WG21 adopted papers, IETF RFC Standards Track, IEEE 754.

**Key property:** Violation = objectively wrong.

**Review cycle:** 24 months.

### Consensus (C) — "The precedent"

**Definition:** Industry-wide guidelines by recognized professional organizations. Documented version history. Adopted by 3+ independent organizations.

**Examples:** C++ Core Guidelines, SEI/CERT, OWASP Top 10, MISRA C++.

**Key property:** Best current knowledge. Departures require documented reasoning.

**Review cycle:** 12 months. Critical-C sub-band (≥3 harnesses or security-related): 6 months.

### Advisory (A) — "The wisdom"

**Definition:** Expert literature, major org internal standards, community consensus. Context-dependent.

**Examples:** Effective C++ series, Google/LLVM Style Guides, C++ Concurrency in Action.

**Key property:** Valuable but not binding. May conflict with higher tiers. May age poorly.

**Review cycle:** 24 months.

## Conflict Resolution

| Scenario | Rule |
|----------|------|
| N vs. C/A | N wins |
| C vs. A | C wins |
| N vs. N | Newer edition |
| C vs. C | Broader adoption; if tied, file issue |
| A vs. A | More recent publication; cross-check against N/C |
| P vs. N/C/A | P never overrides N/C/A externally; within project, P is enforced regardless |
| P vs. P | Project owner decides; file an issue, discuss, document |

## Tier ≠ Enforcement

The authority tier describes the **source**, not the rule's severity. A C-tier source saying "use `std::scoped_lock`" is as important in practice as an N-tier rule about destructors — but if they conflict, N wins.

We deliberately separate source authority from rule severity. MISRA uses Mandatory/Required/Advisory for rule enforcement; we use N/C/A for source authority. A rule can be both "from an expert book" and "security-critical."

### Project (P) — "The team rule"

**Definition:** Project-internal conventions established by the team. No external authority required. Enforcement is mandatory within the project.

**Examples:** "No exceptions in our codebase," "Allman brace style only," "No Chinese in source," "UTF-8 BOM encoding."

**Key property:** As strictly enforced as N-tier within the project, but carries no weight outside it. Does not override N/C/A assessments in other contexts.

**Review cycle:** 12 months (team review).

**P vs. A distinction:** (A) describes "Meyers says prefer X" — an external voice worth listening to. (P) describes "our team decided X is mandatory" — an internal rule. Both are "non-standard" but (P) is enforced.

## Why Four Tiers?

N/C/A covers source authority across standards, industry consensus, and expert literature. P handles the real case where a team has mandatory conventions with no external standard to cite — the codebase must be consistent, but we don't want to over-claim "this is industry consensus" for something internal.

## See Also

- [Harness Evolution and Lifecycle Governance](../common/meta/harness-evolution.md) — tier challenge resolution process and lifecycle governance
