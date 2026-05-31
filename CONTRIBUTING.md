# Contributing to dev-guidelines

## Harness Lifecycle

| Transition | Gate |
|------------|------|
| draft → reviewed | Approving PR review from a CODEOWNER |
| reviewed → stable | Used in ≥1 real code review for ≥1 month; `stable_since` date set |
| any → deprecated | Superseding harness published; related links updated per deprecation rules |
| deprecated → archive | After 12 months in deprecated state |

## Proposing a New Harness

1. File an issue using the **New Harness** template
2. After discussion, create a PR with:
   - The `.md` file in the correct directory
   - Full frontmatter per the [harness template](templates/harness.template.md)
   - At least one C-tier source citation with tier justification
3. Request review from the CODEOWNER of the target directory

## Placement Rules

- Language-specific syntax/idioms → `<language>/`
- Language-agnostic → `common/`
- Spans multiple categories → see [design spec](docs/specs/2026-05-31-repo-structure-design.md#86-within-common-placement)

## Tier Assignment

New sources must include a tier justification table per the design spec (Section 2.2). Disputed classifications use the **Authority Challenge** issue template.

## Tier Challenge Process

1. File an **Authority Challenge** issue with counter-source evidence
2. CODEOWNER adjudicates within 14 days
3. Escalation: additional evidence → majority vote of all CODEOWNERS

## Review Cycle

CODEOWNERS run `python scripts/validate.py --stale` within their review windows. Unresponsive for >2 cycles → maintainer reassigns.
