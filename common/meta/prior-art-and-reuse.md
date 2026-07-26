---
type: harness
id: "common-prior-art-and-reuse"
title: "Prior Art and Reuse Checklist"
language: "common"
category: "meta"
tier: "A"
scope: "Enforce a duplicate-detection and reuse pass before any new harness is proposed: search the INDEX, read candidates in full, and choose extend / fork / new with recorded rationale"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-26"
review_cycle: "24m"
tags: [meta, prior-art, duplication, reuse, extend-vs-new, naming-collision]
based_on:
  - "[A] dev-guidelines Harness Evolution and Lifecycle Governance"
  - "[A] dev-guidelines Harness Template"
related:
  - "common/meta/harness-evolution.md"
  - "common/meta/harness-quality-standards.md"
supersedes: []
changelog:
  - "2026.07: Initial draft — fills the missing meta harness referenced from INDEX.md Quick Lookup"
---

# Prior Art and Reuse Checklist

**Based on:** dev-guidelines Harness Evolution ([A]), dev-guidelines Harness Template ([A]).
**Scope:** The mandatory pre-proposal pass for every new harness. Run this BEFORE drafting a new harness file. The goal is to extend or fork existing harnesses rather than create near-duplicates; new harnesses are proposed only when the prior-art search is exhausted.

This harness is invoked by the INDEX.md Quick Lookup row "Ensure new harnesses don't duplicate existing ones."

---

## Prerequisites / Concepts

| Decision | When to choose it |
|----------|-------------------|
| **Extend** | An existing harness covers ≥80% of the intended scope; add the missing items to it (if it stays ≤12 items) |
| **Fork** | An existing harness covers the domain but with a different language/tier/scope; create a sibling with bidirectional `related` links |
| **New** | No existing harness covers the domain; prior-art search is exhausted; the new scope is cohesive and ≤12 items |

**Hard reuse rule:** if a checklist item you intend to write already exists verbatim or near-verbatim in another harness, **link to it** via `related` and `See Also` rather than copying the text.

---

## Checklist

### 1. INDEX Search — Cast a Wide Net **(A)** [R1]

- [ ] Searched INDEX.md by category AND by free-text keyword (synonyms included) → **(A)** a single keyword is not enough; the same concept is often named differently across harnesses. [R1]
- [ ] Listed ≥3 candidate harnesses that might overlap before reading any of them → **(A)** list before reading to avoid anchoring on the first hit. [R1]
- [ ] Searched the authoritative-source registry (`references/sources.md`) for sources you intend to cite → **(A)** if a source is already registered, reuse its label; if not, plan to register it. [R1]

### 2. Read Candidates in Full **(A)** [R1]

- [ ] Read every candidate harness end-to-end (frontmatter, checklist, anti-patterns, decision tree, reference sources) → **(A)** skim-reading the checklist only misses scope boundaries declared in the prose. [R1]
- [ ] For each candidate, recorded: what it explicitly owns, what it explicitly defers, and its tier → **(A)** the "defers to" / "See Also" sections are where overlap boundaries are declared. [R1]

### 3. Extend / Fork / New Decision **(A)** [R1][R2]

- [ ] Candidate exists and covers ≥80% of intended scope, combined checklist would be ≤12 items → **(A)** EXTEND: add items to the existing harness with a changelog entry. [R1][R2]
- [ ] Candidate covers the domain but differs in language, tier, or project scope → **(A)** FORK: create a sibling with explicit scope difference and bidirectional `related`. [R1]
- [ ] No candidate covers the domain; the intended scope is cohesive and ≤12 items → **(A)** NEW: record the prior-art decision and proceed. [R1]
- [ ] Intended scope spans ≥3 categories → **(A)** reconsider; either narrow the scope or place under `common/cross-cutting/` per harness-evolution Item 7. [R2]

### 4. ID and Naming Collision Check **(A)** [R1]

- [ ] Proposed `id` is unique repo-wide among non-deprecated harnesses → **(A)** check via `git grep "^id:" -- '*.md'` and against `archive/`. [R1]
- [ ] Proposed filename and directory placement are consistent with the `id`'s language and category → **(A)** see `harness-quality-standards.md` for the naming contract. [R1]
- [ ] Proposed `id` is not in `archive/` (would-be reuse of a retired id) → **(A)** pick a new id; archived ids are retired permanently. [R1]

### 5. Reuse via Cross-Reference, Not Copy **(A)** [R1]

- [ ] Any checklist item that duplicates an existing harness's item is removed and replaced with a `See Also` / `related` pointer → **(A)** duplication rots; links stay fresh. [R1]
- [ ] Bidirectional `related` links are added: new harness lists the related one, and the related one is edited to list the new one → **(A)** `validate.py` checks existence only; bidirectionality is a human gate enforced here. [R1]
- [ ] Sources cited are registered in `references/sources.md` before the harness is committed → **(A)** unregistered sources break the single-source-of-truth invariant. [R1]

### 6. Record the Prior-Art Decision **(A)** [R1]

- [ ] PR description records: candidates considered, decision (extend/fork/new), rationale → **(A)** a future contributor proposing a similar harness must be able to find this decision. [R1]
- [ ] If NEW: explicitly state which existing harnesses were considered and why none applied → **(A)** "no prior art" without evidence is not acceptable. [R1]
- [ ] If EXTEND or FORK: the extended/forked harness's changelog is updated to reference the change → **(A)** both ends of the relationship must record it. [R1]

---

## Quick Decision Tree

```
About to propose a new harness?
  │
  ├─ [1] Searched INDEX by category + keywords? ── NO → search first
  │
  ├─ [2] Read top candidates end-to-end? ── NO → read them
  │
  ├─ [3] Coverage decision:
  │     ├─ ≥80% overlap, ≤12 combined → EXTEND existing
  │     ├─ Domain overlap, diff language/tier/scope → FORK with related links
  │     └─ No real overlap → NEW (record rationale)
  │
  ├─ [4] id / filename / directory unique & consistent? ── NO → rename
  │
  ├─ [5] Duplicated items replaced with links? related bidirectional?
  │
  └─ [6] PR description records the decision?
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Search-Then-Rationalize

- **Appearance:** Author searches, finds a candidate, reads its title, concludes "that's about X, mine is about Y," and proceeds with a new harness.
- **Trap:** Titles under-scope. The actual boundary between two harnesses is declared in the body's "defers to" and "See Also" sections, not the title.
- **Consequence:** Two harnesses with overlapping checklists drift independently; reviewers cannot tell which applies; both eventually need a split/merge per harness-evolution Item 7.
- **Fix:** Read the full candidate. The decision to extend/fork/new must cite the candidate's actual scope boundary, not its title.

### Anti-Pattern 2: Copy-Paste Reuse

- **Appearance:** A new harness reproduces three checklist items verbatim from an existing one "for self-containment."
- **Trap:** Self-contained harnesses feel easier to apply.
- **Consequence:** When the source harness updates an item, the copy does not. The two diverge silently. The registry of "what is authoritative where" is lost.
- **Fix:** Link, do not copy. A reviewer applying this harness can follow a `See Also` pointer.

### Anti-Pattern 3: "No Prior Art" Without Evidence

- **Appearance:** PR description says "No existing harness covers this" with no list of candidates considered.
- **Trap:** The author did not search thoroughly, or searched only by exact keyword.
- **Consequence:** Reviewers cannot verify the claim. The new harness may duplicate an existing one named differently.
- **Fix:** Item 6 requires the candidates considered and the reason each was rejected. Absence of evidence is not evidence of absence.

---

## See Also

- [Harness Evolution and Lifecycle Governance](harness-evolution.md) — Item 7 (split vs merge) is the authority this harness operationalizes; Items 1–2 cover the lifecycle gates a new harness must pass.
- [Harness Quality Standards](harness-quality-standards.md) — naming, scope, and checklist-item quality contracts that the id-collision check (item 4) defers to.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines Harness Evolution (common/meta/harness-evolution.md) | Item 7 (split vs merge), Items 1–2 (lifecycle gates) | verified-2026 | 2026-07 |
| R2 | A | dev-guidelines Harness Template (templates/harness.template.md) | Frontmatter and body contract | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft — 6 items covering INDEX search, full read, extend/fork/new decision, id collision, link-not-copy reuse, and prior-art decision recording. Fills the missing meta harness referenced from INDEX.md Quick Lookup.
