---
type: harness
id: "common-harness-quality-standards"
title: "Harness Quality Standards Checklist"
language: "common"
category: "meta"
tier: "A"
scope: "Validate the structural and naming quality of a harness: id/filename/directory/category consistency, scope-statement quality, checklist item shape (condition→action + tier + [Rx]), reference-source integrity, and anti-pattern structure"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-26"
review_cycle: "24m"
tags: [meta, quality, naming, scope, checklist-shape, reference-integrity, anti-patterns]
based_on:
  - "[A] dev-guidelines Harness Template"
  - "[A] dev-guidelines validate.py behavior contract"
related:
  - "common/meta/harness-evolution.md"
  - "common/meta/prior-art-and-reuse.md"
supersedes: []
changelog:
  - "2026.07: Initial draft — fills the missing meta harness referenced from INDEX.md Quick Lookup"
---

# Harness Quality Standards Checklist

**Based on:** dev-guidelines Harness Template ([A]), dev-guidelines `validate.py` behavior contract ([A]).
**Scope:** The quality gate a harness must pass beyond what `validate.py` enforces mechanically. `validate.py` checks frontmatter presence, id uniqueness, and `related` link existence. This harness covers the conventions the validator does NOT enforce: naming consistency, scope-statement quality, checklist-item shape, reference-source integrity, and anti-pattern structure.

This harness is invoked by the INDEX.md Quick Lookup row "Validate harness description, naming, and scoping."

---

## Prerequisites / Concepts

**What `validate.py` enforces vs. what this harness adds:**

| Aspect | Enforced by `validate.py`? | Enforced by this harness? |
|--------|----------------------------|---------------------------|
| Required frontmatter fields present | YES | — |
| `type`/`status`/`tier`/`language` valid enums | YES | — |
| `id` unique repo-wide (non-deprecated) | YES | — |
| `related` target file exists | YES | — |
| `related` bidirectionality | NO (one-way links pass) | YES (item 5) |
| id / filename / directory / language consistency | NO | YES (item 1) |
| Scope statement quality | NO | YES (item 2) |
| Checklist item shape (condition→action + tier + [Rx]) | NO | YES (item 3) |
| Every [Rx] resolved in Reference Sources table | NO | YES (item 4) |
| Source registered in `references/sources.md` | NO | YES (item 4) |
| Anti-pattern 4-field structure | NO | YES (item 6) |

---

## Checklist

### 1. Naming and Placement Consistency **(A)** [R1][R2]

- [ ] `id` follows `<language>-<slug>` form (e.g., `cpp-raii`, `common-naming-conventions`) → **(A)** a bare slug without language prefix is ambiguous in cross-references. [R1]
- [ ] Filename is `<slug>.md` where `<slug>` matches the `id`'s slug portion → **(A)** `id: cpp-raii` lives in `raii.md`, not in `memory_raii.md`. [R1]
- [ ] Directory placement is consistent with `language` and the spirit of `category` → **(A)** a `language: cpp` harness lives under `cpp/`; the subdirectory need not match `category` exactly (validator does not check), but should be sensible to a reader browsing the tree. [R2]
- [ ] `category` value is a known INDEX bucket (lowercase slug) → **(A)** novel categories are allowed but should be intentional and documented in the Category Descriptions table. [R2]

### 2. Scope Statement Quality **(A)** [R1]

- [ ] `scope` frontmatter field is a single action-oriented sentence: "<action> for <what> in <context>" → **(A)** a noun-phrase scope ("RAII patterns") does not communicate what the harness *does*. [R1]
- [ ] The body's `**Scope:**` line distinguishes what the harness covers AND what it defers to neighbors → **(A)** the "defers to" half is what prevents overlap; without it, two harnesses silently grow into each other. [R1]
- [ ] Scope does not span ≥3 categories → **(A)** if it does, split per harness-evolution Item 7. [R1]

### 3. Checklist Item Shape **(A)** [R1][R2]

- [ ] Every checklist action line follows `<condition> → **(TIER)** <action> [Rx]` → **(A)** conditions without actions, or actions without tier tags, are incomplete. [R1]
- [ ] Every action has a tier tag: `**(N)**`, `**(C)**`, `**(A)**`, or `**(P)**` → **(A)** untagged actions cannot be gated in review. [R1]
- [ ] Tier tags are not inflated (see harness-evolution Anti-Pattern 3): tag the highest tier you can cite, not the tier you wish you could → **(A)** a book-backed recommendation is (A), not (C). [R2]
- [ ] Checklist has 5–12 items → **(A)** <5 is too thin to justify a harness; >12 triggers a split per harness-evolution Item 7. [R2]
- [ ] Each item has at least one `[Rx]` reference label → **(A)** uncited assertions are unverifiable. [R1]

### 4. Reference-Source Integrity **(A)** [R1]

- [ ] Every `[Rx]` label used in the checklist appears as a row in the Reference Sources table → **(A)** dangling references cannot be resolved. [R1]
- [ ] Every Reference Sources row cites a source registered in `references/sources.md` → **(A)** unregistered sources break the single-source-of-truth invariant; register first, cite second. [R1]
- [ ] Every Reference Sources row has a `Timeliness` cell of form `verified-YYYY` and a `Last Verified` cell of form `YYYY-MM` → **(A)** stale sources must be re-verified before use. [R1]
- [ ] The `based_on` frontmatter list and the Reference Sources table are consistent (same sources, possibly different granularity) → **(A)** drift between them signals an incomplete edit. [R1]

### 5. Cross-Reference Bidirectionality **(A)** [R1]

- [ ] For every entry in `related`, the target harness's `related` field reciprocally lists this harness → **(A)** `validate.py` checks existence only; bidirectionality is a human gate. [R1]
- [ ] The `See Also` body section lists each `related` target with a one-line description of the relationship → **(A)** the relationship description is what makes the link useful to a reader. [R1]
- [ ] Cross-references use repo-relative forward-slash paths in frontmatter (`cpp/correctness/interface-contracts.md`), not display-relative paths → **(A)** frontmatter paths are validated; body `See Also` paths may use `../` for readability. [R1]

### 6. Anti-Pattern Structure **(A)** [R1]

- [ ] Each anti-pattern uses the 4-field structure: **Appearance / Trap / Consequence / Fix** → **(A)** omitting "Consequence" leaves the reader unconvinced; omitting "Trap" makes the pattern seem obviously wrong when it is seductively reasonable. [R1]
- [ ] Anti-patterns are drawn from real review experience or authoritative sources, not invented → **(A)** speculative anti-patterns dilute the harness. [R1]
- [ ] At least 2 anti-patterns are present → **(A)** a single anti-pattern is usually a sign the harness was drafted too quickly. [R2]

---

## Quick Decision Tree

```
Harness drafted — quality gate before PR
  │
  ├─ [1] id / filename / directory / category consistent? ── NO → fix naming
  │
  ├─ [2] Scope is action-oriented + declares deferrals? ── NO → rewrite scope
  │
  ├─ [3] Every checklist line: condition→action + tier + [Rx]? ── NO → complete
  │      └─ 5–12 items? ── NO → split or expand
  │
  ├─ [4] Every [Rx] in Reference Sources? sources registered in sources.md?
  │
  ├─ [5] related bidirectional? See Also has relationship descriptions?
  │
  └─ [6] Anti-patterns: 4-field structure, ≥2 entries, real-world?
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Validator-Clean but Convention-Broken

- **Appearance:** A harness passes `validate.py` but its `id` does not match its filename, its `category` is a novel unsdocumented bucket, and its scope statement is a noun phrase.
- **Trap:** "If the validator passes, the harness is valid." The validator enforces a minimum, not the full convention.
- **Consequence:** INDEX.md becomes inconsistent; cross-references become hard to follow; future contributors cannot predict where a harness lives or what its id will be.
- **Fix:** The validator is necessary but not sufficient. Run this checklist as the second gate.

### Anti-Pattern 2: Tier Inflation

- **Appearance:** A recommendation backed only by a book is tagged `**(C)**` because "everyone agrees."
- **Trap:** Consensus feels stronger than advisory; (C)-tier carries review weight that (A) does not.
- **Consequence:** Reviewers treat the item as non-negotiable without a published consensus source. A future tier challenge (harness-evolution Item 5) exposes the gap and damages the harness's credibility.
- **Fix:** Tag the highest tier you can cite. If only a book supports it, tag `**(A)**`. (See also harness-evolution Anti-Pattern 3.)

### Anti-Pattern 3: Orphan Reference Labels

- **Appearance:** A checklist action cites `[R3]`, but the Reference Sources table only has R1 and R2.
- **Trap:** The label was added during drafting; the table was not updated.
- **Consequence:** A reviewer following the citation hits a dead end. The claim appears unsupported. Trust in the item erodes.
- **Fix:** Item 4 requires every `[Rx]` to resolve. Add the missing row or remove the label.

---

## See Also

- [Harness Evolution and Lifecycle Governance](harness-evolution.md) — lifecycle gates (draft→reviewed→stable), tier-challenge resolution, and the split/merge decision that this harness's item counts feed into.
- [Prior Art and Reuse](prior-art-and-reuse.md) — the duplicate-detection pass that runs before this quality gate; item 4 (id collision) and item 1 (naming) here are the second line of defense after prior-art search.
- [Harness Template](../../templates/harness.template.md) — the canonical structure this harness validates against.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines Harness Template (templates/harness.template.md) | Frontmatter schema, body section order, checklist item shape | verified-2026 | 2026-07 |
| R2 | A | dev-guidelines validate.py (scripts/validate.py) | Enforced rules (frontmatter, id uniqueness, related existence) and documented non-enforcement (bidirectionality, tier tags, naming) | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft — 6 items covering naming/placement, scope quality, checklist item shape, reference-source integrity, cross-reference bidirectionality, and anti-pattern structure. Fills the missing meta harness referenced from INDEX.md Quick Lookup; documents what `validate.py` enforces vs. what is convention-only.
