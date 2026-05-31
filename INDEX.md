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
### Uncategorized

| ID | Title | Language | Tier | Status | Version |
|----|-------|----------|------|--------|---------|
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
