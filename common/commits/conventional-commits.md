---
type: harness
id: "common-conventional-commits"
title: "Commit Message Conventions Checklist"
language: "common"
category: "commits"
tier: "C"
scope: "Write consistent, machine-readable commit messages following Conventional Commits specification"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [commits, conventional-commits, semver, changelog]
based_on:
  - "[C] Conventional Commits 1.0.0"
  - "[C] Angular Commit Guidelines"
  - "[A] How to Write a Git Commit Message (chris.beams.io)"
  - "[A] Semantic Versioning 2.0.0"
related: []
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Commit Message Conventions Checklist

**Based on:** Conventional Commits 1.0.0 ([C]), Angular Commit Guidelines ([C]), Chris Beams ([A]), SemVer 2.0.0 ([A]).
**Scope:** Structure, format, and automation value of commit messages.

---

## Concepts

| Field | Format | Example |
|-------|--------|---------|
| Type | `feat`/`fix`/`build`/`ci`/`docs`/`perf`/`refactor`/`style`/`test`/`chore` | `feat` |
| Scope | Optional parenthetical | `feat(auth)` |
| Subject | ≤50 chars, imperative, no period | `add login rate limiting` |
| Body | Blank line after subject, 72-char wrap | Explains what and why |
| Footer | `BREAKING CHANGE:` or `Closes #123` | `Closes #456` |

**SemVer:** `feat`=MINOR, `fix`=PATCH, `BREAKING CHANGE`=MAJOR.

---

## Checklist

### 1. Type Field  **(C)** [R1][R2]

- [ ] `type:` present from defined set → **(C)** [R1]
- [ ] `feat` for features, `fix` for bugs → **(C)** [R1]

### 2. Subject Line Format  **(C)** [R2][R3]

- [ ] ≤50 characters → **(C)** [R2]
- [ ] Imperative mood → **(C)** [R2]
- [ ] No trailing period → **(C)** [R2]

### 3. Body Separation  **(A)** [R3]

- [ ] Blank line separates subject from body → **(A)** [R3]
- [ ] Body wrapped at 72 characters → **(A)** [R3]
- [ ] Explains WHAT and WHY → **(A)** [R3]

### 4. Breaking Change Signaling  **(C)** [R1]

- [ ] `!` after type/scope OR `BREAKING CHANGE:` footer → **(C)** [R1]
- [ ] Migration guide in body for breaking changes → **(C)** [R1]

### 5. SemVer Alignment  **(C)** [R1][R4]

- [ ] `feat` → MINOR bump → **(C)** [R1]
- [ ] `fix` → PATCH bump → **(C)** [R1]
- [ ] `BREAKING CHANGE` → MAJOR bump → **(C)** [R1]

### 6. Footer References  **(C)** [R2]

- [ ] Issue tracker IDs in footer → **(C)** [R2]
- [ ] `Closes #123` or `Refs #456` format → **(C)** [R2]

### 7. Changelog Automation  **(A)** [R1]

- [ ] Commits are input for automated changelog → **(A)** [R1]

---

## Decision Tree

```
Commit to write:
  → Feature? → feat [1]
  → Bug? → fix [1]
  → Subject ≤50 chars, imperative? [2]
  → Body for complex changes? [3]
  → Breaking? → ! or BREAKING CHANGE: [4]
  → feat=MINOR, fix=PATCH, break=MAJOR [5]
  → Issue refs? [6]
```

---

## Anti-Patterns

### 1. "Fix stuff" Commit

- **Appearance:** `fix: fix stuff` or `update code`.
- **Trap:** Descriptive enough for the author who just wrote it.
- **Consequence:** Months later, `git blame` shows this commit. Nobody can tell what was fixed or why. Useless for debugging.
- **Fix:** Be specific: `fix: handle null session in login redirect when cookie expires`.

### 2. Mega Commit

- **Appearance:** 20 files across 5 unrelated changes: `feat: add features and fix bugs`.
- **Trap:** Squashing is convenient.
- **Consequence:** Reverting any one change requires reverting all. Bisecting points to a commit that changed everything.
- **Fix:** One logical change per commit. Split via interactive rebase.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Conventional Commits 1.0.0 | Sections 1-7 | verified-2026 | 2026-06 |
| R2 | C | Angular Commit Guidelines | Types, Subject, Footer | verified-2026 | 2026-06 |
| R3 | A | Chris Beams — Git Commit Message | 7 Rules | verified-2026 | 2026-06 |
| R4 | A | Semantic Versioning 2.0.0 | MAJOR.MINOR.PATCH | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
