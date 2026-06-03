---
type: harness
id: "cpp-catch2"
title: "Catch2 Testing Patterns Checklist"
language: "cpp"
category: "testing"
tier: "C"
scope: "Write idiomatic, maintainable Catch2 tests using SECTION, matchers, generators, and BDD macros"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [catch2, testing, cpp, unit-tests, bdd]
based_on:
  - "[C] Catch2 Official Documentation v3.x"
  - "[C] C++ Core Guidelines CP.1-CP.50 — Concurrency rules"
  - "[A] xUnit Test Patterns (Meszaros, 2007)"
  - "[A] SWE at Google Ch.11 — Testing (2020)"
related:
  - "common/testing/testing-strategy.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Catch2 Testing Patterns Checklist

**Based on:** Catch2 Docs v3.x ([C]), C++ Core Guidelines CP ([C]), xUnit Test Patterns ([A]), SWE at Google Ch.11 ([A]).
**Scope:** Idiomatic Catch2 tests. Complements `common/testing/testing-strategy.md` with Catch2-specific patterns.

---

## Concepts

| Feature | Purpose |
|---------|---------|
| `TEST_CASE` + `SECTION` | Tree-structured; each SECTION fresh from root |
| `REQUIRE` vs `CHECK` | REQUIRE aborts; CHECK continues |
| `SCENARIO` / `GIVEN` / `WHEN` / `THEN` | BDD-style structure |
| `GENERATE` | Data-driven input generation |
| `TEMPLATE_TEST_CASE` | Instantiate for multiple types |
| `Matchers` | Composable, readable assertions |
| `BENCHMARK` | Microbenchmark in test framework |
| Tags `[tag]` | Runtime test filtering |

---

## Checklist

### 1. TEST_CASE Naming  **(C)** [R1][R2]

- [ ] Name describes behavior, not implementation → **(C)** [R1]
- [ ] ✅ `"Factorial of 0 returns 1"` — ❌ `"test_factorial_zero"` → **(C)** [R2]

```cpp
// Good — behavior-described
TEST_CASE("Factorial of 0 returns 1") { /* ... */ }
// Bad — implementation-described
TEST_CASE("test_factorial") { /* ... */ }
```

### 2. SECTION Over Nested Setup  **(C)** [R1][R3]

- [ ] SECTION tree for shared setup with variant behavior → **(C)** [R1]
- [ ] Each leaf SECTION re-executes all parent setup → **(C)** [R1]
- [ ] Never manually call setup before SECTION — use the tree → **(C)** [R3]

```cpp
// Good — every SECTION gets a fresh Stack<int>
TEST_CASE("Stack operations") {
    Stack<int> s;
    SECTION("empty stack") { REQUIRE(s.empty()); }
    SECTION("push then top") { s.push(1); REQUIRE(s.top() == 1); }
}
```

### 3. REQUIRE vs CHECK  **(C)** [R1]

- [ ] REQUIRE for preconditions (subsequent code depends on this) → **(C)** [R1]
- [ ] CHECK for independent observations (gather more failures) → **(C)** [R1]
- [ ] REQUIRE_THROWS_AS for expected exception type → **(C)** [R1]

```cpp
auto ptr = get_resource();
REQUIRE(ptr != nullptr);      // Must pass — dereferencing below
CHECK(ptr->name() == "test"); // Observe without aborting
```

### 4. BDD-Style Macros  **(A)** [R1]

- [ ] SCENARIO for user-facing behavior → **(A)** [R1]
- [ ] GIVEN/WHEN/THEN document state→action→assertion → **(A)** [R1]
- [ ] BDD for integration/acceptance; classic TEST_CASE for unit → **(A)** [R1]

```cpp
SCENARIO("User logs in with valid credentials") {
    GIVEN("a registered user") {
        User user{"alice", "pass"};
        WHEN("correct password provided") {
            THEN("login succeeds") { REQUIRE(user.login("pass")); }
        }
    }
}
```

### 5. Matchers Over Raw Assertions  **(C)** [R1]

- [ ] `REQUIRE_THAT(value, Matcher)` for composable checks → **(C)** [R1]
- [ ] `WithinAbs`, `Contains`, `StartsWith`, `Matches` for built-in → **(C)** [R1]
- [ ] Custom matcher when assertion used 3+ times → **(A)** [R1]
- [ ] Matcher description explains what was expected → **(C)** [R1]

```cpp
REQUIRE_THAT(result, WithinAbs(3.14, 0.01));
REQUIRE_THAT(log, Contains("error") && StartsWith("[ERR]"));
```

### 6. Data-Driven Testing  **(C)** [R1]

- [ ] GENERATE for input combinations (each creates independent run) → **(C)** [R1]
- [ ] TEMPLATE_TEST_CASE for type-generic tests → **(C)** [R1]
- [ ] SECTION + GENERATE combines combinatorial paths → **(C)** [R1]

```cpp
auto a = GENERATE(1, 2, 5, 100);
auto b = GENERATE(0, 1, 7);
REQUIRE(a * b == b * a); // 4 x 3 = 12 runs

TEMPLATE_TEST_CASE("Clear empties container", "[container]",
                   std::vector<int>, std::list<int>) {
    TestType c{1, 2, 3};
    c.clear();
    REQUIRE(c.empty());
}
```

### 7. Tag-Based Filtering  **(C)** [R1]

- [ ] Tags on every test: `[unit]`, `[integration]`, `[slow]`, `[component]` → **(C)** [R1]
- [ ] CI: `[!slow]` for PR, `[slow]` for nightly → **(C)** [R1]
- [ ] Tag conventions documented in project CONTRIBUTING → **(C)** [R1]

### 8. Benchmarking  **(A)** [R1]

- [ ] BENCHMARK for microbenchmarks → **(A)** [R1]
- [ ] Flag regressions >20% from baseline → **(C)** [R1]
- [ ] Run on dedicated hardware, not shared CI → **(C)** [R1]

### 9. Fixture and Lifecycle  **(C)** [R1][R3]

- [ ] Prefer SECTION tree over setUp/tearDown → **(C)** [R1]
- [ ] Locals in TEST_CASE body; destructors on scope exit → **(C)** [R1]
- [ ] Shared expensive setup → Catch2 templated fixture → **(A)** [R3]

---

## Decision Tree

```
New Catch2 test?
  → Behavior-named TEST_CASE [1]
  → SECTION tree for shared setup [2]
  → REQUIRE for preconditions; CHECK for observations [3]
  → User-facing? → BDD SCENARIO [4]
  → Complex assertion? → Matchers [5]
  → Multiple inputs? → GENERATE [6]
  → Multiple types? → TEMPLATE_TEST_CASE [6]
  → Tag [unit]/[integration]/[slow] [7]
  → Microbenchmark? → BENCHMARK [8]
  → Expensive shared state? → fixture [9]
```

---

## Anti-Patterns

### 1. REQUIRE for Everything

- **Appearance:** All assertions use REQUIRE; test stops at first failure.
- **Trap:** REQUIRE is "safer" — stops on bad state.
- **Consequence:** One failure hides all others. N CI runs to find N independent bugs.
- **Fix:** CHECK for independent observations. REQUIRE only when code downstream depends on it passing.

### 2. Manual Loop Instead of GENERATE

- **Appearance:** `for (int x : {1,2,3}) { SECTION(...) { ... } }`.
- **Trap:** Familiar for-loop; works.
- **Consequence:** First failure aborts loop — other values untested.
- **Fix:** `GENERATE(values...)`. Each value is an independent run.

### 3. Commented-Out Tests

- **Appearance:** `// TEST_CASE("broken") { ... }` with no tracking.
- **Trap:** Quick way to silence flaky/unfinished tests.
- **Consequence:** Tests silently bitrot. Six months later they don't compile.
- **Fix:** `[!mayfail]` for known-flaky. `[.]` (hidden) for WIP. Both visible to tooling.

---

## See Also

- [Testing Strategy](../../common/testing/testing-strategy.md) — Test sizes, pyramid, mock rules
- [Undefined Behavior](../correctness/undefined-behavior.md) — UB testing with sanitizers

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | Catch2 Official Documentation | v3.x — assertions, sections, generators | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | CP.1-CP.50 | verified-2026 | 2026-06 |
| R3 | A | xUnit Test Patterns (Meszaros) | Test organization, fixtures | verified-2026 | 2026-06 |
| R4 | A | SWE at Google Ch.11 (Winters) | Testing practices | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
