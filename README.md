# dev-guidelines

Cross-project shared development guidelines and checklists, for use across all code repositories.

## What's Inside

**6 harnesses** live in the tree today, covering C++ correctness, resource management, and language-agnostic security/error-handling.
**5 more** are scheduled for Phase 2 (undefined behavior, exception safety, move semantics, concurrency, object lifetime).

Each harness is a focused decision document that breaks down a single topic into 5-10 actionable checklist items.
Every item is tagged with an authority tier **(N)** / **(C)** / **(A)** and backed by specific citations -- ISO standards, industry consensus guidelines, or expert literature.

## Directory Structure

```
dev-guidelines/
├── common/           Language-agnostic (security, error-handling, api-design, testing, ...)
├── cpp/              C++ specific (functions, memory, correctness, lifetime, concurrency, ...)
├── concepts/         Harness methodology and authority system explainers
├── prompts/          AI prompt templates (code review with harness, create new harness)
├── references/       Authoritative source registry (29 entries)
├── scripts/          Validation and index generation (Python 3.10+)
├── templates/        Harness and language-pack templates
├── docs/specs/       Design specifications
└── archive/          Deprecated harnesses after 12-month grace period
```

## Quick Start: Use a Harness for Code Review

1. Browse [INDEX.md](INDEX.md) to find the right harness for your task.
2. Open the harness and work through its 5-10 checklist items.
3. Each item has a clear condition, action, and source reference -- answer each one and follow the prescribed action.
4. For AI-assisted review, use the prompt template in [prompts/code-review-with-harness.md](prompts/code-review-with-harness.md).

## Quick Start: Contribute a New Harness

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for the full lifecycle and proposal workflow.
2. File an issue using the **New Harness** template.
3. Copy [templates/harness.template.md](templates/harness.template.md) into the correct directory (`common/` or `<language>/`).
4. Fill in the frontmatter, 5-10 checklist items (each with tier tags and reference keys), anti-patterns, and reference sources table.
5. Submit a PR and request review from the directory's CODEOWNER.

## Key Concepts

### Authority Tiers (N / C / A)

Every checklist item is grounded in a specific source at one of three tiers:

| Tier | Name | Source Examples | Weight |
|------|------|-----------------|--------|
| **N** | Normative | ISO 14882, IETF RFCs, IEEE 754 | Non-negotiable |
| **C** | Consensus | C++ Core Guidelines, SEI/CERT, OWASP | Default for most harnesses; overridable only by N or 2+ C sources |
| **A** | Advisory | Effective C++, Google Style Guide, org conventions | Context-dependent; overridable by any C-tier or above |

Conflict resolution is formalized: N beats C beats A, newer editions win, and escalation is via the **Authority Challenge** issue template.

### Harness Lifecycle

```
draft  -->  reviewed  -->  stable  -->  deprecated  -->  archived
```

A harness graduates from draft to reviewed with a CODEOWNER-approved PR, and to stable after real-world use for one month.
Deprecated harnesses redirect to their replacements for 12 months before archival.

For the full lifecycle and transition gates, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Reference

| Document | Purpose |
|----------|---------|
| [INDEX.md](INDEX.md) | Full harness catalog with quick-lookup table |
| [AGENTS.md](AGENTS.md) | AI agent entry point -- orientation, rules, and harness format |
| [ROADMAP.md](ROADMAP.md) | Priority-ordered plan for future harnesses and languages |
| [Design Spec](docs/specs/2026-05-31-repo-structure-design.md) | Complete specification: authority system, directory layout, tooling, templates |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Harness lifecycle, proposal workflow, tier assignment, review standards |
| [CHANGELOG.md](CHANGELOG.md) | Repo-level structural change log |

## Tooling

```bash
# Validate all harnesses (frontmatter, cross-refs, tier consistency)
python scripts/validate.py --json

# Regenerate the harness index in INDEX.md
python scripts/generate_index.py
```

Validation runs in CI on every PR. Requires Python 3.10+.
