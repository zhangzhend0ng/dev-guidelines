# Dev-Guidelines Repository Structure Design v1.0

**Status:** REVISED (Round 1 Santa Review)
**Date:** 2026-05-31

---

## 1. Directory Structure

```
dev-guidelines/
├── README.md
├── INDEX.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── ROADMAP.md
├── LICENSE
├── .editorconfig
├── CODEOWNERS
│
├── common/                             # Language-Agnostic Guidelines
│   ├── security/
│   │   └── input-validation.md
│   ├── error-handling/
│   │   └── error-handling-strategy.md
│   ├── api-design/
│   ├── commits/
│   ├── naming/
│   ├── logging/
│   ├── code-review/
│   ├── testing/
│   └── dependencies/
│
├── cpp/                                # C++ Specific Guidelines
│   ├── functions/
│   │   └── parameter-validation.md     # Migrated from root
│   ├── memory/
│   │   ├── raii.md
│   │   └── ownership.md
│   ├── correctness/
│   │   ├── const-correctness.md
│   │   ├── undefined-behavior.md
│   │   └── exception-safety.md
│   ├── lifetime/
│   ├── concurrency/
│   ├── style/
│   └── build/
│
├── templates/
│   ├── harness.template.md
│   └── language-pack.template.md
│
├── scripts/
│   ├── validate.py                     # Python, cross-platform
│   └── generate_index.py
│
├── docs/
│   └── specs/
│       └── 2026-05-31-repo-structure-design.md
│
└── .github/
    ├── workflows/
    │   └── validate.yml
    ├── ISSUE_TEMPLATE/
    │   ├── new-harness.md
    │   └── authority-challenge.md
    └── PULL_REQUEST_TEMPLATE.md
```

### Key Changes from Draft

- **No `.harness.md` suffix** — Plain `.md`. Harness identification via frontmatter `type: harness`.
- **No empty future-language directories** — Replaced by `ROADMAP.md` with planned additions.
- **Scripts in Python** — Cross-platform by default (Windows/Linux/macOS). Requires Python 3.10+.
- **Community files added** — `CONTRIBUTING.md`, `CHANGELOG.md`, `CODEOWNERS`, `ISSUE_TEMPLATE/`, `PULL_REQUEST_TEMPLATE.md`.

### Naming Conventions

| Artifact | Convention | Example |
|----------|-----------|---------|
| Harness files | `<topic>.md` | `raii.md`, `const-correctness.md` |
| Template files | `<name>.template.md` | `harness.template.md` |
| Script files | `<name>.py` | `validate.py` |
| Non-harness markdown | UPPER_CASE.md | `README.md`, `INDEX.md`, `CONTRIBUTING.md` |
| Spec files | `YYYY-MM-DD-<topic>-design.md` | `2026-05-31-repo-structure-design.md` |
| Language directories | lowercase | `cpp/`, `python/`, `go/` |
| Sub-directories by concern | kebab-case | `api-design/`, `error-handling/` |

---

## 2. Authority Tier System: Normative / Consensus / Advisory

### 2.1 Tier Definitions

The previous A/B/C naming collides with ISO 26262 ASIL, MISRA categories, and academic letter grades. Renamed to descriptive tiers.

| Tier | Name | Definition | Example Sources | Review Cycle |
|------|------|------------|-----------------|--------------|
| **N** | **Normative** | Official standards, formally adopted by recognized standards bodies. Non-negotiable. | ISO 14882, WG21 adopted papers, IETF RFC, IEEE 754, ISO 26262 | 24 months |
| **C** | **Consensus** | Industry consensus guidelines with recognized maintainer organizations and version management. Widely adopted (3+ independent organizations). | C++ Core Guidelines, SEI/CERT, OWASP Top 10/ASVS, MISRA, NIST SP 800, CWE Top 25, OpenSSF Scorecard | 12 months |
| **A** | **Advisory** | Expert literature, major organization internal standards, community consensus. Valuable but context-dependent. | Effective C++/Modern C++, Google/LLVM Style Guides, C++ Concurrency in Action, Clean Code, large-org internal guidelines | 24 months |

### 2.2 Tier Assignment Criteria

When evaluating a new source for inclusion:

| Criterion | Normative | Consensus | Advisory |
|-----------|-----------|-----------|----------|
| Maintainer | Standards body (ISO/IEC/IEEE/IETF) | Recognized professional organization | Individual author or single company |
| Versioning | Formal edition cycle | Documented version history | May be unversioned |
| Adoption | Universal (all implementations must comply) | 3+ independent large organizations | Variable |
| Override cost | Requires newer standard from same body | Requires N-tier source or 2+ C-tier sources in agreement | Can be overridden by any C-tier or above |

### 2.3 Conflict Resolution

| Scenario | Rule |
|----------|------|
| N vs. C or A | N wins |
| C vs. A | C wins |
| N vs. N | Newer standard edition wins |
| C vs. C | (a) Check if one has broader adoption evidence; (b) if still tied, prefer the more general-purpose source; (c) if still tied, file an issue and document the decision |
| A vs. A | More recent publication wins, but must be cross-checked against current N/C sources |
| Exception: N vs. C | C may be preferred if: (a) WG21 Defect Report or equivalent committee clarification shows the N text is ambiguous or superseded, AND (b) at least one other independent C source agrees. Must document full reasoning chain. |

### 2.4 Timeliness Tags

Timeliness metadata lives in the **Reference Sources table** at the end of each harness, not inline. Each checklist item carries only the tier letter (N/C/A) inline; the full tag including date is in the reference table.

**Reference table format:**

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO 14882:2020 | §12.4.2 | `verified-2026` | 2026-04 |
| R2 | C | C++ Core Guidelines | I.6 | `verified-2026` | 2026-04 |
| R3 | C | SEI/CERT C++ | API00-C (v2025) | `needs-review` | — |
| R4 | A | Meyers, Eff. Modern C++ | Item 23 | `deprecated` | — |

**Inline citation format in checklist items:**

```
- [ ] Condition description → **(N)** action instruction [R1]
- [ ] Another condition → **(C)** action instruction [R2]
```

Using **(N)** / **(C)** / **(A)** parenthesized bold avoids bracket collision with `- [ ]` checkboxes.

**Tag lifecycle:**

```
verified-YYYY → (cycle elapses) → needs-review → (reviewed) → verified-YYYY
                                                              → deprecated → historical
```

### 2.5 Deprecation Criteria

A source reference is marked `deprecated` if:
- Superseded by a newer version from the same origin
- Core premise no longer holds (e.g., pre-C++11 advice in C++23 era)
- Explicitly overturned by an N-tier source
- Maintainer declared it retired
- Referenced compiler feature removed from all major compilers
- Over 10 years unupdated AND language standard has advanced 3+ major versions

### 2.6 Review Burden Management

Consensus-tier sources require 12-month review. To prevent unsustainable backlog:

| Priority Band | Criteria | Review Cycle |
|---------------|----------|-------------|
| C-Critical | Referenced by ≥3 harnesses OR in a security-related harness | 6 months |
| C-Routine | Referenced by 1-2 harnesses, non-security | 12 months |
| C-Low | Informational only, not load-bearing for any checklist item | 24 months |

A `scripts/validate.py --stale` command identifies all citations past their review window and reports them grouped by priority.

---

## 3. Harness Document Template

### 3.1 YAML Frontmatter (REQUIRED)

```yaml
---
type: harness
id: "cpp-param-validation"
title: "Parameter Validation Checklist"
language: "cpp"
category: "functions"
tier: "C"                         # Highest tier among all cited sources (N/C/A)
scope: "Select validation mechanism for function parameters in public APIs"
version: "2026.05"               # Date-based: YYYY.MM of last content change
status: "draft"                  # draft → reviewed → stable → deprecated
last_validated: "2025-12-01"
review_cycle: "12m"
tags:
  - validation
  - parameters
  - contracts
based_on:
  - "[C] C++ Core Guidelines I.6, I.12, I.13"
  - "[C] SEI/CERT API00-C (v2025)"
  - "[C] P1743R0 (Bloomberg BDE)"
related:
  - "common/security/input-validation"
supersedes: []
changelog:
  - "2026.05: Initial draft"
---
```

### 3.2 Field Descriptions

| Field | Constraint | Example |
|-------|-----------|---------|
| `id` | `<language>-<slug>`, stable, never reused after deprecation | `cpp-param-validation` |
| `scope` | Template: `<action> for <what> in <context>` | `Select validation mechanism for function parameters in public APIs` |
| `version` | `YYYY.MM` date-based; bump on any content change | `2026.05` |
| `status` | Controlled vocabulary: `draft` / `reviewed` / `stable` / `deprecated` | `draft` |
| `tier` | Single letter: `N` / `C` / `A` (highest among all cited sources) | `C` |
| `review_cycle` | `6m` / `12m` / `24m` based on tier and C-priority band | `12m` |

### 3.3 Harness Lifecycle

```
draft ──(peer review)──> reviewed ──(used in ≥1 real project)──> stable
  │                           │                                      │
  └──(abandoned)──> [delete]  └──(superseded)──> deprecated ──(1yr)──> [archive]
```

| Transition | Gate |
|------------|------|
| draft → reviewed | At least one other person reviews and approves |
| reviewed → stable | Used in at least one real code review or implementation without issues for ≥1 month |
| any → deprecated | A superseding harness is published; old harness links to new via `supersedes` |
| deprecated → archive | After 12 months, deprecated harness moved to `archive/` directory |

### 3.4 Internal Sections

1. **Title + Summary** (REQUIRED) — Tier icon, based-on sources, applicable/non-applicable scope
2. **Prerequisites / Concepts** (OPTIONAL) — Background knowledge needed for the checklist
3. **Checklist** (REQUIRED) — 5-10 items. Each: condition → action with **(N)**/**(C)**/**(A)** tag + `[Rx]` reference key. Optional Good/Bad code examples.
4. **Quick Decision Tree** (OPTIONAL) — ASCII art, when items form a decision flow
5. **Anti-Patterns / Common Mistakes** (RECOMMENDED) — 2-3 entries, each structured as: **Appearance** (what it looks like) → **Trap** (why it seems correct) → **Consequence** (actual harm) → **Fix** (correct approach)
6. **See Also** (REQUIRED when `related` is non-empty) — Bullet links to related harnesses
7. **Reference Sources** (REQUIRED) — Table: Label | Tier | Source | Clause | Timeliness | Last Verified
8. **Changelog** (REQUIRED) — Summarized from frontmatter `changelog` field for human readability

### 3.5 Checklist Item Specification

Each item MUST contain:
- A decision condition (answerable with yes/no or a choice from enumerated options)
- An action instruction for each branch
- A tier tag **(N)** / **(C)** / **(A)** on each action
- A reference key `[Rx]` pointing to the reference table

Each item MAY contain:
- A Good/Bad code example pair (one paragraph each)
- A one-sentence rationale (when the action is non-obvious)

**Granularity:** 5-10 items per harness. Hard maximum 12. One item = one independent decision point.

### 3.6 Cross-Reference Convention

When harness A references harness B in body text:

```markdown
> See also: [Const Correctness](../correctness/const-correctness.md) — ensures validation logic doesn't mutate inputs.
```

Cross-references MUST be bidirectional: if A links to B, B's `related` field must list A.

### 3.7 Diátaxis Consideration

Each harness blends "how-to guide" (checklist) with "reference" (sources) and "explanation" (anti-patterns). This is a deliberate trade-off: the blended format allows a reviewer to complete a full review pass without switching between 3-4 files. The file is structured so sections can be read independently — a reviewer who only needs the checklist can skip directly to Section 3.

---

## 4. Cross-Cutting Topic Rules

### 4.1 Placement Decision Tree

```
Does the guideline require language-specific syntax, idioms, or compiler behavior?
  ├─ YES → Place in <language>/ directory
  │         If a corresponding common/ harness exists, add it to `related`
  │         and add a body-text cross-reference.
  └─ NO  → Place in common/ directory
            If language-specific details exist, add a "Language-Specific Notes"
            subsection listing links to each language's harness on the topic.
```

### 4.2 Cross-Layer Consistency

When a topic has both a common/ and a language/ harness:
1. The common/ harness defines the general principle
2. The language/ harness defines how that principle applies in the specific language
3. Both harnesses MUST cross-reference each other via `related` and body text
4. They MUST NOT contradict each other on the same checklist item
5. The `CODEOWNERS` file assigns each directory to specific owners who are responsible for consistency

### 4.3 Example: Error Handling

```
common/error-handling/error-handling-strategy.md   ← General: when to use what mechanism
cpp/correctness/exception-safety.md                ← C++ specific: exception guarantees, noexcept
```

`exception-safety.md` starts with: "This harness applies the general error-handling strategy (see [Error Handling Strategy](../../common/error-handling/error-handling-strategy.md)) to C++ specifically."

---

## 5. INDEX.md System

### 5.1 Structure

```markdown
# Harness Index

## Quick Lookup
  (Manually curated: "I need to..." → link)

## All Harnesses by Category
<!-- INDEX_START -->
  (Auto-generated from frontmatter. Run scripts/generate_index.py)
<!-- INDEX_END -->

## Category Descriptions
## Harness Status Definitions
```

### 5.2 Categories

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

---

## 6. Tooling

### 6.1 `scripts/validate.py`

```
Usage: python scripts/validate.py [--stale] [--dead-links] [--json]

Performs:
  1. Frontmatter completeness check (all required fields present)
  2. Tier consistency check (no deprecated sources without replacement)
  3. Category consistency (file path matches frontmatter category)
  4. Cross-reference bidirectionality (related links go both ways)
  5. --stale: Report all citations past their review window
  6. --dead-links: Check all external URLs return 200
  7. --json: Machine-readable output for CI integration

Dependencies: Python 3.10+, PyYAML, requests
```

### 6.2 `scripts/generate_index.py`

```
Usage: python scripts/generate_index.py

Scans all .md files with type: harness in frontmatter.
Regenerates the <!-- INDEX_START --> ... <!-- INDEX_END --> zone
in INDEX.md. Run as a pre-commit hook and in CI.
```

### 6.3 CI Pipeline

`.github/workflows/validate.yml` runs on every PR:
1. `python scripts/validate.py --json` — hard-fail on frontmatter errors
2. `python scripts/validate.py --stale` — warn-only on stale citations
3. `python scripts/generate_index.py --check` — fail if INDEX.md is out of sync
4. Dead-link check runs weekly, not per-PR

---

## 7. Migration Plan

### Phase 0: Structure Bootstrap (this branch)
1. Create directory structure as specified in Section 1
2. Write `templates/harness.template.md`
3. Write `scripts/validate.py` and `scripts/generate_index.py`
4. Write `CONTRIBUTING.md`, `CHANGELOG.md`, `ROADMAP.md`, `CODEOWNERS`
5. Set up `.github/workflows/validate.yml`
6. Bootstrap `INDEX.md` with auto-generation zone

### Phase 0.5: Existing Content Migration
1. Copy `function_design_harness.md` → `cpp/functions/parameter-validation.md`
2. Add complete frontmatter to the copy
3. Add `<!-- MIGRATED: superseded by cpp/functions/parameter-validation.md -->` to old file
4. Update `README.md` to point to new structure
5. Commit. Old file stays as redirect for one release cycle, then removed.

### Phase 1: First 5 New Harnesses
1. `cpp/memory/raii.md`
2. `cpp/memory/ownership.md`
3. `cpp/correctness/const-correctness.md`
4. `common/security/input-validation.md`
5. `common/error-handling/error-handling-strategy.md`

### Phase 2: Deepening Coverage
Per ROADMAP.md priorities.

---

## 8. Summary of Santa Round 1 Fixes

| Issue | Fix |
|-------|-----|
| OWASP ASVS B/C contradiction | OWASP consistently N-tier |
| A/B/C naming collision | Renamed to Normative/Consensus/Advisory (N/C/A) |
| `.harness.md` suffix unjustified | Plain `.md` with `type: harness` frontmatter |
| Empty future directories | Replaced by ROADMAP.md |
| No common/language cross-cutting rules | Section 4 with decision tree and consistency rules |
| Naming conventions incomplete/inconsistent | Consolidated table in Section 1 |
| Citation format inconsistent | Unified: inline `(N)`/`(C)`/`(A)` + `[Rx]` key; full timeliness in reference table |
| Checkbox `[ ]` vs authority `[A]` clash | Authority uses bold parentheses `(N)` instead of brackets |
| No anti-pattern entry structure | Appearance → Trap → Consequence → Fix template |
| No scope field constraint | Template: `<action> for <what> in <context>` |
| No migration plan | Section 7 with Phase 0/0.5/1/2 |
| No CONTRIBUTING.md/CHANGELOG.md/CODEOWNERS | Added to directory structure and design |
| SemVer for docs inappropriate | Changed to date-based `YYYY.MM` |
| No harness lifecycle definition | Section 3.3 with transition gates |
| No authority assignment criteria | Section 2.2 with 4-dimension criteria table |
| Timeliness tags cluttering inline text | Moved to reference table; inline carries only tier letter |
| Review burden unsustainable | Section 2.6 with C-Critical/Routine/Low priority bands |
| Conflict resolution subjective | Specific measurable criteria with escalation path |
| Scripts on Windows | Switched to Python 3.10+, cross-platform |
| Diátaxis mode-blending concern | Section 3.7 documents deliberate trade-off |
| SEI CERT language-first divergence | Section 4 documents rationale for common/language split |
