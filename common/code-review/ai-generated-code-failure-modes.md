---
type: harness
id: "common-ai-generated-code-failure-modes"
title: "AI-Generated Code Failure Modes Checklist"
language: "common"
category: "code-review"
tier: "A"
scope: "Detect subtle semantic defects in LLM/AI-generated code that compile and pass surface tests but are wrong — the failure class Simon Willison identifies as more dangerous than obvious hallucinations"
version: "2026.08"
status: "draft"
stable_since: ""
last_validated: "2026-08-04"
review_cycle: "12m"
tags: [code-review, code-generation, ai, testing, defect-detection]
based_on:
  - "[C] NIST AI 600-1 Generative AI Profile (C19) — Generative AI reliability & hallucination risk management"
  - "[A] Mutation Testing Concepts (A17/A18) — method for detecting tests that pass on incorrect code"
related:
  - "common/code-review/review-checklist.md"
  - "common/code-review/harness-driven-review.md"
  - "common/testing/testing-strategy.md"
  - "common/ai/ai-evaluation-and-regression-strategy.md"
supersedes: []
changelog:
  - "2026.08: Initial draft. Failure-mode taxonomy distilled from sustained adversarial code review of AI-generated code (the same defect class the $adversarial-development-loop skill targets, generalized for all reviewers)."
---

# AI-Generated Code Failure Modes Checklist

**Based on:** NIST AI 600-1 GenAI Profile [C19], OWASP LLM Top 10 [C16], Mutation Testing concepts [A17/A18].
**Scope:** A focused checklist for the defect class that is *specific to AI-assisted code* and that
generic review checklists under-weight: code that **compiles, passes the tests the AI wrote, and looks
plausible — but is semantically wrong**. This is the "subtle mistake that bypasses the compiler" that
is harder to catch than an obvious hallucination and, because it hides, more likely to ship.

**When to use:** During `harness-driven-review.md` Part B (code review) of any change authored or
substantially modified by an LLM. Especially for scoring/detection/diagnostic/threshold logic where
the output is consumed as truth by a machine or a human.

## Why a separate harness?

Generic review checklists (correctness, edge cases, dead code) cover these failure modes at the
*dimension* level. AI-generated code concentrates them into a recognizable *taxonomy* with shared
root causes: the model optimizes for "looks correct" (passes the visible check) over "is correct"
(satisfies the full state space). Reviewing by failure-mode class is faster than re-deriving each
one from first principles on every PR.

## Checklist

### 1. False-Perfect on Degenerate Input  **(N)** [R1]

The most frequent AI defect: an input the model did not consider (empty, zero, single-element,
missing field, sentinel value) produces a result that *looks* like success — a perfect score, an
empty diff, a "no issues" verdict — because the code path returns a default that mimics a good
answer.

- [ ] Enumerate the legal state space of every input (not "what does this function do", but "what
      shapes can this datum take"). For each shape, predict the output before reading the code →
      **(N)** a shape the reviewer cannot predict is a shape the code likely mishandles [R1]
- [ ] For each "success-like" output (score=100, count=0, empty list, `pass=true`), trace backward:
      what input produces it, and is that input *genuinely* a success or a *gap masquerading as
      success*? → **(N)** [R1]
- [ ] Sentinel values (0, -1, 1e10, 99, 100, null) each have multiple possible meanings
      ("not evaluated" / "legitimate extreme" / "evaluated, non-dominant"). Verify the code
      distinguishes them rather than treating them uniformly → **(N)** [R1]

### 2. Single-Layer Fix (Cross-Layer Data Drift)  **(N)** [R1]

A defect is fixed at the layer where it was reported, but the same incorrect datum is read
unchanged at the next layer (UI label, cache, serialized output, downstream consumer). The fix
"works" in the unit test and fails in production.

- [ ] For any datum that crosses a function/module boundary (id-space, encoding, nullness, format),
      list the full path: producer → each transform → each consumer, one hop per line → **(N)** [R1]
- [ ] Verify the fix at *every* hop, not just the reported one. A fix at hop 3 that leaves hop 4
      reading the old shape is an incomplete fix → **(N)** [R1]
- [ ] If a field had the bug, check its sibling fields in the same struct and the sibling modules
      in the same pipeline — the same author usually made the same mistake consistently → **(N)** [R1]

### 3. Documented Contract Not Honored (Dead Exit Code / Stub Flag)  **(N)** [R1]

The docstring, spec, or argparse help promises behavior (an exit code, a flag's effect, a returned
value) that no code path delivers. The promise and the implementation drift apart silently.

- [ ] For every documented exit code / return value / flag effect, grep the code: is there a code
      path that actually produces it? → **(N)** a documented-but-unreachable code is a lie that CI
      or a user will trust [R1]
- [ ] For every argparse flag, confirm `main()` reads `args.<flag>` — a flag accepted but never
      consumed is a no-op masquerading as a feature → **(N)** [R1]
- [ ] If the spec says "X returns Y", verify by *running* it on a representative input, not by
      reading the code — the code and the spec can both be wrong in the same way the author
      misremembered → **(N)** [R1]

### 4. Threshold / Magic Number Without Provenance  **(C)** [R1]

The model picks a plausible-looking constant (a timeout, a cutoff, a clamp boundary, a percentage)
that has no source. It may conflict with an established default elsewhere, or encode a wrong
physical/logical assumption.

- [ ] Every threshold/magic number has a comment citing its source (spec, standard, measurement,
      or "chosen to match X at file:line") → **(C)** [R1]
- [ ] The threshold is checked against the established default for the same quantity elsewhere in
      the codebase — a new value that silently differs from an existing one is a symmetry bug →
      **(C)** [R1]
- [ ] If the threshold depends on another variable the model treated as constant (a coupling it
      folded away), flag it: "does this quantity actually vary in the real scenario?" → **(C)** [R1]

### 5. Test That Cannot Fail  **(C)** [R2]

The AI writes a test alongside the code. The test passes — but it would also pass if the code were
wrong, because it does not exercise the distinguishing behavior (the mutation-testing concept: a
test is valuable only if some single-code-edit mutation makes it fail).

- [ ] For each new test, ask: what single-line change to the code under test would make this test
      *fail*? If you cannot name one, the test asserts nothing → **(C)** [R2] (grounded in A17/A18)
- [ ] Tests on degenerate input (item 1) are present *and* assert the *distinguishing* output, not
      just "no crash" → **(C)** [R2]
- [ ] Before claiming a fix works by "tests pass", run the suite *before and after* the change and
      confirm the output actually differs — a green suite on an insensitive test is false evidence →
      **(C)** [R2]

### 6. Status-Description Drift  **(A)** [R1]

The review/plan/report *describes* the current behavior ("X returns 0", "this is dead code", "Y is
the default") and the description is wrong — but the *direction* of the proposed change is right, so
the error hides. The fix is applied to a mis-described starting point and lands slightly off.

- [ ] Every statement of current behavior ("now returns", "currently is", "presently does") is
      verified against the actual code at file:line, not recalled → **(A)** [R1]
- [ ] When in doubt, run the code on a minimal input and observe the output; do not trust a
      description of it → **(A)** [R1]

## Anti-Patterns

### Anti-Pattern: "Tests pass, ship it"

- **Appearance:** The change has tests, they are green, the reviewer approves.
- **Trap:** Green tests on AI-generated code frequently assert the code does *something* rather than
  the *right thing*. The model writes the test to match its own (possibly wrong) mental model.
- **Consequence:** A defect ships with false confidence; the green suite is cited as evidence.
- **Fix:** Apply item 5 (mutation-style questioning) before trusting any AI-authored test. A test
  the same model wrote for the same code it wrote is not independent evidence.

### Anti-Pattern: "The direction is right, details later"

- **Appearance:** The plan/fix points the correct way; small inaccuracies in the description of
  current state are deferred as cosmetic.
- **Trap:** Implementation proceeds against the inaccurate description (item 6), so the fix lands
  at the wrong offset — correct in spirit, wrong in effect.
- **Consequence:** The bug is "fixed" but persists, reported again later, because the implementation
  targeted a mis-described starting point.
- **Fix:** Treat every "current state" claim as a hypothesis to verify at file:line before acting
  on it, regardless of how plausible the overall direction sounds.

## See Also

- [Code Review Checklist](review-checklist.md) — the dimension-level checklist (correctness,
  security, performance). This harness is the AI-specific complement, not a replacement.
- [Harness-Driven Development Protocol](harness-driven-review.md) — the process meta-harness; apply
  this checklist during its Part B (code review).
- [Testing Strategy](../testing/testing-strategy.md) — for item 5's mutation-testing grounding.

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | NIST AI 600-1 Generative AI Profile (C19) | Reliability, hallucination, output verification | verified-2026 | 2026-08 |
| R2 | A | Mutation Testing Concepts (A17/A18) | Test adequacy / mutation score | verified-2026 | 2026-08 |
