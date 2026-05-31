---
type: harness
id: "common-harness-driven-review"
title: "Harness-Driven Review Protocol"
language: "common"
category: "code-review"
tier: "A"
scope: "Enforce that every code review loads and applies all relevant harnesses — no review may complete without passing each harness checklist"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags:
  - code-review
  - meta-harness
  - process-enforcement
based_on:
  - "[A] dev-guidelines AGENTS.md — Code Review Entry Rules"
  - "[A] dev-guidelines CLAUDE.md — Harness Usage Protocol"
  - "[A] dev-guidelines Harness Methodology (concepts/01-harness-methodology.md)"
related:
  - "common/meta/harness-evolution.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---
# Harness-Driven Review Protocol

**This harness is the MANDATORY entry point for every code review.** Before evaluating any code, apply this harness to identify relevant harnesses, load them, execute each checklist, and gate the verdict. No review may complete without passing this protocol.

---

## Checklist

### 1. Harness Discovery — BEFORE reading the code

- [ ] Read [INDEX.md](../../INDEX.md), list all applicable harnesses by category → **(A)** [R1]
- [ ] Include any harness that *might* apply — false positives are cheap, missed issues are expensive → **(A)** [R1]

### 2. Harness Loading — Load all applicable harnesses

- [ ] Read each harness in full (prerequisites, items, anti-patterns, decision tree) → **(A)** [R1]

### 3. Harness Application — Execute every checklist item

- [ ] For each item: state condition, check code, cite file:line, report PASS or FAIL → **(A)** [R1]
- [ ] Tag each finding with authority tier → **(N)** = BLOCKING, **(C)** = HIGH (needs justification), **(A)** = suggestion [R2]

### 4. Verdict Gate

- [ ] All harnesses applied? If NO → **DO NOT ISSUE VERDICT** → **(A)** [R1]
- [ ] Any (N) failure? → **REQUEST CHANGES** → **(A)** [R2]
- [ ] Any unjustified (C) failure? → **REQUEST CHANGES** or **APPROVE with comments** → **(A)** [R2]
- [ ] All PASS or (A)-only? → **APPROVE** → **(A)** [R2]

### 5. Report Format

- [ ] List each harness by name, report items as PASS/FAIL with tier+line → **(A)** [R1]
- [ ] Include summary table → **(A)** [R1]

```
## Harness: Parameter Validation (cpp/functions/parameter-validation.md)
Item 1 — N/A (static internal)
Item 2 — PASS (line 1193, region checked)
...
## Verdict: APPROVE
```

---

## Decision Tree

```
Review requested
  → 1. Discover harnesses (INDEX.md, BEFORE code)
  → 2. Load each harness fully
  → 3. Apply each item → PASS/FAIL + line + tier
  → 4. Gate: (N)=BLOCK (C)=HIGH (A)=suggestion
  → 5. Report + verdict
```

---

## Anti-Patterns

### Anti-Pattern 1: Review Without Harnesses

- **Appearance:** Read diff → ad-hoc comments → verdict. No harness loaded.
- **Consequence:** Systematic gaps. Inconsistent coverage.
- **Fix:** Every review starts at Item 1. No harnesses loaded = review not started.

### Anti-Pattern 2: Post-Hoc Harness Selection

- **Appearance:** Read code first, then pick harnesses that confirm the verdict.
- **Consequence:** Confirmation bias. Harness becomes rubber stamp.
- **Fix:** Item 1 requires harness selection BEFORE reading code.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines CLAUDE.md | Harness Usage Protocol, Report Format | verified-2026 | 2026-06 |
| R2 | A | dev-guidelines AGENTS.md | Key Rules, Tier-Based Severity | verified-2026 | 2026-06 |
