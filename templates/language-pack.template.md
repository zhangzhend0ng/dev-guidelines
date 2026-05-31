# New Language Pack Checklist

Use this checklist when adding a new language directory to the repository.

## Pre-Flight

- [ ] Language has a formal standard (ISO/ECMA/etc.) or widely adopted specification
- [ ] At least 3 Consensus-tier or above sources exist for this language
- [ ] At least one CODEOWNER volunteers to maintain the language directory

## Setup

- [ ] Create `<lang>/` directory with subdirectories by concern area
- [ ] Add CODEOWNERS entry for `<lang>/`
- [ ] Add language to CI matrix in `.github/workflows/validate.yml`
- [ ] Add entry to ROADMAP.md marking it as active
- [ ] Update `scripts/generate_index.py` if language-specific index grouping is needed

## First Harness

- [ ] Identify the most impactful language-specific topic (per ROADMAP.md priority)
- [ ] Apply the harness template from `templates/harness.template.md`
- [ ] Ensure at least one N-tier and one C-tier source citation
- [ ] Submit PR with tier justification per Section 8.4 of the design spec
