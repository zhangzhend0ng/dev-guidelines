---
type: harness
id: "cpp-sanitizers"
title: "Sanitizer Integration and Usage Checklist"
language: "cpp"
category: "testing"
tier: "N"
scope: "Integrate ASan, UBSan, TSan, and MSan into CMake builds and CI pipelines to detect memory errors, undefined behavior, data races, and uninitialized reads"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [sanitizers, asan, ubsan, tsan, msan, address-sanitizer, undefined-behavior, thread-sanitizer, memory-sanitizer, cmake, ci, llvm-symbolizer]
based_on:
  - "[N] ISO C++ [defns.undefined]"
  - "[C] LLVM Compiler-RT Sanitizer Documentation"
  - "[A] Google Sanitizers Wiki (GitHub: google/sanitizers)"
related:
  - "common/ai/ai-assisted-cpp-development.md"
  - "cpp/security/secure-coding.md"
  - "cpp/testing/fuzzing.md"
  - "cpp/testing/static-analysis.md"
  - "cpp/debugging/sanitizer-triage.md"
  - "cpp/runtime/observability-and-diagnostics.md"
  - "cpp/build/toolchain-and-compiler-flags.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/concurrency/thread-safety.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Sanitizer Integration and Usage Checklist

**Based on:** ISO C++ [defns.undefined] ([N]), LLVM Compiler-RT Documentation ([C]), Google Sanitizers Wiki ([A]).
**Scope:** Systematic integration of compiler sanitizers into CMake-based C++ projects. Covers ASan, UBSan, TSan, MSan -- from local dev flags through CI gating.

---

## Concepts

| Sanitizer | Flag | Detects | Slowdown | Incompatible With |
|-----------|------|---------|----------|-------------------|
| AddressSanitizer (ASan) | `-fsanitize=address` | Heap/stack buffer overflow, use-after-free, double-free, memory leaks (LSan) | ~2x | TSan, MSan |
| UndefinedBehaviorSanitizer (UBSan) | `-fsanitize=undefined` | Integer overflow, null deref, misaligned access, shift overflow, signed overflow | minimal | -- (compatible with all) |
| ThreadSanitizer (TSan) | `-fsanitize=thread` | Data races, thread leaks, deadlocks | 5-15x, ~5-10x memory | ASan, MSan |
| MemorySanitizer (MSan) | `-fsanitize=memory` | Uninitialized reads (stack + heap) | ~3x | ASan, TSan |
| LeakSanitizer (LSan) | Built into ASan | Memory leaks | negligible (standalone) | TSan, MSan |

**Symbolization:** All sanitizers require `llvm-symbolizer` in PATH (or `ASAN_SYMBOLIZER_PATH` / `UBSAN_SYMBOLIZER_PATH` / `TSAN_SYMBOLIZER_PATH` / `MSAN_SYMBOLIZER_PATH` env vars) and unstripped debug symbols (`-g`) to produce human-readable stack traces.

---

## Checklist

### 1. AddressSanitizer (ASan) -- Heap/Stack Memory Errors  **(N)** [R1][R2]

- [ ] ASan enabled for all debug and test builds -- **(N)** [R1][R2]
- [ ] `-fsanitize=address` added to **both** `CMAKE_CXX_FLAGS` and `CMAKE_EXE_LINKER_FLAGS` -- **(N)** [R2]
- [ ] `ASAN_OPTIONS` configured for thorough detection -- **(C)** [R2]
  - `detect_stack_use_after_return=1` -- catch use-after-return bugs
  - `strict_string_checks=1` -- detect string OOB writes
  - `check_initialization_order=1` -- catch static init order fiasco
- [ ] LeakSanitizer (LSan) active (enabled by default with ASan on Linux) -- **(C)** [R2]
  - `ASAN_OPTIONS=detect_leaks=1` set explicitly in CI
- [ ] `detect_container_overflow=1` for libstdc++ container bounds checking -- **(C)** [R2]

```cmake
# CMake -- ASan enabled via preset or -DENABLE_ASAN=ON
if(ENABLE_ASAN)
    set(SANITIZER_FLAGS "-fsanitize=address -fno-omit-frame-pointer -g")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${SANITIZER_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=address")
endif()
```

```bash
# Runtime options (CI)
export ASAN_OPTIONS=detect_stack_use_after_return=1:strict_string_checks=1:check_initialization_order=1:detect_leaks=1
```

### 2. UndefinedBehaviorSanitizer (UBSan) -- Undefined Behavior  **(N)** [R1][R2]

- [ ] `-fsanitize=undefined` enabled for all debug and test builds -- **(N)** [R1][R2]
  - Covers: division by zero, null deref, misaligned access, shift overflow, signed integer overflow, out-of-bounds (bounds), vptr, function, float-cast-overflow
- [ ] `-fsanitize=signed-integer-overflow` added (not in `undefined` default on all compilers) -- **(C)** [R2]
- [ ] `-fsanitize=implicit-conversion` for narrowing/lossy implicit conversions -- **(C)** [R2]
- [ ] `UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1` in CI (fail-fast) -- **(C)** [R2]
- [ ] `-fno-sanitize-recover=all` in CI to treat every UBSan report as fatal -- **(C)** [R2]

```cmake
if(ENABLE_UBSAN)
    set(UBSAN_FLAGS
        -fsanitize=undefined
        -fsanitize=signed-integer-overflow
        -fsanitize=implicit-conversion
        -fno-sanitize-recover=all
        -g
    )
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${UBSAN_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=undefined")
endif()
```

```bash
export UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1
```

### 3. ThreadSanitizer (TSan) -- Data Races  **(N)** [R1][R2]

- [ ] TSan enabled for all test builds that exercise concurrent code paths -- **(N)** [R1][R2]
- [ ] `-fsanitize=thread` added to both compile and link flags -- **(N)** [R2]
- [ ] `TSAN_OPTIONS` configured for thorough reporting -- **(C)** [R2]
  - `history_size=7` -- maximum history depth per memory access
  - `second_deadlock_stack=1` -- capture second stack in deadlock reports
  - `halt_on_error=1` in CI
- [ ] TSan used in a **separate build** from ASan and MSan (runtime-incompatible) -- **(N)** [R2]
- [ ] **Both** the sanitized binary and all shared libraries linked at runtime instrumented -- **(C)** [R2]
  - Linking uninstrumented libraries while running TSan produces false positives or silent misses
- [ ] TSan detects only racy executions that actually occur; a clean TSan run does **not** prove absence of data races -- **(A)** [R2]
  - Mitigation: run TSan tests under high contention, varied thread schedules, and stress runs

```cmake
if(ENABLE_TSAN)
    set(TSAN_FLAGS "-fsanitize=thread -fno-omit-frame-pointer -g")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TSAN_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=thread")
endif()
```

```bash
export TSAN_OPTIONS=history_size=7:second_deadlock_stack=1:halt_on_error=1
```

### 4. MemorySanitizer (MSan) -- Uninitialized Reads  **(C)** [R2]

- [ ] MSan enabled for projects where uninitialized reads are a known risk -- **(C)** [R2]
  - MSan requires **all** linked libraries (including libc++/libstdc++) to be instrumented
  - On Linux, use `-stdlib=libc++` with an MSan-instrumented libc++ build
- [ ] `-fsanitize=memory` and `-fsanitize-memory-track-origins` for origin tracking -- **(C)** [R2]
- [ ] `MSAN_OPTIONS=poison_in_dtor=1` to catch reads from destroyed objects -- **(C)** [R2]
- [ ] MSan in a **separate build** from ASan and TSan (incompatible) -- **(N)** [R2]

```cmake
if(ENABLE_MSAN)
    set(MSAN_FLAGS
        -fsanitize=memory
        -fsanitize-memory-track-origins
        -fno-omit-frame-pointer
        -g
    )
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${MSAN_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=memory")
endif()
```

```bash
export MSAN_OPTIONS=poison_in_dtor=1
```

### 5. CMake Integration Patterns  **(C)** [R2]

- [ ] Sanitizer flags behind CMake cache variables (`-DENABLE_ASAN=ON`, `-DENABLE_UBSAN=ON`, etc.) -- **(C)** [R2]
- [ ] Sanitizer flags added to **both** `CMAKE_CXX_FLAGS` and linker flags -- **(N)** [R2]
  - `-fsanitize=address` requires linking with the ASan runtime; omitting from link flags produces link errors
- [ ] `-fno-omit-frame-pointer` and `-g` included with every sanitizer build -- **(N)** [R2]
  - Ensures complete, symbolized stack traces
- [ ] CMake presets (`CMakePresets.json`) defining sanitizer configurations -- **(C)** [R2]
  - `asan-debug`, `tsan-debug`, `msan-debug`, etc.
- [ ] `-O1` or `-O0` for sanitizer builds (higher optimization reduces report quality) -- **(C)** [R2]
- [ ] Thread/address sanitizers use separate build directories (incompatible at link/runtime) -- **(N)** [R2]

```json
// CMakePresets.json -- example sanitizer preset
{
  "name": "asan-debug",
  "displayName": "ASan Debug",
  "cacheVariables": {
    "CMAKE_BUILD_TYPE": "Debug",
    "ENABLE_ASAN": "ON",
    "ENABLE_UBSAN": "ON"
  }
}
```

### 6. Suppression Files and Inline Suppressions  **(C)** [R2][R3]

- [ ] Suppression file checked into the repository for known false positives -- **(C)** [R2]
  - Format: one suppression per line as `function:pattern` or `source:pattern`
- [ ] Each suppression documented with: **reason**, **date added**, **review deadline** -- **(C)** [R2]
  - Example: `# 2026-06: Third-party libfoo::parse() false positive; revisit after libfoo v2.1`
- [ ] Inline suppression via `__attribute__((no_sanitize("address")))` or `__attribute__((no_sanitize("thread")))` only when no other fix is possible -- **(C)** [R2]
  - Each inline suppression carries a comment explaining why and a tracking issue reference
- [ ] Suppression files reviewed per release cycle; stale suppressions removed -- **(C)** [R2]

```bash
# .asan-suppressions -- checked into repo
# Reason: libfoo allocator uses custom pool, LSan reports as leak
# Added: 2026-06-03, review by: 2026-09-03
leak:libfoo::PoolAllocator::allocate
```

```cpp
// Inline suppression -- use sparingly, with justification
void legacy_handler(void* buf) {
    // Tracking: PROJ-1234 -- remove after rewriting handler with std::span
    #if defined(__has_feature)
    #if __has_feature(address_sanitizer)
    __attribute__((no_sanitize("address")))
    #endif
    #endif
    memcpy(dest, buf, size);  // buf validated elsewhere, ASan false positive
}
```

### 7. CI Integration  **(N)** [R2][R3]

- [ ] Dedicated sanitizer build job(s) in CI pipeline -- **(N)** [R2]
- [ ] Sanitizer jobs run on every PR (not just nightly) -- **(N)** [R2]
- [ ] Sanitizer failures treated as **hard CI failures** (non-optional gate) -- **(N)** [R2]
- [ ] Test suite fully executed under each sanitizer (not just compilation) -- **(N)** [R2]
- [ ] Sanitizer job names clearly indicate which sanitizer is running -- **(C)** [R2]
  - Example: `test-asan-ubsan`, `test-tsan`, `test-msan`
- [ ] `halt_on_error=1` set for all sanitizers in CI to fail fast -- **(C)** [R2]
- [ ] CI logs capture full symbolized stack traces (not raw addresses) -- **(N)** [R2] -- see Item 10
- [ ] `ASAN_OPTIONS=log_path=/tmp/asan.log` to archive structured reports for post-mortem -- **(C)** [R2]

```yaml
# GitHub Actions -- sanitizer job snippet
asan-ubsan:
  runs-on: ubuntu-22.04
  steps:
    - uses: actions/checkout@v4
    - name: Configure
      run: cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug -DENABLE_ASAN=ON -DENABLE_UBSAN=ON
    - name: Build
      run: cmake --build build
    - name: Test
      run: |
        export ASAN_OPTIONS=detect_leaks=1:strict_string_checks=1:halt_on_error=1
        export UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1
        ctest --test-dir build --output-on-failure
```

### 8. Performance Trade-offs  **(A)** [R2][R3]

- [ ] Developers aware that ASan adds ~2x slowdown and ~2-3x memory overhead -- **(A)** [R2]
- [ ] Developers aware that TSan adds 5-15x slowdown and 5-10x memory overhead -- **(A)** [R2]
  - Test suites that normally take 5 minutes may take 25-75 minutes under TSan
- [ ] Developers aware that MSan adds ~3x slowdown -- **(A)** [R2]
- [ ] UBSan has minimal overhead (typically <10%); suitable for broader deployment -- **(A)** [R2]
- [ ] Sanitizer-enabled builds are **never** shipped to production -- **(N)** [R2]
  - Performance degradation and increased attack surface from diagnostic instrumentation
- [ ] Sanitizer builds used for testing/debugging only; release builds sanitizer-free -- **(N)** [R2]
- [ ] Consider `-O1` over `-O0` for sanitizer builds on large test suites to keep CI runtimes manageable -- **(A)** [R2]

### 9. Combining Sanitizers  **(C)** [R2][R3]

- [ ] ASan + UBSan combined in a single build (fully compatible) -- **(C)** [R2]
  - Flags: `-fsanitize=address,undefined`
- [ ] ASan includes LSan by default -- no separate flag needed for leak detection -- **(C)** [R2]
- [ ] TSan used in a **separate** build from ASan and MSan (mutually exclusive at runtime) -- **(N)** [R2]
  - Attempting `-fsanitize=address,thread` results in a compiler error or runtime crash
- [ ] UBSan combined with **either** ASan or TSan (compatible with both) -- **(C)** [R2]
  - `-fsanitize=address,undefined` -- single ASan+UBSan build
  - `-fsanitize=thread,undefined` -- single TSan+UBSan build
- [ ] MSan used in a separate build from ASan and TSan -- **(N)** [R2]

| Combination | Supported | Notes |
|-------------|-----------|-------|
| ASan + UBSan | Yes | Standard combined build |
| ASan + LSan | Yes | LSan integrated into ASan |
| TSan + UBSan | Yes | Recommended for concurrent code |
| MSan + UBSan | Yes | Requires instrumented libc++ |
| ASan + TSan | **No** | Compiler error or runtime crash |
| ASan + MSan | **No** | Runtime incompatibility |
| TSan + MSan | **No** | Runtime incompatibility |

### 10. Interpreting Reports and Symbolization  **(C)** [R2][R3]

- [ ] `llvm-symbolizer` available in PATH or via `ASAN_SYMBOLIZER_PATH` env var -- **(N)** [R2]
  - Without symbolization, reports show raw addresses -- nearly impossible to debug
- [ ] Debug symbols available -- binary not stripped, compiled with `-g` -- **(N)** [R2]
- [ ] CI logs contain symbolized stack traces, not raw addresses -- **(N)** [R2]
- [ ] `halt_on_error=1` in CI to stop at the first sanitizer report (fail-fast for deterministic bugs) -- **(C)** [R2]
- [ ] Developers know how to read a sanitizer stack trace -- **(C)** [R2]
  - Top frame: the memory operation that triggered the error
  - Earlier frames: allocation site (for use-after-free) or prior access (for data races)
  - ASan adds "The shadow memory layout" summary if `print_shadow_map=1`
- [ ] `ASAN_OPTIONS=symbolize=1` set explicitly (default on most platforms, but explicit avoids surprises) -- **(C)** [R2]
- [ ] Report output archived as CI artifacts for post-mortem analysis -- **(C)** [R2]

```bash
# Ensure llvm-symbolizer is found
export ASAN_SYMBOLIZER_PATH=$(which llvm-symbolizer)
export ASAN_OPTIONS=symbolize=1:print_shadow_map=1
```

**How to read an ASan report (quick reference):**

```
==12345==ERROR: AddressSanitizer: heap-use-after-free on address 0x... at pc 0x...
READ of size 4 at 0x... thread T0
    #0 0x... in use_after_free() src/example.cpp:15   <<< WHERE the bug triggered
    #1 0x... in main src/example.cpp:22
0x... is located 0 bytes inside of 100-byte region [0x...,0x...)
freed by thread T0 here:                               <<< WHERE it was freed
    #0 0x... in operator delete(void*)
    #1 0x... in release() src/example.cpp:10
previously allocated by thread T0 here:                <<< WHERE it was allocated
    #0 0x... in operator new(unsigned long)
    #1 0x... in allocate() src/example.cpp:5
```

---

## Decision Tree

```
New C++ project or adding sanitizer support?
  |-- Add CMake cache variables for each sanitizer [5]
  |-- Create CMake presets: asan-debug, tsan-debug, etc. [5]
  |-- ASan + UBSan in a single debug/test build [1][2][9]
  |-- Concurrent code? -- Separate TSan + UBSan build [3][9]
  |-- Uninitialized read risk? -- Separate MSan build (if feasible) [4][9]
  |-- Add sanitizer CI job(s) as PR gate [7]
  |-- Configure runtime options (halt_on_error, stacktraces, symbolization) [1][2][3][4]
  |-- Verify llvm-symbolizer in PATH on CI runners [10]
  |-- Create suppression file for third-party noise, document each entry [6]
  \-- Set performance expectations with the team [8]
```

---

## Anti-Patterns

### 1. Sanitizers Only in Local Development

- **Appearance:** Developers run sanitizers locally but CI has no sanitizer build.
- **Trap:** "I tested it locally with ASan" -- sanitizers catch bugs based on runtime code paths, and a different CI run may exercise different paths.
- **Consequence:** Bugs slip through because the CI-specific code paths (error handling, edge cases) are never run under a sanitizer.
- **Fix:** CI must have a sanitizer job that runs the full test suite. Local sanitizer use is additive, not a substitute.

### 2. Shipping Sanitized Binaries

- **Appearance:** `-fsanitize=address` flags left in release build configuration.
- **Trap:** "It catches bugs in production" -- ASan in production means 2x slowdown, 2-3x memory overhead, and increased attack surface from diagnostic instrumentation.
- **Consequence:** Production performance degradation, false-positive user-visible crashes (`halt_on_error`), security risk from ASan internals.
- **Fix:** Sanitizer flags behind a CMake cache variable. Release presets must not set it. Validate with `readelf -d <binary> | grep asan` or `nm <binary> | grep asan`.

### 3. Combining TSan with ASan

- **Appearance:** `-fsanitize=address,thread` in the same build.
- **Trap:** "I want to check both memory and thread issues at once."
- **Consequence:** Compiler rejects the combination or runtime crashes. They are fundamentally incompatible -- both replace `malloc`/`free`, manage shadow memory, and hook the same functions.
- **Fix:** Separate build directories. ASan+UBSan in one. TSan+UBSan in another.

### 4. Suppressing Without Documentation

- **Appearance:** Suppression file grows with entries like `leak:*` or `race:*` and no comments.
- **Trap:** "It's just a false positive -- we'll remember why we added it."
- **Consequence:** Six months later, nobody knows which suppressions are still valid. Real bugs hidden behind stale blanket suppressions.
- **Fix:** Every suppression has a date, reason, and review deadline. Blanket wildcards prohibited without explicit justification.

### 5. Ignoring Sanitizer Reports as "Noise"

- **Appearance:** CI logs show ASan/UBSan warnings but nobody investigates; team treats them like compiler warnings.
- **Trap:** "ASan reports a lot of things, most are probably false positives."
- **Consequence:** ASan and UBSan have **very low false positive rates** for well-instrumented code. Every report is a real bug until proven otherwise.
- **Fix:** `halt_on_error=1` in CI. Every report breaks the build. If it is a true false positive, add a documented suppression -- do not ignore.

---

## See Also

- [Undefined Behavior Prevention](../correctness/undefined-behavior.md) -- UB categories caught by UBSan and static analysis
- [Concurrency and Thread Safety](../concurrency/thread-safety.md) -- Data race prevention patterns; TSan validates these at runtime

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | [N1] ISO/IEC 14882 (C++ Standard) | [defns.undefined], [intro.races] | verified-2026 | 2026-06 |
| R2 | C | LLVM Compiler-RT Sanitizer Documentation | AddressSanitizer, ThreadSanitizer, MemorySanitizer, UndefinedBehaviorSanitizer -- flags, options, suppression format | verified-2026 | 2026-06 |
| R3 | A | Google Sanitizers Wiki (github.com/google/sanitizers) | Usage patterns, common pitfalls, combining sanitizers, CI recipes | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft -- ASan, UBSan, TSan, MSan coverage; CMake integration; CI patterns; symbolization guide
