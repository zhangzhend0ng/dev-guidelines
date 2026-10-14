---
type: harness
id: "common-nsis-installer-scripts"
title: "NSIS Installer Script Checklist"
language: "common"
category: "packaging"
tier: "C"
scope: "Write and review NSIS-based Windows installer scripts (.nsi/.nsh), including CPack-injected fragments — install/uninstall symmetry, registry views, silent installs, version stamping, and duplicated-variant drift"
version: "2026.10"
status: "draft"
stable_since: ""
last_validated: "2026-10-14"
review_cycle: "12m"
tags: [nsis, installer, windows, packaging, uninstall, registry, wow64, silent-install, cpack]
based_on:
  - "[C] NSIS Users Manual — SetRegView, WriteReg*/DeleteReg*, IfSilent, SetErrorLevel, ExecWait, silent installs (/S)"
  - "[C] Microsoft Learn — Registry Redirector (WOW64 32-bit vs 64-bit registry views)"
  - "[C] Microsoft Learn — Uninstall Registry Key (required values)"
  - "[C] MITRE CWE-732 / CWE-829 (installer privilege and bundled payload scope)"
  - "[A] NSIS known compiler issues and community guidance (LZMA /SOLID error, uninstaller _?= idiom)"
related:
  - "projects/snapmaker-orca/windows-installer.md"
supersedes: []
changelog:
  - "2026.10: Initial draft. Grounded in Snapmaker Orca installer.nsi / cmake/nsis wiring review; first observed drift case: divergent VERSION fallbacks between installer variants (2.4.0 vs 2.3.5)."
---

# NSIS Installer Script Checklist

**Based on:** NSIS Users Manual ([C]), Microsoft Learn Registry Redirector & Uninstall Registry Key ([C]), MITRE CWE-732/CWE-829 ([C]), NSIS known issues ([A]).
**Scope:** NSIS installer scripts (`.nsi`/`.nsh`) and the CPack variables that inject NSIS fragments. Covers what a reviewer can verify by reading the script and registry effects. Does NOT cover code signing infrastructure, WiX/MSI, or installer UI/UX design.

---

## Prerequisites / Concepts

| Concept | Meaning |
|---------|---------|
| **Registry view** | On 64-bit Windows, a 32-bit process (NSIS installers are 32-bit by default) sees the `WOW6432Node`-redirected view. `SetRegView 64` switches to the 64-bit view so a 64-bit application finds the keys. |
| **Silent install** | `installer.exe /S` skips UI. CI and automated deployment rely on it: interaction must branch on `IfSilent`, failure must exit non-zero via `SetErrorLevel`. |
| **Compile-time vs runtime** | `!define` values (payload dir, VERSION) are baked in by `makensis` (often via `/DNAME=value`); `$INSTDIR`, `$DESKTOP` are runtime. Mixing them up fails silently or produces wrong paths. |
| **Uninstall key** | `HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\<Name>` is what "Apps & Features" reads; missing values = invisible or broken entries. |
| **Symmetric pairs** | Three write/remove pairs must mirror each other: install section ↔ uninstall section; `CPACK_NSIS_EXTRA_INSTALL_COMMANDS` ↔ `CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS`; variant A ↔ variant B of near-duplicate scripts. |

---

## Checklist

### 1. Install/Uninstall Symmetry  **(C)** [R1]

Every registry key, shortcut, directory, and shell context (`SetShellVarContext`) written during install has a matching removal in the uninstall section — same registry view, same shell context, same key name.

- [ ] Every `WriteRegStr`/`WriteRegDWORD` has a corresponding `DeleteRegKey`/`DeleteRegValue` in the uninstall section → **(C)** [R1]
- [ ] Every `CreateShortcut` has a corresponding `Delete`; every `CreateDirectory` under the start menu has a corresponding `RMDir` → **(C)** [R1]
- [ ] Shortcuts created under `SetShellVarContext current` are deleted under `SetShellVarContext current` (and likewise for `all`) → **(C)** [R1]
- [ ] CPack path: `CPACK_NSIS_EXTRA_INSTALL_COMMANDS` and `CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS` are reviewed as a pair in the same change → **(C)** [R1]

```nsis
; Good — write and removal mirror each other, same view
SetRegView 64
WriteRegStr HKLM "Software\Classes\myapp" "URL Protocol" ""
SetRegView 32
; ... uninstall section:
SetRegView 64
DeleteRegKey HKLM "Software\Classes\myapp"
SetRegView 32

; Bad — written under view 64, deleted under default view 32: key survives uninstall
```

### 2. Registry View Discipline (WOW64)  **(C)** [R2]

- [ ] Registry keys that a 64-bit application (or Windows shell surfaces like Apps & Features) must read are written with `SetRegView 64` when the installer is 32-bit → **(C)** [R2]
- [ ] `SetRegView` is restored (`SetRegView 32` or documented baseline) after the block, so later default-view writes are unaffected → **(C)** [R2]
- [ ] Read-back guards (`.onInit` previous-version detection) query the same view the installer wrote → **(C)** [R2]

### 3. Silent Install Support  **(C)** [R1]

CI and end-user automation run with `/S`; any UI-only failure path is an unkillable hang or a false success.

- [ ] Every `MessageBox` on an error path has an `IfSilent` branch that aborts instead of waiting for a click → **(C)** [R1]
- [ ] Failure exits set a distinct non-zero error level (`SetErrorLevel <n>`) so CI can fail the job → **(C)** [R1]
- [ ] Retry loops (e.g. app-running guard) terminate in silent mode instead of looping forever → **(C)** [R1]

### 4. Version Stamping and Injection  **(C)** [R1][R3]

- [ ] `VERSION` comes from the build invocation (`makensis /DVERSION=...` or CI variable); the `!ifndef VERSION` fallback equals the version actually being released → **(C)** stale-fallback risk (drift observed in the wild: two variants carrying 2.4.0 vs 2.3.5)
- [ ] `VIProductVersion` gets a 4-numeric-part value (e.g. `${VERSION}.0`); a suffix like `-beta` breaks compilation at release time → **(C)** [R1]
- [ ] `DisplayVersion` in the uninstall key and the `OutFile` name embed the same `${VERSION}` → **(C)** [R3]

### 5. Duplicated-Script / Variant Drift  **(A)** [R1]

Near-identical installer variants (per-CI, per-distribution) and logic duplicated between a hand-written `.nsi` and a CPack-injected `.nsh` are the top drift source: a fix lands in one sibling, the other keeps the bug.

- [ ] A semantic change to one variant is mirrored to its sibling in the same change set; the variant diff stays limited to build paths and output names → **(A)** [R1]
- [ ] Logic existing in both a `.nsi` and a `.nsh` (e.g. protocol registration) is changed at every occurrence — grep the sibling before finishing → **(A)** [R1]

### 6. Payload Hygiene and Integrity Self-Check  **(C)** [R4]

- [ ] Recursive `File /r` from a build/pack directory carries an exclusion list (`/x`) for build junk (`.pdb`, `.lib`, build dirs); new artifact types extend the list → **(C)** [R4]
- [ ] After payload extraction, the installer verifies a sentinel file (`IfFileExists "$INSTDIR\<main exe>"`) and aborts with a clear message if missing → **(C)** [R4]

### 7. Running-App Guard and Previous-Version Uninstall  **(C)** [R1]

- [ ] Install blocks while the app is running (process check loop) instead of force-killing it; uninstall may `taskkill` as a last resort → **(C)** [R1]
- [ ] Process checks cover renamed/legacy executable names from earlier releases → **(A)** [R1]
- [ ] `.onInit` previous-version removal runs the old uninstaller synchronously (`ExecWait '"$R0" _?=$INSTDIR'`) and handles its error result → **(C)** [R1]

### 8. Destructive Deletion Blast Radius  **(C)** [R4]

`RMDir /r "$INSTDIR"` deletes recursively and unrecoverably.

- [ ] `$INSTDIR` is never assumed to contain only installer-owned files when user data may live there (documents, profiles); user data is preserved or explicitly migrated → **(C)** [R4]
- [ ] Locked files use `/REBOOTOK` rather than failing the whole uninstall → **(C)** [R1]
- [ ] No `RMDir /r` on paths outside `$INSTDIR`, `$SMPROGRAMS\<Product>` and equivalent installer-created directories → **(C)** [R4]

### 9. Elevation and Install Scope  **(C)** [R4]

- [ ] `RequestExecutionLevel admin` matches the actual scope of writes (HKLM, `$PROGRAMFILES64`); a per-user installer writes HKCU and uses `$LOCALAPPDATA` instead → **(C)** [R4]
- [ ] 64-bit application default directory is `$PROGRAMFILES64`, not `$PROGRAMFILES` (which resolves to `Program Files (x86)` for a 32-bit installer process) → **(C)** [R2]

### 10. Uninstall Key Completeness  **(C)** [R3]

- [ ] `HKLM\...\Uninstall\<Name>` sets at minimum: `DisplayName`, `DisplayVersion`, `UninstallString`, `InstallLocation`, `Publisher`, `DisplayIcon` → **(C)** [R3]
- [ ] `UninstallString` points at the uninstaller actually written by `WriteUninstaller` under `$INSTDIR` → **(C)** [R3]
- [ ] The uninstall key name is stable across versions (renaming it orphans the previous entry in Apps & Features) → **(C)** [R3]

---

## Quick Decision Tree

```
Change touches .nsi/.nsh?
  ├─ Registry write/delete → views match + mirrored in uninstall? [1][2]
  ├─ New user interaction or failure path → silent-mode branch + error level? [3]
  ├─ VERSION touched → fallback, VIProductVersion, DisplayVersion, OutFile all agree? [4]
  ├─ One of two sibling scripts → mirrored to the other? [5]
  ├─ File /r payload → exclusions current, sentinel check present? [6]
  ├─ Process/upgrade flow → guard covers legacy names, old uninstaller awaited? [7]
  └─ Deletion paths → blast radius limited, /REBOOTOK for locked files? [8]
Change touches CPack NSIS variables?
  ├─ EXTRA_INSTALL/UNINSTALL pair reviewed together? [1]
  ├─ Scope: HKLM writes require admin; per-user uses HKCU? [9]
  └─ Uninstall key values complete? [10]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Uninstall Leaves Orphans

- **Appearance:** Install writes protocol classes, an install key, and shortcuts; uninstall deletes only the uninstall key.
- **Trap:** The visible uninstall succeeds; nobody diffs the registry before/after.
- **Consequence:** Broken `scheme://` handlers pointing at deleted exes; duplicate Apps & Features entries after rename.
- **Fix:** Review install and uninstall sections side by side; every write needs a removal (Item 1).

### Anti-Pattern 2: 32-Bit View Writes for a 64-Bit App

- **Appearance:** `WriteRegStr HKLM "Software\Classes\..."` with no `SetRegView 64` in a 32-bit NSIS installer.
- **Trap:** Compiles, installs, "works" when tested by reading through the same 32-bit view.
- **Consequence:** The 64-bit application never sees the keys (protocol launch, file association silently broken).
- **Fix:** `SetRegView 64` around writes the 64-bit app must read; restore afterwards (Item 2).

### Anti-Pattern 3: MessageBox in Silent Mode

- **Appearance:** Error handler does `MessageBox MB_OK "failed"` unconditionally; CI runs `/S`.
- **Trap:** Interactive testing passes.
- **Consequence:** CI job hangs until timeout; exit code 0 false-green if the message box is skipped.
- **Fix:** `IfSilent` → `SetErrorLevel <n>` + `Abort`/`Quit` (Item 3).

---

## See Also

- [Snapmaker Orca Windows Installer](../../projects/snapmaker-orca/windows-installer.md) — project-level wiring of these rules: installer.nsi/gitlab_installer.nsi variants, CPack NSIS injection, CI `cpack -G NSIS` stage

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | NSIS Users Manual (nsis.sourceforge.io/Docs) | SetRegView, WriteRegStr/WriteRegDWORD, DeleteRegKey, IfSilent, SetErrorLevel, ExecWait, silent installs /S | verified-2026 | 2026-10 |
| R2 | C | Microsoft Learn — Registry Redirector | WOW64: 32-bit vs 64-bit registry views | verified-2026 | 2026-10 |
| R3 | C | Microsoft Learn — Uninstall Registry Key | Required values (DisplayName, UninstallString, DisplayVersion, ...) | verified-2026 | 2026-10 |
| R4 | C | MITRE CWE-732, CWE-829 | Incorrect permission assignment; inclusion of unneeded functionality (payload scope) | verified-2026 | 2026-10 |
| R5 | A | NSIS known issues / community guidance | LZMA `/SOLID` internal compiler error workaround; synchronous old-uninstaller `_?=` idiom | verified-2026 | 2026-10 |

---

## Changelog

- 2026.10: Initial draft. Grounded in Snapmaker Orca installer.nsi / cmake/nsis wiring review; first observed drift case: divergent VERSION fallbacks between installer variants (2.4.0 vs 2.3.5).
