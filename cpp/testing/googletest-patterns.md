---
type: harness
id: "cpp-googletest"
title: "GoogleTest and GMock Patterns Checklist"
language: "cpp"
category: "testing"
tier: "C"
scope: "Write idiomatic, maintainable GoogleTest tests using test fixtures, parameterized tests, typed tests, death tests, and GMock expectations"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [googletest, gmock, testing, cpp, unit-tests]
based_on:
  - "[C] GoogleTest Official Documentation"
  - "[A] xUnit Test Patterns (Meszaros, 2007)"
  - "[A] SWE at Google Ch.11 (Winters, 2020)"
related:
  - "common/testing/test-doubles.md"
  - "common/testing/testing-strategy.md"
  - "cpp/testing/catch2-patterns.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# GoogleTest and GMock Patterns Checklist

**Based on:** GoogleTest Official Documentation ([C]), xUnit Test Patterns ([A]), SWE at Google Ch.11 ([A]).
**Scope:** Idiomatic GoogleTest and GMock tests. Complements `common/testing/testing-strategy.md` with GoogleTest-specific patterns. Use this for C++ codebases built on GoogleTest; for Catch2 projects see `cpp/testing/catch2-patterns.md`.

---

## Concepts

| Feature | Purpose |
|---------|---------|
| `TEST(Suite, Name)` | Basic test definition; Suite groups related tests |
| `TEST_F(Fixture, Name)` | Test that inherits from a fixture class; SetUp/TearDown run before/after each test |
| `TEST_P(Fixture, Name)` | Value-parameterized test; instantiated with `INSTANTIATE_TEST_SUITE_P` |
| `ASSERT_*` | Fatal assertion -- aborts current test function on failure |
| `EXPECT_*` | Non-fatal assertion -- records failure but continues execution |
| `SetUp()` / `TearDown()` | Per-test initialization and cleanup (virtual, called before/after each TEST_F) |
| `GetParam()` | Access the current parameter value inside a TEST_P body |
| `TYPED_TEST_SUITE` / `TYPED_TEST` | Type-parameterized tests; instantiate a test over a list of concrete types |
| `ASSERT_DEATH` / `ASSERT_EXIT` | Death tests -- verify that a statement causes program termination |
| `EXPECT_CALL` | GMock expectation -- define expected calls, arguments, and actions on mock objects |
| `Times(n)` / `AtLeast(n)` | GMock cardinalities -- how many times a mocked method is expected to be called |
| `SCOPED_TRACE` | Add context to assertion failure messages (lazy evaluation) |
| `--gtest_filter` | Runtime test selection with glob patterns |

---

## Checklist

### 1. TEST / TEST_F / TEST_P Naming  **(C)** [R1][R2]

GoogleTest uses a two-part name: `SuiteName` and `TestName`. The suite groups related tests; the test name describes a specific behavior. Good naming makes test failures self-documenting and enables precise `--gtest_filter` targeting.

- [ ] SuiteName is the class or module under test → **(C)** [R1]
- [ ] TestName describes the behavior or scenario, not implementation details → **(C)** [R2]
- [ ] TEST(Suite, Name) for standalone tests with no shared setup → **(C)** [R1]
- [ ] TEST_F(FixtureClass, Name) when shared setup is needed; Suite = fixture class name → **(C)** [R1]
- [ ] TEST_P(FixtureClass, Name) for value-parameterized tests → **(C)** [R1]
- [ ] Suite names are consistent within a test file (typically one primary suite per file) → **(A)** [R2]

```cpp
// Good -- suite groups related behavior; test name describes scenario
TEST(VectorTest, EmptyVectorReturnsZeroSize) {
    std::vector<int> v;
    EXPECT_EQ(v.size(), 0u);
}

TEST(VectorTest, PushBackIncreasesSize) {
    std::vector<int> v;
    v.push_back(42);
    EXPECT_EQ(v.size(), 1u);
}

// Bad -- test name describes implementation, not behavior
TEST(VectorTest, test_push_back) { /* ... */ }
TEST(VectorTest, test_size)      { /* ... */ }
```

---

### 2. ASSERT_* vs EXPECT_*  **(C)** [R1][R3]

GoogleTest provides two assertion families. `ASSERT_*` is fatal: it aborts the current test function immediately (returns from the function). `EXPECT_*` is non-fatal: it records the failure and continues executing. This is directly analogous to Catch2's `REQUIRE` vs `CHECK`.

- [ ] Use `EXPECT_*` for independent observations -- gather more failures per run → **(C)** [R1]
- [ ] Use `ASSERT_*` when subsequent code depends on the assertion passing (e.g., pointer not null before dereference) → **(C)** [R1]
- [ ] Use `ASSERT_NO_FATAL_FAILURE(statement)` to wrap a subroutine that may call `ASSERT_*` → **(C)** [R1]
- [ ] Do not put `ASSERT_*` in non-void functions with return values -- use `EXPECT_*` and return → **(C)** [R1]
- [ ] Prefer `ASSERT_THAT(value, matcher)` over raw `ASSERT_TRUE(condition)` for better failure messages → **(A)** [R1]

```cpp
// Good -- ASSERT for precondition, EXPECT for independent observations
auto* conn = pool->AcquireConnection();
ASSERT_NE(conn, nullptr);       // Must pass -- dereferencing below
EXPECT_TRUE(conn->IsOpen());    // Observe without aborting
EXPECT_GT(conn->LatencyMs(), 0); // Another independent check

// Bad -- all ASSERT hides independent failures
ASSERT_NE(conn, nullptr);
ASSERT_TRUE(conn->IsOpen());    // If this fails, LatencyMs never checked
ASSERT_GT(conn->LatencyMs(), 0);
```

---

### 3. Test Fixtures: SetUp/TearDown vs Constructor/Destructor  **(C)** [R1][R2]

A test fixture class provides shared setup for multiple tests. GoogleTest constructs the fixture, calls `SetUp()`, runs the test body, calls `TearDown()`, then destroys the fixture. Understanding the ordering is critical for correct resource handling.

- [ ] Prefer `SetUp()` over constructor for test-specific initialization → **(C)** [R1]
- [ ] Use `TearDown()` for cleanup that may need to inspect test state or call virtual methods → **(C)** [R1]
- [ ] Constructor may be used for const member initialization; destructor for RAII cleanup → **(A)** [R1]
- [ ] Keep fixtures focused -- one responsibility per fixture; split large fixtures → **(C)** [R2]
- [ ] Do not suppress exceptions in `TearDown()` -- let them propagate to fail the test → **(C)** [R1]
- [ ] `SetUp()` / `TearDown()` run per-test; expensive one-time setup belongs in `SetUpTestSuite()` / `TearDownTestSuite()` (static) → **(C)** [R1]

```cpp
// Good -- SetUp initializes test state; TearDown cleans up
class DatabaseTest : public ::testing::Test {
protected:
    void SetUp() override {
        db_ = std::make_unique<TestDatabase>();
        db_->Connect();
        db_->CreateTestSchema();
    }

    void TearDown() override {
        db_->DropTestSchema();
        db_->Disconnect();
    }

    std::unique_ptr<TestDatabase> db_;
};

TEST_F(DatabaseTest, InsertReturnsRowId) {
    auto id = db_->Insert("users", {{"name", "alice"}});
    EXPECT_GT(id, 0);
}

// Bad -- putting everything in constructor makes debugging harder
class BadFixture : public ::testing::Test {
protected:
    BadFixture() {
        // Exception here produces cryptic "constructor threw" message
        // SetUp() failure messages are clearer
    }
};
```

---

### 4. Value-Parameterized Tests  **(C)** [R1]

Value-parameterized tests (`TEST_P`) let you run the same test logic with multiple input values. Each parameter combination produces an independently reported test case. This replaces hand-written loops that abort on the first failure.

- [ ] Use `TEST_P` when the same assertions apply to many input values → **(C)** [R1]
- [ ] Name `INSTANTIATE_TEST_SUITE_P` prefix to describe the parameter set (e.g., `PositiveNumbers`, `EdgeCases`) → **(C)** [R1]
- [ ] Use `testing::Values(v1, v2, ...)` for small explicit sets → **(C)** [R1]
- [ ] Use `testing::ValuesIn(container)` for data from a vector/array → **(C)** [R1]
- [ ] Use `testing::Combine(g1, g2)` for Cartesian product of parameter sets → **(C)** [R1]
- [ ] Use `testing::Range(begin, end, step)` for numeric ranges → **(A)** [R1]
- [ ] Each parameterization is an independent test -- one failure does not block other values → **(C)** [R1]

```cpp
// Good -- each value is an independent test run
class IsPrimeTest : public ::testing::TestWithParam<int> {};

TEST_P(IsPrimeTest, ReturnsTrueForPrimes) {
    EXPECT_TRUE(IsPrime(GetParam()));
}

INSTANTIATE_TEST_SUITE_P(Primes, IsPrimeTest,
                         ::testing::Values(2, 3, 5, 7, 11, 13, 17, 19));

INSTANTIATE_TEST_SUITE_P(NonPrimes, IsPrimeTest,
                         ::testing::Values(0, 1, 4, 6, 8, 9, 10));

// Bad -- hand-written loop aborts on first failure
TEST(PrimeTest, TestMany) {
    for (int n : {2, 3, 5, 7, 11}) {
        ASSERT_TRUE(IsPrime(n)); // Failure here skips remaining values
    }
}
```

---

### 5. Typed Tests  **(C)** [R1]

Typed tests verify that a template or generic interface behaves correctly for every type in a type list. Each concrete type produces an independently reported test.

- [ ] Use `TYPED_TEST_SUITE` when a template must satisfy the same contract across multiple types → **(C)** [R1]
- [ ] Use `TypeParam` to reference the type under test inside the test body → **(C)** [R1]
- [ ] Use `TYPED_TEST_SUITE_P` + `REGISTER_TYPED_TEST_SUITE_P` + `INSTANTIATE_TYPED_TEST_SUITE_P` when the type list is defined in a different translation unit or you need type-parameterized fixture state → **(C)** [R1]
- [ ] Each type is an independent test -- type-specific failures are clearly identified → **(C)** [R1]
- [ ] Combine with operator tests: verify commutativity, associativity, identity for arithmetic types → **(C)** [R1]

```cpp
// Good -- TYPED_TEST verifies container contract for all types
template <typename T>
class ContainerTest : public ::testing::Test {};

using ContainerTypes = ::testing::Types<
    std::vector<int>, std::list<int>, std::deque<int>>;
TYPED_TEST_SUITE(ContainerTest, ContainerTypes);

TYPED_TEST(ContainerTest, DefaultConstructedIsEmpty) {
    TypeParam c;
    EXPECT_TRUE(c.empty());
}

TYPED_TEST(ContainerTest, PushBackIncreasesSize) {
    TypeParam c;
    c.push_back(1);
    EXPECT_EQ(c.size(), 1u);
}

// Bad -- copy-pasting the same test for each type
TEST(VectorTest, Empty) { EXPECT_TRUE(std::vector<int>{}.empty()); }
TEST(ListTest,   Empty) { EXPECT_TRUE(std::list<int>{}.empty()); }
TEST(DequeTest,  Empty) { EXPECT_TRUE(std::deque<int>{}.empty()); }
```

---

### 6. Death Tests  **(C)** [R1]

Death tests verify that a statement causes program termination (crash, abort, or exit). They run the statement in a subprocess, so they are significantly more expensive than normal assertions. Use them sparingly for safety-critical invariants.

- [ ] Use `ASSERT_DEATH(statement, regex)` for statements expected to crash or abort → **(C)** [R1]
- [ ] Use `ASSERT_EXIT(statement, predicate, regex)` to also check the exit code → **(C)** [R1]
- [ ] Use `ASSERT_DEBUG_DEATH` for invariants only enforced in debug mode (e.g., `assert()`) → **(A)** [R1]
- [ ] Death test expression must be simple -- avoid complex lambdas or thread-spawning → **(C)** [R1]
- [ ] Prefer non-death assertions when possible; each death test forks a subprocess → **(C)** [R1]
- [ ] Do not use death tests for error paths that can be tested with normal assertions → **(C)** [R1]
- [ ] Regex matches stderr output; use `.*` generously or literal substrings → **(A)** [R1]

```cpp
// Good -- death test for an invariant that should abort
TEST(PreconditionTest, DiesOnNullPointer) {
    ASSERT_DEATH(Dereference(nullptr), "precondition.*failed");
}

TEST(ExitTest, ExitsWithCodeOnFatalError) {
    ASSERT_EXIT(FatalShutdown(), ::testing::ExitedWithCode(1), "fatal error");
}

// Bad -- using death test for an error path with a normal return
// Just test the error code instead.
TEST(ErrorTest, DiesOnInvalidInput) {
    ASSERT_DEATH(ParseOrDie("garbage"), ""); // ParseOrDie could return an error
}
```

---

### 7. GMock Expectations: EXPECT_CALL, Matchers, and Cardinalities  **(C)** [R1][R3]

GMock provides a declarative mocking framework. `EXPECT_CALL` sets expectations on mock objects: which methods are called, with what arguments, how many times, and what they return. All expectations are verified when the mock object is destroyed.

- [ ] Use `EXPECT_CALL(mock, Method(args))` to declare expected calls → **(C)** [R1]
- [ ] Use matchers for argument matching: `_` (wildcard), `Eq(v)`, `Ne(v)`, `Lt(v)`, `Gt(v)`, `HasSubstr(s)`, `Contains(e)`, `IsNull()`, `NotNull()` → **(C)** [R1]
- [ ] Specify cardinality: `Times(n)`, `AtLeast(n)`, `AtMost(n)`, `Between(m, n)` → **(C)** [R1]
- [ ] Use `.WillOnce(action)` for sequenced return values; `.WillRepeatedly(action)` for the rest → **(C)** [R1]
- [ ] Use `ON_CALL` for default (stub) behavior; `EXPECT_CALL` only when the call is required → **(C)** [R1]
- [ ] Prefer `NiceMock<T>` for stubs (ignores uninteresting calls); `StrictMock<T>` only when you must verify every call → **(C)** [R1]
- [ ] Return references with `.WillOnce(ReturnRef(ref))` -- do not return temporaries → **(C)** [R1]
- [ ] Compose matchers: `AllOf(m1, m2, m3)`, `AnyOf(m1, m2)`, `Not(m)` → **(A)** [R1]
- [ ] Mock only at architectural boundaries (I/O, network, external services) -- never mock value objects or the SUT's own types → **(C)** [R3]

```cpp
// Good -- EXPECT_CALL with matchers and cardinality controls
class MockClock : public Clock {
public:
    MOCK_METHOD(std::chrono::system_clock::time_point, Now, (), (const, override));
};

TEST(OrderTest, ExpiresAfterTimeout) {
    NiceMock<MockClock> clock;
    EXPECT_CALL(clock, Now())
        .Times(AtLeast(1))
        .WillOnce(Return(Jan_1_2020))
        .WillRepeatedly(Return(Jan_1_2020 + 1h));

    Order order(&clock);
    ASSERT_FALSE(order.IsExpired());
}

// Bad -- over-specifying with StrictMock makes tests brittle
StrictMock<MockClock> clock; // Fails if any call is not explicitly expected
// Prefer NiceMock unless you must verify every interaction
```

---

### 8. SCOPED_TRACE for Failure Context  **(C)** [R1]

`SCOPED_TRACE` attaches a message to all assertion failures within its scope. It is essential for loops and helper functions where the failing line number alone does not identify which iteration or context caused the failure.

- [ ] Use `SCOPED_TRACE` inside loops to report the iteration index/value on failure → **(C)** [R1]
- [ ] Use `SCOPED_TRACE` in helper/subroutine functions called from multiple tests → **(C)** [R1]
- [ ] Stream message: `SCOPED_TRACE("key: " << key << ", index: " << i)` → **(C)** [R1]
- [ ] Multiple `SCOPED_TRACE` are allowed -- output is printed LIFO (last pushed, first shown) → **(A)** [R1]
- [ ] `SCOPED_TRACE` is lazy: the message is only formatted if an assertion fails → **(C)** [R1]

```cpp
// Good -- SCOPED_TRACE identifies which iteration failed
void VerifyUser(const User& user) {
    SCOPED_TRACE("User: " + user.name());
    EXPECT_GT(user.age(), 0);
    EXPECT_FALSE(user.email().empty());
}

TEST(UserValidationTest, AllUsersValid) {
    std::vector<User> users = LoadUsers();
    for (size_t i = 0; i < users.size(); ++i) {
        SCOPED_TRACE("index: " + std::to_string(i));
        VerifyUser(users[i]);
    }
    // Failure output shows: index: 3 -> User: bob -> age > 0 failed
}

// Bad -- loop without SCOPED_TRACE gives no context
TEST(UserValidationTest, AllUsersValid_Bad) {
    for (const auto& user : LoadUsers()) {
        EXPECT_GT(user.age(), 0); // Which user failed? Unknown.
    }
}
```

---

### 9. Test Discovery and Filtering  **(C)** [R1]

GoogleTest provides runtime flags to select, repeat, shuffle, and configure tests without recompilation. These are essential for CI workflows, flaky-test investigation, and developer productivity.

- [ ] Use `--gtest_filter=Suite.Test` to run a specific test (glob patterns supported) → **(C)** [R1]
- [ ] Use `--gtest_filter=Suite.*` to run all tests in a suite → **(C)** [R1]
- [ ] Use `--gtest_filter=*-Suite.Test` (negative pattern) to exclude specific tests → **(C)** [R1]
- [ ] Use `--gtest_repeat=N` to run tests N times for flaky detection → **(C)** [R1]
- [ ] Use `--gtest_shuffle` with `--gtest_random_seed` to detect order dependencies → **(C)** [R1]
- [ ] Use `--gtest_list_tests` to enumerate all tests without running them → **(A)** [R1]
- [ ] Use `--gtest_output=xml:report.xml` for CI test reporting → **(C)** [R1]
- [ ] Use the `DISABLED_` prefix to skip a test (preferred over commenting out); CI runs `--gtest_also_run_disabled_tests` periodically → **(C)** [R1]
- [ ] Document the project's filter conventions for CI (e.g., `--gtest_filter=-*Slow*:*Integration*` for fast PR checks) → **(C)** [R1]

```bash
# Run all tests in the VectorTest suite
./my_test --gtest_filter=VectorTest.*

# Run everything except slow and integration tests (common CI fast path)
./my_test --gtest_filter=-*Slow*:*Integration*

# Repeat 100 times to check for flakes
./my_test --gtest_repeat=100 --gtest_break_on_failure

# Shuffle to detect order-dependency bugs
./my_test --gtest_shuffle --gtest_random_seed=42
```

```cpp
// Good -- DISABLED_ prefix keeps test in source, visible to tooling
TEST(VectorTest, DISABLED_ResizeRegressionBug123) {
    // Known issue -- tracked in JIRA-123
}

// Bad -- commented-out test silently bitrots
// TEST(VectorTest, ResizeRegressionBug123) {
//     // Nobody remembers why this is here
// }
```

---

## Decision Tree

```
New GoogleTest needed?
  ├─ No shared setup → TEST(Suite, Name) [1]
  ├─ Shared setup needed → TEST_F(Fixture, Name) [3]
  │    ├─ SetUp() for test initialization
  │    ├─ TearDown() for cleanup
  │    └─ One-time setup → SetUpTestSuite() (static)
  ├─ Same logic, many values → TEST_P + INSTANTIATE_TEST_SUITE_P [4]
  ├─ Same logic, many types → TYPED_TEST_SUITE + TYPED_TEST [5]
  ├─ Expects crash/abort → ASSERT_DEATH / ASSERT_EXIT [6]
  └─ ASSERT_* vs EXPECT_* decision [2]:
       ├─ Subsequent code depends on result? → ASSERT_*
       └─ Independent observation? → EXPECT_*

Adding a mock?
  ├─ Default behavior only → ON_CALL in NiceMock [7]
  └─ Required call → EXPECT_CALL with matchers + cardinality [7]

Need failure context? → SCOPED_TRACE in loops/helpers [8]

CI and filtering? → --gtest_filter for selection, --gtest_repeat for flakes [9]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: ASSERT_* for Everything

- **Appearance:** Every assertion uses `ASSERT_*`; the test aborts at the first failure.
- **Trap:** `ASSERT_*` feels "safer" because it stops immediately on invalid state.
- **Consequence:** One failure hides all others. Debugging requires N fix-and-rerun cycles for N independent bugs.
- **Fix:** Use `EXPECT_*` for independent observations. Reserve `ASSERT_*` for preconditions where subsequent code literally cannot execute (null pointer dereference, out-of-bounds access).

### Anti-Pattern 2: Commented-Out Tests Instead of DISABLED_

- **Appearance:** `// TEST(Suite, Name) { ... }` or `#if 0 ... #endif` around test blocks with no tracking or issue reference.
- **Trap:** Commenting out is quick and suppresses the failing test in CI.
- **Consequence:** Tests silently bitrot. The code drifts away from the test expectations. Six months later the commented-out test does not compile. There is no record of why it was disabled.
- **Fix:** Use `DISABLED_` prefix: `TEST(Suite, DISABLED_Name)`. The test is compiled, visible in `--gtest_list_tests`, and can be run explicitly. Schedule periodic `--gtest_also_run_disabled_tests` runs to prevent drift.

### Anti-Pattern 3: Over-Mocking with GMock

- **Appearance:** Every dependency is mocked, including value objects, standard library types, and sibling classes within the same module. Tests use `StrictMock` everywhere.
- **Trap:** "Isolation" is interpreted as mocking all types except the method under test. GMock makes this easy.
- **Consequence:** Tests verify mock behavior, not real behavior. A refactoring that changes an internal helper breaks dozens of tests that should not care. The test suite gives false confidence.
- **Fix:** Mock only architectural boundaries: I/O, network, clock, external services. Use real instances for in-process collaborators. Prefer `NiceMock` for stubs; use `StrictMock` only when every interaction must be verified.

---

## See Also

- [Testing Strategy](../../common/testing/testing-strategy.md) -- Test sizes, pyramid proportions, mocking rules, flaky test management
- [Catch2 Testing Patterns](catch2-patterns.md) -- Framework-specific patterns for Catch2 (analogous constructs)

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | C | GoogleTest Official Documentation | v1.14 -- assertions, fixtures, parameterized tests, death tests, GMock | verified-2026 | 2026-06 |
| R2 | A | xUnit Test Patterns (Meszaros) | Test organization, fixtures, naming, test discovery | verified-2026 | 2026-06 |
| R3 | A | SWE at Google Ch.11 (Winters) | Testing practices, mocking strategy | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
