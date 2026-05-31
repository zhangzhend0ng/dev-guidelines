# Harness Index

Cross-project shared code review and generation guidelines. Each harness is a checklist-based decision document.

## Quick Lookup

| I need to... | See |
|-------------|------|
| Validate function parameters | Parameter Validation (cpp/functions/) |
| Propose a new harness | [Contributing Guide](CONTRIBUTING.md) |
| Understand the authority system | [Design Spec](docs/specs/2026-05-31-repo-structure-design.md) |

## All Harnesses by Category

<!-- INDEX_START -->
### code-review

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-harness-driven-review | [Harness-Driven Review Protocol](common\code-review\harness-driven-review.md) | common | A | draft | 2026.06 |

### correctness

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-thread-safety | [Concurrency and Thread Safety Checklist](cpp\concurrency\thread-safety.md) | cpp | N | draft | 2026.06 |
| cpp-const-correctness | [Const Correctness Checklist](cpp\correctness\const-correctness.md) | cpp | N | draft | 2026.05 |
| cpp-exception-safety | [Exception Safety Guarantees Checklist](cpp\correctness\exception-safety.md) | cpp | N | draft | 2026.06 |
| cpp-lifetime | [Object Lifetime and Dangling References Checklist](cpp\lifetime\dangling-references.md) | cpp | N | draft | 2026.06 |
| cpp-undefined-behavior | [Undefined Behavior Prevention Checklist](cpp\correctness\undefined-behavior.md) | cpp | N | draft | 2026.06 |

### design

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-error-handling | [Error Handling Strategy Checklist](common\error-handling\error-handling-strategy.md) | common | C | draft | 2026.05 |

### functions

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| cpp-param-validation | [Parameter Validation Checklist](cpp\functions\parameter-validation.md) | cpp | C | draft | 2026.05 |

### meta

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
| common-harness-evolution | [Harness Evolution and Lifecycle Governance](common\meta\harness-evolution.md) | common | A | draft | 2026.05 |

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

<!-- INDEX_END -->

## Category Descriptions

| Category | Description |
|----------|-------------|
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
