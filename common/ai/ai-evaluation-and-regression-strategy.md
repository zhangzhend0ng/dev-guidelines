---
type: harness
id: "common-ai-evaluation-regression"
title: "AI Evaluation and Regression Strategy Checklist"
language: "common"
category: "ai"
tier: "C"
scope: "Define evaluation datasets, regression gates, risk thresholds, and release evidence for LLM applications and AI-assisted development workflows"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags:
  - ai
  - evaluation
  - regression
  - testing
  - release-gates
based_on:
  - "[C] NIST AI Risk Management Framework 1.0"
  - "[C] NIST AI 600-1 Generative AI Profile"
  - "[C] NIST SP 800-218 SSDF"
  - "[C] Google Testing Blog"
related:
  - "common/ai/ai-assisted-cpp-development.md"
  - "common/ai/prompt-injection-and-llm-security.md"
  - "common/testing/testing-strategy.md"
  - "common/ci-cd/pipeline-patterns.md"
  - "common/documentation/documentation-standards.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# AI Evaluation and Regression Strategy Checklist

**Based on:** NIST AI RMF 1.0 ([C]), NIST AI 600-1 Generative AI Profile ([C]), NIST SSDF ([C]), Google Testing guidance ([C]).
**Scope:** Applies to LLM applications, AI coding assistants, RAG systems, agent workflows, prompt changes, model upgrades, and tool-schema changes. This harness defines release evidence; it does not define model training methodology.

---

## Concepts

| Term | Meaning |
|------|---------|
| Evaluation suite | Curated cases used to measure behavior before release |
| Regression case | A case that previously failed, was fixed, and must not fail again |
| Golden case | A stable expected behavior case with an agreed oracle or rubric |
| Risk threshold | The minimum acceptable score or maximum acceptable failure rate for a release gate |
| Judge | Human reviewer, deterministic checker, or model-assisted grader with documented limitations |

---

## Checklist

### 1. Risk-Based Evaluation Scope

- [ ] AI behavior affects security, safety, production operations, user trust, or code correctness -> **(C)** Define evaluation goals before release. [R1][R2]
- [ ] The feature is advisory only and low impact -> **(A)** Use lightweight smoke evals plus manual review. [R1]
- [ ] The feature can execute tools, change code, or influence high-impact decisions -> **(C)** Include security, correctness, and misuse cases in the eval suite. [R1][R2]

### 2. Dataset Composition

- [ ] Evaluation suite exists -> **(C)** Include happy-path, edge, adversarial, out-of-scope, and refusal cases. [R1][R2]
- [ ] System uses RAG or external context -> **(C)** Include stale, conflicting, missing, malicious, and low-quality source cases. [R2]
- [ ] System writes or reviews C++ code -> **(C)** Include cases that exercise applicable C++ harness failures, not only syntax examples. [R3]

### 3. Oracles and Rubrics

- [ ] Expected answer can be deterministic -> **(C)** Use exact, structured, or property-based checks where possible. [R3][R4]
- [ ] Expected answer requires judgment -> **(C)** Use a written rubric with pass/fail criteria and examples. [R1]
- [ ] Model-assisted judging is used -> **(A)** Calibrate against human-reviewed samples and track judge drift. [R1]

### 4. Regression Capture

- [ ] A production incident, red-team finding, user report, or review failure occurs -> **(C)** Add a minimized regression case before or with the fix. [R2][R3]
- [ ] Prompt, model, retrieval, tool schema, or safety policy changes -> **(C)** Re-run all relevant regression cases. [R1][R3]
- [ ] A regression is intentionally accepted -> **(C)** Document the owner, reason, expiration date, and compensating control. [R1][R3]

### 5. Release Gates

- [ ] AI behavior is released to users or used in CI/review automation -> **(C)** Define blocking thresholds for correctness, safety, leakage, tool misuse, and latency/cost where relevant. [R1][R2][R3]
- [ ] A threshold fails -> **(C)** Block release unless a documented risk acceptance is approved. [R1][R3]
- [ ] Metrics improve overall but a critical class regresses -> **(C)** Block release for that class; do not average it away. [R1][R2]

### 6. Change Management

- [ ] Model, prompt, system instruction, retrieval corpus, embedding model, tool schema, or temperature changes -> **(C)** Treat it as a behavior-affecting change and re-run targeted evals. [R1][R2]
- [ ] Vendor model is updated silently or version is floating -> **(C)** Pin versions where possible or schedule periodic canary evals. [R1][R3]
- [ ] Eval suite itself changes -> **(A)** Record why cases were added, removed, or reweighted. [R1]

### 7. Evidence and Audit Trail

- [ ] Eval run supports a release or review decision -> **(C)** Record model/version, prompt/version, tools enabled, dataset version, scores, failures, and reviewer disposition. [R1][R3]
- [ ] Failures remain at release -> **(C)** Link each failure to risk acceptance, mitigation, or follow-up issue. [R1][R2]
- [ ] Eval data contains sensitive information -> **(C)** sanitize storage and logs according to privacy and logging rules. [R2][R3]

---

## Decision Tree

```
AI behavior changes?
  -> Classify risk
  -> Select eval suites
  -> Run golden + adversarial + regression cases
  -> Apply release thresholds
  -> Record evidence
  -> Add new failures back into regression set
```

---

## Anti-Patterns

### Anti-Pattern 1: Demo-Only Evaluation

- **Appearance:** The system is judged by a few hand-picked examples.
- **Trap:** Demos show capability but not failure boundaries.
- **Consequence:** Known weak classes regress unnoticed.
- **Fix:** Maintain versioned happy-path, edge, adversarial, and regression cases.

### Anti-Pattern 2: Averaging Away Critical Failures

- **Appearance:** Overall score improves while prompt-injection or code-correctness failures worsen.
- **Trap:** One number is easy to report.
- **Consequence:** A release passes despite unacceptable risk in a critical class.
- **Fix:** Use per-risk thresholds and block on critical class regressions.

### Anti-Pattern 3: Floating Model Gate

- **Appearance:** The eval passes once, but the provider model later changes without revalidation.
- **Trap:** The application code did not change.
- **Consequence:** Behavior changes outside source control.
- **Fix:** Pin model versions when possible and run canary evals when versions are floating.

---

## See Also

- [AI-Assisted C++ Development](ai-assisted-cpp-development.md) - C++ correctness and verification expectations for AI-authored changes
- [Prompt Injection and LLM Application Security](prompt-injection-and-llm-security.md) - security cases that must feed the regression suite
- [Testing Strategy](../testing/testing-strategy.md) - general test taxonomy and strategy
- [CI/CD Pipeline Patterns](../ci-cd/pipeline-patterns.md) - automation and release gates
- [Documentation Standards](../documentation/documentation-standards.md) - evidence, changelog, and decision documentation

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C18] NIST AI Risk Management Framework 1.0 | Govern, Map, Measure, Manage | needs-review | 2026-06 |
| R2 | C | [C19] NIST AI 600-1 Generative AI Profile | GAI risks, pre-deployment testing, incident disclosure | verified-2026 | 2026-06 |
| R3 | C | [C6] NIST SP 800-218 SSDF | Verification, release, and response practices | verified-2026 | 2026-06 |
| R4 | C | [C12] Google Testing Blog | Test sizing, quality, and regression practices | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
