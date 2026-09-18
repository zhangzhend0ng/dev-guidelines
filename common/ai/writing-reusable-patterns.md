---
type: harness
id: "common-writing-reusable-patterns"
title: "Writing Reusable Experience Patterns Checklist"
language: "common"
category: "ai"
tier: "A"
scope: "Distill a lesson (incident, correction, rework, test failure) into a reusable pattern entry for the cross-repo pattern index, and gate it against dilution, duplication, and domain lock-in"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-18"
review_cycle: "12m"
tags: [ai, experience, patterns, knowledge-distillation, agent-collaboration]
based_on:
  - "[A] ReasoningBank (Google Research, 2025)"
  - "[A] dev-guidelines references/pattern-index.md — Abstraction Method"
apply_globs: ["**/loop-journal.md", "**/pattern-index.md"]
related:
  - "references/pattern-index.md"
  - "common/meta/prior-art-and-reuse.md"
  - "common/code-review/harness-driven-review.md"
supersedes: []
changelog:
  - "2026.09: Initial draft — operationalizes the abstraction method distilled from three-repo loop-journal pattern indexes (59 entries, same lesson independently re-learned up to 4 times across repos)"
---

# Writing Reusable Experience Patterns Checklist

**Based on:** ReasoningBank ([A]), `references/pattern-index.md` Part 2 — Abstraction Method ([A]).
**Scope:** Applies when converting any learned lesson into an index entry — personal loop-journal updates, cross-repo pattern proposals, post-incident notes. Defers to `common/meta/prior-art-and-reuse.md` for harness-level dedup and to `references/pattern-index.md` for the current family list.

---

## Concepts

| Term | Meaning |
|------|---------|
| Family | A cluster of same-cause lessons sharing one strategy card (e.g., `false-green`) |
| Strategy card | The reusable unit: trigger / why-it-fails / countermeasure, stripped of proper nouns |
| Stable key | A kebab-case English name plus 2–3 grep words; never renamed, only aliased |
| 超坐检查 (supersede check) | grep the shared index before adding — a hit means new evidence for an existing family, not a new entry |
| Abstraction ladder | L0 incident → L1 tool rule → L2 strategy (target) → L3 vacuous principle (stop) |

---

## Checklist

### 1. Strip Proper Nouns **(A)** [R1][R3]

- [ ] Entry draft replaces every project/module/tool/dataset name with its category word → **(A)** only trigger-condition, failure-mode, and countermeasure survive the strip. [R1]
- [ ] Domain knowledge that cannot survive the strip (needs domain context to trigger) → **(A)** keep it in project docs or repo-local journal, not the shared index. [R1]

### 2. Pass the Generalization Test **(A)** [R1]

- [ ] Place the sentence in a project you have never worked on → **(A)** it must still fire at the right moment; if it needs background to be understood, return to Item 1. [R1]

### 3. Write the Three-Slot Form **(A)** [R1][R2]

- [ ] Entry is exactly trigger / failure mode / countermeasure → **(A)** trigger must be detectable (grep-able or askable); a lesson without a detectable trigger can never fire. [R1]
- [ ] Countermeasure is a strategy, not a procedure ("prove X first", not "click button Y") → **(A)** procedural rules do not transfer across tools; ReasoningBank attributes its gains to strategy-level abstraction. [R2]

### 4. Calibrate the Abstraction Level **(A)** [R1]

- [ ] Stop at L2: abstract upward only while the trigger remains detectable; keep downward only while the entry is executable without knowing the original incident → **(A)** one level up is vacuous truth, one level down is domain lock-in. [R1]

### 5. Assign a Stable Key **(A)** [R1]

- [ ] One kebab-case name + 2–3 grep words chosen; the name is permanent → **(A)** later synonym discoveries attach as aliases; renaming breaks grep history ("措辞不稳 = 等于没索引"). [R1]

### 6. Run the Supersede Check **(A)** [R1][R3]

- [ ] Before adding, grep the shared index discriminators and record what was searched and hit/missed → **(A)** a hit means attach an alias to that family instead of opening a new entry; three repos paid 4× tuition for one heredoc lesson because this step did not cross repo boundaries. [R1][R3]

### 7. Capture at the Moment, Not from Memory **(A)** [R1][R2]

- [ ] Within the session where a correction/rework/test failure happens, write one failure-counterfactual ("if I had 〈countermeasure〉, 〈failure〉 would not have happened") → **(A)** the counterfactual is natively three-slot; entries rewritten later drop sharply in quality. [R1][R2]

### 8. Attach Provenance and Respect the Cap **(A)** [R1][R3]

- [ ] Entry cites first-seen repo + one-line incident as provenance → **(A)** an entry that cannot answer "what real cost taught this" is an opinion, not experience. [R1]
- [ ] Family count stays under the soft cap (~15); exceeding it requires deprecating a ≥2-season hitless family first → **(A)** the index rots by accretion, not by error. [R1][R3]

---

## Reference Sources

| Ref | Source |
|-----|--------|
| [R1] | `references/pattern-index.md` Part 2 — Abstraction Method (five steps, ladder, stopping rule), distilled from three-repo loop-journal evidence |
| [R2] | [A24] ReasoningBank (Google Research, 2025) — strategy-vs-procedural memory, failure-driven extraction, append-only robustness |
| [R3] | Session-digest corpus analysis 2026-09 (1501 sessions): heredoc lesson re-learned 4× across 3 repos; pattern indexes frozen for 165 iterations |

## Anti-Patterns

| Name | Symptom | Cause | Fix |
|------|---------|-------|-----|
| Incident-level entry | Entry readable only with knowledge of the original bug | Wrote at L0/L1 of the ladder | Items 1–2: strip + generalization test |
| Vacuous principle | "Be careful with encoding" — always true, never fires | Over-abstracted past L2 | Item 4: stop where trigger is detectable |
| Fourth island | Same lesson under a new name in a new repo | Supersede check skipped or scoped to one repo | Item 6: grep the shared index, attach aliases |
| Post-hoc memoir | Entry written weeks after the incident, generic and unfireable | Distillation from memory instead of the moment | Item 7: failure-counterfactual in-session |
