---
type: harness
id: "dart-json-boundaries"
title: "Dart Dynamic JSON Boundary Checklist"
language: "dart"
category: "security"
tier: "C"
scope: "Convert untrusted JSON (server/device/pushed config) safely inside a Dart/Flutter app: type-discriminate before casts, respect missing-key vs explicit-null semantics, centralize dual-key transitional lookups, and prevent null pollution of persistent view-model maps"
version: "2026.09.1"
status: "draft"
stable_since: ""
last_validated: "2026-09-10"
review_cycle: "12m"
tags: [dart, flutter, json, dynamic, type-safety, input-validation, serialization, view-model]
based_on:
  - "[C] Dart and Flutter Official Documentation (dart.dev / flutter.dev)"
  - "[C] Effective Dart"
  - "[A] dev-guidelines engineering experience (lava monorepo dual-diff review)"
related:
  - "common/security/input-validation.md"
  - "design/feature-flag-rollout.md"
supersedes: []
changelog:
  - "2026.09.10: Item 4 and anti-pattern 2 refined for numeric-drift accuracy — the decoder maps whole-number JSON payloads to `int` (when they fit) and fractional/out-of-range values to `double`, so a drifted field can be `int`, `double`, or quoted `String`; anti-pattern 2 now distinguishes the two failure shapes (`\"3600\"` breaks both `as num` and `as int`; `3600.5` as `double` breaks `as int` but not `as num`). Matches dart:convert decode semantics."
  - "2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)"
---

# Dart Dynamic JSON Boundary Checklist

**Based on:** Dart/Flutter official docs ([C]), Effective Dart ([C]), dev-guidelines engineering experience from the lava monorepo dual-diff review ([A]).
**Scope:** How `jsonDecode`'s `dynamic` results cross into typed Dart state. This is the Dart landing of `common/security/input-validation.md` for **inbound JSON from a server, device, or pushed remote config** — not for JSON this app serializes itself (that path is under your control). It covers type discrimination before casts, missing-key vs explicit-`null` semantics, the dual-key (camelCase + snake_case) transitional lookup, and null pollution of **persistent** view-model fields that are not rebuilt on every message.

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|------------|
| Trust boundary | A server/device response or pushed config enters the app. `jsonDecode` returns `dynamic`; static type information about the payload is **gone**. |
| `as` cast failure | `value as int` throws a runtime `TypeError` when `value` is not an `int`. A payload field that is `num` today can drift to `String` (or to a different numeric encoding) in a later server version — the cast then throws where no one expected it. |
| `is` type check | `value is num` / `value is int` tests the runtime type and fails closed (branch, don't throw). |
| Missing key vs explicit null | `map[key]` returns `null` for a missing key **and** for a stored `null`. Only `containsKey` distinguishes them. Writing `view[k] = data[k]` when `data` lacks `k` *stores* `null` and destroys the "absent" information. |
| Persistent view-model field | A field on a long-lived view model that is *not* rebuilt from scratch per message — it accumulates/merges across events. A single null-stamping response pollutes it for the rest of the session. |
| Dual-key transition | During a camelCase→snake_case (or reverse) server migration, both spellings of a field exist in the wild. Lookup must try both with one deterministic rule. |

**When this harness applies:** parsing any JSON that arrives over the network/device link, including remote feature-flag configs. **When it does not apply:** `jsonEncode`/`jsonDecode` round-trips of objects this app wrote itself with a locked schema.

---

## Checklist

### 1. Type-Discriminate Before Casting Inbound Values **(C)** [R1][R2]

- [ ] A value from decoded JSON is cast with `as` (`as num`, `as int`, `as String`) → **(C)** replace with an `is`-check (or `tryParse`) that branches on the actual runtime type; if the type is unexpected, treat the field as invalid/absent per the boundary policy. [R2]
- [ ] Downstream type drift is treated as possible (a `num` field becomes a numeric `String`, an `int` becomes a `double`) → **(C)** the conversion handles both, or fails closed with a log — it must not throw a `TypeError` into an unprepared caller. [R1][R3]

```dart
// Good — fails closed on drift, no TypeError.
final raw = decoded['estimated_time'];
if (raw is num) {
  meta.estimatedTime = raw.toInt();
} else if (raw is String) {
  meta.estimatedTime = int.tryParse(raw); // numeric-string drift tolerated
}
// else: log + leave previous value — do not throw here.

// Bad — one server-side change from int to "123" crashes this line.
meta.estimatedTime = decoded['estimated_time'] as int;
```

### 2. Distinguish Missing Key From Explicit Null When Presence Matters **(C)** [R1][R3]

- [ ] Code writes `dest[k] = data[k]` where `data` may lack `k` → **(C)** guard with `containsKey` (or write only non-null values) when "absent" must stay distinguishable from "explicitly null". [R3]
- [ ] A downstream reader uses `containsKey`/`if (field == null) → backfill` semantics on a map you mutate → **(C)** never stamp `null` into that map for a missing source key; the stored null blocks later backfill because the key now *appears* present. [R3]

```dart
// Bad — when data lacks the key, this writes null and marks it "set".
// Later backfill code that checks containsKey sees the key present and stops.
fileMetaData['estimated_time'] = data['estimated_time'];

// Good — absent stays absent; backfill still possible later.
if (data.containsKey('estimated_time')) {
  fileMetaData['estimated_time'] = data['estimated_time'];
}
```

### 3. Persistent View-Model Maps Merge Additively **(A)** [R3]

- [ ] A view-model map/field lives across messages (incremental load, lazy fetch, push updates) and is not rebuilt per event → **(A)** audit the impact scope: every mutation site is a potential long-lived null or stale value; merging logic must write only meaningful updates. [R3]
- [ ] A null write is intended as a deliberate "clear this field" → **(A)** make that explicit (documented sentinel or an explicit remove/clear) so it is not confused with a parsing artifact. [R3]
- [ ] A stale-value risk exists when a later valid payload arrives after an earlier null-stamping one → **(A)** add a regression test that replays "missing-key response, then valid response" and asserts the field reaches the valid value. [R3]

### 4. Numeric JSON Fields Handle int/double/String Forms **(C)** [R1]

- [ ] A numeric field is read with a single cast → **(C)** accept `num` and convert (`toInt()`/`toDouble()`), and decide a policy for numeric strings (`num.tryParse`) — JSON has one number type, and `jsonDecode` maps a whole-number payload to `int` (when it fits) and any fractional or out-of-range value to `double`, so the same field can arrive as `int`, `double`, or (quoted) `String`. [R1][R3]
- [ ] Rounding/truncation semantics for `double`→`int` are chosen deliberately → **(C)** `toInt()` truncates; if the protocol means a whole number, validate, don't silently truncate a drifted fractional value. [R1][R3]

### 5. Dual-Key (camelCase + snake_case) Lookup Is One Centralized Rule **(A)** [R2][R3]

- [ ] Two spellings of the same field must both be read during a migration → **(A)** implement one lookup helper (`readField(map, [camel, snake])` → first *present* key wins) and use it everywhere; do not scatter `a['x'] ?? a['y']` chains across call sites. [R2][R3]
- [ ] Both keys present simultaneously → **(A)** precedence is deterministic and documented (e.g., canonical spelling wins); the helper is covered by a unit test for each spelling and for the both-present case. [R3]

### 6. Cast Sites Are Confined to One Adapter Layer **(C)** [R1][R2]

- [ ] `dynamic`-to-typed conversion happens directly inside business logic → **(C)** confine all unsafe conversion to one parsing/adapter module that returns typed models; consumers never see `dynamic`. [R1][R2]
- [ ] The adapter's outputs are validated (type/range/presence) before use → **(C)** the boundary is the only place that needs an `is`-matrix; drift then surfaces as one testable module instead of scattered `TypeError`s. [R1][R2]

---

## Quick Decision Tree

```
Inbound JSON value (dynamic) about to be used
  ├─ convert with `as`?                → NO — use `is`/tryParse and fail closed  [1][4]
  ├─ copying data[k] into a map?       → does the source lack k? → guard containsKey  [2]
  ├─ map/field outlives one message?   → merge additively; never stamp parsing nulls  [3]
  ├─ two spellings of one field?       → central readField helper, one precedence  [5]
  ├─ conversion inside business code?  → move to adapter; expose typed models  [6]
  └─ all adapters validated?           → yes: boundary complete
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Explicit-Null Write That Blocks Later Backfill

- **Appearance:** `fileMetaData['estimated_time'] = data['estimated_time']` runs on every file-meta update; when `data` lacks the key, the assignment stores `null` in the long-lived `fileMetaData` map.
- **Trap:** The assignment is symmetric and reads fine; `data['estimated_time']` returning `null` for a missing key makes the line look harmless. The map is a persistent view-model field, not rebuilt per message.
- **Consequence:** `fileMetaData` now *contains* `estimated_time` with value `null`. Any downstream "fill if not yet present" logic sees the key present and never backfills — so even after a later valid payload with real data arrives, the field stays null for the rest of the session.
- **Fix:** Item 2 — write only when `data.containsKey('estimated_time')` (or write non-null values only), keeping "absent" distinct from "explicit null"; add a missing-then-valid replay test (item 3).

### Anti-Pattern 2: Trusting `as num` / `as int` on a Drifting Field

- **Appearance:** Server sends `estimated_time: 3600`; client reads `data['estimated_time'] as num` (or `as int`) and feeds it to the UI.
- **Trap:** The payload is correct today; the cast documents intent and the code passes against the current server. Nobody expects the field type to change.
- **Consequence:** A later server/device version sends `"3600"` (a numeric string) or `3600.5` for the same semantic field. `"3600"` makes **both** `as num` and `as int` throw a runtime `TypeError`; `3600.5` decodes as `double`, which `as int` rejects (a `double` is not an `int`) even though `as num` would accept it. Either drift fails at a read site nobody expected to break; if the read is inside an update handler with no guard, the whole update path dies — or worse, a partial update leaves the view model half-populated.
- **Fix:** Items 1 and 4 — `is num`/`is String` discrimination with a fail-closed branch (log + keep previous value), confined to the adapter layer (item 6) so the drift is caught in one testable module.

### Anti-Pattern 3: Scattered Ad-Hoc Dual-Key `??` Chains

- **Appearance:** During a snake_case migration, each read site writes its own `json['estimatedTime'] ?? json['estimated_time']` (or the reverse order at a different site).
- **Trap:** Each site handles "both spellings" and the migration seems covered. Two sites disagree on precedence (which spelling wins), and the chain also *swallows the difference* between a missing key and a stored null.
- **Consequence:** The same logical field resolves to different values at different call sites, and a future canonical-spelling change requires editing every scattered chain — some of which are missed. The `??` also collapses "explicit null" into "missing", re-introducing the item-2 bug.
- **Fix:** Item 5 — one `readField(map, [camel, snake])` helper (first *present* key wins, documented precedence), unit-tested per spelling and for the both-present and explicit-null cases.

---

## See Also

- [Input Validation Checklist (common)](../common/security/input-validation.md) — the trust-boundary foundation this harness instantiates in Dart; item 4 (type and range) is the general rule behind items 1 and 4 here.
- [Remote Feature-Flag Evaluation and Rollout Checklist](../design/feature-flag-rollout.md) — a pushed remote config is exactly the inbound-JSON case in this harness; its fail-closed evaluation depends on the type-discrimination rules here.
- [Python Input Deserialization Checklist](../python/security/input-deserialization.md) — the Python concrete form of the same boundary concern.
- [C++ Parsing and Validation Checklist](../cpp/serialization/parsing-and-validation.md) — parsing untrusted serialized input safely in C++.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C29] Dart and Flutter Official Documentation | JSON support, `dynamic`, runtime type checks, `TypeError` semantics of `as` | verified-2026 | 2026-09 |
| R2 | C | [C30] Effective Dart | Avoid unchecked casts; prefer type tests / explicit conversion | verified-2026 | 2026-09 |
| R3 | A | dev-guidelines engineering experience (lava monorepo dual-diff review) | `estimated_time` null-stamping/backfill blocking; persistent view-model pollution | verified-2026 | 2026-09 |

> **Tier honesty note:** The type-checking and cast mechanics (items 1, 4, 6) are grounded in the Dart language/Effective Dart and are tagged (C). The map-semantics rules (items 2, 3) and the dual-key pattern (item 5) are strongly informed by one real incident (explicit-null write blocking backfill in a persistent view model) and carry (A) evidence; the harness stays (C) because the underlying principle — validate all input at a trust boundary and never corrupt durable state with a parsing artifact — is the input-validation consensus this repo already treats as normative.

---

## Changelog

- 2026.09.10: Item 4 and anti-pattern 2 refined for numeric-drift accuracy — the decoder maps whole-number JSON payloads to `int` (when they fit) and fractional/out-of-range values to `double`, so a drifted field can be `int`, `double`, or quoted `String`; anti-pattern 2 now distinguishes the two failure shapes (`"3600"` breaks both `as num` and `as int`; `3600.5` as `double` breaks `as int` but not `as num`). Matches dart:convert decode semantics.
- 2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)
