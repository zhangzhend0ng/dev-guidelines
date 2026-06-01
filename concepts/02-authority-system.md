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

## Tier ≠ Enforcement

The authority tier describes the **source**, not the rule's severity. A C-tier source saying "use `std::scoped_lock`" is as important in practice as an N-tier rule about destructors — but if they conflict, N wins.

We deliberately separate source authority from rule severity. MISRA uses Mandatory/Required/Advisory for rule enforcement; we use N/C/A for source authority. A rule can be both "from an expert book" and "security-critical."

## Why Three Tiers?

Two tiers (standard vs. everything else) lumps expert literature with blog posts. Four tiers adds complexity without discrimination power. Three tiers cleanly separate: standards bodies → professional consensus → individual expertise.

## See Also

- [Harness Evolution and Lifecycle Governance](../common/meta/harness-evolution.md) — tier challenge resolution process and lifecycle governance
