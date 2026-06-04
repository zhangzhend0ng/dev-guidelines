---
type: harness
id: "common-test-doubles"
title: "Test Doubles Taxonomy and Selection Checklist"
language: "common"
category: "testing"
tier: "C"
scope: "Classify test doubles per the Meszaros taxonomy and choose the correct type for each dependency based on cost-vs-fidelity trade-offs"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [testing, test-doubles, mocking, stubs, fakes, meszaros]
based_on:
  - "[A] xUnit Test Patterns (Meszaros, 2007)"
  - "[A] Mocks Aren't Stubs (Fowler, 2007)"
  - "[C] Google Testing Blog"
related:
  - "common/testing/testing-strategy.md"
  - "cpp/testing/catch2-patterns.md"
  - "cpp/testing/googletest-patterns.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Test Doubles Taxonomy and Selection Checklist

**Based on:** xUnit Test Patterns (Meszaros, 2007) ([A]), Mocks Aren't Stubs (Fowler, 2007) ([A]), Google Testing Blog ([C]).
**Scope:** Classify test doubles according to the Meszaros taxonomy and select the correct type per dependency. Language-agnostic; framework-specific patterns (Catch2, GoogleTest/GMock) are covered in the language harnesses.

---

## Concepts

| Double | Purpose | Has Behavior? | Self-Verifying? | Example |
|--------|---------|---------------|-----------------|---------|
| **Dummy** | Fill parameter slots; never used by the SUT | No | No | `nullptr` passed to satisfy a signature |
| **Stub** | Return canned answers to indirect inputs | Yes (return values) | No | `clock.Now()` always returns `Jan_1_2020` |
| **Spy** | Record calls for later assertions | Yes (record + return) | No (asserted manually) | `EmailSenderSpy.sent_emails()` returns list of sent emails |
| **Mock** | Pre-programmed expectations; self-verifying | Yes (expectations) | Yes (verifies on destruction) | GMock `EXPECT_CALL(service, Send).Times(1)` |
| **Fake** | Working but simplified implementation | Yes (real logic) | No (asserted against) | In-memory SQLite instead of PostgreSQL |

**Fidelity spectrum** (left to right: increasing fidelity and maintenance cost): Dummy < Stub < Spy < Mock. Fakes sit parallel: high fidelity with real logic, but not configurable like Stubs/Mocks.

---

## Checklist

### 1. Dummy -- Parameter Placeholder  **(C)** [R1]

A Dummy is an object passed to the SUT solely to satisfy a parameter list. The SUT never calls any method on it. Dummies have no behavior and require no verification.

- [ ] Parameter is required by the interface but the SUT never invokes it in this test scenario → use a Dummy → **(C)** [R1]
- [ ] Preferred Dummy: `nullptr` for pointer/reference parameters → **(C)** [R1]
- [ ] For non-nullable parameters: a default-constructed instance that will never be touched → **(C)** [R1]
- [ ] Do not use a Stub or Mock when a Dummy suffices -- it adds maintenance cost with zero benefit → **(C)** [R1]
- [ ] Naming convention: suffix with `Dummy` or pass inline with a comment `// dummy` → **(A)** [R1]

```cpp
// Good -- Dummy logger fills a parameter slot; SUT never logs in this test
TEST(CalculatorTest, AddDoesNotLog) {
    LoggerDummy logger;          // Never called
    Calculator calc(&logger);    // Satisfies constructor parameter
    EXPECT_EQ(calc.Add(2, 3), 5);
}

// Good -- nullptr as Dummy for pointer parameter
TEST(ParserTest, ParseEmptyDoesNotUseReporter) {
    auto result = Parser::Parse("", /*reporter=*/nullptr);
    EXPECT_TRUE(result.empty());
}

// Bad -- Full mock used where Dummy would suffice
TEST(CalculatorTest, AddDoesNotLog_Overkill) {
    StrictMock<MockLogger> logger; // Never called; StrictMock will fail if SUT is refactored
    Calculator calc(&logger);
    EXPECT_EQ(calc.Add(2, 3), 5);
}
```

---

### 2. Stub -- Canned Answers  **(C)** [R1][R2]

A Stub provides predetermined responses to indirect inputs (method calls from the SUT). The SUT calls the stub as part of its normal execution and acts on the returned values. Stubs have no verification -- the test does not assert that the stub was called, only that the SUT behaved correctly given the stub's responses.

- [ ] SUT depends on return values from a collaborator → provide canned answers via a Stub → **(C)** [R1]
- [ ] Stub returns are configurable: `when(method).thenReturn(value)` / `ON_CALL(...).WillByDefault(Return(...))` → **(C)** [R1]
- [ ] Stub should return values that drive the code path under test (happy path, error path, edge case) → **(C)** [R1]
- [ ] Do NOT assert that a Stub was called -- that transforms it into a Mock → **(C)** [R2]
- [ ] Naming: suffix with `Stub` or use framework stub facilities (e.g., `NiceMock<T>`) → **(A)** [R1]
- [ ] Prefer Stubs over Mocks for queries (methods that return data without side effects) → **(C)** [R2]

```cpp
// Good -- Stub provides canned response; test verifies SUT behavior, not stub calls
TEST(OrderTest, ExpiresAfterTimeout) {
    ClockStub clock;
    clock.SetNow(Jan_1_2020);                    // Canned answer: always Jan 1
    Order order(&clock);
    ASSERT_FALSE(order.IsExpired());
    clock.SetNow(Jan_1_2020 + 1h);               // Move clock forward
    ASSERT_TRUE(order.IsExpired());
    // No assertion on how many times clock.Now() was called -- that is a stub
}

// Bad -- asserting on stub calls turns it into a mock; tests become brittle
TEST(OrderTest, ExpiresAfterTimeout_Brittle) {
    ClockStub clock;
    EXPECT_CALL(clock, Now())                     // Stub with mock expectations
        .Times(Exactly(2));                       // Refactoring SUT internals breaks this
    Order order(&clock);
    order.IsExpired();
}
```

---

### 3. Spy -- Call Recording  **(C)** [R1]

A Spy records the calls made to it so that the test can inspect them afterward. Unlike a Mock, a Spy does not fail automatically -- the test writes explicit assertions against the recorded data. Spies are useful when the SUT's interaction pattern is complex or the side effect must be inspected after the fact.

- [ ] Need to verify that the SUT made specific calls AND the call count/order is nontrivial → use a Spy → **(C)** [R1]
- [ ] Spy records: method name, arguments, call count, call order → **(C)** [R1]
- [ ] Assert on recorded calls AFTER exercising the SUT (arrange-act-assert; spy inspection is the "assert") → **(C)** [R1]
- [ ] Prefer Spy over Mock when: the same collaborator is called in multiple test scenarios with different expectations → **(C)** [R1]
- [ ] Spy can be a hand-rolled class that accumulates calls in a `std::vector` → **(C)** [R1]
- [ ] Naming: suffix with `Spy` → **(A)** [R1]

```cpp
// Good -- Spy records sent emails; test inspects after SUT execution
class EmailSenderSpy : public EmailSender {
public:
    void Send(const Email& email) override {
        sent_.push_back(email);
    }
    const std::vector<Email>& sent() const { return sent_; }
    size_t count() const { return sent_.size(); }
private:
    std::vector<Email> sent_;
};

TEST(NotifierTest, SendsEmailToAllSubscribers) {
    EmailSenderSpy spy;
    Notifier notifier(&spy);
    notifier.Notify({Subscriber{"alice"}, Subscriber{"bob"}});
    EXPECT_EQ(spy.count(), 2u);
    EXPECT_EQ(spy.sent()[0].to(), "alice");
    EXPECT_EQ(spy.sent()[1].to(), "bob");
}

// Bad -- Spy that verifies internally is a Mock in disguise
class BadSpy : public EmailSender {
public:
    void Send(const Email& e) override {
        if (++count_ > 1) abort(); // Self-verifying: defeats spy purpose
    }
};
```

---

### 4. Mock -- Pre-Programmed Expectations  **(C)** [R1][R2]

A Mock is pre-programmed with expectations about which calls will be made, with what arguments, in what order, and how many times. The Mock self-verifies: when the mock object is destroyed, it checks that all expected calls occurred. Mocks are the highest-fidelity double but also the most tightly coupled to the SUT's internal implementation.

- [ ] Need to verify that the SUT makes specific calls with specific arguments → use a Mock → **(C)** [R1]
- [ ] Expectations declared BEFORE exercising the SUT (arrange → EXPECT_CALL → act → mock auto-verifies) → **(C)** [R1]
- [ ] Specify cardinality: exactly N times (`Times(N)`), at least N (`AtLeast(N)`), optional (`WillRepeatedly`) → **(C)** [R1]
- [ ] Use loose matchers where the exact value does not matter: `_` (wildcard), `NotNull()`, `Gt(0)` → **(C)** [R1]
- [ ] Prefer `NiceMock<T>` when most calls are not verified; `StrictMock<T>` only when every call must be accounted for → **(C)** [R1]
- [ ] Mock only architectural boundaries (I/O, network, clock, external services) → **(C)** [R2]
- [ ] A test with 3+ mocks is a design smell -- the SUT may have too many collaborators → **(C)** [R1]
- [ ] Mocks verify behavior (commands); Stubs provide state (queries) -- Fowler's classic distinction → **(C)** [R2]

```cpp
// Good -- Mock verifies required interaction at an architectural boundary
TEST(PaymentProcessorTest, ChargesOnValidOrder) {
    NiceMock<MockPaymentGateway> gateway;       // NiceMock: uninteresting calls ignored
    EXPECT_CALL(gateway, Charge(               // Expectation: Charge MUST be called
        "cust_123",                             // Exact match for customer
        ::testing::DoubleEq(99.99)))            // Exact match for amount
        .Times(1)                               // Exactly once
        .WillOnce(Return(PaymentResult::Ok));   // Canned response for the SUT

    PaymentProcessor processor(&gateway);
    auto result = processor.Process(ValidOrder()); // Act
    EXPECT_EQ(result, ProcessorResult::Success);    // Also verify SUT output
    // Mock auto-verifies Charge() was called on destruction
}

// Bad -- Mocking a value object (tight coupling to implementation)
StrictMock<MockEmailAddress> email;             // Value object, not an architectural boundary
EXPECT_CALL(email, domain()).Times(1);          // Refactoring EmailAddress breaks this test
```

---

### 5. Fake -- Working Simplified Implementation  **(C)** [R1]

A Fake is a lightweight but fully functional implementation of a dependency. Unlike Stubs and Mocks, a Fake has real business logic -- it just trades fidelity for speed, determinism, or test isolation. Fakes are shared across tests and can accumulate state.

- [ ] Dependency has complex state or behavior that cannot be adequately captured by canned answers → use a Fake → **(C)** [R1]
- [ ] Classic Fakes: in-memory database, fake filesystem, fake clock, fake network → **(C)** [R1]
- [ ] Fake must implement the SAME interface/contract as the real dependency → **(C)** [R1]
- [ ] Document the fidelity gap: what does the Fake NOT do that the real dependency does? → **(C)** [R1]
- [ ] Fake should be reusable across test suites; invest effort proportional to usage → **(C)** [R1]
- [ ] Test the Fake itself -- a buggy Fake creates false positives/negatives across all tests that use it → **(C)** [R1]
- [ ] Naming: suffix with `Fake` (e.g., `FakeDatabase`, `FakeFileSystem`) → **(A)** [R1]

```cpp
// Good -- FakeDatabase implements the full Database interface with in-memory storage
class FakeDatabase : public Database {
public:
    Result Insert(std::string_view table, const Row& row) override {
        auto id = next_id_++;
        tables_[std::string(table)].emplace(id, row);
        return Result::Ok(id);
    }
    std::optional<Row> Find(std::string_view table, int64_t id) override {
        auto t = tables_.find(std::string(table));
        if (t == tables_.end()) return std::nullopt;
        auto it = t->second.find(id);
        return it != t->second.end() ? std::optional(it->second) : std::nullopt;
    }
    // Full interface; documented gap: no transactions, no foreign key enforcement
private:
    int64_t next_id_ = 1;
    std::unordered_map<std::string, std::unordered_map<int64_t, Row>> tables_;
};

TEST(UserRepoTest, InsertAndFind) {
    FakeDatabase db;                                   // Fast, deterministic, no Postgres needed
    UserRepo repo(&db);
    auto id = repo.CreateUser("alice");
    auto user = repo.FindUser(id);
    ASSERT_TRUE(user.has_value());
    EXPECT_EQ(user->name, "alice");
}

// Bad -- Fake with behavior that diverges from the real contract
class BrokenFakeDatabase : public Database {
    // Find() returns random results for "realism" -- breaks determinism
    // Missing half the interface -- returns default values instead of errors
};
```

---

### 6. Selecting the Right Double  **(C)** [R1][R2]

Each double type exists on a spectrum of fidelity vs. maintenance cost. Choosing correctly reduces test brittleness while maintaining sufficient confidence.

| Factor | Dummy | Stub | Spy | Mock | Fake |
|--------|-------|------|-----|------|------|
| **Fidelity** | None | Low | Medium | High | High |
| **Coupling to SUT internals** | None | Low | Medium | High | Low |
| **Maintenance cost** | None | Low | Medium | High | Medium |
| **Setup complexity** | None | Low | Low | High | Medium |
| **Reusability** | N/A | Per-test | Per-test | Per-test | Cross-suite |

- [ ] SUT never calls the dependency in this scenario → Dummy → **(C)** [R1]
- [ ] SUT needs return values; call verification is irrelevant → Stub → **(C)** [R1]
- [ ] SUT produces a side effect that must be inspected → Spy → **(C)** [R1]
- [ ] SUT must call a specific method with specific arguments; this IS the contract → Mock → **(C)** [R2]
- [ ] Dependency has complex state/behavior; canned answers are insufficient → Fake → **(C)** [R1]
- [ ] Favor real objects over any double for in-process, fast, deterministic dependencies → **(C)** [R2]
- [ ] Prefer Stubs over Mocks for queries; Mocks over Stubs for commands → **(C)** [R2]
- [ ] When in doubt, go one fidelity level LOWER -- it is easier to upgrade than to recover from over-mocking → **(A)** [R1]

---

### 7. Over-Mocking Guard  **(C)** [R1][R2][R3]

Over-mocking is the most prevalent test double misuse. It produces a test suite that is tightly coupled to implementation details, brittle under refactoring, and gives false confidence.

- [ ] Mock only at architectural boundaries: I/O, network, clock, external services → **(C)** [R2]
- [ ] Never mock value objects, DTOs, standard library types, or the SUT's own types → **(C)** [R2]
- [ ] Never mock types you do not own (3rd-party libs) without an adapter layer → **(C)** [R1]
- [ ] A test that has 3+ mocks → examine whether the SUT has too many responsibilities → **(C)** [R1]
- [ ] A mock whose expectations change every time the SUT implementation changes → the mock is at the wrong abstraction level → **(C)** [R3]
- [ ] Tests that pass with mock expectations satisfied but fail in integration → the mock hid a contract violation → **(C)** [R3]
- [ ] Prefer real instances + Fakes for in-process dependencies; save Mocks for out-of-process boundaries → **(C)** [R2]

```cpp
// Good -- Mock only the payment gateway (architectural boundary); real objects in-process
TEST(OrderProcessorTest, ChargesOnCheckout) {
    NiceMock<MockPaymentGateway> gateway;    // Architectural boundary: external service
    TaxCalculator real_tax;                  // In-process: fast, deterministic
    Inventory real_inventory;                // In-process: fast, deterministic
    OrderProcessor processor(&gateway, &real_tax, &real_inventory);
    // ...
}

// Bad -- Everything mocked: value objects, sibling classes, std::string
TEST(OrderProcessorTest_OverMocked, ChargesOnCheckout) {
    StrictMock<MockPaymentGateway> gateway;
    StrictMock<MockTaxCalculator> tax;       // In-process class -- should be real
    StrictMock<MockInventory> inventory;     // In-process class -- should be real
    StrictMock<MockOrder> order;             // Value object -- should be real
    StrictMock<MockAddress> address;         // Value object -- should be real
    // 5 mocks in one test: design and testing smell
}
```

---

## Decision Tree

```
SUT has a dependency. Choose the right double:

  SUT never calls the dependency in this test scenario?
    └─ Yes → Dummy [1]

  SUT needs return values from the dependency?
    ├─ Simple canned values suffice → Stub [2]
    └─ Dependency has complex state/behavior → Fake [5]

  SUT produces a side effect you must verify?
    ├─ Inspect after the fact → Spy [3]
    └─ Verify call contract (method, args, count) → Mock [4]

  Dependency is in-process, fast, deterministic?
    └─ Use the real object. Do not double it. [6]

Fidelity selection [6]:
  Dummy < Stub < Spy < Mock
  Fakes sit parallel: high fidelity but real logic (not configurable)

Over-mocking guard [7]:
  Mock only architectural boundaries.
  3+ mocks in one test? → Refactor SUT or downgrade some mocks.
```

---

## Anti-Patterns

### 1. Stub Doing Verification

- **Appearance:** A Stub is created with `when().thenReturn()`, then the test also asserts `verify(stub).called()`.
- **Trap:** "I want to be sure the SUT used my canned value."
- **Consequence:** The stub becomes a mock. Tests couple to internal call patterns. Refactoring the SUT to call the dependency fewer/more times breaks tests that should not care.
- **Fix:** If call verification matters, use a Mock. Otherwise, trust that the SUT's output proves it used the right inputs -- behavior verification, not interaction verification.

### 2. Mock Without Architectural Boundary

- **Appearance:** Every class in the SUT's module has a corresponding Mock, including value objects and internal helpers.
- **Trap:** "Full isolation means mocking everything except the method under test."
- **Consequence:** Tests verify mock behavior, not real behavior. A refactoring that changes an internal helper breaks dozens of tests. The test suite becomes a barrier to change instead of a safety net.
- **Fix:** Mock only architectural boundaries (I/O, network, clock, external services). Use real objects for in-process dependencies. If a class is hard to use in tests without mocking, that is a design smell -- the class may need a better interface.

### 3. Fake Diverging From Real Contract

- **Appearance:** `FakeDatabase` returns `Result::Ok` for every insert but the real database enforces unique constraints.
- **Trap:** "It is just a fake; it does not need to be complete."
- **Consequence:** Tests pass with the Fake but fail in production. The Fake creates false confidence. The fidelity gap is undocumented.
- **Fix:** Document the Fake's fidelity gap explicitly. Test the Fake against the same contract tests as the real implementation (contract test suite). If the gap is too large, the Fake may need more logic, or the test should use the real dependency.

### 4. Mocking Types You Do Not Own

- **Appearance:** `Mock<ThirdPartyLib::HttpClient>` with expectations matching internal library behavior.
- **Trap:** "I need to control what the library returns."
- **Consequence:** Library upgrade changes internal call patterns; dozens of mocks break. The mock expectations encode guesses about library internals.
- **Fix:** Wrap third-party types in an adapter that you own. Mock the adapter, not the library directly.

---

## See Also

- [Testing Strategy Checklist](testing-strategy.md) -- Test sizes, pyramid proportions, mocking rules at the strategy level
- [GoogleTest and GMock Patterns](../../cpp/testing/googletest-patterns.md) -- GMock-specific `EXPECT_CALL`, `ON_CALL`, `NiceMock`/`StrictMock` usage
- [Catch2 Testing Patterns](../../cpp/testing/catch2-patterns.md) -- Catch2-specific test double patterns

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | A | xUnit Test Patterns (Meszaros, 2007) | Ch.11 Test Doubles, Ch.23-26 Dummy/Stub/Spy/Mock/Fake | verified-2026 | 2026-06 |
| R2 | A | Mocks Aren't Stubs (Fowler, 2007) | Classical vs. Mockist TDD, state vs. interaction testing | verified-2026 | 2026-06 |
| R3 | C | Google Testing Blog | Test doubles, mocking strategy, over-mocking | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
