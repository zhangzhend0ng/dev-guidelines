---
type: harness
id: "snapmaker-orca-windows-installer"
title: "Snapmaker Orca Windows Installer Pipeline"
language: "cpp"
category: "project-specific"
tier: "P"
scope: "Review changes to Snapmaker Orca Windows packaging: installer.nsi/gitlab_installer.nsi variants, CPack NSIS wiring in CMakeLists.txt, cmake/nsis/*.nsh injection fragments, and the build_orca.yml cpack stage"
version: "2026.10"
status: "draft"
stable_since: ""
last_validated: "2026-10-14"
review_cycle: "6m"
tags: [snapmaker-orca, nsis, installer, cpack, windows, packaging]
based_on:
  - "[P] Snapmaker Orca repo — installer.nsi, gitlab_installer.nsi, cmake/nsis/SnapmakerURLProtocols_{install,uninstall}.nsh, CMakeLists.txt CPACK block (as of 2026-10)"
  - "[P] .github/workflows/build_orca.yml — choco install nsis; cpack -G NSIS"
  - "[C] NSIS Users Manual (SetRegView, IfSilent, SetErrorLevel, silent installs)"
related:
  - "common/packaging/nsis-installer-scripts.md"
supersedes: []
changelog:
  - "2026.10: Initial draft. Evidence base: 2026-10 review of the two .nsi variants (observed VERSION fallback drift 2.4.0 vs 2.3.5), CPack NSIS wiring, and CI packaging stage."
---

# Snapmaker Orca Windows Installer Pipeline

**Based on:** Snapmaker Orca packaging files ([P]), NSIS Users Manual ([C]).
**Scope:** Project-specific rules for the Windows installer of Snapmaker Orca — the two hand-written `.nsi` variants, the CPack-generated NSIS path, their shared fragments, and the CI stage that builds them. Generic NSIS rules live in the [NSIS Installer Script Checklist](../../common/packaging/nsis-installer-scripts.md); this harness only adds what is specific to this repo's wiring.

---

## Prerequisites / Concepts

**Two packaging paths ship the same app:**

| Path | Entry points | Where its logic lives |
|------|--------------|----------------------|
| Hand-written NSIS | `installer.nsi` (GitHub/local, payload from `.\build\...`) and `gitlab_installer.nsi` (GitLab CI, payload from `.\gitlab_build\...`) | All logic inside each `.nsi` |
| CPack-generated NSIS | `cpack -G NSIS` in build_orca.yml | `CMakeLists.txt` `CPACK_NSIS_*` variables + `cmake/nsis/*.nsh` fragments injected via `file(READ ... CPACK_NSIS_EXTRA_{INSTALL,UNINSTALL}_COMMANDS)` |

Because both paths register the same things (URL protocols, shortcuts, uninstall keys), several rules exist in **two or three places at once** — that duplication is the main review surface.

---

## Checklist

### 1. Variant Sync: installer.nsi ↔ gitlab_installer.nsi  **(P)** [R1]

The two variants are near-duplicates; the only legitimate differences are payload source dir, output file name, and VERSION fallback.

- [ ] The `diff installer.nsi gitlab_installer.nsi` of a change is limited to build paths (`.\build` vs `.\gitlab_build`), output naming (`..._Windows_Installer_V...` vs `..._Windows_V...`), and version fallback → **(P)** [R1]
- [ ] No semantic fix (registry, sections, guards, pages) lands in only one variant → **(P)** drift already observed: fallback `VERSION` 2.4.0 vs 2.3.5
- [ ] When changing one variant, grep the sibling for every touched construct (`WriteRegStr`, `Section`, guard labels) before finishing → **(P)** [R1]

### 2. URL-Protocol Registration Exists in Three Places  **(P)** [R1]

`snapmaker-orca://` and `Snapmaker_Orca://` are registered in: (a) both `.nsi` main sections, (b) `cmake/nsis/SnapmakerURLProtocols_install.nsh` with its mirror `SnapmakerURLProtocols_uninstall.nsh` (CPack path), (c) the macOS bundle `CFBundleURLSchemes` (the `.nsh` header documents the mirroring intent).

- [ ] Adding/renaming/removing a scheme updates all of: both `.nsi` main sections, both `.nsh` fragments, and the macOS scheme list → **(P)** [R1]
- [ ] The uninstall mirror (`.nsh` and `Uninstall` section) removes exactly what install wrote — same `SetRegView 64` block boundaries → **(P)** [R1]

### 3. CPack Injection Wiring  **(P)** [R1]

- [ ] Edits to `cmake/nsis/*.nsh` only reach the installer because `CMakeLists.txt` does `file(READ ... CPACK_NSIS_EXTRA_INSTALL_COMMANDS / EXTRA_UNINSTALL_COMMANDS)` — re-configure and rebuild the installer to verify the edit landed; do not judge from the `.nsh` file alone → **(P)** [R1]
- [ ] `CPACK_NSIS_CREATE_ICONS_EXTRA` and `CPACK_NSIS_DELETE_ICONS_EXTRA` are changed as a pair, same `SetShellVarContext current` → **(P)** [R1]
- [ ] New `CPACK_NSIS_*` variables follow `CPACK_VERBATIM_VARIABLES ON` (escaping-sensitive) — check generated `.nsi` output under the CPack temp dir if behavior looks off → **(P)** [R1]

### 4. Preinstall Guard: Two Copies, Same Semantics  **(P)** [R1]

The running-app/upgrade guard exists twice: `EnsureSnapmakerNotRunning` (`.nsi` path) and `CPACK_NSIS_EXTRA_PREINSTALL_COMMANDS` (CPack path).

- [ ] Both copies check both process names: `snapmaker-orca.exe` and legacy `Snapmaker_Orca.exe` → **(P)** [R1]
- [ ] Both copies branch on `IfSilent` with `SetErrorLevel 7` so CI fails loudly → **(P)** [R1]
- [ ] `CPACK_NSIS_ENABLE_UNINSTALL_BEFORE_INSTALL` stays `OFF` — upgrade flow is owned by the custom guard (CPack's default prompt fires at the wrong time); do not "fix" this to ON → **(P)** [R1]

### 5. Version Source of Truth  **(P)** [R1]

- [ ] Release builds pass `/DVERSION=...` (makensis) / `CPACK_PACKAGE_VERSION` (cpack); the `!ifndef VERSION` fallbacks in both variants equal the version being released → **(P)** observed drift: 2.4.0 vs 2.3.5
- [ ] `VIProductVersion "${VERSION}.0"` stays 4-numeric-part — release tags with a suffix (`-beta`, `-rc1`) must be sanitized before reaching it → **(P)** [R1]
- [ ] Output artifact names embed `${VERSION}` consistently across both variants and the CPack package name → **(P)** [R1]

### 6. Registry Identity Stability  **(P)** [R1]

The two paths intentionally use two registry identities: hand-written path uninstall key `HKLM\...\Uninstall\Snapmaker Orca` (space, from `PRODUCT_NAME`) and CPack `CPACK_PACKAGE_INSTALL_REGISTRY_KEY "Snapmaker_Orca"` (underscore).

- [ ] Neither identity is renamed without a migration step — renaming orphans the old Apps & Features entry and breaks upgrade detection (`EnsureSnapmakerNotRunning`/.onInit read-back) → **(P)** [R1]
- [ ] Install-key writes (`Software\Snapmaker\...`) and their `DeleteRegKey` mirrors (including the `HKCU` fallback delete) stay symmetric → **(P)** [R1]

### 7. CI Packaging Stage Prerequisites  **(P)** [R2]

- [ ] In build_orca.yml the Windows packaging job keeps the order: `choco install nsis` → build + install target populates the pack dir → `cpack -G NSIS` → checksum (`CPACK_PACKAGE_CHECKSUM SHA256`) → upload artifact → **(P)** [R2]
- [ ] A change to installer inputs (icons via `/DICON_FILE`, license file, payload dir layout) is reflected in the invocation in the same change → **(P)** [R2]

### 8. Known Workarounds Are Load-Bearing  **(P)** [R1]

- [ ] `SetCompressor lzma` without `/SOLID` stays as-is — `/SOLID` triggers NSIS "internal compiler error #12345" on this payload; the comment documents it → **(P)** [R1]
- [ ] Uninstall-path `taskkill /F` (last resort, app already closed) is not copied into the install path — install blocks-and-retries instead → **(P)** [R1]

---

## Quick Decision Tree

```
Which file does the change touch?
  ├─ installer.nsi / gitlab_installer.nsi
  │    ├─ semantic edit → mirrored in the sibling? [1]
  │    ├─ protocol block → .nsh pair + macOS schemes too? [2]
  │    └─ guard/version → CPack copy semantics + fallbacks aligned? [4][5]
  ├─ cmake/nsis/*.nsh
  │    ├─ install fragment → uninstall mirror matches? [2]
  │    └─ verified through a real cpack run? [3]
  ├─ CMakeLists.txt CPACK_* block
  │    ├─ EXTRA_INSTALL/UNINSTALL or CREATE/DELETE_ICONS pair reviewed together? [3]
  │    ├─ registry key renamed → migration for old identity? [6]
  │    └─ ENABLE_UNINSTALL_BEFORE_INSTALL still OFF? [4]
  └─ build_orca.yml packaging job → stage order + inputs intact? [7]
Any change → known workarounds untouched? [8]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Fixing One Variant Only

- **Appearance:** Bug fix merged into `installer.nsi`; release actually built from `gitlab_installer.nsi` (or vice versa).
- **Trap:** The fixed file passes local testing; the shipped artifact runs the unfixed sibling.
- **Consequence:** The bug ships; VERSION fallback drift (2.4.0/2.3.5) shows the failure mode is real.
- **Fix:** Item 1 — variant diff limited to build path/name/version; mirror every semantic change.

### Anti-Pattern 2: Renaming a Registry Identity

- **Appearance:** "Cleanup" renames `Snapmaker Orca` → `Snapmaker_Orca` (or the CPack registry key) for consistency.
- **Trap:** Both look equally valid; fresh installs work fine.
- **Consequence:** Upgrades from existing installs orphan the old Apps & Features entry and re-trigger the "already installed" path against a stale key.
- **Fix:** Item 6 — identities are stable contracts; rename only with explicit migration.

### Anti-Pattern 3: Judging .nsh Edits Without a cpack Run

- **Appearance:** `.nsh` fragment edited; review approves the diff directly.
- **Trap:** The fragment is inert until CMake re-reads it into `CPACK_NSIS_EXTRA_*_COMMANDS`; syntax that survives `makensis` standalone can still break template substitution.
- **Consequence:** Broken or silently-missing step in the generated installer.
- **Fix:** Item 3 — rebuild the installer via `cpack -G NSIS` and inspect the generated script before approving.

---

## See Also

- [NSIS Installer Script Checklist](../../common/packaging/nsis-installer-scripts.md) — generic rules this project harness builds on (symmetry, registry views, silent installs, version stamping)

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | P | Snapmaker Orca repo | installer.nsi, gitlab_installer.nsi, cmake/nsis/*.nsh, CMakeLists.txt CPACK block | verified-2026 | 2026-10 |
| R2 | P | Snapmaker Orca CI | .github/workflows/build_orca.yml (nsis install, cpack -G NSIS, artifacts) | verified-2026 | 2026-10 |
| R3 | C | NSIS Users Manual | SetRegView, IfSilent, SetErrorLevel, silent installs | verified-2026 | 2026-10 |

---

## Changelog

- 2026.10: Initial draft. Evidence base: 2026-10 review of the two .nsi variants (observed VERSION fallback drift 2.4.0 vs 2.3.5), CPack NSIS wiring, and CI packaging stage.
