# Capability Roadmap: Languages, Planning, Debugging, and Modular Harnesses

## Goal

Turn `dev-guidelines` from a C++-focused harness library into a modular engineering guidance system:

- language packs can be installed on demand
- AI agents can plan tasks with bounded autonomy
- debugging workflows are harness-driven and evidence-based
- weak/local/domestic models can be used with low human supervision

Execution checklist: [AI Task Checklist](2026-06-15-ai-task-checklist.md)

## Track 1: Language Pack Expansion

### Language Pack Contract

Every new language starts as a pack:

```text
packs/<lang>-core/pack.yml
<lang>/
  build/
  correctness/
  dependencies/
  error-handling/
  security/
  testing/
```

The first PR for a language must include:

- `packs/<lang>-core/pack.yml`
- CODEOWNERS entry
- source registry additions
- at least 5 high-impact harnesses
- validation and index support through existing scripts

### Priority Order

| Priority | Language | Reason | First Harnesses |
|----------|----------|--------|-----------------|
| 1 | Python | High AI/tooling usage; broad project fit | packaging, typing, testing, security, async |
| 2 | Rust | Strong safety model; good contrast with C++ | ownership, error handling, unsafe, cargo, testing |
| 3 | Go | Common services/tooling language | errors, concurrency, modules, testing, HTTP |
| 4 | TypeScript | Frontend/backend glue; API clients | typing, async, package security, testing, build |

### Python Pack Seed

`python-core` should start with:

- `python/packaging/dependency-management.md`
- `python/correctness/type-hints-and-mypy.md`
- `python/testing/pytest-patterns.md`
- `python/security/input-deserialization.md`
- `python/concurrency/asyncio-cancellation.md`

### Rust Pack Seed

`rust-core` should start with:

- `rust/ownership/borrowing-and-lifetimes.md`
- `rust/error-handling/result-panic.md`
- `rust/unsafe/unsafe-boundaries.md`
- `rust/build/cargo-features.md`
- `rust/testing/property-and-fuzz-testing.md`

### Go Pack Seed

`go-core` should start with:

- `go/error-handling/errors-and-wrapping.md`
- `go/concurrency/goroutines-and-context.md`
- `go/modules/dependency-management.md`
- `go/testing/table-driven-tests.md`
- `go/security/input-validation.md`

## Track 2: Task Planning Capability

### Problem

AI agents often fail by doing too much at once: broad edits, weak plans, hidden assumptions, and poor stopping conditions.

### Target Capability

Add planning harnesses that make work decomposable and checkable:

- `common/planning/task-decomposition.md`
- `common/planning/change-scope-control.md`
- `common/planning/risk-and-verification-plan.md`
- `common/planning/rollback-and-migration-plan.md`

### Planning Protocol

Every non-trivial task should produce:

```text
Objective:
Applicable harnesses:
Scope:
Non-goals:
Steps:
Verification:
Rollback:
Human approval gates:
```

### Automation

Add `scripts/check_plan_protocol.py`:

- verifies required sections
- checks line budget
- rejects missing verification
- rejects plans without non-goals for multi-file work
- flags high-risk actions without approval gates

## Track 3: Debugging Capability

### Problem

Debugging often becomes ad hoc: logs are pasted, symptoms are chased, and root cause evidence is weak.

### Target Harnesses

- `common/debugging/bug-report-triage.md`
- `common/debugging/reproduction-and-minimization.md`
- `common/debugging/root-cause-analysis.md`
- `common/debugging/fix-verification.md`
- `cpp/debugging/sanitizer-triage.md`
- `cpp/debugging/crash-dump-analysis.md`
- `cpp/debugging/flaky-test-triage.md`

### Debug Protocol

Every bug fix should record:

```text
Symptom:
Reproduction:
Suspected component:
Evidence:
Root cause:
Fix:
Regression test:
Verification:
Residual risk:
```

### Automation

Add `scripts/check_debug_report.py`:

- blocks "fixed" claims without reproduction or verification
- requires regression test or documented reason
- flags raw log dumps over budget
- requires NOT VERIFIED when reproduction is missing

## Track 4: Weak Model and Agent Workflow

### Near-Term Enhancements

- Add real model eval runs under `docs/ai/evals/runs/<model>/<date>/`
- Generate reports with `scripts/evaluate_ai_protocol.py --output`
- Update `docs/ai/model-registry.md` with `scripts/update_model_registry.py`
- Add model-specific prompt notes only after eval evidence exists

### Tier Governance

| Tier | Default Model Authority |
|------|-------------------------|
| T0 | summarize/classify only |
| T1 | plan and harness selection |
| T2 | small bounded patch after approval |
| T3 | multi-file subsystem work with tests |
| T4 | autonomous tool workflow with approval gates |

Promotion requires:

- passing eval cases for that task class
- no fake verification
- no progress spam
- no skipped harness selection
- stable behavior across repeated runs

## Track 5: Pack Distribution

### Current State

The repository supports:

- `packs/<id>/pack.yml`
- `scripts/list_packs.py`
- `scripts/install_pack.py`
- `scripts/validate.py --pack/--installed`
- `scripts/generate_index.py --pack/--installed`

### Next Distribution Steps

1. Add `.github/workflows/package-packs.yml`
2. Build zip artifacts per pack:
   - `common-core-2026.06.zip`
   - `cpp-core-2026.06.zip`
   - `cpp-testing-2026.06.zip`
   - `cpp-security-2026.06.zip`
   - `ai-dev-2026.06.zip`
3. Add checksums and manifest index:
   - `packs/index.yml`
4. Add `scripts/export_pack.py <pack> --out dist/`
5. Add sparse-checkout instructions for Git users

## Track 6: Quality Gates

### Repository Gates

- `validate.py --json`
- `generate_index.py --check`
- `test_ai_protocol.py`
- `evaluate_ai_protocol.py` smoke
- pack install/validate smoke

### Future Gates

- `check_plan_protocol.py`
- `check_debug_report.py`
- `export_pack.py` smoke
- stale source review dashboard
- pack dependency consistency check

## Milestones

### Milestone A: Planning and Debug Core

- Add planning harnesses
- Add debug harnesses
- Add plan/debug protocol check scripts
- CI smoke for both

### Milestone B: Python Pack

- Add `packs/python-core/pack.yml`
- Add first 5 Python harnesses
- Add Python source registry entries
- Validate `--pack python-core`

### Milestone C: Pack Export

- Add pack export script
- Add pack index
- Add GitHub release packaging workflow
- Document consumer installation path

### Milestone D: Real Model Evaluation

- Run dsv4pro eval set
- Generate report
- Update model registry
- Decide allowed tier by task class

### Milestone E: Rust and Go Packs

- Add seed Rust pack
- Add seed Go pack
- Add cross-language common harnesses where duplication appears

## Decision Rules

- Do not add a language without a pack manifest.
- Do not promote a model without eval evidence.
- Do not add automation that requires humans to read large raw logs.
- Do not duplicate common guidance inside language packs; link to common harnesses.
- Prefer pack-aware scripts over manual installation instructions.
