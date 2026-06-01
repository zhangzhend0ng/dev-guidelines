---
type: harness
id: "common-dependency-management"
title: "Dependency Management Checklist"
language: "common"
category: "dependencies"
tier: "N"
scope: "Secure, versioned, and auditable dependency management across the supply chain"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [dependencies, supply-chain, security, sbom]
based_on:
  - "[N] OWASP Top 10 A06:2021 — Vulnerable Components"
  - "[C] NIST SP 800-161 — Supply Chain Risk Management"
  - "[C] OpenSSF Scorecard — Dependency Update Tooling"
  - "[C] SLSA Framework — Supply-chain Levels"
  - "[C] NIST SP 800-218 SSDF — PS.2 Secure Components"
related:
  - "common/security/input-validation.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Dependency Management Checklist

**Based on:** OWASP Top 10 A06 ([N]), NIST SP 800-161 ([C]), OpenSSF Scorecard ([C]), SLSA ([C]), NIST SSDF ([C]).
**Scope:** Secure, versioned, auditable dependency management.

---

## Concepts

| Practice | Standard |
|----------|----------|
| Lockfile | Commit lockfiles; no floating versions |
| CVE scanning | Automated check on every CI run; HIGH/CRITICAL blocks merge |
| SBOM | SPDX or CycloneDX at build time |
| Provenance | Signed attestations; SLSA Level 2+ |

---

## Checklist

### 1. Lockfile in VCS  **(N)** [R1]

- [ ] Commit lockfiles → **(N)** [R1]
- [ ] No floating versions or `latest` tags → **(N)** [R1]

### 2. Vulnerability Scanning  **(N)** [R1][R2]

- [ ] Automated CVE on every CI run → **(N)** [R1]
- [ ] HIGH/CRITICAL blocks merge → **(N)** [R1]
- [ ] Documented remediation plan if deferred → **(C)** [R2]

### 3. SBOM Generation  **(C)** [R3]

- [ ] SBOM at build time (SPDX/CycloneDX) → **(C)** [R3]
- [ ] Published with release artifacts → **(C)** [R3]

### 4. Provenance Attestation  **(C)** [R3][R4]

- [ ] Signed provenance metadata on build artifacts → **(C)** [R3]
- [ ] Verifiable post-build (SLSA Level 2+) → **(C)** [R4]

### 5. License Compliance  **(C)** [R2]

- [ ] Every dep has declared license → **(C)** [R2]
- [ ] Copyleft violations blocked → **(C)** [R2]

### 6. Transitive Review  **(C)** [R1][R2]

- [ ] Review transitive dependency footprint → **(C)** [R1]
- [ ] Prefer fewer deps over "latest everything" → **(A)** [R1]

### 7. Version Strategy  **(A)** [R1]

- [ ] Declare minimum compatible version → **(A)** [R1]
- [ ] Lockfile resolves latest within range → **(A)** [R1]

---

## Decision Tree

```
New dep?
  → Lockfile committed [1]
  → CVE scan clean [2]
  → License compliant [5]
  → Transitive review [6]
  → Version pinned [7]

Build: SBOM [3] + provenance [4]
```

---

## Anti-Patterns

### 1. Floating Versions

- **Appearance:** `"dep": "^1.0.0"` with no lockfile.
- **Trap:** "Always get latest compatible automatically."
- **Consequence:** CI breaks with no code change. Old builds unreproducible.
- **Fix:** Commit lockfile. Use automated update PRs with CI validation.

### 2. Dependency Hoarding

- **Appearance:** Large framework imported for one utility function.
- **Trap:** "It's already installed, one more import."
- **Consequence:** Bloated attack surface. Slow installs. Conflicting transitive deps.
- **Fix:** Implement in <50 lines before adding a dependency.

---

## See Also

- [Input Validation](../security/input-validation.md) — Validate external data from dependencies

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | OWASP Top 10 | A06:2021 | verified-2026 | 2026-06 |
| R2 | C | NIST SP 800-161 | Supply chain | verified-2026 | 2026-06 |
| R3 | C | OpenSSF Scorecard | Dep updates | verified-2026 | 2026-06 |
| R4 | C | SLSA Framework | Provenance | verified-2026 | 2026-06 |
| R5 | C | NIST SP 800-218 SSDF | PS.2 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
