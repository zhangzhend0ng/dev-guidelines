# AI Task Checklist: Long-Term Roadmap

This document is the execution checklist for turning `dev-guidelines` into a modular, AI-assisted engineering harness system.

## Objectives

- Support C++ as the primary workload.
- Add more languages through installable packs.
- Make planning, debugging, review, and verification machine-checkable.
- Reduce human involvement by using short, bounded, evidence-based AI workflows.
- Treat weak models as constrained workers, not autonomous editors.

## Operating Rules

- Start with the narrowest task slice.
- Require applicable harness selection before editing.
- Prefer short plans, short status updates, and deterministic verification.
- Do not accept "looks correct" without evidence.
- Do not scale autonomy by brand; scale it by repo-specific evals.

## Phase 1: Core AI Control

- [x] Add weak-model protocol checks for plan, patch, review, and verification outputs.
- [x] Add AI capability/adherence harnesses.
- [x] Add model registry and evaluation docs.
- [x] Add CI checks for AI protocol compliance.
- [ ] Add real evaluation runs for the current weak model family.
- [ ] Update capability tiers from eval evidence.
- [ ] Add prompt templates for common bounded AI task types.

Exit criteria:
- weak-model outputs are rejected automatically when they exceed budget or skip evidence
- model capability is assigned from local evals, not naming

## Phase 2: Planning and Debugging Core

- [x] Add planning harnesses.
- [x] Add debugging harnesses.
- [x] Add plan/debug protocol checkers.
- [x] Add smoke tests and CI coverage.
- [ ] Add more task-specific planning templates for refactor, migration, and release work.
- [ ] Add bug triage intake templates for user reports and CI failures.
- [ ] Add standardized evidence bundles for RCA and rollback decisions.

Exit criteria:
- every non-trivial task has an objective, scope, verification, and stop condition
- every bug fix has reproduction, root cause, fix, verification, and residual risk

## Phase 3: Modular Pack System

- [x] Add pack manifests and install scripts.
- [x] Make validate/index scripts pack-aware.
- [ ] Add pack export and packaging workflow.
- [ ] Add pack manifest index and checksums.
- [ ] Add sparse-checkout / download instructions for consumers.
- [ ] Make pack validation part of release gating.

Exit criteria:
- users can install only the harnesses they need
- packs validate independently from the full repo

## Phase 4: Python Core Pack

- [ ] Create `packs/python-core/pack.yml`.
- [ ] Add first five Python harnesses:
  - dependency management
  - typing and mypy
  - pytest patterns
  - input deserialization
  - asyncio cancellation
- [ ] Add Python source registry entries.
- [ ] Add Python-specific validation and index coverage.
- [ ] Add pack smoke tests for `python-core`.

Exit criteria:
- Python is available as a first-class installable pack
- Python harnesses reuse common guidance instead of duplicating it

## Phase 5: Additional Languages

- [ ] Add `rust-core` with ownership, error handling, unsafe boundaries, cargo, and testing.
- [ ] Add `go-core` with errors, concurrency, modules, testing, and input validation.
- [ ] Add `typescript-core` if and when repo demand justifies it.
- [ ] Keep language packs small, independent, and source-backed.

Exit criteria:
- each new language starts from a pack manifest and a minimal seed set

## Phase 6: Real Model Evaluation Loop

- [ ] Add per-model eval runs under `docs/ai/evals/runs/<model>/<date>/`.
- [ ] Evaluate plan, patch, review, verification, and debug outputs.
- [ ] Generate eval reports and store them with the run.
- [ ] Update the model registry from the same change as the eval.
- [ ] Promote only the task class that passed.
- [ ] Add regressions back into the eval suite.

Exit criteria:
- capability is governed by repeated local evidence
- weak models can do more, but only for slices they have earned

## Phase 7: Human-Work Reduction

- [ ] Keep progress updates phase-bound and short.
- [ ] Summarize evidence instead of dumping logs.
- [ ] Prefer automatic checks over manual inspection.
- [ ] Use approval gates only for high-risk actions and final judgment calls.
- [ ] Add templates that tell the user what was planned, done, verified, and not verified.

Exit criteria:
- users can see status without reading raw tool output
- humans are only pulled in where judgment is actually needed

## Execution Order

Run these two tracks in parallel so external model evaluation does not block repository delivery.

Repo-internal delivery:
1. Build pack export.
2. Ship Python pack.
3. Add Rust and Go packs.
4. Expand AI task templates and evidence bundles.

Model-eval delivery:
1. Collect real model eval runs.
2. Generate model reports.
3. Update capability tiers.
4. Re-evaluate capability after each major task slice.

## Non-Goals

- No full-repo rewrite.
- No model-brand-based trust.
- No autonomous code edits without harness coverage.
- No long narrative prompts when a short bounded protocol works.
