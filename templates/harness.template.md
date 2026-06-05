---
type: harness
id: "<language>-<slug>"
title: "<Harness Display Title>"
language: "<cpp|common|python|go|rust>"
category: "<category-from-INDEX.md>"
tier: "<N|C|A|P>"
scope: "<action> for <what> in <context>"
version: "2026.05"
status: "draft"
stable_since: ""
last_validated: "2026-05-31"
review_cycle: "12m"
tags:
  - <tag1>
  - <tag2>
based_on:
  - "[<N|C|A|P>] <Source Name> <Clause>"
related: []
supersedes: []
changelog:
  - "2026.05: Initial draft"
---

# <Harness Display Title>

**Based on:** <Source 1> ([N]), <Source 2> ([C]), ...
**Scope:** <One to two sentences describing what this harness covers and what it does not cover.>

---

## Prerequisites / Concepts

<!-- OPTIONAL: Remove this section if no background knowledge is needed. -->

<Explain key concepts, classification frameworks, or theoretical models needed to understand the checklist. Use tables or short definitions.>

---

## Checklist

<!-- 5-10 items. Each: condition → action with (N)/(C)/(A)/(P) tag + [Rx] reference key. -->

### 1. <Item Title>

<Brief explanation of what this item checks and why it matters.>

- [ ] <Condition branch 1> → **(N)** <Action instruction> [R1]
- [ ] <Condition branch 2> → **(C)** <Action instruction> [R2]
- [ ] <Condition branch 3> → **(A)** <Action instruction> [R3]

```cpp
// Good — <explanation>
<correct example>

// Bad — <explanation>
<incorrect example>
```

---

## Quick Decision Tree

<!-- OPTIONAL: Remove this section if items don't form a decision flow. -->

```
<Condition 1>?
  ├─ YES → <Action>
  └─ NO  → <Condition 2>?
              ├─ YES → <Action>
              └─ NO  → <Action>
```

---

## Anti-Patterns / Common Mistakes

<!-- RECOMMENDED: 2-3 entries. -->

### Anti-Pattern 1: <Name>

- **Appearance:** <What the mistake looks like in code or behavior>
- **Trap:** <Why it seems correct or harmless>
- **Consequence:** <The actual harm it causes>
- **Fix:** <The correct approach>

---

## See Also

<!-- REQUIRED when `related` is non-empty. Remove otherwise. -->

- [<Related Harness>](../path/to/related.md) — <brief description of relationship>

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | <Source> | <Clause> | verified-2026 | 2026-05 |
| R2 | C | <Source> | <Clause> | verified-2026 | 2026-05 |
| R3 | A | <Source> | <Clause> | verified-2026 | 2026-05 |

---

## Changelog

<!-- Rendered from frontmatter `changelog` field. -->

- 2026.05: Initial draft
