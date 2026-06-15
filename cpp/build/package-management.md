---
type: harness
id: "cpp-package-management"
title: "C++ Package Management Checklist"
language: "cpp"
category: "build"
tier: "C"
scope: "Select, configure, and audit C++ package managers (vcpkg, Conan, CPM.cmake) for reproducible, hermetic, and secure dependency management"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [package-management, vcpkg, conan, cpm, cmake, dependencies, supply-chain, reproducible-builds, version-pinning]
based_on:
  - "[C] Microsoft vcpkg Documentation — manifest mode, versioning, binary caching"
  - "[C] Conan Documentation — lockfiles, profiles, custom recipes"
  - "[C] CMake FetchContent / CPM.cmake Documentation — script-based dependency retrieval"
  - "[C] OpenSSF Scorecard — Dependency Update Tooling, CVE scanning"
related:
  - "cpp/build/toolchain-and-compiler-flags.md"
  - "cpp/build/cmake-include-hygiene.md"
  - "common/dependencies/dependency-management.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Package Management Checklist

**Based on:** Microsoft vcpkg docs ([C]), Conan docs ([C]), CMake FetchContent/CPM.cmake docs ([C]), OpenSSF Scorecard ([C]).
**Scope:** Package manager selection, version pinning, hermetic builds, dependency resolution, CI caching, custom ports/recipes, license and security auditing.

---

## Concepts

| Practice | Principle |
|----------|-----------|
| Manifest-first | `vcpkg.json` / `conanfile.py` / `CPM.cmake` at repo root; no implicit system deps |
| Version pinned | Exact baseline, lockfile, or git hash; no floating versions |
| Hermetic | Every dependency resolved through the package manager; build anywhere, anytime |
| Override documented | Version conflicts resolved explicitly with recorded rationale |
| Binary cached | CI reuses pre-built packages; cache keyed on lockfile |
| License audited | SPDX identifiers for every transitive dependency |
| CVE scanned | Full dependency tree scanned; HIGH/CRITICAL blocks merge |

---

## Checklist

### 1. Package Manager Selection  **(A)** [R1][R2][R3]

- [ ] **vcpkg (manifest mode):** for cross-platform CMake projects needing a large curated catalog and tight MSVC integration → **(A)** [R1]
- [ ] **Conan:** for projects needing fine-grained binary configuration (profiles, settings, options) and private package servers → **(A)** [R2]
- [ ] **CPM.cmake:** for header-only or single-source libraries where a lightweight scripted approach suffices; avoid for large dependency graphs with complex transitive requirements → **(A)** [R3]
- [ ] Document the choice and rationale in project README or `docs/dependencies.md` → **(A)** [R1][R2][R3]
- [ ] Single package manager per project; mixing managers produces conflicting resolution strategies → **(A)** [R1][R2]

### 2. Manifest-First Configuration  **(C)** [R1][R2][R3]

- [ ] Manifest file at repository root committed to VCS → **(C)** [R1][R2][R3]
- [ ] vcpkg: `vcpkg.json` with `"dependencies"` array; `vcpkg-configuration.json` for registries and overlays → **(C)** [R1]
- [ ] Conan: `conanfile.py` (or `conanfile.txt` for simple cases) declaring `requires` and `generators` → **(C)** [R2]
- [ ] CPM.cmake: `CPMAddPackage()` calls in a dedicated `cmake/dependencies.cmake` included from root `CMakeLists.txt` → **(C)** [R3]
- [ ] No implicit reliance on system-global packages (e.g., `apt-get install libfoo-dev` or `brew install foo` undocumented) → **(C)** [R1][R2]

### 3. Version Pinning  **(C)** [R1][R2][R3]

- [ ] **vcpkg:** baseline pinned in `vcpkg-configuration.json` via `"builtin-baseline"` (git commit hash of the vcpkg registry) → **(C)** [R1]
- [ ] **Conan:** `conan.lock` file committed to VCS; generated with `conan lock create` → **(C)** [R2]
- [ ] **CPM.cmake:** exact git tag, release hash, or semantic version pinned per dependency; no `master`/`main` branches → **(C)** [R3]
- [ ] No floating version ranges (`>=1.0`, `*`, `latest`) that resolve nondeterministically → **(C)** [R1][R2]
- [ ] Dependency update is an explicit PR with CI validation; not a side effect of a rebuild → **(C)** [R1][R2]

### 4. Hermetic and Reproducible Builds  **(C)** [R1][R2][R3]

- [ ] All dependencies resolved through the chosen package manager; no system-global library paths in build scripts → **(C)** [R1][R2]
- [ ] Fresh checkout + single build command produces identical binaries (modulo timestamps) → **(C)** [R1][R2]
- [ ] CI validates reproducibility: clean checkout, no pre-warmed caches on at least one matrix leg → **(A)** [R1]
- [ ] Toolchain file (vcpkg) or profile (Conan) committed to VCS; not developer-local → **(C)** [R1][R2]
- [ ] Environment variable dependencies (e.g., `VCPKG_ROOT`, `CONAN_HOME`) documented in build instructions → **(A)** [R1][R2]

### 5. Dependency Resolution and Conflict Management  **(C)** [R1][R2][R3]

- [ ] Understand the dependency graph: `vcpkg depend-info`, `conan graph info`, or manual CPM audit → **(C)** [R1][R2]
- [ ] **Diamond dependency:** two direct dependencies requiring conflicting versions of a shared transitive dependency → must be explicitly resolved → **(C)** [R1][R2]
- [ ] **vcpkg:** use `"overrides"` in `vcpkg.json` to force a single version; document reason → **(C)** [R1]
- [ ] **Conan:** use `override` keyword on requires or `conan.lock` to pin resolution; document reason → **(C)** [R2]
- [ ] **CPM.cmake:** manually align versions across `CPMAddPackage` calls; CPM has no built-in resolver → **(C)** [R3]
- [ ] Document every override with a comment stating the conflict, resolution, and expected removal condition → **(C)** [R1][R2]

### 6. CI Integration and Binary Caching  **(C)** [R1][R2][R4]

- [ ] Cache downloaded package artifacts in CI using the platform's native cache mechanism (GitHub Actions `cache`, GitLab CI cache) → **(C)** [R1][R2]
- [ ] Cache key includes the lockfile/baseline hash so cache invalidates when dependencies change → **(C)** [R1][R2]
- [ ] **vcpkg:** enable binary caching (`VCPKG_BINARY_SOURCES`) pointing to a CI-accessible storage (GitHub Actions cache, Azure Artifacts, local directory) → **(C)** [R1]
- [ ] **Conan:** configure `conan remote` for a private Artifactory/Conan Server if needed; use `CONAN_REVISIONS_ENABLED=1` → **(C)** [R2]
- [ ] **CPM.cmake:** set `CPM_SOURCE_CACHE` to a CI-persisted directory to avoid re-downloading → **(C)** [R3]
- [ ] At least one CI leg does a clean (cache-miss) build to catch cache poisoning or staleness → **(A)** [R4]

### 7. Custom Ports, Recipes, and Overlays  **(A)** [R1][R2]

- [ ] Create a custom port/recipe only when no upstream package exists or the upstream is unmaintained → **(A)** [R1][R2]
- [ ] vcpkg: custom ports in a `ports/` directory, registered via `vcpkg-configuration.json` overlay-ports → **(A)** [R1]
- [ ] Conan: custom recipe in a `conanfile.py` exported to a local or private remote → **(A)** [R2]
- [ ] CPM.cmake: custom `CPMAddPackage` with a `GIT_REPOSITORY` pointing to a maintained fork → **(A)** [R3]
- [ ] Maintain a plan to upstream custom ports/recipes; track in an issue with an owner and target date → **(A)** [R1][R2]
- [ ] Custom ports/recipes follow the same versioning, licensing, and CVE scanning rules as first-party dependencies → **(C)** [R1][R2]

### 8. License Compliance  **(C)** [R1][R2][R4]

- [ ] Every direct and transitive dependency has a declared SPDX license identifier → **(C)** [R1][R2]
- [ ] Automated license check in CI (Conan: query `conan info`; vcpkg/CPM: integrate OWASP Dependency-Check or FOSSA) → **(C)** [R1][R2]
- [ ] Copyleft licenses (GPL, AGPL) flagged for legal review; blocking merge if project policy forbids them → **(C)** [R1][R2]
- [ ] Generate an SBOM (SPDX or CycloneDX) at build time and publish with release artifacts → **(C)** [R4]

### 9. CVE Scanning on Dependency Tree  **(C)** [R1][R2][R4]

- [ ] Scan the full transitive dependency tree for known CVEs on every CI run → **(C)** [R1][R2]
- [ ] Integrate OWASP Dependency-Check, Grype, or Trivy for CVE scanning on dependency tree → **(C)** [R1]
- [ ] Conan: integrate with JFrog Xray or run `conan info` output through a scanner → **(C)** [R2]
- [ ] CPM.cmake: external scanner (Grype, Trivy, OWASP Dependency-Check) against the fetched source tree → **(C)** [R3]
- [ ] HIGH or CRITICAL CVEs block merge unless a documented remediation plan exists (version bump, patch, or accepted risk with owner and deadline) → **(C)** [R4]

---

## Decision Tree

```
New C++ project or adding dependencies?
  → Choose package manager (project scale, platform needs) [1]
  → Commit manifest file to VCS [2]
  → Pin versions (baseline / lockfile / git hash) [3]
  → Verify hermetic: clean checkout builds [4]
  → Audit dep graph for diamond conflicts [5]
  → CI: cache packages, binary cache enabled [6]
  → Custom ports needed? → create + upstream plan [7]
  → License check: SPDX for every transitive dep [8]
  → CVE scan: HIGH/CRITICAL blocks merge [9]
```

---

## Anti-Patterns

### 1. System-Global Dependency Assumption

- **Appearance:** `find_package(Boost REQUIRED)` without a manifest; "install Boost with your system package manager."
- **Trap:** Quick setup on the developer's machine.
- **Consequence:** Different versions on different machines. CI fails unpredictably. New team member cannot build.
- **Fix:** Declare Boost in `vcpkg.json` / `conanfile.py` / `CPMAddPackage("boost")`. Remove the system-dependency instruction.

### 2. Floating Versions

- **Appearance:** `"fmt": "*"`, `CPMAddPackage("gh:fmtlib/fmt@master")`, `requires = "fmt/[>9.0]"`.
- **Trap:** "Always get the latest."
- **Consequence:** Build breaks without code changes. Bisecting old commits is impossible because dependencies shifted. CI is nondeterministic.
- **Fix:** Pin to exact baseline, lockfile, or git tag. Updates are explicit, reviewed PRs.

### 3. Mixed Package Managers

- **Appearance:** vcpkg for Boost, Conan for gRPC, CPM.cmake for fmt, all in one project.
- **Trap:** "Each tool is best for a particular library."
- **Consequence:** Conflicting transitive dependencies. Two copies of the same library linked into the binary. ODR violations. Unauditable supply chain.
- **Fix:** Choose one package manager. If a library is not in the catalog, create a custom port/recipe within that manager.

### 4. Uncommitted Lockfiles

- **Appearance:** `conan.lock` or `vcpkg-configuration.json` in `.gitignore`.
- **Trap:** "Generated files don't belong in VCS."
- **Consequence:** Every developer and CI run resolves dependencies independently. Different machines get different versions. Reproducibility is impossible.
- **Fix:** Commit the lockfile/baseline. It is the build contract.

---

## See Also

- [CMake Include Hygiene](../build/cmake-include-hygiene.md) — Build system configuration for CMake targets
- [Dependency Management (Common)](../../common/dependencies/dependency-management.md) — Language-agnostic dependency security and supply-chain practices

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Microsoft vcpkg Documentation | Manifest mode, versioning, binary caching, registries | verified-2026 | 2026-06 |
| R2 | C | Conan Documentation | Lockfiles, profiles, custom recipes, remotes | verified-2026 | 2026-06 |
| R3 | C | CMake FetchContent / CPM.cmake Documentation | Script-based dependency retrieval, source cache | verified-2026 | 2026-06 |
| R4 | C | OpenSSF Scorecard | Dependency Update Tooling, CVE scanning, SBOM | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft — package manager selection, version pinning, hermetic builds, dependency resolution, CI caching, custom ports, license compliance, CVE scanning
