# Harness Index

Cross-project shared code review and generation guidelines. Each harness is a checklist-based decision document.

## Quick Lookup

| I need to... | See |
|-------------|------|
| Validate function parameters | Parameter Validation (cpp/functions/) |
| Use AI to write or review C++ code | [AI-Assisted C++ Development](common\ai\ai-assisted-cpp-development.md) |
| Control AI tool calls or agent actions | [Tool Calling and Agent Control](common\ai\tool-calling-and-agent-control.md) |
| Propose a new harness | [Contributing Guide](CONTRIBUTING.md) |
| Understand the authority system | [Design Spec](docs/specs/2026-05-31-repo-structure-design.md) |

## All Harnesses by Category

<!-- INDEX_START -->
### ai

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-ai-evaluation-regression | [AI Evaluation and Regression Strategy Checklist](common\ai\ai-evaluation-and-regression-strategy.md) | common | C | draft | 2026.06 |
| common-ai-assisted-cpp-development | [AI-Assisted C++ Development Checklist](common\ai\ai-assisted-cpp-development.md) | common | C | draft | 2026.06 |
| common-prompt-injection-llm-security | [Prompt Injection and LLM Application Security Checklist](common\ai\prompt-injection-and-llm-security.md) | common | C | draft | 2026.06 |
| common-tool-calling-agent-control | [Tool Calling and Agent Control Checklist](common\ai\tool-calling-and-agent-control.md) | common | C | draft | 2026.06 |

### build

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-build-system | [C++ Build System and Include Hygiene Checklist](cpp\build\cmake-include-hygiene.md) | cpp | C | draft | 2026.06 |
| cpp-package-management | [C++ Package Management Checklist](cpp\build\package-management.md) | cpp | C | draft | 2026.06 |

### code-review

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-code-review-checklist | [Code Review Checklist](common\code-review\review-checklist.md) | common | C | draft | 2026.06 |
| common-harness-driven-review | [Harness-Driven Development Protocol](common\code-review\harness-driven-review.md) | common | A | draft | 2026.06 |

### commits

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-conventional-commits | [Commit Message Conventions Checklist](common\commits\conventional-commits.md) | common | C | draft | 2026.06 |

### correctness

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-class-hierarchies | [Class Hierarchies and Virtual Dispatch Checklist](cpp\correctness\class-hierarchies.md) | cpp | N | draft | 2026.06 |
| cpp-compile-time | [Compile-Time Programming Checklist](cpp\correctness\compile-time-programming.md) | cpp | N | draft | 2026.06 |
| cpp-thread-safety | [Concurrency and Thread Safety Checklist](cpp\concurrency\thread-safety.md) | cpp | N | draft | 2026.06 |
| cpp-const-correctness | [Const Correctness Checklist](cpp\correctness\const-correctness.md) | cpp | N | draft | 2026.05 |
| cpp-exception-safety | [Exception Safety Guarantees Checklist](cpp\correctness\exception-safety.md) | cpp | N | draft | 2026.06 |
| cpp-integer-safety | [Integer Safety Checklist](cpp\correctness\integer-safety.md) | cpp | N | draft | 2026.06 |
| cpp-interface-contracts | [Interface Contracts and Design-by-Contract Checklist](cpp\correctness\interface-contracts.md) | cpp | N | draft | 2026.06 |
| cpp-lifetime | [Object Lifetime and Dangling References Checklist](cpp\lifetime\dangling-references.md) | cpp | N | draft | 2026.06 |
| cpp-stl-containers | [STL Algorithms and Containers Checklist](cpp\correctness\stl-algorithms-containers.md) | cpp | N | draft | 2026.06 |
| cpp-type-safety | [Type Safety and Implicit Conversions Checklist](cpp\correctness\type-safety.md) | cpp | N | draft | 2026.06 |
| cpp-undefined-behavior | [Undefined Behavior Prevention Checklist](cpp\correctness\undefined-behavior.md) | cpp | N | draft | 2026.06 |

### dependencies

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-dependency-management | [Dependency Management Checklist](common\dependencies\dependency-management.md) | common | N | draft | 2026.06 |

### design

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-api-design | [API Design Principles Checklist](common\api-design\restful-api-design.md) | common | C | draft | 2026.06 |
| common-error-handling | [Error Handling Strategy Checklist](common\error-handling\error-handling-strategy.md) | common | C | draft | 2026.05 |

### documentation

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-documentation-standards | [Documentation Standards Checklist](common\documentation\documentation-standards.md) | common | C | draft | 2026.06 |

### functions

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-param-validation | [Parameter Validation Checklist](cpp\functions\parameter-validation.md) | cpp | C | draft | 2026.05 |

### logging

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-logging-standards | [Logging Standards Checklist](common\logging\logging-standards.md) | common | N | draft | 2026.06 |

### meta

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-harness-evolution | [Harness Evolution and Lifecycle Governance](common\meta\harness-evolution.md) | common | A | draft | 2026.05 |

### naming

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-naming-conventions | [Naming Conventions Checklist](common\naming\naming-conventions.md) | common | C | draft | 2026.06 |

### performance

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-performance-patterns | [C++ Performance Patterns Checklist](cpp\performance\optimization-patterns.md) | cpp | N | draft | 2026.06 |

### resource-management

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-move-semantics | [Move Semantics and Rule of Five Checklist](cpp\memory\move-semantics.md) | cpp | N | draft | 2026.06 |
| cpp-raii | [RAII and Resource Management Checklist](cpp\memory\raii.md) | cpp | N | draft | 2026.05 |
| cpp-ownership | [Smart Pointer and Ownership Semantics Checklist](cpp\memory\ownership.md) | cpp | N | draft | 2026.05 |

### security

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-input-validation | [Input Validation Checklist](common\security\input-validation.md) | common | N | draft | 2026.05 |

### templates

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-template-best-practices | [Template Best Practices and Concepts Checklist](cpp\templates\template-best-practices.md) | cpp | N | draft | 2026.06 |

### testing

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-catch2 | [Catch2 Testing Patterns Checklist](cpp\testing\catch2-patterns.md) | cpp | C | draft | 2026.06 |
| cpp-googletest | [GoogleTest and GMock Patterns Checklist](cpp\testing\googletest-patterns.md) | cpp | C | draft | 2026.06 |
| cpp-sanitizers | [Sanitizer Integration and Usage Checklist](cpp\testing\sanitizers.md) | cpp | N | draft | 2026.06 |
| common-test-doubles | [Test Doubles Taxonomy and Selection Checklist](common\testing\test-doubles.md) | common | C | draft | 2026.06 |
| common-testing-strategy | [Testing Strategy Checklist](common\testing\testing-strategy.md) | common | C | draft | 2026.06 |

### tooling-process

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-cicd-pipeline | [CI/CD Pipeline Patterns Checklist](common\ci-cd\pipeline-patterns.md) | common | C | draft | 2026.06 |

<!-- INDEX_END -->

## Category Descriptions

| Category | Description |
|----------|-------------|
| AI | AI-assisted development, agent tools, prompt/tool injection, model evaluation |
| Security | Input validation, access control, encryption, threat modeling |
| Design | API design, architecture patterns, interface contracts, type usage |
| Correctness | Undefined behavior, const correctness, exception safety, lifetime |
| Resource Management | RAII, ownership, smart pointers, move semantics |
| Testing | Unit tests, integration tests, TDD, coverage, mocking |
| Performance | Algorithm selection, memory layout, caching, concurrency |
| Tooling/Process | CI/CD, code review workflow, Git conventions, build system |
| Cross-Language | Language-agnostic design principles applicable to all projects |

## Harness Status Definitions

| Status | Meaning |
|--------|---------|
| draft | Initial proposal, under review |
| reviewed | Approved by CODEOWNER, ready for use |
| stable | Used in real projects for ≥1 month without issues |
| deprecated | Superseded; links to replacement. Will be archived after 12 months. |
