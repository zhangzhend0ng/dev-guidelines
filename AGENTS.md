# AGENTS.md — AI Agent Entry Navigator

You are in the `dev-guidelines` repository. Cross-project shared development guidelines and checklists.

## Quick Orientation

| You need to... | Go to |
|---------------|-------|
| Review or write code against a guideline | [INDEX.md](INDEX.md) — find the right harness |
| Understand the repo structure | [Design Spec](docs/specs/2026-05-31-repo-structure-design.md) |
| Create a new harness | [Template](templates/harness.template.md) + [Contributing Guide](CONTRIBUTING.md) |
| Understand the methodology | [concepts/](concepts/01-harness-methodology.md) — harness philosophy + tier system |
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

- **(N) Normative** — ISO standards, WG21 adopted papers. Non-negotiable.
- **(C) Consensus** — C++ Core Guidelines, SEI/CERT, OWASP. Industry consensus.
- **(A) Advisory** — Expert books (Effective C++, etc.), org style guides.

## Key Rules

1. **Always commit each logical change separately.** Phase-by-phase, harness-by-harness.
2. **Run `python scripts/validate.py` before committing** any harness change.
3. **Run `python scripts/generate_index.py` if you add/remove/rename a harness.**
4. **Cross-references must be bidirectional.** If A links to B, B's `related` field lists A.
5. **Source references include timeliness tags.** Check Reference Sources table format.
6. **Directory structure:** `common/` for language-agnostic, `cpp/` for C++ specific.
