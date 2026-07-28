---
type: harness
id: "common-harness-evolution"
title: "Harness Evolution and Lifecycle Governance"
language: "common"
category: "meta"
tier: "A"
scope: "Govern how coding guideline harnesses evolve through their lifecycle, from draft proposal to archival, ensuring authority integrity and cross-reference consistency"
version: "2026.07.1"
status: "draft"
stable_since: ""
last_validated: "2026-07-27"
review_cycle: "12m"
tags:
  - harness-governance
  - lifecycle
  - evolution
  - deprecation
  - tier-challenge
based_on:
  - "[A] dev-guidelines Design Spec — Sections 2.6, 3.3, 3.4"
  - "[A] dev-guidelines CONTRIBUTING.md — Harness Lifecycle Gates"
  - "[A] dev-guidelines Authority System (concepts/02-authority-system.md)"
related:
  - "concepts/01-harness-methodology.md"
  - "concepts/02-authority-system.md"
  - "common/meta/prior-art-and-reuse.md"
  - "common/meta/harness-quality-standards.md"
  - "common/code-review/harness-driven-review.md"
supersedes: []
changelog:
  - "2026.05: Initial draft"
  - "2026.07: Fix Item 6 — corrected false claim that validate.py catches one-way (non-bidirectional) related links. validate.py checks link existence only; bidirectionality is a human gate enforced by harness-quality-standards.md item 5."
  - "2026.07.1: Item 3 — added feedback-signal trigger. When check_feedback_signals.py reports a harness has accumulated ≥3 same-type signals in harness-feedback-log.md, trigger re-review within 4 weeks. Closes the evolution-side of the distillation->evolution bridge: review B6 writes signals, this item reads them."
---

# Harness Evolution and Lifecycle Governance

**Based on:** dev-guidelines Design Spec ([A]), CONTRIBUTING.md ([A]), Authority System concepts ([A]).
**Scope:** Define when and how a harness transitions between lifecycle states, how to challenge tier assignments, what triggers mandatory review, and when to deprecate or split a harness. This harness governs the evolution process itself — every harness in this repository is subject to these rules.

---

## Prerequisites / Concepts

**Harness Lifecycle States:**

| State | Meaning | Entered By |
|-------|---------|------------|
| `draft` | Initial proposal, not yet approved | Author creates PR |
| `reviewed` | CODEOWNER-approved, ready for use | PR approval + validation pass |
| `stable` | Proven in real code review | Used ≥1 project, ≥1 month |
| `deprecated` | Superseded or withdrawn | Superseding harness published |
| `archived` | Historical record only | 12 months after deprecation |

**Review Cycle Cadence:**

| Tier | Review Cycle | Rationale |
|------|-------------|-----------|
| N (Normative) | 24 months | Standards evolve slowly |
| C (Consensus) | 12 months (Critical-C: 6 months) | Industry practices shift faster |
| A (Advisory) | 24 months | Book editions are relatively stable |

**Authority Hierarchy:** N overrides C overrides A. Newer edition wins for same-tier conflicts. See [Authority System](../../concepts/02-authority-system.md) for full conflict resolution.

---

## Checklist

### 1. State Transition Gate: draft → reviewed

Is this harness ready for CODEOWNER approval?

- [ ] All frontmatter fields present and valid → **(A)** Proceed to PR [R1]
- [ ] `validate.py` exits 0 (no frontmatter, xref, or ID errors) → **(A)** Proceed to PR [R1]
- [ ] Checklist has 5–12 items, each with condition branches and tier tags → **(A)** Proceed to PR [R1]
- [ ] All reference sources have timeliness tags (`verified-YYYY`) → **(A)** Proceed to PR [R1]
- [ ] Any of the above missing → **(A)** Fix before opening PR. Incomplete frontmatter blocks review. [R1]

### 2. State Transition Gate: reviewed → stable

Has this harness been used in real code review?

- [ ] Applied in ≥1 real project code review for ≥1 month → **(A)** Update `status: "stable"`, set `stable_since` date, bump version. [R1]
- [ ] Applied but found a correctness issue → **(A)** Fix the issue, reset the clock — 1 month from the fix. [R1]
- [ ] Not yet applied to any real project → **(A)** Remain `reviewed`. Do not promote without evidence. [R1]

### 3. Mandatory Review Trigger Detection

What signals indicate this harness needs re-review now (regardless of `review_cycle`)?

- [ ] A `based_on` source has a new edition or revision → **(N)/(C)/(A)** Trigger re-review within 3 months. Update timeliness tags. [R2]
- [ ] A `related` harness changed tier or was deprecated → **(A)** Check for contradiction. Update cross-references. [R1]
- [ ] `validate.py --stale` reports this harness overdue → **(A)** Schedule review within 4 weeks. [R1]
- [ ] `check_feedback_signals.py` reports this harness has accumulated ≥3 same-type signals in `common/meta/harness-feedback-log.md` → **(A)** Trigger re-review within 4 weeks. Same-type accumulation (e.g., 3× "inoperable") is stronger evidence than scattered signals. Run the script quarterly or after any review that logged an entry. [R1]
- [ ] An authority-challenge issue was filed against this harness → **(A)** Resolve within 2 weeks. See Item 5. [R3]
- [ ] None of the above → **(A)** Defer to `review_cycle`-based review. [R1]

### 4. Deprecation Decision

Should this harness be deprecated?

- [ ] A new harness explicitly claims this one via `supersedes` → **(A)** Set `status: "deprecated"`, add `superseded_by` reference, keep for 12-month grace period. [R1]
- [ ] All `based_on` sources are withdrawn/obsolete AND no replacement sources exist → **(A)** Deprecate. If the practice itself is harmful, note this in the changelog. [R1]
- [ ] The practice described is now known to be actively harmful → **(N)/(C)** Deprecate immediately, publish a prominent warning in the harness body. [R1][R2]
- [ ] Only one checklist item is obsolete, the rest are valid → **(A)** Do NOT deprecate. Remove the obsolete item (with changelog entry) and keep the harness. [R1]

### 5. Tier Challenge Resolution

A contributor disputes the authority tier of a recommendation. How to resolve?

- [ ] Challenger provides ≥2 sources at the claimed tier (or higher) → **(A)** CODEOWNER adjudicates. If upheld, update tier and sources. [R3]
- [ ] Challenger provides a single higher-tier source → **(A)** CODEOWNER adjudicates. N-tier source trumps C-tier recommendation — update immediately. [R3]
- [ ] Challenger provides no sources, only opinion → **(A)** Reject. Tier challenges require evidence. [R3]
- [ ] Use the `authority-challenge` issue template — do not bury challenges in PR comments. [R3]

### 6. Cross-Reference Drift Prevention

When harness A links to harness B via `related`, how to keep them consistent?

- [ ] Harness B is created or modified → **(A)** Check that A's `related` field still accurately describes the relationship. Run `validate.py`. [R1]
- [ ] Harness B is deprecated → **(A)** Remove B from A's `related` within 30 days, or add a note that B is deprecated and point to the replacement. [R1]
- [ ] Harness B is archived → **(A)** `validate.py` will error on the dead link. Remove B from `related` immediately. [R1]
- [ ] Cross-reference is one-way (A links to B but B does not link back) → **(A)** `validate.py` does NOT catch this — it checks link existence only, not bidirectionality. Verify reciprocation manually, or apply `common/meta/harness-quality-standards.md` item 5. Fix before merge. [R1]

### 7. Split vs. Merge Decision

When should a harness be split or merged?

- [ ] A harness has ≥12 checklist items → **(A)** Split. Find the natural divide between concerns. Create two harnesses with bidirectional `related` links. [R1]
- [ ] Two harnesses share ≥3 of the same `based_on` sources AND their checklists overlap by ≥30% → **(A)** Consider merging. If the combined checklist would exceed 12 items, split by concern instead. [R1]
- [ ] A harness spans 3+ categories → **(A)** Re-evaluate. Place in `common/cross-cutting/` if truly necessary; otherwise split into per-category harnesses. [R1]

---

## Quick Decision Tree

```
Harness event occurs (new PR, review due, source update, challenge, etc.)
  │
  ├─ New harness proposed? ──────────────→ Item 1 (draft → reviewed gate)
  ├─ Review cycle expired? ──────────────→ Item 3 (mandatory review trigger)
  ├─ Source updated externally? ─────────→ Item 3 (re-review within 3 months)
  ├─ Tier challenged? ───────────────────→ Item 5 (tier challenge resolution)
  ├─ Observed harmful practice? ─────────→ Item 4 (deprecation decision)
  ├─ Superseded by new harness? ─────────→ Item 4 (deprecation, 12-month grace)
  ├─ Checklist too long? ────────────────→ Item 7 (split)
  ├─ Overlapping with another harness? ──→ Item 7 (merge)
  └─ Used ≥1 month in real review? ─────→ Item 2 (reviewed → stable gate)
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Premature Stabilization

- **Appearance:** A harness is promoted to `stable` immediately after CODEOWNER approval without real-world usage evidence.
- **Trap:** "It passed review, it's correct, why wait?" Review catches logical errors, not practical gaps. Only usage reveals missing branches, unclear conditions, or items that never trigger.
- **Consequence:** A `stable` harness with untested checklist items provides false confidence. Reviewers skip their own judgment because "the checklist says so."
- **Fix:** Apply the harness to at least one real code review on production code. Document the outcome. Only then promote.

### Anti-Pattern 2: Silent Deprecation

- **Appearance:** A harness is removed or replaced without marking the old one `deprecated` or updating cross-references.
- **Trap:** "The new harness is better, everyone should use it. Removing the old one avoids confusion." But other harnesses still link to the old one, and contributors may have bookmarked it.
- **Consequence:** Broken `related` links. `validate.py` errors on dead references. External consumers relying on the old harness are stranded without migration guidance.
- **Fix:** Always use the deprecation propagation protocol: new harness declares `supersedes`, old harness gets `status: deprecated` with a pointer forward, all `related` links are updated, 12-month grace period before archival.

### Anti-Pattern 3: Tier Inflation

- **Appearance:** An (A)-tier recommendation is tagged (C) because "it's widely agreed upon" or "everyone does this."
- **Trap:** Consensus feels stronger than advisory. But without a published C-tier source (C++ Core Guidelines, OWASP, SEI/CERT), the higher tier is unverifiable.
- **Consequence:** Reviewers treat the recommendation as non-negotiable when it should be context-dependent. A future tier challenge exposes the lack of supporting evidence, damaging the harness's credibility.
- **Fix:** Tag each action with the highest tier you can cite. If the strongest source is a book (A-tier), tag it (A). If you believe it should be (C), find the consensus source — don't inflate without evidence.

---

## See Also

- [Harness Methodology](../../concepts/01-harness-methodology.md) — what a harness is and why checklists work
- [Authority System](../../concepts/02-authority-system.md) — N/C/A tier definitions, conflict resolution, source registry
- [CONTRIBUTING.md](../../CONTRIBUTING.md) — harness proposal workflow, tier assignment, challenge process
- [Design Spec](../../docs/specs/2026-05-31-repo-structure-design.md) — full architectural specification

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines Design Spec (docs/specs/2026-05-31-repo-structure-design.md) | Sections 2.6 (Lifecycle), 3.3-3.4 (Review Cycles, Deprecation) | verified-2026 | 2026-05 |
| R2 | A | dev-guidelines CONTRIBUTING.md | Harness Lifecycle Gates, Tier Assignment | verified-2026 | 2026-05 |
| R3 | A | dev-guidelines Authority System (concepts/02-authority-system.md) | Tier Hierarchy, Conflict Resolution, Challenge Process | verified-2026 | 2026-05 |

---

## Changelog

- 2026.05: Initial draft
