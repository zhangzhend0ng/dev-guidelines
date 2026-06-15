---
type: harness
id: "common-documentation-standards"
title: "Documentation Standards Checklist"
language: "common"
category: "documentation"
tier: "C"
scope: "Write maintainable documentation: code comments, READMEs, ADRs, and API docs that stay current with code"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [documentation, comments, adr, readme, openapi]
based_on:
  - "[C] IETF RFC 2119/8174 — Keyword Conventions"
  - "[C] Google Technical Writing Courses"
  - "[C] OpenAPI 3.1 Specification"
  - "[A] ADR Pattern (Michael Nygard, 2011)"
  - "[A] Keep a Changelog (keepachangelog.com)"
related:
  - "common/ai/ai-evaluation-and-regression-strategy.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Documentation Standards Checklist

**Based on:** RFC 2119/8174 ([C]), Google Technical Writing ([C]), OpenAPI 3.1 ([C]), ADR Pattern ([A]), Keep a Changelog ([A]).
**Scope:** Inline comments, READMEs, architecture decisions, API docs, changelogs.

---

## Concepts

| Doc Type | Standard |
|----------|----------|
| Code comments | WHY, not WHAT; `WARNING:` for hazards |
| README | Summary + quick-start ≤5 min + full docs link |
| ADR | Status/Context/Decision/Consequences; immutable |
| API docs | Auto-generated; build fails on missing descriptions |
| Changelog | Keep a Changelog format |

---

## Checklist

### 1. RFC 2119 Keywords  **(C)** [R1]

- [ ] Specs declare BCP 14 conformance → **(C)** [R1]
- [ ] ALL-CAPS = normative; lowercase = not → **(C)** [R1]

### 2. Inline Comments  **(C)** [R2]

- [ ] WHY, not WHAT → **(C)** [R2]
- [ ] `WARNING:` prefix for hazards → **(C)** [R2]
- [ ] No commented-out code without ticket ref → **(C)** [R2]

### 3. README Structure  **(C)** [R2]

- [ ] One-sentence summary → **(C)** [R2]
- [ ] Quick-start ≤5 min → **(C)** [R2]
- [ ] Link to full docs → **(C)** [R2]

### 4. Architecture Decisions  **(A)** [R3]

- [ ] Non-trivial decision → ADR → **(A)** [R3]
- [ ] Title/Status/Context/Decision/Consequences → **(A)** [R3]
- [ ] Immutable; superseded links to replacement → **(A)** [R3]

### 5. API Documentation  **(C)** [R4]

- [ ] Public APIs have OpenAPI spec → **(C)** [R4]
- [ ] `description` on every operation/parameter/schema → **(C)** [R4]
- [ ] Build fails on missing descriptions → **(C)** [R4]

### 6. Changelog Format  **(A)** [R5]

- [ ] Keep a Changelog: Added/Changed/Deprecated/Removed/Fixed/Security → **(A)** [R5]
- [ ] Reverse chronological per release → **(A)** [R5]

### 7. Docs Live with Code  **(A)** [R2]

- [ ] Same repo as code → **(A)** [R2]
- [ ] API docs auto-generated from source → **(A)** [R2]

---

## Decision Tree

```
Documenting:
  → Spec? → RFC 2119 [1]
  → Code? → WHY + WARNING: [2]
  → Repo? → README [3]
  → Architecture? → ADR [4]
  → API? → OpenAPI [5]
  → Release? → Changelog [6]
  → Location? → Same repo [7]
```

---

## Anti-Patterns

### 1. WHAT Comment

- **Appearance:** `// increment i by 1` above `i++`.
- **Trap:** Feels like being thorough.
- **Consequence:** Comment rots when code changes. Wrong comment worse than none.
- **Fix:** Comment WHY: `// skip index 0; reserved for header row`.

### 2. Orphaned Wiki

- **Appearance:** Architecture docs in separate wiki no one updates.
- **Trap:** Wiki is easy — no PR required.
- **Consequence:** Wiki diverges from code in weeks. New team trusts wrong docs.
- **Fix:** Docs in repo. PR for doc change alongside code change.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | IETF RFC 2119/8174 | BCP 14 | verified-2026 | 2026-06 |
| R2 | C | Google Technical Writing | Courses 1-2 | verified-2026 | 2026-06 |
| R3 | A | ADR Pattern (Nygard) | Full template | verified-2026 | 2026-06 |
| R4 | C | OpenAPI 3.1 | info/paths/components | verified-2026 | 2026-06 |
| R5 | A | Keep a Changelog | v1.1.0 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
