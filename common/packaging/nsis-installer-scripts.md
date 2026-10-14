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
  - "[C] NSIS Users Manual, Chapter 4 + Reference pages (SetRegView, IfSilent, SetErrorLevel, ExecWait, silent /S, VIProductVersion, File /x, RMDir /REBOOTOK, $PROGRAMFILES64, RequestExecutionLevel, WriteUninstaller, uninstaller _?= parameter)"
  - "[C] Microsoft Learn — Registry Redirector (WOW64 32-bit vs 64-bit registry views)"
  - "[C] Microsoft Learn — Windows Installer Properties for the Uninstall Registry Key (documented ARP value names)"
  - "[C] MITRE CWE-732 (Incorrect Permission Assignment for Critical Resource)"
related:
  - "projects/snapmaker-orca/windows-installer.md"
supersedes: []
changelog:
  - "2026.10: Initial draft. Grounded in Snapmaker Orca installer.nsi / cmake/nsis wiring review; first observed drift case: divergent VERSION fallbacks between installer variants (2.4.0 vs 2.3.5)."
  - "2026.10.14: Citation audit against primary sources (NSIS Chapter 4/Reference pages, Microsoft Learn Registry Redirector and Uninstall Registry Key, MITRE CWE-732 — all fetched and verified). Retiered obligation-only items (symmetry, variant sync, payload hygiene, elevation-scope matching) from (C) to (A); kept document-backed mechanics at (C). Removed CWE-829 (its definition — inclusion of functionality from an untrusted sphere — does not cover shipping build junk) and the unused NSIS-known-issues row. Added CWE-732-backed ACL bullet. ARP claims scoped to documented value names: no authoritative source defines a required minimum, so the 'minimum values' claim was retiered to (A) practice."
---

# NSIS Installer Script Checklist

**Based on:** NSIS Users Manual ([C]), Microsoft Learn Registry Redirector ([C]), Microsoft Learn Uninstall Registry Key value names ([C]), MITRE CWE-732 ([C]).
**Scope:** NSIS installer scripts (`.nsi`/`.nsh`) and the CPack variables that inject NSIS fragments. Covers what a reviewer can verify by reading the script and registry effects. Does NOT cover code signing infrastructure, WiX/MSI, or installer UI/UX design.

**Tier discipline in this harness:** (C) items restate documented behavior of a cited source (tool manual, Microsoft Learn, MITRE). (A) items are engineering obligations built on top of those mechanics — the references inform them, but no standard mandates them.

---

## Prerequisites / Concepts

| Concept | Meaning |
|---------|---------|
| **Registry view** | On 64-bit Windows, a 32-bit process (NSIS installers are 32-bit by default) operates on the redirected logical view; redirected keys live under `Wow6432Node`. `SetRegView 64` switches NSIS registry commands to the 64-bit view (the script-level equivalent of `KEY_WOW64_64KEY`). |
| **Silent install** | `installer.exe /S` skips UI. CI and automated deployment rely on it: interaction must branch on `IfSilent`, failure must exit non-zero via `SetErrorLevel`. |
| **Compile-time vs runtime** | `!define` values (payload dir, VERSION) are baked in by `makensis` (often via `/DNAME=value`); `$INSTDIR`, `$DESKTOP` are runtime. Mixing them up fails silently or produces wrong paths. |
| **Uninstall key** | `HKLM\Software\Microsoft\Windows\CurrentVersion\Uninstall\<Name>` is what "Apps & Features" reads; Microsoft documents the value names it consumes (DisplayName, UninstallString, DisplayVersion, Publisher, ...). |
| **Symmetric pairs** | Three write/remove pairs must mirror each other: install section ↔ uninstall section; `CPACK_NSIS_EXTRA_INSTALL_COMMANDS` ↔ `CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS`; variant A ↔ variant B of near-duplicate scripts. |

---

## Checklist

### 1. Install/Uninstall Symmetry  **(A)** [R1]

Every registry key, shortcut, directory, and shell context (`SetShellVarContext`) written during install has a matching removal in the uninstall section — same registry view, same shell context, same key name. The manual documents each write/remove instruction pair; the obligation to keep them mirrored is engineering practice.

- [ ] Every `WriteRegStr`/`WriteRegDWORD` has a corresponding `DeleteRegKey`/`DeleteRegValue` in the uninstall section → **(A)** [R1]
- [ ] Every `CreateShortcut` has a corresponding `Delete`; every `CreateDirectory` under the start menu has a corresponding `RMDir` → **(A)** [R1]
- [ ] Shortcuts created under `SetShellVarContext current` are deleted under `SetShellVarContext current` (and likewise for `all`) → **(A)** [R1]
- [ ] CPack path: `CPACK_NSIS_EXTRA_INSTALL_COMMANDS` and `CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS` are reviewed as a pair in the same change → **(A)** [R1]

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

### 2. Registry View Discipline (WOW64)  **(C)** [R2][R1]

Documented semantics: 32-bit processes operate on the redirected view; `SetRegView 64` makes NSIS registry commands target the 64-bit view.

- [ ] Registry keys that a 64-bit application (or shell surfaces like Apps & Features) must read are written with `SetRegView 64` when the installer is 32-bit → **(C)** [R2]
- [ ] `SetRegView` is restored (`SetRegView 32` or documented baseline) after the block, so later default-view writes are unaffected → **(C)** [R1]
- [ ] Read-back guards (`.onInit` previous-version detection) query the same view the installer wrote → **(C)** [R2]

### 3. Silent Install Support  **(A)** [R1]

`/S`, `IfSilent`, and `SetErrorLevel` are documented; branching every interaction on them is the engineering obligation that makes CI installs reliable.

- [ ] Every `MessageBox` on an error path has an `IfSilent` branch that aborts instead of waiting for a click → **(A)** [R1]
- [ ] Failure exits set a distinct non-zero error level (`SetErrorLevel <n>`) so CI can fail the job → **(A)** [R1]
- [ ] Retry loops (e.g. app-running guard) terminate in silent mode instead of looping forever → **(A)** [R1]

### 4. Version Stamping and Injection  **(C)** [R1]

- [ ] `VIProductVersion` receives a 4-numeric-part value (e.g. `${VERSION}.0`); the manual requires `X.X.X.X` — a suffix like `-beta` breaks compilation at release time → **(C)** [R1]
- [ ] `VERSION` comes from the build invocation (`makensis /DVERSION=...` or CI variable); the `!ifndef VERSION` fallback equals the version actually being released → **(A)** fallback drift observed in the wild: two installer variants carrying 2.4.0 vs 2.3.5 [R1]
- [ ] `DisplayVersion` in the uninstall key and the `OutFile` name embed the same `${VERSION}` → **(A)** [R1][R3]

### 5. Duplicated-Script / Variant Drift  **(A)** [R1]

Near-identical installer variants (per-CI, per-distribution) and logic duplicated between a hand-written `.nsi` and a CPack-injected `.nsh` are the top drift source: a fix lands in one sibling, the other keeps the bug.

- [ ] A semantic change to one variant is mirrored to its sibling in the same change set; the variant diff stays limited to build paths and output names → **(A)** [R1]
- [ ] Logic existing in both a `.nsi` and a `.nsh` (e.g. protocol registration) is changed at every occurrence — grep the sibling before finishing → **(A)** [R1]

### 6. Payload Hygiene and Integrity Self-Check  **(A)** [R1]

`File /x` excludes and `IfFileExists`/`Abort` are documented instructions; keeping the exclusion list current and verifying the payload is engineering practice (no standard governs installer payload contents).

- [ ] Recursive `File /r` from a build/pack directory carries an exclusion list (`/x`) for build junk (`.pdb`, `.lib`, build dirs); new artifact types extend the list → **(A)** [R1]
- [ ] After payload extraction, the installer verifies a sentinel file (`IfFileExists "$INSTDIR\<main exe>"`) and aborts with a clear message if missing → **(A)** [R1]

### 7. Running-App Guard and Previous-Version Uninstall  **(A)** [R1]

- [ ] Install blocks while the app is running (process check loop) instead of force-killing it; uninstall may `taskkill` as a last resort → **(A)** [R1]
- [ ] Process checks cover renamed/legacy executable names from earlier releases → **(A)** [R1]
- [ ] `.onInit` previous-version removal runs the old uninstaller with the documented `_?=` parameter (`ExecWait '"$R0" _?=$INSTDIR'`) — the manual notes `_?=INSTDIR` prevents the self-copy to temp so the wait actually waits, must be the last parameter, and cannot contain quotes — and handles its error result → **(C)** [R1]

### 8. Destructive Deletion Blast Radius  **(C)** [R1]

`RMDir /r` deletes recursively — documented semantics; scoping what it may touch is practice.

- [ ] Locked files use `/REBOOTOK` (documented) rather than failing the whole uninstall → **(C)** [R1]
- [ ] `$INSTDIR` is never assumed to contain only installer-owned files when user data may live there (documents, profiles); user data is preserved or explicitly migrated → **(A)** [R1]
- [ ] No `RMDir /r` on paths outside `$INSTDIR`, `$SMPROGRAMS\<Product>` and equivalent installer-created directories → **(A)** [R1]

### 9. Elevation, Install Scope, and Permissions  **(C)** [R1][R4]

- [ ] For a 64-bit application the default directory is `$PROGRAMFILES64` — `$PROGRAMFILES` in a 32-bit installer process resolves to `Program Files (x86)` (documented variable semantics) → **(C)** [R1]
- [ ] Installed files and directories are not left writable by unprivileged users (no `Everyone`-writable ACLs under the install dir) — exactly CWE-732's definition of incorrect permission assignment for a critical resource → **(C)** [R4]
- [ ] `RequestExecutionLevel admin` matches the actual scope of writes (HKLM, `$PROGRAMFILES64`); a per-user installer writes HKCU and uses `$LOCALAPPDATA` instead → **(A)** [R1]

### 10. Uninstall Key Content  **(C)** [R3]

Microsoft documents the value names the Uninstall key carries (DisplayName, UninstallString, DisplayVersion, Publisher, InstallLocation, URLInfoAbout, HelpLink, Comments, ...). Note: the documented page is a value-name reference — no authoritative source defines which subset is mandatory, so completeness is scoped as practice below.

- [ ] The uninstall key sets the documented value names appropriate for the app (at least `DisplayName` and `UninstallString`, plus the descriptive values the ecosystem expects: `DisplayVersion`, `Publisher`, `InstallLocation`, `DisplayIcon`) → **(A)** [R3]
- [ ] `UninstallString` points at the uninstaller actually written by `WriteUninstaller` under `$INSTDIR` → **(A)** [R1][R3]
- [ ] The uninstall key name is stable across versions (renaming it orphans the previous entry in Apps & Features) → **(A)** [R3]

---

## Quick Decision Tree

```
Change touches .nsi/.nsh?
  ├─ Registry write/delete → views match + mirrored in uninstall? [1][2]
  ├─ New user interaction or failure path → silent-mode branch + error level? [3]
  ├─ VERSION touched → fallback, VIProductVersion, DisplayVersion, OutFile all agree? [4]
  ├─ One of two sibling scripts → mirrored to the other? [5]
  ├─ File /r payload → exclusions current, sentinel check present? [6]
  ├─ Process/upgrade flow → guard covers legacy names, old uninstaller _?=-awaited? [7]
  ├─ Deletion paths → blast radius limited, /REBOOTOK for locked files? [8]
  └─ Scope/permissions → admin matches writes, no Everyone-writable ACLs? [9]
Change touches CPack NSIS variables?
  ├─ EXTRA_INSTALL/UNINSTALL pair reviewed together? [1]
  └─ Uninstall key values from the documented set? [10]
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
| R1 | C | NSIS Users Manual — Chapter 4 + Reference pages (nsis.sourceforge.io/Docs) | SetRegView, WriteRegStr/WriteRegDWORD, DeleteRegKey, IfSilent, SetErrorLevel, ExecWait, silent installs /S, VIProductVersion, File /x, IfFileExists, RMDir /REBOOTOK, $PROGRAMFILES/$PROGRAMFILES64, RequestExecutionLevel, WriteUninstaller, uninstaller `_?=` parameter | verified-2026 | 2026-10 |
| R2 | C | Microsoft Learn — Registry Redirector | 32/64-bit logical registry views under WOW64; Wow6432Node; KEY_WOW64_64KEY | verified-2026 | 2026-10 |
| R3 | C | Microsoft Learn — Windows Installer Properties for the Uninstall Registry Key | Documented ARP value names (DisplayName, UninstallString, DisplayVersion, Publisher, InstallLocation, URLInfoAbout, ...) — names only; page defines no required minimum | verified-2026 | 2026-10 |
| R4 | C | MITRE CWE-732 | Incorrect Permission Assignment for Critical Resource (e.g., Everyone-writable installed files/directories) | verified-2026 | 2026-10 |

---

## Changelog

- 2026.10: Initial draft. Grounded in Snapmaker Orca installer.nsi / cmake/nsis wiring review; first observed drift case: divergent VERSION fallbacks between installer variants (2.4.0 vs 2.3.5).
- 2026.10.14: Citation audit against primary sources (NSIS Chapter 4/Reference pages, Microsoft Learn Registry Redirector and Uninstall Registry Key, MITRE CWE-732 — all fetched and verified). Retiered obligation-only items (symmetry, variant sync, payload hygiene, elevation-scope matching) from (C) to (A); kept document-backed mechanics at (C). Removed CWE-829 (its definition — inclusion of functionality from an untrusted sphere — does not cover shipping build junk) and the unused NSIS-known-issues row. Added CWE-732-backed ACL bullet. ARP claims scoped to documented value names: no authoritative source defines a required minimum, so the 'minimum values' claim was retiered to (A) practice.
