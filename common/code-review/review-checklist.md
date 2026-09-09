---
type: harness
id: "common-code-review-checklist"
title: "Code Review Checklist"
language: "common"
category: "code-review"
tier: "C"
scope: "Systematically review code for correctness, security, performance, readability, and test coverage"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-09"
review_cycle: "12m"
tags: [code-review, process, quality]
based_on:
  - "[C] Google Engineering Practices — Code Review"
  - "[C] Microsoft Code Review Guide"
  - "[A] Software Engineering at Google Ch.9 (Winters et al., 2020)"
  - "[A] Best Kept Secrets of Peer Code Review (SmartBear)"
related:
  - "common/code-review/harness-driven-review.md"
  - "common/code-review/ai-generated-code-failure-modes.md"
  - "projects/snapmaker-orca/workflow-standards.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
  - "2026.09: Item 9 (user-visible copy) added — new/changed user-facing strings are checked for spelling and stray/broken symbols, and display copy must not reuse log-format traces. Distilled from the lava monorepo dual-diff review."
---

# Code Review Checklist

**Based on:** Google Engineering Practices ([C]), Microsoft Code Review Guide ([C]), SWE at Google Ch.9 ([A]), SmartBear ([A]).
**Scope:** Review dimensions for every code change. Use with `harness-driven-review.md` (the meta-harness for process).

---

## Concepts

| Dimension | What to Check |
|-----------|---------------|
| Correctness | Logic, edge cases, invariants, error handling |
| Security | Injection, auth, data leak, insecure deps |
| Performance | Algorithmic complexity, N+1 queries, blocking I/O |
| Test Coverage | Behavior changes have tests; untested paths documented |
| Readability | Names, comments, function size, consistency |

**Review limits:** <400 changed lines. Sessions capped at 60 minutes.

---

## Checklist

### 1. Review Size  **(C)** [R1]

- [ ] <400 changed lines → Proceed
- [ ] ≥400 → Author MUST split, or reviewer schedules longer session → **(C)** [R1][R3]

### 2. Author Self-Check  **(C)** [R1]

- [ ] Author ran this checklist BEFORE requesting review → **(C)** [R1]
- [ ] Findings documented in PR description → **(C)** [R1]

### 3. Correctness  **(C)** [R1]

- [ ] Logic correct for all code paths including error/failure → **(C)** [R1]
- [ ] Edge cases: empty input, null, boundaries, concurrent access → **(C)** [R1]
- [ ] Invariants documented and preserved → **(C)** [R1]

### 4. Security  **(C)** [R1][R2]

- [ ] No injection vectors (SQL, command, path traversal) → **(C)** [R2]
- [ ] Auth gates on all protected endpoints → **(C)** [R2]
- [ ] No secrets, tokens, keys in code or logs → **(C)** [R2]
- [ ] No new deps with CRITICAL/HIGH CVEs → **(C)** [R2]

### 5. Test Coverage  **(C)** [R1][R4]

- [ ] Every behavior change has a test → **(C)** [R4]
- [ ] Untested paths documented with rationale → **(C)** [R1]
- [ ] No known-flaky tests introduced → **(C)** [R4]

### 6. Readability  **(C)** [R1]

- [ ] Names communicate intent without comments → **(C)** [R1]
- [ ] Comments explain WHY, not WHAT → **(C)** [R1]
- [ ] Functions <40 lines; single responsibility → **(C)** [R1]
- [ ] No dead code or TODO markers without ticket reference → **(C)** [R1]

### 7. Performance  **(C)** [R1]

- [ ] No O(n^2) on CRUD collections, hot paths, or unbounded input → **(C)** [R1]
- [ ] No N+1 queries → **(C)** [R1]
- [ ] No blocking I/O on request threads → **(C)** [R1]

### 8. Review Speed  **(A)** [R1][R3]

- [ ] Reviewer responds within 1 business day → **(A)** [R3]
- [ ] Author resolves within 2 business days → **(A)** [R3]
- [ ] Stale (>1 week) → author refreshes summary → **(A)** [R1]

### 9. User-Visible Copy  **(A)** [R5]

- [ ] Diff adds or changes a user-facing string → **(A)** check spelling and stray/broken symbols exactly as the user will see it (e.g. `'...please try again later}'` has a stray `}` that renders verbatim); flag typo-grade defects in UI copy. [R5]
- [ ] User-facing text is taken from a log message, error string, or other internal format → **(A)** do not surface log-format traces (correlation IDs, internal codes, log wording) to end users; keep display copy and log copy separate. [R5]

---

## Decision Tree

```
PR received
  → Size [1]: >400 lines? → SPLIT
  → Self-check [2]: Done?
  → Correctness [3]: FAIL? → REQUEST CHANGES
  → Security [4]: (N) FAIL? → BLOCK
  → Tests [5]: Untested? → Document or add
  → Readability [6]: Clear?
  → Performance [7]: Hot path issues?
  → Speed [8]: 1-day response
  → Copy [9]: user-facing strings clean? No log traces?

(N)=BLOCK  (C)=fix-or-justify  (A)=suggestion
```

---

## Anti-Patterns

### 1. Rubber-Stamp

- **Appearance:** "LGTM" with no specific comments.
- **Trap:** Trust in author's experience.
- **Consequence:** Review provides zero value. Systematic gaps.
- **Fix:** At least one specific observation per dimension.

### 2. Scope Creep

- **Appearance:** Reviewer demands unrelated refactoring/redesign.
- **Trap:** "While we're here..."
- **Consequence:** PR scope explodes; review never ends.
- **Fix:** File follow-up issue. Keep review focused on the change.

---

## See Also

- [Harness-Driven Protocol](harness-driven-review.md) — When and how to apply this checklist
- [Input Validation](../security/input-validation.md) — Detailed security checklist

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Google Engineering Practices | Code Review | verified-2026 | 2026-06 |
| R2 | C | Microsoft Code Review Guide | Security | verified-2026 | 2026-06 |
| R3 | A | SWE at Google (Winters) | Ch.9 | verified-2026 | 2026-06 |
| R4 | A | SmartBear Best Practices | Review limits | verified-2026 | 2026-06 |
| R5 | A | dev-guidelines engineering experience (lava monorepo dual-diff review) | Stray `}` in a user-visible retry string rendered verbatim; log-format traces leaking into display copy | verified-2026 | 2026-09 |

---

## Changelog

- 2026.06: Initial draft
- 2026.09: Item 9 (user-visible copy) added — spelling and stray/broken symbols in user-facing strings, and no log-format traces in display copy. Distilled from the lava monorepo dual-diff review.
