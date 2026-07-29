---
type: harness
id: "common-config-option-registration"
title: "Configuration Option Registration and Dimension Classification Checklist"
language: "common"
category: "config"
tier: "A"
scope: "Classify a configuration option by its data dimension and register it symmetrically across every required site, before treating a requirement as a mere registration task"
version: "2026.07"
status: "draft"
stable_since: ""
last_validated: "2026-07-29"
review_cycle: "12m"
tags: [config, configuration, options, presets, data-dimension, serialization, registration, schema]
based_on:
  - "[C] Confluent Schema Registry / Apache Avro Schema Evolution"
  - "[A] dev-guidelines engineering experience"
related:
  - "cpp/design/feature-design-prerequisites.md"
  - "common/planning/task-decomposition.md"
  - "cpp/serialization/parsing-and-validation.md"
supersedes: []
changelog:
  - "2026.07: Initial draft — distilled from a session where a 'different value per mode' requirement was unrepresentable because the key's data dimension was [normal,stealth] (time-estimation mode), not per-extruder; a dimension mismatch is a design blocker, not a registration task"
---

# Configuration Option Registration and Dimension Classification Checklist

**Based on:** Confluent Schema Registry / Avro schema evolution ([C28]), dev-guidelines engineering experience.
**Scope:** The gate run when adding or changing a configuration option (setting/preference/knob): classify it by data dimension, register it at every required site, and treat its serialization name as immutable. This harness answers **whether a requirement is even representable in the current config model and how to wire one option completely**; `cpp/design/feature-design-prerequisites.md` answers what to design for a new feature, and `cpp/serialization/parsing-and-validation.md` answers how to parse untrusted input safely.

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|------------|
| Data dimension | The axis along which an option's value varies: **per-machine** (one value for the whole device), **per-instance/extruder** (one value per physical unit), **per-item/filament** (one value per consumable/item), or **per-mode** (one value per operational mode like normal/stealth). |
| Dimension mismatch | A requirement phrased in one dimension (e.g. "per hot-end type") but the relevant existing key lives in another (e.g. "per time-estimation mode"). This is a *design blocker*, not a registration task. |
| Symmetric registration sites | The set of places an option must appear to function end-to-end; missing any one causes silent partial functionality (the key exists but does not resize, serializes but never enters the dirty-check, etc.). |
| Serialization-name immutability | Once an option's on-disk name/enum value ships in a released format (config file, project file, G-code header), it cannot be renamed without breaking compatibility. |

**When this harness applies:** when adding, exposing, or repurposing a config option in any settings/preset system. **When it does NOT apply:** compile-time constants with no persistence, or pure UI state not serialized.

---

## Checklist

### 1. Classify the Option's Data Dimension First **(A)** [R1]

- [ ] Before registering, classify the new option as per-machine / per-instance / per-item / per-mode → **(A)** the dimension dictates the storage shape, the resize behavior, and which consumers must index it. [R1]
- [ ] The requirement's dimension matches the dimension of the existing key it would extend or reuse → **(A)** a mismatch (e.g. requirement says "per extruder" but the key is indexed by time-estimation mode) means the requirement is **not representable** in the current model; this is a design decision to escalate, not a registration to execute. [R1]
- [ ] Product/requirement vocabulary and code-model vocabulary for the same concept are reconciled → **(A)** "standard vs high-flow mode" (product) and "indexed by [normal,stealth]" (code) can name the same knob in different dimensions; the gap is invisible until you classify both. [R1]

### 2. Register Symmetrically Across Every Site **(A)** [R1]

- [ ] For a new option, every required registration site is touched: struct field declaration, enum static map (if enum), preset/option key list, dirty-check / preset-serialization list, and the build/source manifest → **(A)** missing one site causes silent partial functionality (option exists but does not persist, or persists but never marks the preset dirty). [R1]
- [ ] The set of sites is enumerated *for this system* before editing, not discovered by "it broke" → **(A)** "register in 5 places" discovered empirically ships the option half-wired in the places you forgot to check. [R1]

### 3. Per-Instance Keys Must Resize With Instance Count **(A)** [R1]

- [ ] A per-instance/per-extruder key is added to the resize list (e.g. `extruder_option_keys`) so it grows when the instance count changes → **(A)** without this, the key holds one value regardless of instance count, silently dropping per-instance data. [R1]
- [ ] After registration, changing the instance count is verified to produce N independent values for the new key → **(A)** the resize-list omission does not error; it silently under-allocates. [R1]

### 4. Serialization and Enum Names Are Immutable After First Release **(C)** [R2]

- [ ] The on-disk name and enum serialization value are chosen deliberately *before* first release, with upstream-alignment considered (align-with-upstream eases future rebases; divergent names reduce churn now but fork permanently) → **(C)** once the name is in a shipped format it cannot be renamed without breaking stored files. [R2]
- [ ] Renaming an already-released option requires a migration/alias, not an in-place rename → **(C)** an in-place rename silently breaks every existing stored file that used the old name. [R2]

### 5. Override Precedence Is Defined and Defaults to "User Can Only Tighten" **(A)** [R1]

- [ ] When a user-set global value and an auto-detected/per-instance value both apply, the precedence is explicit (not "whichever writes last") → **(A)** undefined precedence silently lets one source override the other. [R1]
- [ ] The default precedence rule is `max`/most-restrictive: a user global may only *tighten* (raise a safety/physical lower bound), never relax it → **(A)** letting a user global relax a physical/safety floor produces a silently unsafe configuration. [R1]

### 6. Distinguish "User Explicitly Set" from "Default" **(A)** [R1]

- [ ] A new option that participates in override logic has a sentinel/`was_set` flag (or nullable representation) so "user explicitly chose X" is distinguishable from "X is the struct default" → **(A)** without this, a "respect the user's value" rule is unexpressible — you cannot tell a user choice from an untouched default. [R1]
- [ ] The default value is documented alongside the option, not left as whatever the POD zero-initializes → **(A)** a default that is "whatever zero means" is an undocumented contract. [R1]

---

## Quick Decision Tree

```
Asked to "add a config option"
  │
  ├─ Classify its data dimension (machine/instance/item/mode) (item 1)
  │
  ├─ Does the requirement's dimension match the key it would extend?
  │     └─ NO → DESIGN BLOCKER: escalate, do not register (item 1)
  │     └─ YES → continue
  │
  ├─ Enumerate this system's symmetric registration sites; touch ALL (item 2)
  │     └─ per-instance? → add to the resize list; verify N independent values (item 3)
  │
  ├─ First release? → choose serialization/enum name deliberately (item 4)
  │     └─ already released? → migrate/alias, never in-place rename (item 4)
  │
  ├─ Overrides another value? → define precedence; default = max/tighten-only (item 5)
  │
  └─ Needs "user set it" vs "default"? → add sentinel/was_set (item 6)
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Dimension Mismatch Treated as a Registration Task

- **Appearance:** A requirement says "different acceleration per hot-end type"; an engineer adds a flag, expecting the existing acceleration key to "just hold per-hot-end values."
- **Trap:** The existing key is indexed by time-estimation mode (`[normal,stealth]`), not by extruder; both are 2-element, so it *looks* like it could fit.
- **Consequence:** The "registration" silently does nothing useful — one value pair per machine, not per hot-end. The requirement appears done until a second hot-end type is selected and nothing changes.
- **Fix:** Item 1: classify both dimensions first; a mismatch is a design decision (new per-extruder key, or emit-time selection), escalated to the people who own the data model — not a registration.

### Anti-Pattern 2: Half-Wired Option (Missing Registration Site)

- **Appearance:** An enum option is declared in the config struct and appears in the UI, so it "works," but it was never added to the preset dirty-check list.
- **Trap:** The option edits and applies during the session; local testing passes.
- **Consequence:** The option never marks the preset dirty, so it is silently dropped on save/reload — the user's choice vanishes, reproducibly but invisibly.
- **Fix:** Item 2: enumerate *all* registration sites for the system up front and verify each is touched; do not discover the set from bug reports.

### Anti-Pattern 3: In-Place Rename of a Released Name

- **Appearance:** An enum's serialization value `BigTraffic` is renamed to `HighFlow` mid-development "for clarity," directly in the enum declaration.
- **Trap:** The new name is clearer; the change compiles and passes fresh tests.
- **Consequence:** Every already-released config/project/G-code file that stored `BigTraffic` fails to load or silently resets to default — a compatibility break invisible to fresh-test-only verification.
- **Fix:** Item 4: released names are immutable; use a migration/alias, and verify against a file saved under the old name.

---

## See Also

- [Feature Design Prerequisites Checklist](../../cpp/design/feature-design-prerequisites.md) — the broader design gate for a new feature; this harness is the narrower "how to wire one config option completely" gate that runs when a feature needs a new setting.
- [Task Decomposition Checklist](../planning/task-decomposition.md) — splitting confirmed work; adding an option that fails item 1 (dimension mismatch) is *not* a schedulable task, it is a design escalation.
- [C++ Parsing and Validation Checklist](../../cpp/serialization/parsing-and-validation.md) — how to parse the serialized form safely once the option is registered; this harness covers *registration and dimension*, not input parsing.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines engineering experience | Config-system dimension classification and symmetric-registration site sets, observed across real feature work | verified-2026 | 2026-07 |
| R2 | C | [C28] Confluent Schema Registry / Apache Avro Schema Evolution | Backward/forward compatibility, schema-name immutability after release | verified-2026 | 2026-07 |

> **Tier honesty note:** The dimension-classification core (items 1–3, 5–6) is engineering experience with no single external standard — tagged (A), not inflated to (C). Only item 4 (serialization-name immutability) has a genuine consensus source ([C28]) and is tagged (C) at the item level; the harness tier stays (A).

---

## Changelog

- 2026.07: Initial draft — 6 items covering dimension classification, symmetric multi-site registration, per-instance resize, serialization-name immutability, override precedence (max/tighten-only), and the user-set-vs-default sentinel. Distilled from a session where a dimension mismatch was the hidden design blocker behind a "simple" config request.
