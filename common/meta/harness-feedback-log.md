# Harness Feedback Log

Structured record of harness behavior observed in real reviews. This log is the **bridge between conversation distillation and harness evolution**: it is the destination for signals distilled from strong-model review sessions (`docs/ai/conversation-distillation.md`), and the input source for lifecycle decisions in `common/meta/harness-evolution.md`.

**This is not a harness.** It carries no frontmatter, no checklist, no tier tags. It is a structured log. Do not run `validate.py` against it (the script skips non-frontmatter files).

---

## Purpose

Two failures this log exists to fix:

1. **Distillation without storage.** `docs/ai/conversation-distillation.md` converts strong-model decisions into rules, prompts, fixtures, and harness items — but had no aggregate destination for "this harness item was wrong / missing / inoperable in a real review." Signals scattered or were lost.
2. **Evolution without input.** `common/meta/harness-evolution.md` triggers re-review on schedule (`review_cycle`) or source-edition changes, but had no signal source for "this harness is accumulating real-world evidence that it needs change."

This log closes that loop: distillation writes here; evolution reads here.

---

## When to add an entry

Add an entry ONLY when a real review produces one of these signals:

- An item **FAILed** but the harness has **no corresponding item** to frame the finding (gap)
- An item was **marked inoperable** — its condition could not be evaluated against the code (e.g., too vague, wrong abstraction level)
- An item **PASSed but for the wrong reason** — the reviewer verified it via a different path than the item describes (item is misleading)
- An item **failed to trigger** in a scenario where it plausibly should have (under-coverage)
- A tier tag was found **inflated or deflated** relative to actual source backing

Do NOT add entries for routine PASS / FAIL where the item behaved as designed. Routine outcomes are not improvement signals — logging them dilutes the dataset.

---

## Entry schema

Each entry is a markdown block with exactly these fields:

```
### <YYYY-MM-DD> — <target>, item <N> (or "general")
- **Signal:** gap | inoperable | misleading | under-coverage | tier-mismatch
- **Scenario:** one sentence — project + change type + what was under review
- **Observation:** what happened, with file:line if applicable
- **Outcome:** improved (commit/PR ref) | recorded-pending | rejected (reason)
```

**`<target>` may be one of:**

- A **harness id** (e.g. `cpp-feature-design-prerequisites`, `common-harness-evolution`). This is the common case — feedback about a checklist item.
- A **tooling path** prefixed with `tool/` (e.g. `tool/scripts/check_review_signals.py`, `tool/prompts/weak-model-workflow.md`). Use this when the finding concerns a script, prompt, or template — not a harness item. The `tool/` prefix distinguishes tooling targets from harness ids so readers (and `check_feedback_signals.py`) can tell them apart.

Keep each entry under 8 lines. If the finding needs more space, it belongs in a linked commit message or issue, not in the log.

---

## Log

### 2026-07-27 — cpp-feature-design-prerequisites, item 3 (entity classification)
- **Signal:** under-coverage
- **Scenario:** C++ codebase audit — a value type carrying a runtime status field (`error_code`); review exposed drift between the status field and its producer path (a cancel-request flag)
- **Observation:** item 3 "ambiguous classification → record" was too vague to catch the Result/Outcome pattern where a value type carries a status field that must track a runtime producer. The failure mode (producer mutates state, forgets to sync value field) was unowned by any item.
- **Outcome:** improved — commit `2b594cc` added bullet covering value-projection rule for Result/Outcome status fields.

### 2026-07-27 — cpp-layering-and-dip, general (tier)
- **Signal:** tier-mismatch
- **Scenario:** self-review of newly-added layering harness during this session — SOLID items (1 SRP, 2 OCP, 3 DIP) tagged (C) but lacked genuine (C)-tier source backing in C++ context
- **Observation:** C++ Core Guidelines [C1] addresses interface/class mechanics, not SRP/OCP/DIP as architectural principles. SOLID is primarily sourced from Martin [A20] and Meyer [A22], both (A)-tier. Tagging SOLID items (C) was tier inflation per `harness-quality-standards.md` Anti-Pattern 2.
- **Outcome:** improved — commit `046319d` downgraded overall tier C→A and SOLID item-tiers C→A; added Authority Caveat section; added [A22] Meyer as OCP origin source.

### 2026-07-27 — common-harness-evolution, item 6 (cross-reference drift)
- **Signal:** misleading
- **Scenario:** self-review during this session — item 6 claimed `validate.py` catches one-way (non-bidirectional) `related` links
- **Observation:** false claim. `validate.py`'s `check_cross_references` verifies link target existence, errors on archived targets, warns on deprecated targets, but does NOT verify reciprocation. Contributors relying on this claim would ship one-way links that pass CI.
- **Outcome:** improved — commit `79a4c07` corrected the item to state validate.py checks existence only; pointed to `harness-quality-standards.md` item 5 (the human gate that enforces bidirectionality).

### 2026-07-27 — common-meta-feedback-log, general (schema gap: script-targeted entries)
- **Signal:** inoperable
- **Scenario:** ran check_review_signals.py on a real review report to validate the B6 closed loop; attempted to log a finding about the script itself
- **Observation:** the log's entry schema and check_feedback_signals.py's ENTRY_RE assume entries target a harness (id format `[a-zA-Z0-9_-]+`). A finding about a script (`scripts/check_review_signals.py`) cannot be expressed — the `/` and `.` in the path break the regex. The schema has no concept of non-harness targets (scripts, prompts, templates).
- **Outcome:** recorded-pending — schema needs extension to accept script/prompt paths as entry targets, or a separate "tooling feedback" log. Not yet fixed.

### 2026-07-28 — tool/scripts/check_feedback_signals.py, general (schema extension for tooling targets)
- **Signal:** under-coverage
- **Scenario:** resolving the 2026-07-27 recorded-pending entry above — the log schema could not express feedback about scripts/prompts/templates, only harness ids.
- **Observation:** extended the schema to accept tooling targets via a `tool/<rel-path>` prefix (e.g. `tool/scripts/check_feedback_signals.py`). Updated the schema section here to document both target kinds, and widened `ENTRY_RE` in check_feedback_signals.py to `tool/[a-zA-Z0-9_./-]+|[a-zA-Z0-9_-]+` so the reader parses both. Verified backward-compat (all existing harness-id entries still parse) and the new format end-to-end. This entry's own header (`tool/scripts/check_feedback_signals.py`) exercises the new schema.
- **Outcome:** improved — resolves the 2026-07-27 entry above; see commit (this change).

### 2026-07-29 — cpp-wxwidgets-3-1-5, item 20/37 (alpha↔GCDC interaction)
- **Signal:** under-coverage
- **Scenario:** conversation-distillation mining of 117 ZCode sessions — a real wxMSW review hit black corners on a 32-bit alpha bitmap; the fix was `wxGCDC(wxAutoBufferedPaintDC)`.
- **Observation:** #20 documents alpha-bitmap historical bugs and #37 documents `wxGraphicsContext` vs `wxDC`, but neither connects them: 32-bit bitmap RGB at alpha=0 is corrupted, FATAL on `wxDC::DrawBitmap` (black corners) yet HARMLESS via `wxGCDC` because alpha blending (`dst=src.rgb*src.a+dst.rgb*(1-src.a)`) never reads RGB when `src.a==0`. The causal bridge "switching to GCDC is both fix and reason" was missing.
- **Outcome:** improved — added sub-item 20a bridging #20 and #37; commit `f23fdc0`.

### 2026-07-29 — INDEX, general (missing config & requirements categories)
- **Signal:** under-coverage
- **Scenario:** conversation-distillation mining — recurring config-dimension-mismatch and PRD-vs-code gap-analysis patterns across the SnapmakerOrca sessions had no applicable harness or INDEX category.
- **Observation:** INDEX had no `config` category and no requirements-gap-analysis harness; 117 sessions repeatedly exhibited config data-dimension misclassification (treated as registration, actually a design blocker) and memory-based gap-list inflation, with no harness framing these. prior-art check confirmed NONE coverage for both.
- **Outcome:** improved — new `common-config-option-registration` (config category) and `common-planning-requirements-gap-analysis` harnesses; commits `8cbe9fd`, `501cc3b`; INDEX regenerated `91b1898`.

---

## Maintenance

- **Append-only.** Never edit a past entry to change its outcome retroactively — add a new entry referencing the old one if a decision is revisited.
- **Prune on archival.** When a harness is archived, its entries may be moved to an `archive/feedback-log-<date>.md` snapshot to keep this log scannable. Entries referencing active harnesses stay.
- **No frontmatter.** This file is intentionally not a harness. `validate.py` ignores it. `generate_index.py` does not list it.
- **Review cadence.** Skim quarterly. If an active harness accumulates ≥3 entries of the same signal type, that is strong evidence for a re-review trigger (future evolution Item 3 enhancement — not yet wired).
