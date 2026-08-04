---
type: harness
id: "common-output-language"
title: "Output Language Convention"
language: "common"
category: "documentation"
tier: "P"
scope: "Define the default output language for AI-generated reports, code review summaries, and harness application results"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-06"
review_cycle: "12m"
tags:
  - output-language
  - chinese
  - report-convention
  - project-convention
based_on:
  - "[P] Project convention — default output language for AI agents in this workspace"
related: []
supersedes: []
changelog:
  - "2026.07: Initial draft"
---

# Output Language Convention

**Based on:** Project convention ([P]).
**Scope:** When an AI agent produces reports, code review summaries, harness checklists, or implementation notes in this workspace, the default output language is Chinese. Code, identifiers, and technical terms remain in their original language.

---

## Rule

- [ ] Output is a report, summary, review, or explanatory text → **(P)** Write in Chinese (Simplified). [R1]
- [ ] Output is code, a variable name, a function signature, or a technical identifier → **(P)** Keep the original language. Do not translate. [R1]
- [ ] Output contains mixed content (explanation + code) → **(P)** Explanation in Chinese. Code blocks unchanged. [R1]

## Examples

```markdown
# BAD — English report when Chinese is the default
## Harness: Parameter Validation
Item 1 — PASS (line 42, nullptr checked before dereference)
Item 2 — FAIL (line 87, raw pointer returned without ownership documentation)
Verdict: REQUEST CHANGES

# GOOD — Chinese report, code references unchanged
## Harness: Parameter Validation
Item 1 — PASS (line 42, 解引用前已检查 nullptr)
Item 2 — FAIL (line 87, 返回原始指针但未注明所有权)
结论: REQUEST CHANGES
```

## Boundaries

- When the user explicitly requests English output → Follow the user's instruction. This harness is the default, not an override.
- When communicating with an English-speaking audience → Use English. This harness applies to internal workspace output.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | P | Project convention | Default output language for AI agents in this workspace | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft
