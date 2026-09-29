# PR Description Template

> Template, not a harness — no frontmatter, ignored by `validate.py`/`generate_index.py`.
> Authors: copy this into the PR description. Reviewers: enforce via
> `common/code-review/review-checklist.md` Item 2 and Item 10.

---

**Title:** `<type>: <subject>` (Conventional Commits — see `common/commits/conventional-commits.md`)

## Motivation

Why this change exists. Link the issue/ticket. One paragraph max.

## Change Scope  <!-- reviewer spot-checks this section against the actual diff -->

- Files/areas touched:
- Behavior before → after:
- Explicitly out of scope:

## Author Self-Check  (review-checklist Item 2)

- [ ] Ran the code-review checklist before requesting review; findings noted above
- [ ] Claimed verification covers EVERY changed target (no sampling) — list each compile/test run and the targets it covered
- [ ] Targets whose build config generates source text (e.g. `target_compile_definitions` into sources) were sanity-compiled

## Test Evidence  (review-checklist Item 5)

- What ran (suite/target, result):
- New tests added for behavior changes:
- Untested paths + rationale:

## Harnesses Considered  (prior-art-and-reuse)

- Applicable harnesses from `INDEX.md` and the verdict per harness:
- Not applicable — why:

## Rollback  (required for risky changes: schema/config/migration/flag)

- Revert plan (single revert, or data/config migration needed first):
