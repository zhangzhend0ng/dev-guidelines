---
type: harness
id: "dart-testing"
title: "Dart/Flutter Unit Testing Patterns Checklist"
language: "dart"
category: "testing"
tier: "A"
scope: "Isolate Dart/Flutter unit tests from singletons, static-late injection seams, and platform channels; structure evaluators as static pure functions so decision matrices are directly testable"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-09"
review_cycle: "12m"
tags: [dart, flutter, testing, singletons, platform-channels, mocking, flutter_test]
based_on:
  - "[C] Dart and Flutter Official Documentation (dart.dev / flutter.dev)"
  - "[C] Effective Dart"
  - "[A] dev-guidelines engineering experience (lava monorepo dual-diff review)"
related:
  - "common/testing/testing-strategy.md"
supersedes: []
changelog:
  - "2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)"
---

# Dart/Flutter Unit Testing Patterns Checklist

**Based on:** Dart/Flutter official docs ([C]), Effective Dart ([C]), dev-guidelines engineering experience from the lava monorepo dual-diff review ([A]).
**Scope:** Concrete Dart/Flutter unit-test patterns that sit under `common/testing/testing-strategy.md`: how to make tests order-independent when the code under test uses singletons (`Xxx.instance`), `static late` fields, and platform channels, and how to structure flag/logic evaluation as a static pure function so the full decision matrix is directly testable. This harness is about *unit-test mechanics and seam choices*, not about which tests to write (that is the common testing harness).

---

## Prerequisites / Concepts

| Concept | Definition |
|---------|------------|
| `Xxx.instance` singleton | A process-wide global (`static final ... instance = Xxx._()`). Tests that mutate it leak state into the next test unless reset. |
| `static late` seam | A `static late` field assigned lazily. It is assignable from a test (`Xxx.config = fakeConfig`), which makes it an injection point — but it is still a mutable global and must be restored in `tearDown`. |
| `TestWidgetsFlutterBinding.ensureInitialized()` | Must run before any test touches the binding (widget tests do this in the test body; unit tests that hit platform channels need it before channel mocks are installed). |
| Platform-channel mock | `TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(...)` replaces the platform side of a `MethodChannel`. Plugin packages often wrap this in a convenience setter (e.g. `SharedPreferences.setMockInitialValues`, `PackageInfo.setMockInitialValues`). |
| Static pure-function evaluator | A decision function written as `static` with no instance state and no channel access (inputs in, value out). The entire evaluation matrix is then testable without binding, singletons, or async setup. |

**Guiding idea:** each test must start from a known global state. Every seam a test uses (singleton reset, static field override, channel mock) must be installed *before* the code under test runs and removed/restored *after* it, so the suite is order-independent.

---

## Checklist

### 1. Singleton State Is Reset Between Tests **(C)** [R1]

- [ ] A test exercises a singleton (`Xxx.instance`) that keeps mutable state (caches, session, listeners) → **(C)** reset it to a fresh state in `setUp`, or capture and restore the original in `tearDown`, so no state leaks into the next test. [R1][R3]
- [ ] The suite passes in isolation but fails when run as a whole → **(C)** assume singleton leakage first; find every `instance` field mutated by tests and reset it. [R3]

### 2. Injection Order: Constructor First, `static late` Only as a Last-Resort Seam **(A)** [R2]

- [ ] A dependency can be passed through the constructor → **(A)** prefer constructor/parameter injection over a `static late` field; testability should not require mutating a global. [R2][R3]
- [ ] A `static late` field is used as the injection point for a genuinely unavoidable singleton/config (e.g., a `static late` evaluator configuration) → **(A)** document it as a test seam, assign the fake *before* the code under test runs, and restore the original in `tearDown`. [R3]
- [ ] A `static late` field is read by code that is *not* under this test's control at an unpredictable time → **(A)** do not rely on assignment timing; restructure so the value is passed in, or the field is set in `setUpAll` before anything can read it. [R3]

### 3. Platform-Channel Mocks Are Installed Before Use, With the Binding Initialized **(C)** [R1]

- [ ] Code under test can reach a platform channel (`MethodChannel`, plugin) → **(C)** call `TestWidgetsFlutterBinding.ensureInitialized()` (typically once in `setUpAll`/`main`) *before* installing the mock, and install the mock with `setMockMethodCallHandler` / `setMockInitialValues` *before* invoking the code. [R1]
- [ ] A convenience mock setter exists for the plugin (e.g. `SharedPreferences.setMockInitialValues({...})`, `PackageInfo.setMockInitialValues(...)`) → **(C)** use it instead of hand-rolling `setMockMethodCallHandler`; it keeps the mock in sync with the plugin's channel contract. [R1][R3]
- [ ] A mock handler was registered for a channel → **(C)** remove it in `tearDown` (`setMockMethodCallHandler(null)`) so it cannot leak into the next test. [R1]

```dart
void main() {
  TestWidgetsFlutterBinding.ensureInitialized(); // before any channel mock
  setUp(() {
    SharedPreferences.setMockInitialValues({'theme': 'dark'}); // before use
  });
  tearDown(() {
    // restore the default messenger state for the channel
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(SystemChannels.platform, null);
  });
  test('...', () async { ... });
}
```

### 4. Evaluation Logic Is a Static Pure Function So the Matrix Is Directly Testable **(A)** [R2][R3]

- [ ] Flag/decision logic lives in an instance method that reads singleton or channel state → **(A)** extract the pure part into a `static` function taking the decision inputs as parameters (`FeatureFlags.evaluateFlag(flagName, config, version)`); the instance method becomes a thin wrapper that fetches inputs and calls it. [R3]
- [ ] A decision matrix (flag × version × payload) exists → **(A)** parameterize a test over the whole matrix and assert each expected outcome; with a pure function this needs no binding, no singleton reset, and no async — a full matrix (e.g. 409 cases in the lava review) runs as one fast test. [R3]
- [ ] New inputs are added to a decision later → **(A)** the pure signature and the matrix extend together; a compile error in the test is the signal that a matrix case is missing. [R2][R3]

```dart
// Positive example from the lava review: a 409-case evaluation matrix runs
// directly because evaluation is a static pure function.
class FeatureFlags {
  static bool evaluateFlag({
    required String flagName,
    required Map<String, dynamic> payload,
    required int schemaVersion,
  }) { /* no instance state, no channels — pure decision */ }
}

void main() {
  test('evaluation matrix', () {
    for (final c in _matrix) {           // 409 rows: flag x payload x version
      expect(
        FeatureFlags.evaluateFlag(
            flagName: c.flag, payload: c.payload, schemaVersion: c.version),
        c.expected,
      );
    }
  });
}
```

### 5. Async Tests Complete Deterministically **(C)** [R1]

- [ ] A widget test awaits real asynchronous work (network, isolates, real timers) → **(C)** drive it with `tester.pumpAndSettle()`/fake time, or run it under `tester.runAsync()` when the code genuinely needs real async; never leave pending timers at the end of a test. [R1]
- [ ] A unit test awaits a `Future` that never completes on failure (see the dangling-Completer case) → **(C)** the test will hang — bound the wait (`timeout`) or assert the error path completes; a hanging test suite is itself a bug report. [R1][R3]

### 6. Every Behavior Change Ships With Its Test **(C)** [R1]

- [ ] A diff changes decision, parsing, or state-transition behavior → **(C)** the corresponding matrix/adapter/state test is part of the same change (see review-checklist item 5); a pure-function seam makes this cheap enough to be routine. [R1][R3]

---

## Quick Decision Tree

```
Writing/keeping a Dart unit test
  ├─ code under test touches a singleton?        → reset in setUp, restore in tearDown  [1]
  ├─ dependency injectable via constructor?      → inject; static late only if unavoidable  [2]
  │     └─ static late seam used?                → assign before use, restore after  [2]
  ├─ code can reach a platform channel?          → ensureInitialized + mock before invoke  [3]
  │     └─ convenience setter exists?            → use it; clear handler in tearDown  [3]
  ├─ decision/flag logic buried in instance?     → extract static pure evaluator  [4]
  │     └─ matrix test now direct                → parameterize full matrix  [4]
  ├─ async work in a widget test?                → pumpAndSettle / runAsync; no pending timers  [5]
  └─ behavior changed in this diff?              → ship the matching test in the same change  [6]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: Singleton State Leaking Across Test Cases

- **Appearance:** A suite of tests drives `Session.instance` / `FeatureFlags.instance` (a `static` singleton). The first test logs in and caches state; the second test starts already-logged-in and its assertions about the *initial* state fail. The suite order flips, failures move around.
- **Trap:** Each test reads correctly in isolation. Singletons are convenient and the state "belongs" to the object, so resetting it feels like fighting the design.
- **Consequence:** Order-dependent, flaky suites; a test that passes alone fails in CI, and the team starts blaming test ordering instead of fixing isolation.
- **Fix:** Item 1 — reset every mutated singleton in `setUp` (or capture/restore in `tearDown`), and prefer injecting the stateful object through the constructor so most tests never touch the global (item 2).

### Anti-Pattern 2: Platform Channel Hit Before the Mock Is Installed

- **Appearance:** A test exercises code that calls a plugin (e.g. reading `PackageInfo`) but only calls `setMockInitialValues` *inside* the code path under test, or forgets `TestWidgetsFlutterBinding.ensureInitialized()`. The first run throws `MissingPluginException` (or performs a real platform call on a device).
- **Trap:** The channel call is one level below the assertion, so the test looks like it "almost" works; on a machine with the plugin present it may even pass once and fail on the next run.
- **Consequence:** Flaky or environment-dependent tests, and — when the mock is installed too late — tests that silently exercise the *real* plugin against the host, coupling the suite to the machine it runs on.
- **Fix:** Item 3 — `ensureInitialized()` in `setUpAll`/`main`, convenience mocks installed in `setUp` *before* the code under test is invoked, handlers cleared in `tearDown`.

### Anti-Pattern 3: Decision Logic Buried in an Instance Method (Untestable Matrix)

- **Appearance:** Flag evaluation lives in an instance method that reads `SomeSingleton.instance` and a `static late` config, returning `void` after applying side effects. A "matrix test" has to construct the singleton, set the config, and then inspect applied side effects — so the suite tests only a handful of cases.
- **Trap:** Instance methods are the natural place for logic that "belongs" to an object, and the side effects make the behavior feel integrated and realistic.
- **Consequence:** The evaluation matrix — exactly the code that needs broad parameterized coverage (flag × version × payload) — gets only spot coverage because each case is expensive to set up. The 409-case matrix in the lava review was only possible after extraction.
- **Fix:** Item 4 — extract the pure decision into `static FeatureFlags.evaluateFlag({flagName, payload, schemaVersion})`; the instance path becomes a thin input-fetching wrapper, and the full matrix becomes one fast parameterized test with no binding, singleton reset, or async.

---

## See Also

- [Testing Strategy Checklist (common)](../common/testing/testing-strategy.md) — test classification, pyramid, and mocking policy; this harness is the Dart/Flutter concrete form.
- [Dart Asynchronous Error and Exception Safety Checklist](error-handling.md) — async test determinism (item 5) and the dangling-Completer failure mode that makes tests hang.
- [Dart Dynamic JSON Boundary Checklist](json-boundaries.md) — the parsing matrix this harness's item 4 makes directly testable.
- [Code Review Checklist (common)](../common/code-review/review-checklist.md) — item 5 (every behavior change has a test) is what item 6 here enforces in Dart.

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | [C29] Dart and Flutter Official Documentation | `flutter_test`, `TestWidgetsFlutterBinding`, platform-channel mocking, widget-test async | verified-2026 | 2026-09 |
| R2 | C | [C30] Effective Dart | Testability guidance, prefer explicit parameters over hidden global state | verified-2026 | 2026-09 |
| R3 | A | dev-guidelines engineering experience (lava monorepo dual-diff review) | Singleton leakage, `static late` seams, 409-case `FeatureFlags.evaluateFlag` matrix | verified-2026 | 2026-09 |

> **Tier honesty note:** The binding/channel-mock mechanics (items 1, 3, 5) follow the official Flutter testing documentation and are tagged (C). The seam and structure guidance (items 2 and 4 — injection order, `static late` discipline, static pure-function evaluators) is best practice without a single normative source; those are tagged (A) and the harness tier is (A), matching the strongest *evidence-backed* claim it makes rather than the aspiration.

---

## Changelog

- 2026.09: Initial draft — distilled from lava monorepo dual-diff review (feature-flag fail-closed cache / login state machine / PII log findings)
