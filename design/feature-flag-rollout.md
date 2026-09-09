---
type: harness
id: "common-feature-flag-rollout"
title: "Remote Feature-Flag Evaluation and Rollout Checklist"
language: "common"
category: "design"
tier: "C"
scope: "Evaluate remotely-pushed feature-flag configs with fail-closed semantics across client versions and schema upgrades: last-known-good caching on rejection, explicit gate-tier semantics, generic evaluation loops, and doc-to-code contract sync"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-09"
review_cycle: "12m"
tags: [feature-flags, remote-config, fail-closed, rollout, schema-versioning, cache, client-server]
based_on:
  - "[C] Confluent Schema Registry / Apache Avro Schema Evolution"
  - "[A] Release It! (Michael Nygard)"
  - "[A] dev-guidelines engineering experience (lava monorepo dual-diff review)"
related:
  - "common/config/option-registration-and-dimension.md"
  - "dart/json-boundaries.md"
supersedes: []
changelog:
  - "2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)"
---

# Remote Feature-Flag Evaluation and Rollout Checklist

**Based on:** Confluent Schema Registry / Avro schema evolution ([C28], for version/schema compatibility), Release It! ([A], for stability under partial failure), dev-guidelines engineering experience from the lava monorepo dual-diff review ([A]).
**Scope:** The discipline for **clients that evaluate feature flags pushed by a remote/cloud config** — the payload crosses a trust boundary, different installed client versions evaluate the *same* payload with *different* evaluation logic, and a bad apply must not corrupt the client's durable flag state. This is the design gate that pairs with `common/config/option-registration-and-dimension.md` (registering the option correctly) and `dart/json-boundaries.md` (parsing the inbound payload safely). It is language-agnostic; examples are Dart/Flutter only because that is where the source incidents occurred.

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|------------|
| Fail-closed evaluation | If any input needed to decide a flag is missing, malformed, unknown, or from an unsupported schema version, the flag resolves to its **safe default** (usually off / keep-current-behavior). It never "guesses on". |
| Client schema version vs payload version | Each installed client knows the config schema it was built against. A payload marked with a newer schema version, or carrying fields the client cannot parse, must be **rejected as a whole** — not half-applied. |
| Eval-semantics upgrade (dual-write) | When the *meaning* of a config changes (e.g. a new gate tier is introduced), new and old clients run different logic over the same payload. The transition must keep **both** old and new clients fail-closed; a field only the new client understands must never be the sole source a payload's meaning rests on. |
| Last-known-good cache | The client persists the most recent config that *passed* validation. A rejected config must **not** overwrite it; otherwise a restart after a bad push loses even the last valid values. |
| Gate tier | The level at which a problem is handled: the whole config is rejected (keep current values; update blocked) vs a single flag is forced off (a definite fail-closed result). These have different semantics and must be explicit. |

**Why this harness exists:** the source incident combined (a) an evaluation path that hard-coded one flag name, (b) a rejected config overwriting the cached one so values drifted after restart, and (c) evaluation-semantics changes whose contract lived only in code comments referencing a doc that was not updated in the same diff. Each failure looked local; each produced a silent, reproducible behavior change.

---

## Checklist

### 1. Every Flag Evaluation Ends in a Definite Value, Defaulting Closed **(C)** [R1][R3]

- [ ] A flag name is absent from the payload, or its value is null/malformed → **(C)** resolve to the documented safe default (off / keep-current); never fall through to "on" or to an uninitialized value. [R1][R3]
- [ ] The default is the *same* value a client that has never received config would use → **(C)** a fresh install and an install with a rejected update must agree; otherwise first-run and post-failure behavior diverge. [R3]

### 2. The Evaluation Engine Knows No Flag Names; New Flags Go Through the Generic Loop **(C)** [R3]

- [ ] Evaluation code names a specific flag (`flags['modelCommunity']`) inside the apply routine → **(C)** the engine iterates/registers generically and reads values by key; a hard-coded name means every new flag needs an engine edit and untested flags silently read nothing. [R3]
- [ ] A new flag is added → **(C)** it is declared in one registration place (schema + default + doc) and the generic loop picks it up; adding a flag is not a code change to the evaluator. [R3]

```dart
// Bad — the engine hard-codes one flag; every sibling flag needs its own edit.
void _applyConfig(Map<String, dynamic> cfg) {
  final flags = (cfg['flags'] as Map?) ?? const {};
  _modelCommunityEnabled = flags['modelCommunity'] == true; // hard-coded
}

// Good — generic loop + declared defaults; new flags need no engine change.
void _applyConfig(Map<String, dynamic> cfg, FlagSchema schema) {
  for (final f in schema.flags) {
    final raw = flags[f.key];
    _setFlag(f.key, _evaluate(f, raw)); // _evaluate fails closed per item 1
  }
}
```

### 3. A Rejected Config Never Overwrites the Cache (Last-Known-Good) **(C)** [R2][R3]

- [ ] A received config fails validation (schema version too new, unparseable field, gate not met) → **(C)** reject the whole update and **keep the cached last-known-good config**; do not write the bad payload to the cache. [R2][R3]
- [ ] The client restarts after a rejected push → **(C)** it must reload the last-known-good config, not re-derive defaults from the rejected payload; verify this path in a test (reject → restart → values unchanged). [R3]
- [ ] The cache write and the in-memory apply happen together → **(C)** make "config accepted" the single gate before either the cache write or the apply; a partial write (cache updated, apply failed, or vice versa) is a corruption bug. [R3]

### 4. Evaluation-Semantics Upgrades Keep Old and New Clients Fail-Closed (Dual-Write) **(C)** [R1][R3]

- [ ] A semantics upgrade changes how a flag is decided (e.g. adding a gate tier the old client cannot express) → **(C)** the rollout carries both encodings or a compatibility rule so that **old clients** (which do not know the new field) still resolve to a safe value — an unrecognized field must never be the only thing a payload's meaning depends on. [R1][R3]
- [ ] New-client-only fields appear in a payload consumed by old clients → **(C)** treat them as unknown-and-ignorable for old clients *only if* the old semantics remain fail-closed without them; if old clients would now mis-evaluate, the payload must still carry what old clients need until they are drained. [R1][R3]

### 5. Gate-Tier Semantics Are Explicit and Documented **(A)** [R2][R3]

- [ ] Two different failure levels exist — "whole config rejected" vs "one flag forced off" → **(A)** name and document them distinctly: config-level rejection **keeps current values** (update blocked), while a per-flag off is a **definite fail-closed result**; code, tests, and the config doc must not blur them. [R2][R3]
- [ ] A UI/state consumer reads a flag after a config-level rejection → **(A)** it sees the previous values (not "everything defaulted"); make the distinction observable in tests so a future refactor cannot silently convert a keep-current into a reset-to-default. [R3]

### 6. Schema/Version Gating Runs Before Any Apply **(C)** [R1][R3]

- [ ] A payload's schema version is checked *after* fields have been read/trusted → **(C)** check first: version unsupported → reject whole payload (item 3) before any field is applied. [R1][R3]
- [ ] Unknown future fields are tolerated → **(C)** only when fail-closed defaults (item 1) cover what those fields would have changed; document that tolerance explicitly. [R3]

### 7. Contract Doc and Code Comments Move in the Same Diff **(C)** [R3]

- [ ] Code comments or the schema reference a contract doc (`docs/*.md`) that defines fields/defaults/gate tiers → **(C)** any diff that changes the schema or semantics updates that doc in the **same diff**; a doc that describes a past schema is worse than no doc because it is confidently wrong. [R3]
- [ ] A reviewer sees a schema/behavior change without the doc change → **(C)** request the doc update before merge; the doc is the contract old and new clients are both held to (item 4). [R3]

---

## Quick Decision Tree

```
Remote config payload arrives
  ├─ schema/version supported?      ── NO → reject whole payload; keep cache  [3][6]
  ├─ parseable by this client?     ── NO → reject whole payload; keep cache  [3][6]
  ├─ semantics require new fields? ── old clients still fail-closed? ── NO → dual-write still needed  [4]
  ├─ apply                             → generic loop over declared flags  [2]
  │     └─ per flag                   → fail closed on missing/malformed  [1]
  │           ├─ config rejected as a whole? → keep current values (update blocked)  [5]
  │           └─ single flag off?            → definite off; document the tier  [5]
  ├─ cache write happens ONLY on accept  [3]
  └─ doc/comments referencing docs/*.md updated in the same diff  [7]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Hard-Coded Flag Name in the Apply Routine

- **Appearance:** `_applyConfig` reads `flags['modelCommunity']` directly to set one boolean. When a sibling feature ships, the developer adds another `flags['xxx'] == true` line next to it.
- **Trap:** The first flag works end-to-end, and a per-name read is the shortest path. The engine never looks like it "has" an architecture.
- **Consequence:** Every new flag requires an engine edit; flags that were not hand-wired read nothing (silently off) and the pattern spreads until evaluation is a chain of special cases. A flag added server-side without a client edit does nothing, and nothing in the log explains why.
- **Fix:** Item 2 — make the engine iterate over a declared flag schema with per-flag defaults and fail-closed evaluation; a new flag is a registration change, not a code change to the evaluator.

### Anti-Pattern 2: Rejected Config Overwrites the Cache

- **Appearance:** On every push the client writes the incoming payload to its config cache and applies it, and only *afterwards* validates. A bad push (schema too new, gate not met) is written to the cache before validation fails.
- **Trap:** "Write-then-validate" mirrors naive read-apply flows and keeps the code simple; locally the bad payload may never arrive.
- **Consequence:** The cache now holds a config the client itself rejected. After the next restart the client loads the bad config (or its partial parse) instead of the last valid values — feature state silently drifts to whatever the rejected payload half-decodes to, and the failure is only visible as "flags changed after an update that should have been blocked."
- **Fix:** Item 3 — validation is the single gate before *both* the cache write and the apply; keep last-known-good and add the reject→restart→values-unchanged test.

### Anti-Pattern 3: Old Client Reads a Payload Whose Meaning Only the New Client Can Determine

- **Appearance:** A semantics upgrade adds a gate tier encoded in a brand-new field. The server stops sending the old fields and sends only the new field; the new client (which understands it) is correct, and the old client falls back to "field absent ⇒ default" — but the default is no longer the fail-closed value under the *new* semantics.
- **Trap:** Old clients ignore unknown fields gracefully (no crash), which looks compatible. The fallback path is exercised only by clients you are not testing anymore.
- **Consequence:** Old clients silently evaluate the *new* semantics with *old* logic — the exact window dual-write exists to prevent. A flag meant to be off for everyone is on for old clients, or vice versa, until the old clients drain.
- **Fix:** Item 4 — during a semantics transition the payload keeps what old clients need (or a compatibility rule is defined), and an unrecognized field is never the sole carrier of a payload's meaning. Test the *old-client simulation* against the new payload.

### Anti-Pattern 4: Contract Doc Updated in a Later Diff

- **Appearance:** Code comments say "schema per docs/feature-flags.md", a diff changes the schema (adds the gate-tier field), and the doc update is filed as a follow-up.
- **Trap:** The doc change is "documentation" and feels separable from the code change; the code is what gets reviewed.
- **Consequence:** The doc and the code disagree about what the payload means. When the old/new-client compatibility question (item 4) comes up — often months later during an incident — the doc points at the wrong schema and the investigation starts from a lie.
- **Fix:** Item 7 — the doc is part of the contract; schema/semantics changes and their doc move in the same diff, and reviewers request the doc update before merge.

---

## See Also

- [Configuration Option Registration and Dimension Classification Checklist](../common/config/option-registration-and-dimension.md) — how a flag/option is registered symmetrically across sites and why serialized names are immutable; this harness covers what happens *after* registration, at evaluation/rollout time.
- [Dart Dynamic JSON Boundary Checklist](../dart/json-boundaries.md) — parsing the pushed config payload safely; item 1 (type discrimination) is what makes "malformed flag value" detectable before evaluation.
- [Input Validation Checklist (common)](../common/security/input-validation.md) — the trust-boundary foundation for the payload.
- [Error Handling Strategy Checklist (common)](../common/error-handling/error-handling-strategy.md) — how a rejected payload's error is logged once and how the client communicates the blocked update.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C28] Confluent Schema Registry / Apache Avro Schema Evolution | Schema compatibility across producer/consumer versions; unknown-field and versioning rules | verified-2026 | 2026-09 |
| R2 | A | [A7] Release It! (Nygard) | Stability patterns; keeping last-good state under partial failure | verified-2026 | 2026-09 |
| R3 | A | dev-guidelines engineering experience (lava monorepo dual-diff review) | `_applyConfig` hard-coded `flags['modelCommunity']`; fail-closed cache overwrite → restart drift; eval-semantics upgrade vs old clients; doc/comment contract drift | verified-2026 | 2026-09 |

> **Tier honesty note:** The version/schema compatibility principle (items 1, 6, and the dual-write frame of item 4) is grounded in schema-evolution consensus ([C28]) and is tagged (C). The *operational* rules — last-known-good caching (item 3), generic evaluation loops (item 2), explicit gate tiers (item 5), and doc-sync (item 7) — are distilled from one real incident and carry engineering-experience evidence as (A). The harness tier is (C) because the underlying guarantee (a remote config must never push a client into undefined or drifting behavior) is the fail-closed/versioning consensus; read item-level tags honestly.

---

## Changelog

- 2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)
