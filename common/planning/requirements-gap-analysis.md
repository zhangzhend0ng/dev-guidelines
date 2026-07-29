---
type: harness
id: "common-planning-requirements-gap-analysis"
title: "Requirements-vs-Implementation Gap Analysis Checklist"
language: "common"
category: "planning"
tier: "C"
scope: "Produce a defensible, evidence-backed gap analysis between a requirements document (PRD/spec) and the actual code state, before any backlog is scheduled"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-29"
review_cycle: "12m"
tags: [planning, requirements, gap-analysis, traceability, backlog, PRD, evidence]
based_on:
  - "[N] ISO/IEC/IEEE 29148:2018"
  - "[A] The Pragmatic Programmer"
related:
  - "common/planning/task-decomposition.md"
  - "common/planning/change-scope-control.md"
  - "common/debugging/root-cause-analysis.md"
supersedes: []
changelog:
  - "2026.07: Initial draft — distilled from real requirements-vs-code review sessions where memory-based assumptions inflated the backlog and hidden identity questions carried 10x cost"
---

# Requirements-vs-Implementation Gap Analysis Checklist

**Based on:** ISO/IEC/IEEE 29148:2018 ([N9]), The Pragmatic Programmer ([A8]).
**Scope:** The analytical gate that *produces* a defensible backlog by auditing a requirements document against the actual code state. This harness answers **what is actually missing and what is the risk of each gap**; `common/planning/task-decomposition.md` answers **how to split confirmed work into tasks**. It does NOT cover writing requirements (that is upstream product work) or sizing tasks (that is task-decomposition).

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|------------|
| Gap | A difference between what the PRD requires and what the code currently does, **backed by a file:line evidence of the current code state** |
| Traceability | The ability to follow each requirement forward to its implementation (and back) — ISO/IEC/IEEE 29148 calls this the RTM/VCRM |
| Correction pass | A dedicated re-read of the actual code to overturn assumptions about what is already implemented, performed *before* the backlog is finalized |
| Hidden risk | A gap that looks minor but whose worst-case resolution cost is ~10x the estimate (typically an identity/attribution question: "is our X the same as the spec's X?") |

**When this harness applies:** when handed a requirements/PRD document and asked "what's left to build" or "are we done." **When it does NOT apply:** greenfield work with no existing code to audit, or pure bug triage (use `common/debugging/root-cause-analysis.md`).

---

## Checklist

### 1. Every Gap Claim Cites Code Evidence **(C)** [R1]

- [ ] A requirement is marked "must build" but no `file:line` proving the current code state is recorded → **(C)** record the evidence before marking; "I think it's missing" is an assumption, not a gap. [R1]
- [ ] A requirement is marked "already implemented" but the reviewer is recalling from memory rather than citing the function/file that implements it → **(C)** re-read the code at the cited location; memory-based "done" claims are the #1 source of false gaps. [R1]
- [ ] The gap list distinguishes "code path X exists but is dead/unreachable" from "code path X does not exist" → **(C)** dead code is a different task (remove or revive) than missing code (build). [R1]

### 2. Correction Pass Before Finalizing **(A)** [R2]

- [ ] Before the backlog is frozen, a dedicated pass re-verifies every "must build" item against the actual code → **(A)** assuming-from-memory inflates the backlog by ~30% in practice; some "must build" items turn out already implemented via a path the reviewer forgot. [R2]
- [ ] When the code contradicts the initial judgment, the gap is corrected and the reason recorded → **(A)** the correction (and why the assumption was wrong) is itself the valuable output. [R2]

### 3. Re-Bucket by Schedulability **(A)** [R2]

- [ ] Each confirmed gap is re-bucketed into one of: **(A)** pure-dev-controllable (start immediately regardless of decisions); **(B)** logic-layer buildable now but UI/asset-layer waits on design input; **(C)** blocked by external input (process data, spec confirmation) → **(A)** this separates "what to start Monday" from "what to push externally," which a single flat list cannot. [R2]
- [ ] Gaps in bucket C have an explicit owner and a requested-by date → **(A)** an externally-blocked gap without an owner and deadline stays blocked forever. [R2]

### 4. Escalate Hidden Risks **(C)** [R1]

- [ ] A gap that is an identity/attribution question ("is our implementation of X the same algorithm/approach the spec calls X?") is flagged as a potential schedule-killer → **(C)** if the answer is "no," resolution can cost 10x (rewrite + golden-test invalidation + re-baseline); these need a week-1 decision deadline, not a backlog line. [R1]
- [ ] The worst-case cost of a hidden risk is stated alongside its likelihood → **(C)** "minor confirmation" framing hides a 10x tail; state the tail. [R1]

### 5. Distinguish "Scope Empty" from "Scope Not Written" **(A)** [R2]

- [ ] The PRD's release-scope section is read literally → **(A)** an empty scope section (title followed by no content) means the cut line (what ships vs defers) was never decided, and "review approved" does not change that. [R2]
- [ ] If the scope/cut section is empty, the first deliverable is *defining the cut*, not scheduling tasks against an undefined scope → **(A)** scheduling against an undefined cut guarantees rework. [R2]

### 6. Revision Noise vs Real Change **(A)** [R2]

- [ ] A large revision-number jump on a requirements doc is treated as a signal to diff, not to re-analyze wholesale → **(A)** a 100x revision jump with a tiny text diff usually means backend formatting/image re-upload/version-algorithm churn, not a requirement shift. [R2]
- [ ] The conclusion distinguishes "requirement changed" from "formatting/version churn" → **(A)** wasted re-planning comes from trusting the revision-number magnitude over the actual diff. [R2]

---

## Quick Decision Tree

```
Handed a PRD + "what's left"
  │
  ├─ For each requirement, can you cite file:line of current code state?
  │     └─ NO → do the correction pass first (item 2), then cite evidence (item 1)
  │
  ├─ After correction pass, bucket each confirmed gap:
  │     ├─ A (dev-controllable) → schedulable now
  │     ├─ B (waits on design)  → start logic layer, flag asset dependency
  │     └─ C (external input)   → assign owner + deadline, push externally
  │
  ├─ Any gap an identity/attribution question (item 4)?
  │     └─ YES → set week-1 decision deadline, state 10x worst-case cost
  │
  └─ Release-scope section empty (item 5)?
        └─ YES → first deliverable is defining the cut, not scheduling
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Memory-Based Gap Lists

- **Appearance:** A gap list where every "must build" item reflects the reviewer's recollection, with no `file:line` evidence and no correction pass.
- **Trap:** The reviewer is confident; the list looks complete and actionable.
- **Consequence:** ~30% of items are already implemented (via a forgotten path) — the backlog is inflated, real blockers are buried, and "done" keeps surprising everyone.
- **Fix:** Item 1 + Item 2: cite evidence for every claim; run a correction pass to overturn assumptions before freezing the backlog.

### Anti-Pattern 2: Flat Backlog Hides External Blockers

- **Appearance:** All gaps in one flat list, ordered by perceived size.
- **Trap:** A flat list is easy to estimate and "just start."
- **Consequence:** Dev-controllable work and externally-blocked work compete for the same queue; externally-blocked items sit forever because nobody owns pushing them out.
- **Fix:** Item 3: re-bucket into A/B/C with explicit owners and deadlines on C.

### Anti-Pattern 3: "Minor Confirmation" That Kills the Schedule

- **Appearance:** An identity question ("is our mixer the spec's algorithm?") listed as a low-priority confirmation line.
- **Trap:** It reads as a one-line yes/no, so it gets deprioritized.
- **Consequence:** A "no" answer late in the cycle forces a rewrite, invalidates golden tests, and rebaselines the whole matching-quality floor — a 10x cost that can slip a release.
- **Fix:** Item 4: flag identity/attribution questions as schedule-killers with a week-1 deadline and an explicit worst-case cost.

---

## See Also

- [Task Decomposition Checklist](task-decomposition.md) — the downstream gate; this harness produces the defensible backlog that task-decomposition then splits into tasks.
- [Change Scope Control Checklist](change-scope-control.md) — keeping a *code change* in scope; complementary to this harness's pre-implementation scope *analysis*.
- [Root Cause Analysis Checklist](../debugging/root-cause-analysis.md) — evidence-backed reasoning for *bugs*; this harness applies the same evidence discipline to *requirement gaps*.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | [N9] ISO/IEC/IEEE 29148:2018 | Requirements traceability and coverage analysis (RTM; each requirement traced forward to implementation and back) | verified-2026 | 2026-07 |
| R2 | A | [A8] The Pragmatic Programmer (20th) | "Tracer Bullets," "It's All Writing," traceability of decisions | verified-2026 | 2026-07 |

---

## Changelog

- 2026.07: Initial draft — 6 items covering evidence-backed gaps, correction pass, A/B/C re-bucketing, hidden-risk escalation, empty-vs-unwritten scope, and revision-noise discrimination. Distilled from real PRD-vs-code review sessions.
