---
type: harness
id: "common-model-capability-instruction-adherence"
title: "Model Capability and Instruction Adherence Checklist"
language: "common"
category: "ai"
tier: "C"
scope: "Constrain weaker or less reliable AI models so they follow development instructions, use harnesses, and improve through external verification rather than unchecked autonomy"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags:
  - ai
  - instruction-following
  - weak-models
  - model-capability
  - cpp
based_on:
  - "[C] NIST AI Risk Management Framework 1.0"
  - "[C] NIST AI 600-1 Generative AI Profile"
  - "[C] NIST SP 800-218 SSDF"
  - "[A] dev-guidelines Harness-Driven Development Protocol"
related:
  - "common/ai/ai-assisted-cpp-development.md"
  - "common/ai/ai-evaluation-and-regression-strategy.md"
  - "docs/ai/conversation-distillation.md"
  - "common/ai/tool-calling-and-agent-control.md"
  - "common/ai/prompt-injection-and-llm-security.md"
  - "common/code-review/harness-driven-review.md"
  - "common/planning/task-decomposition.md"
  - "common/planning/risk-and-verification-plan.md"
  - "common/debugging/root-cause-analysis.md"
  - "common/debugging/fix-verification.md"
  - "common/testing/testing-strategy.md"
  - "common/ci-cd/pipeline-patterns.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Model Capability and Instruction Adherence Checklist

**Based on:** NIST AI RMF 1.0 ([C]), NIST AI 600-1 Generative AI Profile ([C]), NIST SSDF ([C]), dev-guidelines harness protocol ([A]).
**Scope:** Applies when using less capable, less reliable, smaller, local, fine-tuned, or instruction-fragile models for software development. This includes models that are good at language completion but weaker at planning, long-context reasoning, tool discipline, or C++ correctness.

---

## Concepts

| Term | Meaning |
|------|---------|
| Capability tier | The permitted autonomy level for a model in a specific task class |
| Low-freedom task | A task with narrow scope, fixed inputs, constrained output schema, and external verification |
| Evidence gate | A required build, test, diff, source citation, or checklist result before accepting model output |
| Escalation | Switching to a stronger model, human review, or smaller subtask when adherence fails |
| Information budget | A fixed limit on user-facing status text so the model reports useful state without dumping process noise |

---

## Checklist

### 1. Capability Tier Before Task Assignment

- [ ] Model has not been evaluated on this repository and task type -> **(C)** Assign the lowest autonomy tier: explain, classify, or propose only; do not let it edit code autonomously. [R1][R2]
- [ ] Model passes repository-specific evals for the task type -> **(C)** Allow only the actions covered by those evals and evidence gates. [R1][R2]
- [ ] Model repeatedly ignores instructions, invents APIs, or skips verification -> **(C)** downgrade autonomy and require human or stronger-model review. [R1][R2]

### 2. Task Slicing for Weak Models

- [ ] Task spans multiple files, design decisions, or build-system changes -> **(A)** Split into single-purpose subtasks with one explicit expected output each. [R4]
- [ ] Task requires C++ ownership, lifetime, concurrency, templates, exception safety, or build configuration -> **(C)** require the model to load the matching harness before producing code. [R3][R4]
- [ ] Model must inspect code -> **(A)** provide exact file paths, relevant snippets, and a bounded question; avoid broad "understand the repo" prompts. [R4]

### 3. Low-Freedom Output Contract

- [ ] Model output will drive code review or implementation -> **(C)** require a fixed structure: objective, applicable harnesses, files touched, planned changes, verification commands, risks. [R3][R4]
- [ ] Model is asked to produce code -> **(C)** require a patch-sized change, not a full rewrite, unless the task explicitly asks for a rewrite. [R3]
- [ ] Model is asked for review -> **(C)** require file:line findings tied to checklist items; do not accept general impressions. [R4]

### 4. Harness Lock-In

- [ ] Applicable harnesses exist -> **(A)** name them before implementation or review, then process each relevant checklist item. [R4]
- [ ] Model skips harness selection -> **(A)** stop the task and ask for harness selection only; do not continue with code generation. [R4]
- [ ] Model cites a rule without a harness/source reference -> **(C)** treat it as advisory until independently verified. [R1][R3]

### 5. External Verification Over Self-Confidence

- [ ] Model claims code is correct -> **(C)** require build, test, static-analysis, sanitizer, or deterministic check evidence before accepting. [R3]
- [ ] Verification cannot be run -> **(A)** require a precise "not verified" note and reduce confidence; do not allow approval language. [R4]
- [ ] Model output conflicts with compiler/test results -> **(C)** trust the tool result and create a repair subtask. [R3]

### 6. Failure Handling and Escalation

- [ ] Model fails the same instruction twice in a task -> **(A)** reduce scope to the smallest failing step and restate the output contract. [R4]
- [ ] Model fails the same instruction three times -> **(C)** escalate to human review or a stronger model; do not continue accumulating changes. [R1][R2]
- [ ] Model produces unsafe tool actions, dependency changes, or broad rewrites outside scope -> **(C)** discard that output and re-run under tool-control constraints. [R2][R3]

### 7. Improvement Loop

- [ ] Model failure is representative of expected usage -> **(C)** add a regression case to the AI evaluation suite. [R1][R2]
- [ ] Prompt or task template is changed to fix adherence -> **(C)** re-run adherence and C++ correctness evals before broader use. [R1][R2]
- [ ] A weaker model consistently passes a task slice -> **(A)** promote only that slice to a higher autonomy tier; do not generalize to unrelated tasks. [R1]

### 8. User-Visible Progress Without Noise

- [ ] Task has more than one step or may take noticeable time -> **(A)** provide a short plan before work starts: goal, files/areas, verification, and stop condition. [R4]
- [ ] Work is in progress -> **(A)** emit concise status updates only at phase boundaries or blockers; avoid dumping chain-of-thought, raw logs, repeated file listings, or speculative narration. [R4]
- [ ] Tool output is long -> **(A)** summarize the decision-relevant result and retain raw details only when the user explicitly asks or the failure cannot be understood without them. [R4]
- [ ] Final response reports completion -> **(C)** include what changed, what was verified, what failed or was NOT VERIFIED, and the next concrete action. [R3][R4]
- [ ] The model is weak or instruction-fragile -> **(A)** use line-limited templates: plan <= 6 lines, progress <= 3 lines per update, final <= 10 lines unless findings require more. [R4]
- [ ] Human time should be minimized -> **(A)** prefer automatic phase-boundary updates, automatic verification summaries, and automatic escalation only on repeated failures or high-risk actions. [R4]

---

## Capability Tiers

| Tier | Allowed Model Actions | Required Gate |
|------|-----------------------|---------------|
| T0 | Summarize, classify, explain a known snippet | Human spot-check |
| T1 | Select harnesses, propose a plan, identify risks | Harness list review |
| T2 | Produce small patch for one bounded issue | Build/test or deterministic check |
| T3 | Multi-file change within known subsystem | Tests + reviewer approval + rollback path |
| T4 | Tool-using autonomous agent workflow | Tool-control harness + eval pass + human approval gates |

Start unknown or weaker models at T0/T1. Promote by task class, not by model brand.

---

## Decision Tree

```
Using a weaker or unproven model?
  -> Assign lowest capability tier
  -> Slice task to one bounded output
  -> Lock applicable harnesses
  -> Require fixed output contract
  -> Report short plan and phase updates
  -> Verify externally
  -> If repeated failure, escalate or downgrade
  -> Add failures to eval suite
```

---

## Anti-Patterns

### Anti-Pattern 1: Longer Prompt as Control

- **Appearance:** A model ignores instructions, so the prompt is expanded with more rules.
- **Trap:** More text feels like more control.
- **Consequence:** Weaker models lose the important constraints in a larger context.
- **Fix:** Shorten the task, fix the output schema, reduce autonomy, and add external checks.

### Anti-Pattern 2: Brand-Based Trust

- **Appearance:** A model is allowed to edit code because it is advertised as a coding model.
- **Trap:** Benchmarks do not prove repository-specific C++ behavior.
- **Consequence:** The model may compile plausible but wrong C++ or skip harness rules.
- **Fix:** Assign capability by local eval results and task class.

### Anti-Pattern 3: Self-Review Acceptance

- **Appearance:** The same model writes code and declares it correct without build/test evidence.
- **Trap:** The answer is coherent and confident.
- **Consequence:** Review accepts hallucinated APIs, missing edge cases, or C++ undefined behavior.
- **Fix:** Require tool evidence or independent review before acceptance.

### Anti-Pattern 4: Progress Spam

- **Appearance:** The model prints long reasoning, full command logs, repeated directory listings, or every micro-step.
- **Trap:** More text looks transparent.
- **Consequence:** Users cannot see the actual plan, current state, or blocking issue.
- **Fix:** Use information budgets: short plan, phase-boundary updates, summarized evidence, and explicit NOT VERIFIED items.

---

## See Also

- [AI-Assisted C++ Development](ai-assisted-cpp-development.md) - C++-specific gates for AI-authored changes
- [AI Evaluation and Regression Strategy](ai-evaluation-and-regression-strategy.md) - evals that determine capability tiers
- [Tool Calling and Agent Control](tool-calling-and-agent-control.md) - autonomy and tool permission boundaries
- [Prompt Injection and LLM Application Security](prompt-injection-and-llm-security.md) - security constraints for instruction boundaries
- [Harness-Driven Development Protocol](../code-review/harness-driven-review.md) - required harness selection and review flow
- [Testing Strategy](../testing/testing-strategy.md) - external verification structure
- [CI/CD Pipeline Patterns](../ci-cd/pipeline-patterns.md) - automation gates

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C18] NIST AI Risk Management Framework 1.0 | Govern, Map, Measure, Manage | verified-2026 | 2026-06 |
| R2 | C | [C19] NIST AI 600-1 Generative AI Profile | Pre-deployment testing, monitoring, risk response | verified-2026 | 2026-06 |
| R3 | C | [C6] NIST SP 800-218 SSDF | Verification and release practices | verified-2026 | 2026-06 |
| R4 | A | dev-guidelines Harness-Driven Development Protocol | Harness discovery and application | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
- 2026.06: Added information-budget rules for concise user-visible progress
