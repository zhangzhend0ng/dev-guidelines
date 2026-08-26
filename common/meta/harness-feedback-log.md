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

### 2026-07-29 — common-harness-quality-standards, item 5 (bidirectionality vs hub-fan-in)
- **Signal:** misleading
- **Scenario:** full-repo cross-reference audit after the new-harness work — ran a bidirectionality check expecting to find peer-neighbor omissions like the prior dogfood (4 fixed in `6c4b701`).
- **Observation:** item 5's blanket "every `related` link must be bidirectional" was misleading: of 62 one-way links, 59 were upper-layer→foundational-hub upstream references (e.g. `wxwidgets→raii`, `asyncio→fix-verification`) and 0 were peer-neighbor omissions. Forcing back-links would stuff hubs (`raii` inbound=13, `undefined-behavior`=14, `testing-strategy`=17) with dozens of "referenced-by" entries, destroying navigability. The real `related` semantics in this repo is mixed: peer (bidirectional) + upstream reference (one-way).
- **Outcome:** improved — item 5 evolved to distinguish peer links (bidirectional) from upstream references (legitimately one-way for inbound-degree≥3 hubs); harness-evolution item 6 synced to classify one-way links instead of blanket "fix before merge". See commits (this change).

### 2026-07-31 — common-code-review-checklist, general (commit-message-vs-content mismatch)
- **Signal:** misleading
- **Scenario:** harness-driven review of SnapmakerOrca PR #652 (mixed-filament dialog, GUI/preset changes) — two findings in one review where commit messages / PR Notes described content the commits did not actually contain.
- **Observation:** (a) commit `78a15a001d` title/body claimed "add 0.2 Full Spectrum / Register new …0.2 nozzle preset" but `git show --stat` + `git ls-tree` proved the preset JSON was never staged (only an untracked `??` working-tree file) — feature's core deliverable missing. (b) merge commit `a0c9e5ca0c` stubbed `check_manual_filament_ratio()` to a no-op while the PR Notes claimed "the upstream …persistence was kept over this branch's earlier removal — upstream's version is more complete." review-checklist §3 (Correctness) and change-scope-control §4 (Review Boundary) caught the *symptom*, but no item frames the *root pattern*: verifying that stated diff content (commit msg / PR description) matches actual committed bytes. Reviewers who trust the description skip the `git show`/`ls-tree` check.
- **Outcome:** recorded-pending — candidate new item ("commit message ↔ tree content consistency") for review-checklist §3 or workflow-standards; two distinct occurrences in one PR suggests non-rare. Not yet added.
### 2026-08-06 — AGENTS, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL #1 (N)** 阻断：注释含事实性错误（竞争论证错误 + 失效行引用 + 臆造 dev-guidelines 章节号），会误导后续维护者。虽不改变运行时行为，但 harness 规
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-06 — AGENTS, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL #2 (C)** 需处理：`tests/gui/` 忽略是架构决策，需明确文档化或改为入库。
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-06 — AGENTS, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL #3 (C)** 需处理：行为变更需补充测试或 PR 手动验证说明。
- **Outcome:** auto-logged — verify and amend outcome if acted upon
### 2026-08-07 — AGENTS, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL #1 (C)**: 注释对 `darkModeColorFor` 的排他性声称失实（实现 + 既有用法三重反证），误导维护者。修注释即可。
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — AGENTS, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL #2 (C)**: badge 移入圆角 clip 是行为变更，border case（大半径/badge 被裁）未评估且注释动机薄弱。建议回退该步或补约束说明 + 实测。
- **Outcome:** auto-logged — verify and amend outcome if acted upon
### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (C)**: PR 描述没有附带 self-check 结果,也没有说明 `extract_model_colors` / `load_model_colors` 的调用方状态。从改
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (C)** [R1]:
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (C)**: 无新增单元测试。PR 引入了一个有状态的三分支(Level-2)决策与一个新的层重映射 Level-3,这些都是可被纯函数化的逻辑(类似 PR 此前 `build_mi
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (A)**: Level-2 三分支注释存在 **误导** —— "Subsequent inheriting volumes that also need a (different
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (C) — [Item 3] `extruder_remap`/`state_map` 的下标无显式上界守卫对 Level-2/3**:`state_map` 是 `std::map
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (C)**: `extruder_remap` 声明为 `unordered_map<int, unsigned int>`(key=int,value=unsigned)。Leve
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (A)**: PR 声称修两个 bug,但未声明 in-scope 函数清单,导致把死代码一并改了。
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (A)** [R3]: diff 把"行为修复"(apply_batch_match_to_model 的 live 改动)与"对死代码的同步修改"(extract_model_co
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-07 — common-code-review-checklist, orphan
- **Signal:** gap
- **Scenario:** auto-detected by check_review_signals.py
- **Observation:** FAIL without Item framing: - **FAIL (A) [R1] — 未使用参数**:`Print& print` 参数在 `apply_batch_match_to_model` 内完全未使用(函数用 `wxGetApp().m
- **Outcome:** auto-logged — verify and amend outcome if acted upon

### 2026-08-26 — cpp-wxwidgets-3-1-5, general (multi-platform compilation under-coverage)
- **Signal:** under-coverage
- **Scenario:** dev-guidelines maintenance session — user flagged that the wxWidgets harness lacks multi-platform compilation/build coverage
- **Observation:** harness only had §10 (app-side setup.h/wx-config/CMake); nothing frames compiling the library itself per port (wxGTK dev deps + GTK3/EGL defaults, wxMSW makefile.vc|gcc + per-config setup.h + RUNTIME_LIBS, wxOSX Xcode/SDK + bundle install_name_tool), cross-toolchain ABI consistency, or CMake find_package vs MinGW-w64 (#19278/#24454)
- **Outcome:** improved — added Sections 137-140 with reference labels R32-R35 and a related link to cpp/build/toolchain-and-compiler-flags.md (this change)

---

## Maintenance

- **Append-only.** Never edit a past entry to change its outcome retroactively — add a new entry referencing the old one if a decision is revisited.
- **Prune on archival.** When a harness is archived, its entries may be moved to an `archive/feedback-log-<date>.md` snapshot to keep this log scannable. Entries referencing active harnesses stay.
- **No frontmatter.** This file is intentionally not a harness. `validate.py` ignores it. `generate_index.py` does not list it.
- **Review cadence.** Skim quarterly. If an active harness accumulates ≥3 entries of the same signal type, that is strong evidence for a re-review trigger (future evolution Item 3 enhancement — not yet wired).
