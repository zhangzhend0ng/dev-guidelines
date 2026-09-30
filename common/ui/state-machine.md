---
type: harness
id: "common-ui-state-machine"
title: "UI State Machine and Event Re-entry Checklist"
language: "common"
category: "correctness"
tier: "A"
scope: "Review UI state transitions for re-entry safety, one-shot flag staleness, guard-path side effects, consumer-entry-point sync, and mutate-then-notify ordering"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-30"
review_cycle: "12m"
tags: [ui, state-machine, reentry, one-shot-flag, mode-switch, event-handling, guards]
based_on:
  - "[A] dev-guidelines snapmaker-orca commit distillation (2026-08-31) — UI state machine cluster (commits e60059ac74, 73d5b2a170, b63ab9afb9, 9490f113e5, 6a2c0715ae)"
related:
  - "common/config/option-registration-and-dimension.md"
supersedes: []
changelog:
  - "2026.09: Initial draft — distilled from the UI state machine cluster (5 findings) of docs/reviews/snapmaker-orca-commit-distillation-2026-08-31.md; the largest orphan family in that batch."
---

# UI State Machine and Event Re-entry Checklist

**Based on:** snapmaker-orca commit distillation, UI state machine cluster ([A]).
**Scope:** State kept by UI layers (modes, dialogs, panels, flags) and the event paths that enter, re-enter, or leave them. Covers: initialization vs re-entry, guard-path visible-state effects, one-shot flags, consumer entry-point sync for state conditions, and mutate-then-notify ordering. Does NOT cover widget look-and-feel, layout/DPI (see `cpp/third-party/wxwidgets-3-1-5.md` for wx), threading/marshaling (see `cpp/concurrency/thread-safety.md`), or backend state machines with no user-visible surface.

---

## Prerequisites / Concepts

UI code rarely has an explicit state machine diagram, but it always has one: each mode/page/dialog is a state, each event handler is a transition. The defect cluster behind this harness is not exotic — every case is a transition written against the *happy first pass* and broken by a *second arrival*:

| Re-entry shape | What breaks | Evidence commit |
|----------------|-------------|-----------------|
| User re-enters a mode/dialog in the same session | Re-initialization overwrites their adjustments | e60059ac74 |
| The same event fires twice (re-drop, reload) | Guard returns silently, stranding the view | 73d5b2a170 |
| Reload/reconnect after a once-only action | One-shot flag suppresses a needed repeat | b63ab9afb9 |
| A state condition gains a new consumer | Only one entry point wired; gate doesn't gate | 9490f113e5 |
| Notification/persistence racing the mutation | UI shows stale state; archive diverges from memory | 6a2c0715ae |

---

## Checklist

### 1. First-Entry vs Re-Entry Initialization

Initialization code that reads "set up this mode" is usually written for the first entry. Re-entry (switching back to a mode, reopening a dialog in the same session) runs it again and silently replaces state the user has since modified.

- [ ] Initialization/backfill code executes on *every* entry to a mode/page/dialog? → **(A)** Split first-entry initialization from re-entry: gate with a session-scoped flag, or make re-entry rebuild only derived view artifacts (legends, tables, layouts) — never user-adjusted state (weights, selections, edits). [R1]
- [ ] A mode switch resets state the user can observe and modify, without an explicit reset action by the user? → **(A)** Persist user-adjusted state across mode switches within the session; resets happen only on explicit user action. [R1]

```cpp
// Bad — every re-entry overwrites the user's weights with defaults
void on_mode_changed(Mode m) {
    m_weights = default_weights_for(m);        // user edits gone
    rebuild_legend();
}

// Good — first entry initializes; re-entry rebuilds only the view artifact
void on_mode_changed(Mode m) {
    if (m_match_state_persisted) { rebuild_legend(); return; }
    m_weights = default_weights_for(m);
    m_match_state_persisted = true;
    rebuild_legend();
}
```

### 2. Guard Paths Must Not Strand Visible State

Early-return guards are reviewed for what they skip, rarely for what the user *sees* afterwards. Two failures pair up: the UI is switched before the content that justifies the switch is known, and the guard then returns without restoring anything — the user is left somewhere they did not choose, with no feedback.

- [ ] A guard early-returns without restoring the caller-visible end state (active view/tab, progress indicator, selection)? → **(A)** Guard paths own the end state: explicitly restore the previous view or present feedback (message, status). A silent return is a state transition the user never chose. [R1]
- [ ] UI state switched before the condition that justifies it is known (e.g., selecting a tab before inspecting the dropped/opened content)? → **(A)** Defer the transition to the decision point; never commit view changes speculatively. [R1]

```cpp
// Bad — unconditional tab switch, then same-file guard returns silently
on_drop(files) {
    select_tab(View3D);                        // flash even in preview-only mode
    if (same_file_already_loaded(files)) return;  // stranded on empty 3D view
    ...
}

// Good — switch only when justified; guard restores the meaningful view
on_drop(files) {
    if (!only_gcode_mode()) select_tab(View3D);
    if (same_file_already_loaded(files)) { select_tab(Preview); redraw(); return; }
    ...
}
```

### 3. One-Shot Flags vs Re-Entry Events

`m_xxx_sent` / `m_done` flags record "already did X once" — but X's trigger can recur (reload, reconnect, re-create, retry), and the flag then suppresses a repetition that has become necessary.

- [ ] A boolean one-shot flag gates an action whose triggering event can recur (page reload, reconnect, retry, object recreation)? → **(A)** Audit the flag against *every* re-entry event: either reset it there, or delete the once-guard in favor of an idempotent action (doing it twice is safe). [R1]
- [ ] "Do once" chosen to avoid duplicate side effects, when the action itself could be made idempotent (dedupe marker on the receiving side, overwrite-not-append)? → **(A)** Prefer idempotency over a remember-flag: idempotent actions survive every re-entry shape without bookkeeping. [R1]

```cpp
// Bad — reload never re-injects; page silently loses auth
if (m_apikey_sent || m_apikey.IsEmpty()) return;
inject_api_key(); m_apikey_sent = true;

// Good — idempotent per load; receiver dedupes
if (m_apikey.IsEmpty()) return;
inject_api_key();   // JS side: mark-and-skip keeps repeats safe
```

### 4. New Condition → Sweep All Consumer Entry Points

A validation/gate/state condition is only as enforced as its *weakest consumer*. Wiring the condition into the logic that computes it, but not into every entry point that acts on the state, produces gates that don't gate.

- [ ] A new validation, compatibility, or state condition added? → **(A)** Enumerate every consumer entry point — button enable/disable, notifications/status panels, batch or plate-wide paths, keyboard shortcuts, timers — and wire each; grep the state's *readers* as the checklist of sites, not just its writers. [R1]
- [ ] A state-changing action applied only to the current view/plate/tab while sibling instances rely on the same state? → **(A)** Synchronize all instances on the change, or derive per-instance state at consumption time instead of caching one instance's copy. [R1]

Same discipline as `common/config/option-registration-and-dimension.md` ("every registration site must be touched"), applied to UI state instead of config options: a condition with unwired consumers is a registration gap.

### 5. Mutate, Then Notify — and Write Back

UI notifications fired in the middle of a mutation render pre-mutation state. In-memory collection changes that are never serialized back leave the persistent store (project file, archive, config) diverged from memory — the divergence surfaces later as deleted items reappearing or stale loads.

- [ ] UI refresh/notification issued before the data mutation it announces completes? → **(A)** Order is: mutate data fully → write back to persistent form → notify UI. Notify-then-mutate is always wrong. [R1]
- [ ] A collection changed in memory (add/delete/reorder) whose serialized form (project entry, config key, archive blob) is not updated in the same operation? → **(A)** Serialize the write-back at the mutation site; an in-memory/persistent split must not survive past the handler that created it. [R1]

```cpp
// Bad — UI notified before deletion; archive never updated
on_filaments_change(current_count);
remove_mixed_filaments(list);

// Good — mutate, write back, then notify
remove_mixed_filaments(list);
if (auto* opt = config.option<ConfigOptionString>("mixed_filament_definitions"))
    opt->value = serializer.serialize_custom_entries();
on_filaments_change(effective_size);
```

---

## Decision Tree

```
UI change review:
  ├─ Mode / page / dialog entry code?
  │     ├─ Runs initialization on every entry? → [Item 1] first-entry vs re-entry split
  │     └─ Resets observable user state? → [Item 1] persist within session
  ├─ Early-return guard / drop / load handler?
  │     ├─ Silent return after a UI transition? → [Item 2] restore end state or feed back
  │     └─ UI switched before content is known? → [Item 2] defer the transition
  ├─ Boolean once-only flag (m_*_sent/done)?
  │     └─ Trigger event can recur? → [Item 3] reset on re-entry, or make the action idempotent
  ├─ New validation / compatibility / state condition?
  │     └─ → [Item 4] enumerate consumers: enables, notifications, batch paths, shortcuts
  └─ Data change feeding UI + persistence?
        └─ → [Item 5] mutate → write back → notify
```

---

## Anti-Patterns / Common Mistakes

### 1. "Init Is Idempotent, So Just Re-run It"

- **Appearance:** Mode-switch handler calls the same `init()` used at construction.
- **Trap:** Re-running init from *defaults* is not re-running it on *the same inputs* — the user has edited state since.
- **Consequence:** Silent loss of user adjustments; reported as "my settings reset themselves."
- **Fix:** Item 1 — split first-entry initialization from re-entry; only derived artifacts may rebuild.

### 2. "The Guard Is Just One Return"

- **Appearance:** `if (already_loaded) return;` looks self-evidently correct.
- **Trap:** The review eye checks the predicate, not the view state the caller is left in.
- **Consequence:** Users stranded on the wrong page/tab with no feedback; bug reports say "UI jumps around."
- **Fix:** Item 2 — every guard return either restores the meaningful end state or explains itself to the user.

### 3. "I Wired the Main Button"

- **Appearance:** New gate condition checked in the primary action's handler.
- **Trap:** Secondary consumers (button *enable*, notifications, batch/sibling paths) are separate code paths that nobody greps for.
- **Consequence:** Gate exists but doesn't gate — the action stays enabled, or half the UI disagrees with the other half.
- **Fix:** Item 4 — sweep readers of the state, not just the primary consumer.

---

## See Also

- [Configuration Option Registration](../config/option-registration-and-dimension.md) — the same "every consumer/registration site" sweep discipline for config options
- [wxWidgets 3.1.5 Pitfalls](../../cpp/third-party/wxwidgets-3-1-5.md) — framework-level UI traps (DIP/physical pixels, wxString temporaries)
- [Thread Safety](../../cpp/concurrency/thread-safety.md) — marshaling UI updates from worker threads

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | dev-guidelines snapmaker-orca commit distillation report | `docs/reviews/snapmaker-orca-commit-distillation-2026-08-31.md` (commits e60059ac74 #602, 73d5b2a170 #732, b63ab9afb9 #679, 9490f113e5 #543, 6a2c0715ae #554) | verified-2026 | 2026-08 |

---

## Changelog

- 2026.09: Initial draft — 5 items (first-entry vs re-entry init, guard-path visible state, one-shot flags, consumer sweep, mutate-notify-writeback) distilled from the snapmaker-orca UI state machine cluster.
