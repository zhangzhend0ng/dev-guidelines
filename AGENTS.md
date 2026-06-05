# AGENTS.md — AI Agent Entry Navigator

You are in the `dev-guidelines` repository. Cross-project shared development guidelines and checklists.

## Quick Orientation

| You need to... | Go to |
|---------------|-------|
| Review or write code against a guideline | [INDEX.md](INDEX.md) — find the right harness |
| Understand the repo structure | [Design Spec](docs/specs/2026-05-31-repo-structure-design.md) |
| Create a new harness | [Template](templates/harness.template.md) + [Contributing Guide](CONTRIBUTING.md) |
| Understand the methodology | [concepts/](concepts/01-harness-methodology.md) — harness philosophy + tier system |
| Govern harness lifecycle & evolution | [common/meta/harness-evolution.md](common/meta/harness-evolution.md) — when to promote, deprecate, split, or challenge |
| Look up an authoritative source | [references/sources.md](references/sources.md) — N/C/A registry (29 entries) |
| Use a prompt template | [prompts/](prompts/code-review-with-harness.md) — AI code review + harness creation |
| Validate all harnesses | `python scripts/validate.py --json` |
| Regenerate index | `python scripts/generate_index.py` |

## Harness Format

Every harness file (`common/**/*.md`, `cpp/**/*.md`) has:
- YAML frontmatter with `type: harness`
- 5-10 checklist items, each tagged **(N)**, **(C)**, or **(A)** for authority tier
- Decision tree, anti-patterns section, reference sources table

## Authority Tiers

- **(N) Normative** — ISO standards, WG21 adopted papers.
- **(C) Consensus** — C++ Core Guidelines, SEI/CERT, OWASP.
- **(A) Advisory** — Expert books (Effective C++, etc.), org style guides.
- **(P) Project** — Team conventions. Mandatory within the project.

## Key Rules

1. **Harness-driven development is MANDATORY for writing and reviewing code.** Load [common/code-review/harness-driven-review.md](common/code-review/harness-driven-review.md):
   - **Before writing code:** Identify applicable harnesses FIRST (Part A), satisfy (N)/(C) items during implementation.
   - **During code review:** Identify harnesses BEFORE reading code (Part B), apply every checklist item, gate verdict on tiered findings.
   Do not write or approve code without passing relevant harnesses.
2. **Always commit each logical change separately.** Phase-by-phase, harness-by-harness.
3. **Run `python scripts/validate.py` before committing** any harness change.
4. **Run `python scripts/generate_index.py` if you add/remove/rename a harness.**
5. **Cross-references must be bidirectional.** If A links to B, B's `related` field lists A.
6. **Source references include timeliness tags.** Check Reference Sources table format.
7. **Directory structure:** `common/` for language-agnostic, `cpp/` for C++ specific.
