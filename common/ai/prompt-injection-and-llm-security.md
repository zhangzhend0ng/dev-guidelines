---
type: harness
id: "common-prompt-injection-llm-security"
title: "Prompt Injection and LLM Application Security Checklist"
language: "common"
category: "ai"
tier: "C"
scope: "Defend LLM applications and AI-assisted development workflows against prompt injection, unsafe outputs, sensitive data exposure, and excessive agency"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-15"
review_cycle: "12m"
tags:
  - ai
  - llm-security
  - prompt-injection
  - data-leakage
  - agent-security
based_on:
  - "[C] OWASP Top 10 for LLM Applications 2025"
  - "[C] NIST AI 600-1 Generative AI Profile"
  - "[C] OWASP ASVS"
  - "[C] NIST SP 800-218 SSDF"
related:
  - "common/ai/model-capability-and-instruction-adherence.md"
  - "common/ai/tool-calling-and-agent-control.md"
  - "common/ai/ai-assisted-cpp-development.md"
  - "common/ai/ai-evaluation-and-regression-strategy.md"
  - "common/security/input-validation.md"
  - "common/dependencies/dependency-management.md"
  - "common/logging/logging-standards.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Prompt Injection and LLM Application Security Checklist

**Based on:** OWASP Top 10 for LLM Applications 2025 ([C]), NIST AI 600-1 Generative AI Profile ([C]), OWASP ASVS ([C]), NIST SSDF ([C]).
**Scope:** Applies to LLM applications, AI coding assistants, RAG systems, agent workflows, and tool-using models. This harness focuses on LLM-specific security risks; use the linked security, dependency, logging, and tool-control harnesses for implementation details.

---

## Concepts

| Term | Meaning |
|------|---------|
| Direct prompt injection | User input attempts to override trusted instructions |
| Indirect prompt injection | External content, retrieved documents, tool outputs, logs, or repo files contain malicious instructions |
| Unsafe output handling | Model output is passed to an interpreter, renderer, database, shell, build system, or tool without validation |
| Excessive agency | The model can perform actions beyond what the user intended or the workflow requires |

---

## Checklist

### 1. Instruction Boundary

- [ ] LLM consumes user, repository, retrieved, web, or tool text -> **(C)** Treat that text as untrusted data, never as system or developer instructions. [R1]
- [ ] External content asks the model to reveal secrets, ignore rules, change goals, or run tools -> **(C)** Reject the instruction and preserve the trusted instruction hierarchy. [R1][R2]
- [ ] The workflow mixes trusted policy with untrusted task data -> **(C)** Separate policy/instructions from data by schema, role, delimiter, or tool contract. [R1][R4]

### 2. Tool and Action Containment

- [ ] Model output can trigger tools, shell commands, file writes, network calls, database writes, or dependency changes -> **(C)** Apply tool-calling controls, least privilege, and human approval gates. [R1][R4]
- [ ] The model can chain multiple tools -> **(C)** Limit tool sequence length, stop conditions, data flow, and permissions across the chain. [R1][R4]
- [ ] A tool result introduces new instructions -> **(C)** Treat them as data and re-check the original task scope before acting. [R1]

### 3. Sensitive Information Protection

- [ ] Prompt, context, retrieval corpus, tool output, or logs may contain secrets, PII, credentials, or proprietary code -> **(C)** Redact, minimize, or block exposure before model use and logging. [R1][R2][R3]
- [ ] Model output may disclose hidden policy, system prompts, private context, or credentials -> **(C)** Filter and review output before returning it to users or tools. [R1][R3]
- [ ] The workflow needs secret-dependent action -> **(C)** Use scoped credentials in the tool layer; do not ask the model to handle raw secrets. [R3][R4]

### 4. Output Handling

- [ ] LLM output reaches HTML, Markdown, SQL, shell, code generation, build config, file paths, or API calls -> **(C)** Validate and encode for the target context before use. [R1][R3]
- [ ] LLM output is used as code or configuration -> **(C)** Require review, tests, and relevant harness checks before execution or merge. [R1][R4]
- [ ] Output cannot be validated for the target context -> **(C)** Keep it advisory only; do not execute or persist it automatically. [R1]

### 5. RAG and Context Integrity

- [ ] Retrieval sources include user-controlled, third-party, or generated content -> **(C)** Mark source trust level and prevent retrieved text from controlling instructions or tools. [R1][R2]
- [ ] Retrieved content is stale, low-confidence, or unauthenticated -> **(A)** Surface uncertainty and require source verification before high-impact decisions. [R2]
- [ ] Embeddings or vector stores are updated from untrusted content -> **(C)** apply supply-chain and data-poisoning review before ingestion. [R1][R2]

### 6. Abuse, Misinformation, and High-Risk Output

- [ ] The model can produce dangerous, illegal, hateful, deceptive, or materially harmful instructions -> **(C)** Add refusal, escalation, and review policy before release. [R1][R2]
- [ ] Output influences user decisions in security, finance, legal, medical, employment, safety, or production operations -> **(C)** Require human review and calibrated uncertainty. [R2]
- [ ] Model answer lacks sufficient evidence for a factual claim -> **(A)** Prefer citations, provenance, or an explicit uncertainty statement. [R2]

### 7. Security Regression Coverage

- [ ] A mitigation is added for prompt injection, leakage, unsafe output, excessive agency, or RAG poisoning -> **(C)** Add it to the AI evaluation regression suite. [R1][R2]
- [ ] A prompt, tool schema, retrieval pipeline, or model version changes -> **(C)** Re-run the LLM security regression cases before release. [R1][R2][R4]

---

## Decision Tree

```
LLM sees untrusted content?
  -> Keep instruction boundary
  -> Minimize sensitive data
  -> If tools/actions exist, apply agent control
  -> Validate output by target context
  -> Add regression tests for discovered attacks
```

---

## Anti-Patterns

### Anti-Pattern 1: Markdown-as-Policy

- **Appearance:** Retrieved Markdown says "ignore previous instructions" and the agent follows it.
- **Trap:** The text appears in a relevant document.
- **Consequence:** Indirect prompt injection can redirect tools or leak secrets.
- **Fix:** Treat retrieved content as data only; trusted policy remains outside retrieval.

### Anti-Pattern 2: Safe-Looking Output

- **Appearance:** Model output is directly inserted into Markdown, shell, SQL, HTML, or generated code.
- **Trap:** Natural language makes the output look reviewed.
- **Consequence:** Injection, XSS, command execution, broken build config, or unsafe code.
- **Fix:** Validate/encode for the target interpreter and require review before execution.

### Anti-Pattern 3: Security by Hidden Prompt

- **Appearance:** The only protection is a system prompt telling the model not to do unsafe things.
- **Trap:** It is fast to add and often works in happy-path demos.
- **Consequence:** Direct or indirect injection bypasses it.
- **Fix:** Combine instruction policy with tool permissions, output validation, approval gates, and regression tests.

---

## See Also

- [Tool Calling and Agent Control](tool-calling-and-agent-control.md) - least privilege, approval gates, and auditability for model actions
- [AI-Assisted C++ Development](ai-assisted-cpp-development.md) - applies these controls to C++ coding workflows
- [AI Evaluation and Regression Strategy](ai-evaluation-and-regression-strategy.md) - stores attack cases and model/prompt regressions
- [Input Validation](../security/input-validation.md) - context-specific validation and output encoding
- [Dependency Management](../dependencies/dependency-management.md) - supply-chain controls for models, tools, and retrieval inputs
- [Logging Standards](../logging/logging-standards.md) - safe observability without leaking sensitive context

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C16] OWASP Top 10 for LLM Applications 2025 | LLM01-LLM10 | verified-2026 | 2026-06 |
| R2 | C | [C19] NIST AI 600-1 Generative AI Profile | GAI risks and suggested actions | verified-2026 | 2026-06 |
| R3 | C | [C8] OWASP ASVS | Input validation, access control, logging, data protection | verified-2026 | 2026-06 |
| R4 | C | [C6] NIST SP 800-218 SSDF | Secure design, verification, and release practices | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
