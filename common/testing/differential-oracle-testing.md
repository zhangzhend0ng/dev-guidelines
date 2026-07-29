---
type: harness
id: "common-testing-differential-oracle"
title: "Differential Oracle and Characterization Testing Checklist"
language: "common"
category: "testing"
tier: "A"
scope: "Validate a refactored or extracted computation against the authoritative runtime implementation as ground truth, so the refactor cannot inherit the author's same flawed mental model in both code and test"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-29"
review_cycle: "12m"
tags: [testing, characterization, differential-testing, oracle, refactoring, golden-master, approval-testing]
based_on:
  - "[A] Working Effectively with Legacy Code"
  - "[A] xUnit Test Patterns"
related:
  - "cpp/testing/property-based-testing.md"
  - "common/testing/testing-strategy.md"
  - "common/testing/test-doubles.md"
supersedes: []
changelog:
  - "2026.07: Initial draft — distilled from a real review where the only correct test used the runtime action as the oracle for a refactored prediction, precisely because a hand-written expectation would have copied the same bug"
---

# Differential Oracle and Characterization Testing Checklist

**Based on:** Working Effectively with Legacy Code ([A23]), xUnit Test Patterns ([A14]).
**Scope:** Tests that use an existing authoritative implementation as the oracle for a refactored or extracted version of the same logic. This harness answers **how to prove a refactor preserves behavior when you cannot trust a hand-written expectation**; `cpp/testing/property-based-testing.md` answers how to test *invariants over generated inputs*. It does NOT cover test design in general (`common/testing/testing-strategy.md`) or property-based generation.

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|------------|
| Characterization test | A test that locks in the *actual current behavior* of code (bugs and all), not the wished-for behavior — Feathers' definition. It is a safety net for refactoring. |
| Differential oracle | Using one implementation of a spec as the truth for another; here, the original runtime path is the oracle for the refactored version. |
| Golden master | A captured output of the authoritative system, frozen as the regression baseline. Synonyms: approval test, snapshot test. |
| The shared-model failure | The failure mode this harness exists for: when you refactor `compute_X()` out of `apply_X()`, an ordinary unit test with a hand-written expected value cannot catch the case where you encoded the *same wrong mental model* into both the code and the expected value. |

**When this harness applies:** when refactoring/extracting a prediction or computation out of a larger runtime-cascading action (e.g. pulling `compute_X()` out of `apply_X()` / `remove_X()`), porting an algorithm to a new component, or changing any logic whose "correct" output you can only trust if it matches the authoritative path. **When it does NOT apply:** greenfield code with a clean external spec, or mechanical renames with no behavioral risk.

---

## Checklist

### 1. Trigger: Refactor of a Computation from a Runtime Action **(A)** [R1]

- [ ] A prediction/computation is being extracted from, or runs alongside, a runtime action that mutates state (e.g. `compute_X` split out of `apply_X`/`remove_X`) → **(A)** this is exactly when a hand-written expectation risks duplicating the author's mental model; switch to a differential oracle. [R1]
- [ ] The refactor is a pure rename / signature change with no logic change → **(A)** no differential test needed; existing tests suffice. [R1]

### 2. Use the Authoritative Runtime as the Oracle **(A)** [R1]

- [ ] The test runs the *real authoritative runtime implementation* on the same input and asserts the refactored version matches it → **(A)** this is what makes the test immune to the shared-model failure: the oracle is the actual behavior, not the author's belief. [R1]
- [ ] The oracle is the genuine production path, not a second hand-written "reference" expected value → **(A)** two hand-written expectations merely duplicate the same wrong model twice. [R1]

### 3. Byte-Level Match and Marked Intentional Differences **(A)** [R2]

- [ ] The assertion is byte-level/exact on identical input, not approximate → **(A)** a fuzzy comparison can hide the divergence the test exists to catch. [R2]
- [ ] Cases where the refactored version is *intentionally* allowed to differ are marked (e.g. `[!shouldfail]`) and a `NOTE:` is placed at the implementation, not only in the test → **(A)** intentional differences documented only in the test rot when the test is skipped; the implementation note survives. [R2]

### 4. Freeze a Golden Value from the Source **(A)** [R2]

- [ ] When porting an algorithm, one byte-level output from the source repo is reproduced exactly and frozen as a permanent regression test in the target → **(A)** a single byte-exact golden from the source validates the entire port (coefficient tables, rounding) far better than structural comparison. [R2]
- [ ] The golden value is attributed to its source (file + case), so a future divergence can be traced to "did the source change, or did we?" → **(A)** an unattributed golden is un-investigable when it breaks. [R2]

### 5. Characterization vs Spec Test — Know Which You Are Writing **(A)** [R1]

- [ ] The test is labeled as characterization (locks current behavior, bugs included) or spec (verifies intended behavior) — not ambiguously both → **(A)** a characterization test that reads like a spec test hides that it is *encoding* a bug as the expected value. [R1]
- [ ] A characterization test that pins a *bug* is paired with a tracking reference (issue/FIXME), so the bug is not silently promoted to "intended" → **(A)** characterization without a bug marker lets bugs ossify into spec. [R1]

### 6. Preserve Surprising-but-Intentional Behavior Under Port **(A)** [R2]

- [ ] When porting, surprising outputs that are the source's *intentional design* are preserved as the default, not "fixed" → **(A)** a "fixed" port diverges from the source of truth and makes cross-validation meaningless; offer opt-in alternatives instead of silently correcting. [R2]

---

## Quick Decision Tree

```
Refactoring / extracting / porting a computation
  │
  ├─ Pure rename, no logic change? ── YES → existing tests suffice (item 1)
  │
  ├─ NO → extracted from a runtime action that mutates state?
  │     └─ YES → shared-model failure risk HIGH → write a differential oracle test (item 2)
  │
  ├─ Is your oracle the real runtime path or another hand-written expected value?
  │     └─ hand-written → INVALID oracle; re-point at the real runtime (item 2)
  │
  ├─ Any case where refactor may legitimately differ?
  │     └─ YES → mark [!shouldfail] + NOTE at implementation (item 3)
  │
  └─ Porting? → freeze one byte-exact golden from source as regression (item 4)
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Two Copies of the Same Wrong Model

- **Appearance:** `compute_X` is extracted from `apply_X`; the new test asserts `compute_X(input) == expected`, where `expected` was hand-computed by the same author using the same mental model.
- **Trap:** The test passes; the author's reasoning looks rigorous.
- **Consequence:** If the author's model was wrong in `apply_X`, the same error is now also in `expected` — the test passes for the wrong reason and the bug is cemented across two locations.
- **Fix:** Item 2: the oracle must be the real `apply_X` runtime path run on the same input, not a hand-derived expected value.

### Anti-Pattern 2: Fuzzy Oracle Hides the Divergence

- **Appearance:** The differential test uses an approximate comparison ("within tolerance," "rounded") because exact match was "too brittle."
- **Trap:** Approximate comparison silences flaky failures and feels pragmatic.
- **Consequence:** The exact divergence the test exists to detect is swallowed by the tolerance; the refactor can ship a real behavior change undetected.
- **Fix:** Item 3: assert byte-level/exact on identical input; if a case legitimately differs, mark it explicitly rather than widening the tolerance globally.

### Anti-Pattern 3: Silent "Fix" on Port

- **Appearance:** A ported algorithm produces a surprising output (e.g. a target color equal to a palette entry matches to a 99:1 recipe, not pure single-color); the porter "corrects" it to the intuitive result.
- **Trap:** The "corrected" result looks more sensible; the porter is confident they improved it.
- **Consequence:** The port now diverges from the validated source; future cross-checks against the source report false failures, and the divergence is untraceable.
- **Fix:** Item 6 + Item 4: preserve surprising-but-intentional behavior as the default, freeze the source golden, and offer opt-in alternatives rather than silently correcting.

---

## See Also

- [C++ Property-Based Testing Checklist](../../cpp/testing/property-based-testing.md) — Item 4 ("Oracles") covers "reference implementation as one oracle type" over generated inputs; this harness specializes it to the *refactoring* trigger and the shared-model failure mode.
- [Testing Strategy Checklist](testing-strategy.md) — general test classification and the legacy-code testing context ([A23] Feathers) this harness builds on.
- [Test Doubles Taxonomy](test-doubles.md) — when a dependency must be substituted to run the authoritative path in isolation.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | [A23] Working Effectively with Legacy Code (Feathers, 2004) | Characterization tests ("document actual behavior, not wished behavior"), seams, breaking dependencies to enable testing | verified-2026 | 2026-07 |
| R2 | A | [A14] xUnit Test Patterns (Meszaros, 2007) | Golden master / recorded-output patterns, test organization | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft — 6 items covering the refactor trigger, authoritative-runtime oracle, byte-level match with marked intentional differences, source golden freezing, characterization-vs-spec labeling, and preserving surprising-but-intentional behavior under port. Distilled from a real review where the shared-model failure was the central risk.
