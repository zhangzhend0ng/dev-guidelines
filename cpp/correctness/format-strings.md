---
type: harness
id: "cpp-format-strings"
title: "Format Strings and Variadic API Call Checklist"
language: "cpp"
category: "correctness"
tier: "C"
scope: "Review printf-style variadic API calls for literal format strings, specifier/argument type and count agreement, and silent extra-argument misuse"
version: "2026.09"
status: "draft"
stable_since: ""
last_validated: "2026-09-30"
review_cycle: "12m"
tags: [format-string, printf, variadic, security, imgui, logging]
based_on:
  - "[N] ISO C++ [support.c] — ISO C 7.21.6.1 fprintf conversions (invalid spec / missing argument = UB)"
  - "[C] SEI CERT C Coding Standard FIO47-C — valid format strings"
  - "[A] dev-guidelines snapmaker-orca commit distillation (2026-08-31, commit 76ee70bec8)"
  - "[A] fmtlib / std::format documentation — compile-time format checking"
related:
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/security/secure-coding.md"
  - "common/logging/logging-standards.md"
  - "common/code-review/review-checklist.md"
supersedes: []
changelog:
  - "2026.09: Initial draft — distilled from snapmaker-orca commit 76ee70bec8 (ImGui::Text runtime format string with silently swallowed ImVec2 argument). Closes the orphan finding in docs/reviews/snapmaker-orca-commit-distillation-2026-08-31.md."
---

# Format Strings and Variadic API Call Checklist

**Based on:** ISO C++ [support.c] ([N]), SEI CERT C FIO47-C ([C]), snapmaker-orca commit distillation ([A]), fmtlib/std::format ([A]).
**Scope:** Calls to printf-family and printf-style variadic APIs (`printf`/`snprintf`, `wxPrintf`/`wxString::Printf`, `ImGui::Text`, log macros with format args). Does NOT cover iostream/`std::format` type safety (use them instead — Item 6) or general string building.

---

## Prerequisites / Concepts

Variadic tails have **no overload resolution and no argument checking**: everything after the format argument is interpreted solely by the format string at runtime. Two failure classes follow:

| Failure | Detected by compiler? | Consequence |
|---------|----------------------|-------------|
| Invalid conversion spec / argument type mismatch / missing argument | No (until `-Wformat` warns on literals) | Undefined behavior |
| Extra argument the callee never consumes | No — silently swallowed | Misuse signal: often a "layout/style" argument meant for a different API |

Real case (snapmaker-orca commit 76ee70bec8): `ImGui::Text(runtime_icon_string, ImVec2{...})` — the icon string was passed as the format, and the layout `ImVec2` was silently consumed by `vsnprintf` as an unused variadic. No compile error; a `%` inside the icon string would misrender (and a user-controlled string would be a format-string injection).

---

## Checklist

### 1. Format Argument Is a Literal  **(C)** [R2]

- [ ] Format argument is a string literal (or otherwise `-Wformat`-analyzable) → OK [R2]
- [ ] Runtime string passed as the format → **(C)** change to `Text("%s", s)`-style; a `%` in the data misrenders, user-controlled data is a format-string injection vector. [R2]

```cpp
// Good — data as argument, literal format
ImGui::Text("%s", icon.c_str());

// Bad — runtime string as format; '%'-bearing icons misrender
ImGui::Text(icon.c_str());
```

### 2. Specifiers Match Argument Types  **(N)** [R1]

- [ ] Every conversion spec matches the promoted argument type (`%s` ↔ `char*`, `%lld` ↔ `long long`, ...) → **(N)** invalid spec or wrong type is UB [R1]
- [ ] Wrapper types passed to a `%s`-family spec (`wxString`, `QString`, `std::string`, `ImVec2`) → **(N)** convert explicitly first (`.utf8_str()`, `.toStdString()`, `.c_str()`); a non-`char*` under `%s` is UB, and objects decay silently in variadic position. [R1]

### 3. Argument Count Matches Consumption  **(N)/(A)** [R1][R3]

- [ ] Fewer arguments than specs → **(N)** UB — must fix [R1]
- [ ] More arguments than specs → **(A)** treat as an API-misuse signal: the callee is variadic so the extra argument is silently swallowed; almost always the caller confused two APIs (e.g. passing a layout `ImVec2` to `ImGui::Text`). [R3]

### 4. Callee Is Actually the Intended API  **(A)** [R3]

- [ ] Passing "layout/style/config" arguments to a text function → **(A)** verify the callee signature is genuinely printf-style variadic; layout arguments belong to a different overload/function (`ImGui::Text` has no `ImVec2` overload — use `ImGui::SetCursorPos`/window sizing). [R3]

### 5. No `%n`, No External Format Strings  **(C)** [R2]

- [ ] Format string reachable from external/config input contains `%n` → **(C)** remove; `%n` writes to memory and is disabled/hardened on modern targets [R2]
- [ ] Format string assembled at runtime from user/config data → **(C)** pass data as arguments instead. [R2]

### 6. Prefer Compile-Time-Checked Formatting for New Code  **(A)** [R4]

- [ ] New code formats with `std::format`/`fmt::format`/spdlog's fmt syntax (type-checked at compile time) → OK; new raw printf-style call sites without a platform constraint → **(A)** prefer the type-checked alternative. [R4]

---

## Quick Decision Tree

```
printf-style call site
  ├─ format argument is a runtime string? → "%s"-style rewrite (Item 1, 5)
  ├─ wrapper type under %s/%ls? → explicit conversion (Item 2)
  ├─ argument count ≠ spec count?
  │    ├─ fewer → UB, fix (Item 3)
  │    └─ extra  → API confusion signal, re-check callee signature (Item 3, 4)
  └─ new call site? → prefer std::format/fmt (Item 6)
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: The Silently Swallowed Argument

- **Appearance:** `ImGui::Text(label, ImVec2{w, h})` — compiles, runs, "looks fine".
- **Trap:** Variadic tails accept anything; `vsnprintf` ignores unconsumed arguments without a diagnostic.
- **Consequence:** Layout argument has no effect; a `%` in `label` misrenders or becomes an injection.
- **Fix:** Route layout through the API that consumes it; pass text via `"%s"`. [R3]

### Anti-Pattern 2: Runtime String as Format

- **Appearance:** `printf(msg)`, `wxPrintf(status_text)`.
- **Trap:** Works until the data contains `%`.
- **Consequence:** Misrendered output; user-controlled data → format-string injection (memory read/`%n` write on hardened-off targets).
- **Fix:** `printf("%s", msg.c_str())`. [R2]

---

## See Also

- [Undefined Behavior Prevention](undefined-behavior.md) — UB class for invalid specs and type mismatches
- [C++ Secure Coding](../security/secure-coding.md) — injection class where format strings come from input
- [Logging Standards](../../common/logging/logging-standards.md) — log macros are printf-style call sites too
- [Code Review Checklist](../../common/code-review/review-checklist.md) — dimension-level review entry point

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO/IEC 14882 (C++ Standard) | [support.c]: ISO C 7.21.6.1 fprintf — invalid conversion spec, missing argument, or `%s` with non-`char*` = UB | verified-2026 | 2026-09 |
| R2 | C | SEI CERT C Coding Standard | FIO47-C — use valid format strings; no external format strings | verified-2026 | 2026-09 |
| R3 | A | dev-guidelines engineering experience (snapmaker-orca commit distillation 2026-08-31, commit 76ee70bec8) | `ImGui::Text` runtime format string; `ImVec2` argument silently swallowed by `vsnprintf` | verified-2026 | 2026-09 |
| R4 | A | fmtlib / ISO C++ `std::format` documentation | Compile-time format-string checking | verified-2026 | 2026-09 |

---

## Changelog

- 2026.09: Initial draft — distilled from snapmaker-orca commit 76ee70bec8.
