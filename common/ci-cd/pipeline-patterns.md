---
type: harness
id: "common-cicd-pipeline"
title: "CI/CD Pipeline Patterns Checklist"
language: "common"
category: "tooling-process"
tier: "C"
scope: "Automated, fast, and secure CI/CD pipelines with quality gates, caching, and pipeline-as-code"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [ci-cd, pipeline, automation, build, security, quality-gates, caching]
based_on:
  - "[C] OpenSSF Scorecard — CI Best Practices"
  - "[C] NIST SP 800-218 SSDF — PS.2 Secure Build"
  - "[C] GitHub Actions Documentation"
  - "[A] Continuous Delivery (Humble/Farley, 2010)"
related:
  - "common/ai/model-capability-and-instruction-adherence.md"
  - "common/ai/ai-evaluation-and-regression-strategy.md"
  - "common/ai/ai-assisted-cpp-development.md"
  - "common/planning/risk-and-verification-plan.md"
  - "common/planning/rollback-and-migration-plan.md"
  - "common/dependencies/dependency-management.md"
  - "common/security/input-validation.md"
  - "cpp/build/toolchain-and-compiler-flags.md"
  - "cpp/testing/static-analysis.md"
  - "python/packaging/dependency-management.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# CI/CD Pipeline Patterns Checklist

**Based on:** OpenSSF Scorecard ([C]), NIST SSDF PS.2 ([C]), GitHub Actions Docs ([C]), Continuous Delivery — Humble/Farley ([A]).
**Scope:** Automated, fast, and secure CI/CD pipelines with quality gates, caching, and pipeline-as-code.

---

## Concepts

| Practice | Standard |
|----------|----------|
| Pipeline as code | Workflow definition in repo, versioned, reviewable |
| Fast feedback | CI completes in <10 min; developers notified immediately on failure |
| Build matrix | Multi-platform, multi-compiler, multi-version testing |
| Quality gate | Automated check that must pass before merge (lint, SAST, tests, coverage) |
| Caching | Compiler cache, dependency cache, Docker layer cache to keep builds fast |
| Artifact retention | Versioned build outputs, test reports, coverage reports with defined TTL |

---

## Checklist

### 1. CI Triggers  **(C)** [R1][R4]

- [ ] Pipeline triggers automatically on every push and PR → **(C)** [R4]
- [ ] No manual-only trigger for primary build/test pipeline → **(C)** [R4]
- [ ] Fast feedback: CI completes in under 10 minutes → **(C)** [R4]
- [ ] 10-30 minute pipelines: have a documented plan to reach <10 min (cache, parallelize, split slow tests) → **(A)** [R4]
- [ ] Failed builds notify the author immediately → **(C)** [R1]

### 2. Build Matrix  **(C)** [R3]

- [ ] Build and test on all target platforms (Linux, macOS, Windows as applicable) → **(C)** [R3]
- [ ] Multiple compiler/toolchain versions tested → **(C)** [R3]
- [ ] Multiple language/runtime versions if library supports a range → **(C)** [R3]
- [ ] Matrix defined declaratively, not via copy-pasted job definitions → **(A)** [R3]

### 3. Caching Strategies  **(C)** [R3]

- [ ] Compiler cache enabled (ccache, sccache) with cache keyed on compiler version + flags → **(C)** [R3]
- [ ] Dependency cache (package manager lockfile hash as key) → **(C)** [R3]
- [ ] Docker layer caching: order layers by change frequency (deps first, source last) → **(C)** [R3]
- [ ] Cache hit rates monitored; cache size bounded with eviction policy → **(A)** [R3]

### 4. Quality Gates in CI  **(C)** [R1][R2]

- [ ] Lint check runs and must pass before merge → **(C)** [R1]
- [ ] Static analysis (SAST) runs and must pass before merge → **(C)** [R2]
- [ ] Full test suite runs and must pass before merge → **(C)** [R1]
- [ ] Coverage threshold enforced; drop below threshold blocks merge → **(C)** [R1]
- [ ] Code format check runs; non-conforming code blocked → **(C)** [R1]
- [ ] All quality gates are automated; no manual approval substitutes for automated checks → **(C)** [R1]

### 5. Pre-Commit Hooks  **(C)** [R1][R3]

- [ ] Autoformat staged files (prettier, clang-format, black, etc.) → **(C)** [R1]
- [ ] Lint staged files; violations block commit → **(C)** [R1]
- [ ] Secret scanning prevents commits containing credentials, tokens, keys → **(C)** [R1]
- [ ] Hooks are fast (<5 seconds) to avoid disrupting flow → **(A)** [R3]
- [ ] `--no-verify` escape hatch documented for emergencies (rebase, WIP, hotfix) → **(C)** [R3]
- [ ] CI re-runs the same checks that pre-commit runs; pre-commit is a fast path, not a bypass → **(C)** [R1]

### 6. Artifact Management  **(C)** [R3][R4]

- [ ] Build artifacts published with unique version identifier → **(C)** [R4]
- [ ] Test reports (JUnit XML, JSON) archived and accessible post-run → **(C)** [R3]
- [ ] Coverage reports published (HTML, cobertura XML) with trend dashboard → **(C)** [R3]
- [ ] Retention policy defined: how long artifacts and logs are kept → **(C)** [R3]
- [ ] Snapshot/PR artifacts expire faster than release artifacts → **(A)** [R3]

### 7. Pipeline as Code  **(C)** [R3][R4]

- [ ] CI/CD workflow definition stored in the repository it builds → **(C)** [R3]
- [ ] Workflow changes reviewed via PR, same as application code → **(C)** [R3]
- [ ] Workflow versioned alongside the code it builds and deploys → **(C)** [R4]
- [ ] Shared workflow components extracted into reusable templates/actions → **(A)** [R3]
- [ ] No critical pipeline logic exists only in the CI provider's web UI → **(C)** [R3]

### 8. Security Scanning in CI  **(C)** [R1][R2]

- [ ] Dependency CVE scanning on every CI run → **(C)** [R1]
- [ ] HIGH/CRITICAL CVEs block merge → **(C)** [R1]
- [ ] Secret scanning detects credentials, tokens, and keys in source and config → **(C)** [R2]
- [ ] SAST (static application security testing) integrated into CI pipeline → **(C)** [R2]
- [ ] Scan results published with build; regressions flagged → **(A)** [R1]

---

## Decision Tree

```
Push/PR?
  → Trigger CI automatically [1]
  → Restore caches [3]
  → Build matrix (all platforms/versions) [2]
  → Quality gates:
      ├─ Lint [4]
      ├─ Format check [4]
      ├─ SAST [4][8]
      ├─ Tests [4]
      ├─ Coverage threshold [4]
      ├─ Dependency CVE scan [8]
      └─ Secret scanning [8]
  → Publish artifacts + reports [6]
  → Notify on failure [1]

Pre-commit (local):
  → Autoformat [5]
  → Lint [5]
  → Secret scan [5]
  → (Emergency: --no-verify escape hatch [5])

Pipeline changes:
  → Stored in repo [7]
  → Reviewed via PR [7]
  → Versioned with code [7]
```

---

## Anti-Patterns

### 1. ClickOps Pipeline

- **Appearance:** Build/deploy steps configured entirely in CI provider's web UI. No config file in repo.
- **Trap:** "It's faster to set up in the UI."
- **Consequence:** Unreviewable changes. No rollback. Repo gives false impression of build status. New team members cannot reproduce the pipeline.
- **Fix:** Move pipeline definition into repo (`.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`). Web UI only for secrets.

### 2. Slow Feedback Loop

- **Appearance:** CI takes 30+ minutes. Developers context-switch and miss failures.
- **Trap:** "We need comprehensive testing on every commit."
- **Consequence:** Developers ignore CI results. Broken main becomes normal. Merge conflicts pile up.
- **Fix:** Profile the pipeline. Split into fast critical path (<10 min) and slower extended suite. Use caching [3]. Parallelize independent jobs.

### 3. Pre-Commit as the Only Gate

- **Appearance:** Pre-commit hooks run lint/format/tests, CI is a lightweight passthrough.
- **Trap:** "We already checked it locally."
- **Consequence:** Different environments (OS, Node version, tool versions) produce different results. `--no-verify` bypasses all checks.
- **Fix:** CI must independently reproduce all quality gates. Pre-commit is a convenience, not a gate.

### 4. Cache Poisoning

- **Appearance:** Stale cache causes intermittent build failures or silently skips rebuilds.
- **Trap:** "Always use cache to save time."
- **Consequence:** Dependency updates don't propagate. Test results from cached builds are invalid. Hard-to-diagnose "works on my machine."
- **Fix:** Key caches on lockfile/content hash. Periodically bust caches (weekly). Monitor cache hit rates and invalidate on toolchain changes.

---

## See Also

- [Dependency Management](../dependencies/dependency-management.md) — CVE scanning, SBOM, provenance
- [Input Validation](../security/input-validation.md) — Validate external data crossing trust boundaries

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | OpenSSF Scorecard | CI Best Practices, Dependency Update Tooling | verified-2026 | 2026-06 |
| R2 | C | NIST SP 800-218 SSDF | PS.2 Secure Build | verified-2026 | 2026-06 |
| R3 | C | GitHub Actions Documentation | Workflow syntax, caching, matrices | verified-2026 | 2026-06 |
| R4 | A | Continuous Delivery (Humble/Farley, 2010) | Build pipeline, fast feedback, artifact management | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
