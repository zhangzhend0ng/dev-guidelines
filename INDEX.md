# Harness Index

Cross-project shared code review and generation guidelines. Each harness is a checklist-based decision document.

## Quick Lookup

| I need to... | See |
|-------------|------|
| Validate function parameters | Parameter Validation (cpp/functions/) |
| Use AI to write or review C++ code | [AI-Assisted C++ Development](common/ai/ai-assisted-cpp-development.md) |
| Make weaker AI models follow instructions | [Model Capability and Instruction Adherence](common/ai/model-capability-and-instruction-adherence.md) |
| Control AI tool calls or agent actions | [Tool Calling and Agent Control](common/ai/tool-calling-and-agent-control.md) |
| Propose a new harness | [Contributing Guide](CONTRIBUTING.md) |
| Understand the authority system | [Design Spec](docs/specs/2026-05-31-repo-structure-design.md) |
| Ensure new harnesses don't duplicate existing ones | [Prior Art and Reuse](common/meta/prior-art-and-reuse.md) |
| Validate harness description, naming, and scoping | [Harness Quality Standards](common/meta/harness-quality-standards.md) |
| Ensure AI output defaults to Chinese for reports | [Output Language Convention](common/documentation/output-language.md) |

## All Harnesses by Category

<!-- INDEX_START -->
### ai

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-ai-evaluation-regression | [AI Evaluation and Regression Strategy Checklist](common/ai/ai-evaluation-and-regression-strategy.md) | common | C | draft | 2026.06 |
| common-ai-assisted-cpp-development | [AI-Assisted C++ Development Checklist](common/ai/ai-assisted-cpp-development.md) | common | C | draft | 2026.06 |
| common-model-capability-instruction-adherence | [Model Capability and Instruction Adherence Checklist](common/ai/model-capability-and-instruction-adherence.md) | common | C | draft | 2026.06 |
| common-prompt-injection-llm-security | [Prompt Injection and LLM Application Security Checklist](common/ai/prompt-injection-and-llm-security.md) | common | C | draft | 2026.06 |
| common-tool-calling-agent-control | [Tool Calling and Agent Control Checklist](common/ai/tool-calling-and-agent-control.md) | common | C | draft | 2026.06 |

### api

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-abi-compatibility | [C++ ABI Compatibility Checklist](cpp/api/abi-compatibility.md) | cpp | C | draft | 2026.06 |

### architecture

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-module-boundaries | [C++ Module Boundaries Checklist](cpp/architecture/module-boundaries.md) | cpp | C | draft | 2026.06 |
| cpp-layering-and-dip | [Layering and Dependency Inversion Checklist](cpp/architecture/layering-and-dependency-inversion.md) | cpp | A | draft | 2026.07.1 |

### build

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-build-system | [C++ Build System and Include Hygiene Checklist](cpp/build/cmake-include-hygiene.md) | cpp | C | draft | 2026.06 |
| cpp-package-management | [C++ Package Management Checklist](cpp/build/package-management.md) | cpp | C | draft | 2026.06 |
| cpp-toolchain-compiler-flags | [C++ Toolchain and Compiler Flags Checklist](cpp/build/toolchain-and-compiler-flags.md) | cpp | C | draft | 2026.06 |

### code-review

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-ai-generated-code-failure-modes | [AI-Generated Code Failure Modes Checklist](common/code-review/ai-generated-code-failure-modes.md) | common | A | draft | 2026.08 |
| common-code-review-checklist | [Code Review Checklist](common/code-review/review-checklist.md) | common | C | draft | 2026.09 |
| common-harness-driven-review | [Harness-Driven Development Protocol](common/code-review/harness-driven-review.md) | common | A | draft | 2026.07.2 |

### commits

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-conventional-commits | [Commit Message Conventions Checklist](common/commits/conventional-commits.md) | common | C | draft | 2026.06 |

### concurrency

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| python-asyncio-cancellation | [Python asyncio Cancellation Checklist](python/concurrency/asyncio-cancellation.md) | python | C | draft | 2026.06 |

### config

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-config-option-registration | [Configuration Option Registration and Dimension Classification Checklist](common/config/option-registration-and-dimension.md) | common | A | draft | 2026.09 |

### correctness

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-class-hierarchies | [Class Hierarchies and Virtual Dispatch Checklist](cpp/correctness/class-hierarchies.md) | cpp | N | draft | 2026.06 |
| cpp-compile-time | [Compile-Time Programming Checklist](cpp/correctness/compile-time-programming.md) | cpp | N | draft | 2026.06 |
| cpp-thread-safety | [Concurrency and Thread Safety Checklist](cpp/concurrency/thread-safety.md) | cpp | N | draft | 2026.06 |
| cpp-const-correctness | [Const Correctness Checklist](cpp/correctness/const-correctness.md) | cpp | N | draft | 2026.05 |
| dart-error-handling | [Dart Asynchronous Error and Exception Safety Checklist](dart/error-handling.md) | dart | C | draft | 2026.09.3 |
| cpp-exception-safety | [Exception Safety Guarantees Checklist](cpp/correctness/exception-safety.md) | cpp | N | draft | 2026.06 |
| cpp-integer-safety | [Integer Safety Checklist](cpp/correctness/integer-safety.md) | cpp | N | draft | 2026.06 |
| cpp-interface-contracts | [Interface Contracts and Design-by-Contract Checklist](cpp/correctness/interface-contracts.md) | cpp | N | draft | 2026.06 |
| cpp-lifetime | [Object Lifetime and Dangling References Checklist](cpp/lifetime/dangling-references.md) | cpp | N | draft | 2026.06 |
| python-type-hints-mypy | [Python Type Hints and mypy Checklist](python/correctness/type-hints-and-mypy.md) | python | C | draft | 2026.06 |
| cpp-stl-containers | [STL Algorithms and Containers Checklist](cpp/correctness/stl-algorithms-containers.md) | cpp | N | draft | 2026.06 |
| cpp-type-safety | [Type Safety and Implicit Conversions Checklist](cpp/correctness/type-safety.md) | cpp | N | draft | 2026.06 |
| cpp-undefined-behavior | [Undefined Behavior Prevention Checklist](cpp/correctness/undefined-behavior.md) | cpp | N | draft | 2026.06 |

### debugging

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-bug-report-triage | [Bug Report Triage Checklist](common/debugging/bug-report-triage.md) | common | A | draft | 2026.06 |
| cpp-debugging-crash-dump-analysis | [C++ Crash Dump Analysis Checklist](cpp/debugging/crash-dump-analysis.md) | cpp | C | draft | 2026.06 |
| cpp-debugging-flaky-test-triage | [C++ Flaky Test Triage Checklist](cpp/debugging/flaky-test-triage.md) | cpp | C | draft | 2026.06 |
| cpp-debugging-sanitizer-triage | [C++ Sanitizer Report Triage Checklist](cpp/debugging/sanitizer-triage.md) | cpp | C | draft | 2026.06 |
| common-fix-verification | [Fix Verification Checklist](common/debugging/fix-verification.md) | common | C | draft | 2026.06 |
| common-reproduction-minimization | [Reproduction and Minimization Checklist](common/debugging/reproduction-and-minimization.md) | common | A | draft | 2026.06 |
| common-root-cause-analysis | [Root Cause Analysis Checklist](common/debugging/root-cause-analysis.md) | common | A | draft | 2026.06 |

### dependencies

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-dependency-management | [Dependency Management Checklist](common/dependencies/dependency-management.md) | common | N | draft | 2026.06 |
| python-packaging-dependency-management | [Python Packaging and Dependency Management Checklist](python/packaging/dependency-management.md) | python | C | draft | 2026.06 |

### design

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-api-design | [API Design Principles Checklist](common/api-design/restful-api-design.md) | common | C | draft | 2026.06 |
| cpp-result-vs-exception | [C++ Result vs Exception Checklist](cpp/error-handling/result-vs-exception.md) | cpp | C | draft | 2026.06 |
| common-error-handling | [Error Handling Strategy Checklist](common/error-handling/error-handling-strategy.md) | common | C | draft | 2026.09 |
| cpp-feature-design-prerequisites | [Feature Design Prerequisites Checklist](cpp/design/feature-design-prerequisites.md) | cpp | C | draft | 2026.07.2 |
| common-feature-flag-rollout | [Remote Feature-Flag Evaluation and Rollout Checklist](design/feature-flag-rollout.md) | common | C | draft | 2026.09 |

### documentation

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-documentation-standards | [Documentation Standards Checklist](common/documentation/documentation-standards.md) | common | C | draft | 2026.06 |
| common-output-language | [Output Language Convention](common/documentation/output-language.md) | common | P | draft | 2026.07 |

### functions

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-param-validation | [Parameter Validation Checklist](cpp/functions/parameter-validation.md) | cpp | C | draft | 2026.05 |

### logging

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-logging-standards | [Logging Standards Checklist](common/logging/logging-standards.md) | common | N | draft | 2026.09.1 |

### meta

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-harness-evolution | [Harness Evolution and Lifecycle Governance](common/meta/harness-evolution.md) | common | A | draft | 2026.07.2 |
| common-harness-quality-standards | [Harness Quality Standards Checklist](common/meta/harness-quality-standards.md) | common | A | draft | 2026.07.1 |
| common-prior-art-and-reuse | [Prior Art and Reuse Checklist](common/meta/prior-art-and-reuse.md) | common | A | draft | 2026.07 |

### naming

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-naming-conventions | [Naming Conventions Checklist](common/naming/naming-conventions.md) | common | C | draft | 2026.06 |

### performance

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-performance-patterns | [C++ Performance Patterns Checklist](cpp/performance/optimization-patterns.md) | cpp | N | draft | 2026.06 |

### planning

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-change-scope-control | [Change Scope Control Checklist](common/planning/change-scope-control.md) | common | A | draft | 2026.09 |
| common-planning-requirements-gap-analysis | [Requirements-vs-Implementation Gap Analysis Checklist](common/planning/requirements-gap-analysis.md) | common | C | draft | 2026.07 |
| common-risk-verification-plan | [Risk and Verification Plan Checklist](common/planning/risk-and-verification-plan.md) | common | C | draft | 2026.06 |
| common-rollback-migration-plan | [Rollback and Migration Plan Checklist](common/planning/rollback-and-migration-plan.md) | common | C | draft | 2026.06 |
| common-task-decomposition | [Task Decomposition Checklist](common/planning/task-decomposition.md) | common | A | draft | 2026.06 |

### project-specific

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| lava-login-logout-state-machine | [Lava Login/Logout State Machine Pre-Check](projects/lava/login-logout-state-machine.md) | dart | P | draft | 2026.09 |
| snapmaker-orca-coding-standards | [SnapmakerOrca C++ Coding Standards](projects/snapmaker-orca/coding-standards.md) | cpp | P | draft | 2026.06 |
| snapmaker-orca-workflow | [SnapmakerOrca PR and Workflow Standards](projects/snapmaker-orca/workflow-standards.md) | common | P | draft | 2026.06 |

### resource-management

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-move-semantics | [Move Semantics and Rule of Five Checklist](cpp/memory/move-semantics.md) | cpp | N | draft | 2026.06 |
| cpp-raii | [RAII and Resource Management Checklist](cpp/memory/raii.md) | cpp | N | draft | 2026.05 |
| cpp-ownership | [Smart Pointer and Ownership Semantics Checklist](cpp/memory/ownership.md) | cpp | N | draft | 2026.05 |

### runtime

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-runtime-observability | [C++ Runtime Observability and Diagnostics Checklist](cpp/runtime/observability-and-diagnostics.md) | cpp | C | draft | 2026.06 |

### security

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-secure-coding | [C++ Secure Coding Checklist](cpp/security/secure-coding.md) | cpp | N | draft | 2026.06 |
| dart-json-boundaries | [Dart Dynamic JSON Boundary Checklist](dart/json-boundaries.md) | dart | C | draft | 2026.09.2 |
| common-input-validation | [Input Validation Checklist](common/security/input-validation.md) | common | N | draft | 2026.09 |
| python-input-deserialization | [Python Input Deserialization Checklist](python/security/input-deserialization.md) | python | N | draft | 2026.06 |

### serialization

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-parsing-validation | [C++ Parsing and Validation Checklist](cpp/serialization/parsing-and-validation.md) | cpp | C | draft | 2026.06 |

### templates

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-template-best-practices | [Template Best Practices and Concepts Checklist](cpp/templates/template-best-practices.md) | cpp | N | draft | 2026.06 |

### testing

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-fuzzing | [C++ Fuzzing Checklist](cpp/testing/fuzzing.md) | cpp | C | draft | 2026.06 |
| cpp-mutation-testing | [C++ Mutation Testing Checklist](cpp/testing/mutation-testing.md) | cpp | A | draft | 2026.06 |
| cpp-property-based-testing | [C++ Property-Based Testing Checklist](cpp/testing/property-based-testing.md) | cpp | C | draft | 2026.06 |
| cpp-static-analysis | [C++ Static Analysis Checklist](cpp/testing/static-analysis.md) | cpp | C | draft | 2026.06 |
| cpp-catch2 | [Catch2 Testing Patterns Checklist](cpp/testing/catch2-patterns.md) | cpp | C | draft | 2026.06 |
| dart-testing | [Dart/Flutter Unit Testing Patterns Checklist](dart/testing.md) | dart | A | draft | 2026.09.1 |
| common-testing-differential-oracle | [Differential Oracle and Characterization Testing Checklist](common/testing/differential-oracle-testing.md) | common | A | draft | 2026.07 |
| cpp-googletest | [GoogleTest and GMock Patterns Checklist](cpp/testing/googletest-patterns.md) | cpp | C | draft | 2026.06 |
| cpp-sanitizers | [Sanitizer Integration and Usage Checklist](cpp/testing/sanitizers.md) | cpp | N | draft | 2026.06 |
| common-test-doubles | [Test Doubles Taxonomy and Selection Checklist](common/testing/test-doubles.md) | common | C | draft | 2026.06 |
| common-testing-strategy | [Testing Strategy Checklist](common/testing/testing-strategy.md) | common | C | draft | 2026.09 |
| python-pytest-patterns | [pytest Patterns Checklist](python/testing/pytest-patterns.md) | python | C | draft | 2026.06 |

### third-party

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-qt6-core | [Qt 6 C++ Core Pitfalls, Limitations, and Best Practices Checklist](cpp/third-party/qt6-core.md) | cpp | P | draft | 2026.07 |
| cpp-qt6-qml | [Qt 6 QML Pitfalls, Limitations, and Best Practices Checklist](cpp/third-party/qt6-qml.md) | cpp | P | draft | 2026.07 |
| cpp-wxwidgets-3-1-5 | [wxWidgets 3.1.5 Pitfalls, Limitations, and Best Practices Checklist](cpp/third-party/wxwidgets-3-1-5.md) | cpp | P | draft | 2026.08 |

### tooling-process

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-cicd-pipeline | [CI/CD Pipeline Patterns Checklist](common/ci-cd/pipeline-patterns.md) | common | C | draft | 2026.06 |

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
| Third-Party | Known pitfalls, limitations, and best practices for specific libraries/frameworks |
| Cross-Language | Language-agnostic design principles applicable to all projects |
| Config | Configuration/setting/preset option registration, data-dimension classification, serialization-name immutability, override precedence |

## Harness Status Definitions

| Status | Meaning |
|--------|---------|
| draft | Initial proposal, under review |
| reviewed | Approved by CODEOWNER, ready for use |
| stable | Used in real projects for ≥1 month without issues |
| deprecated | Superseded; links to replacement. Will be archived after 12 months. |



