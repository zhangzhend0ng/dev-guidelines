---
type: harness
id: "cpp-integer-safety"
title: "Integer Safety Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Prevent signed integer overflow, signed/unsigned mixing bugs, narrowing, division/shift UB, and size-type mismatches in C++"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [integer-safety, overflow, signed-unsigned, narrowing, shift, size_t, cpp]
based_on:
  - "[N] ISO C++ [expr], [conv.integral], [expr.shift], [expr.mul]"
  - "[C] C++ Core Guidelines ES.100-ES.107"
  - "[C] SEI/CERT INT30-C through INT36-C"
  - "[A] Boost.SafeNumerics documentation"
  - "[A] GCC/Clang -fsanitize=signed-integer-overflow, -ftrapv, -Wconversion documentation"
related:
  - "cpp/serialization/parsing-and-validation.md"
  - "cpp/security/secure-coding.md"
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/correctness/type-safety.md"
  - "projects/snapmaker-orca/coding-standards.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# Integer Safety Checklist

**Based on:** ISO C++ [expr]/[conv.integral]/[expr.shift]/[expr.mul] ([N]), C++ Core Guidelines ES.100-ES.107 ([C]), SEI/CERT INT30-C through INT36-C ([C]), Boost.SafeNumerics documentation ([A]), GCC/Clang sanitizer and warning documentation ([A]).

**Scope:** Detect and prevent integer-related undefined behavior, portability bugs, and security vulnerabilities. Integer misuse is one of the most common sources of exploitable defects -- signed overflow, truncation on narrowing, shift-out-of-range, and signed/unsigned mismatch each cause UB or wrong results that attackers can weaponize.

---

## Prerequisites / Concepts

### Signed vs Unsigned Behavior

| Operation | Signed | Unsigned |
|-----------|--------|----------|
| Overflow (e.g., `INT_MAX + 1`) | **UB** -- compiler may delete code, assume it never happens | Well-defined wraparound (modulo 2^N) |
| Underflow (e.g., `0 - 1`) | UB if result < `INT_MIN` | Well-defined wraparound to `UINT_MAX` |
| Division by zero | **UB** | **UB** |
| `INT_MIN / -1` | **UB** (result exceeds `INT_MAX` by 1) | N/A |
| Right shift of negative value | Implementation-defined (usually arithmetic) | Well-defined (logical) |
| Left shift of negative value | **UB** in C++11/14, defined in C++17 (two's complement) but sign-change is UB | Well-defined wraparound |

### Integer Promotion Rules (The Silent Killer)

When two integer operands of different types are combined in an arithmetic expression, the compiler applies the **usual arithmetic conversions**:

1. Integral promotion: types smaller than `int` are promoted to `int` (or `unsigned int` if `int` cannot represent all values).
2. If same signedness: the narrower type is converted to the wider type.
3. If different signedness and the unsigned type is wider or equal in conversion rank: the signed type is converted to the unsigned type.
4. If different signedness and the signed type can represent all values of the unsigned type: the unsigned type is converted to the signed type.

**Critical trap:** `uint16_t + int16_t` promotes both to `int` (safe on 32/64-bit platforms). But `uint32_t + int32_t` converts the signed `int32_t` to `uint32_t` -- a negative signed value becomes a huge unsigned value. This is a frequent source of bugs.

### Tooling

| Flag / Tool | What It Catches |
|-------------|-----------------|
| `-fsanitize=signed-integer-overflow` (UBSan) | Runtime signed overflow detection |
| `-fsanitize=integer` (UBSan subset) | Signed overflow + implicit unsigned wraparound |
| `-ftrapv` | Trap (SIGABRT) on signed overflow at runtime |
| `-fwrapv` | Make signed overflow wrap (well-defined, like unsigned). Use only when intentionally relying on wraparound; document why. |
| `-Wconversion` | Warn on implicit narrowing, sign-change, and precision-loss conversions |
| `-Wsign-conversion` | Warn on implicit signed-to-unsigned and unsigned-to-signed conversions |
| `-Wsign-compare` | Warn on comparison between signed and unsigned |
| `-Wshift-overflow` | Warn on shift count >= bit width (compile-time detectable) |
| `-Wshift-negative-value` | Warn on left-shift of negative signed value |
| `-Wshift-count-overflow` | Warn on shift count overflow |
| `-Wdivision-by-zero` | Warn on compile-time detectable division by zero |
| `-Wtautological-constant-out-of-range-compare` | Warn on comparisons always true/false due to type range mismatch |

**Rule: Enable `-Wconversion`, `-Wsign-conversion`, `-Wsign-compare`, `-Wshift-overflow`, and `-Wdivision-by-zero` as errors (`-Werror=...`) in all builds. Enable `-fsanitize=signed-integer-overflow` (or `-fsanitize=integer`) in CI test builds. Never use `-fwrapv` as a blanket flag; apply it only to specific translation units that intentionally rely on signed wraparound, with a documented reason.**

---

## Checklist

### 1. Signed Integer Overflow

Signed integer overflow is undefined behavior. The compiler may assume `x + 1 > x` always holds for signed types and eliminate overflow checks accordingly.

- [ ] Arithmetic on signed integers whose operands could overflow (addition, subtraction, multiplication)? → **(N)** Replace with unsigned types if wraparound is the desired semantics. Use compiler builtins (`__builtin_add_overflow`, `__builtin_mul_overflow`) or `std::ckd_add` (C++23) for checked arithmetic. Never rely on signed overflow as a "feature." [R1][R2][R3]
- [ ] Security-sensitive bounds check like `if (size + delta < size)` or `if (offset + length > capacity)` where operands are signed? → **(N)** If `size + delta` overflows before the comparison, the check is eliminated by the compiler (UB). Use unsigned types or checked-add builtins. [R1][R3]
- [ ] Loop counter increment that could reach `INT_MAX`? → **(C)** Use `size_t` or a wider signed type. If `int` is required by an API, validate before the loop that the range is safe. [R2]
- [ ] Multiplication used to compute buffer size (`width * height * sizeof(T)`)? → **(N)** Use `__builtin_mul_overflow` with overflow check, or a safe-numerics wrapper. Truncation from `size_t` overflow silently allocates too little memory. [R1][R3]

### 2. Signed/Unsigned Mixing

Mixing signed and unsigned types in the same expression triggers the usual arithmetic conversions, often with surprising results. A negative signed value converted to unsigned becomes a large positive number.

- [ ] Expression mixing `int` and `size_t` (or `uint32_t`) without explicit conversion? → **(N)** The signed operand is silently converted to unsigned. A negative value (e.g., `-1`) becomes a huge positive value. Cast explicitly with a range check, or restructure to use consistent types. [R1][R2][R3]
- [ ] Comparison between signed and unsigned types (`x < v.size()` where `x` is `int`)? → **(C)** Enable `-Wsign-compare` as error. Rewrite with `gsl::index` (signed) or cast after range validation. Never suppress the warning with a C-style cast. [R2][R3]
- [ ] Unsigned type used for "must be non-negative" semantics (e.g., function parameter `unsigned int count`)? → **(C)** Guideline ES.106: unsigned does not guarantee non-negative -- it guarantees wraparound. `count - 1` when `count == 0` wraps to `UINT_MAX`. Use `int` with an assertion or `gsl::not_null`/range check. Reserve unsigned for bit manipulation, modulo arithmetic, and size/offset types. [R2]
- [ ] Arithmetic on unsigned types where a negative intermediate result is possible? → **(C)** `(a - b) / c` when `a < b` wraps to a huge value before the division. Restructure to signed arithmetic or explicitly check ordering. [R2]

### 3. Narrowing Conversions

Assigning a wider integer type to a narrower one silently truncates. The truncated value may be semantically wrong and is a common source of security bugs (e.g., allocating `size_t` size truncated to `uint32_t`).

- [ ] Assignment of a wider integer to a narrower one (e.g., `uint64_t → uint32_t`, `int64_t → int`, `size_t → int`)? → **(N)** Use `{}` init (`int x{wide_value}`) to make narrowing a compile-time error. If narrowing is intentional, use `static_cast<T>(value)` with a preceding range check and a comment explaining why. [R1][R2]
- [ ] `{}` init used consistently for variable initialization? → **(C)** Prefer `{}` over `=` for new variables. `int x = 3.14` silently truncates; `int x{3.14}` is a compile error. Consistent use of `{}` catches narrowing at the earliest point. [R2]
- [ ] Function parameter passing from a wider type to a narrower parameter? → **(N)** `{}` init does not protect function parameters. At the call site, validate that the argument fits in the parameter type. `gsl::narrow<T>(value)` for runtime-checked narrowing. [R1][R3]
- [ ] Float-to-integer conversion where the float value exceeds the integer range? → **(N)** UB. Always range-check: `if (f > INT_MAX || f < INT_MIN || !std::isfinite(f))` before conversion. [R1]
- [ ] `-Wconversion` enabled as error? → **(C)** Catch all implicit narrowing, sign-change, and precision-loss conversions at compile time. Suppress only with an explicit `static_cast` and a documented reason. [R2]

### 4. Division by Zero and INT_MIN / -1

Integer division by zero is always UB. For signed integers, `INT_MIN / -1` is also UB because the mathematical result (`INT_MAX + 1`) exceeds the representable range.

- [ ] Division or modulo with a variable divisor? → **(N)** Guard with `if (divisor == 0)` before the operation. This check must precede the division, not follow it. [R1][R3]
- [ ] Signed division where the dividend could be `INT_MIN` and divisor could be `-1`? → **(N)** Add an explicit check: `if (dividend == INT_MIN && divisor == -1)` before the operation. This is UB even on two's complement platforms. [R1][R3]
- [ ] Modulo with negative operands? → **(C)** In C++, the sign of `%` result follows the dividend. `-5 % 3 == -2`, not `1`. If mathematical modulo (always non-negative) is intended, use a helper function. Document the expected sign semantics. [R2]
- [ ] Division used in a performance-critical path where the divisor is an invariant? → **(A)** If the same divisor is used repeatedly, consider replacing division with multiplication by reciprocal (e.g., `libdivide`). This is not a safety issue but a performance pattern that also eliminates the zero-division hazard when done correctly. [R4]

### 5. Shift Overflow

Shifting by a negative count or by a count greater than or equal to the bit width of the promoted left operand is UB. Left-shifting a negative signed value is UB (before C++17) or defined but not recommended (C++17+).

- [ ] Shift count derived from runtime input (variable, function parameter)? → **(N)** Validate that the shift count is `>= 0` and `< bit_width` of the left operand type _after integral promotion_. `uint8_t x; x << 32` promotes `x` to `int` (32-bit), so the max legal shift is `< 32`. [R1][R3]
- [ ] Left shift of a signed integer type? → **(N)** Left-shifting a negative value is UB in C++11/14. In C++17 (two's complement mandate), the result is defined but sign-change overflow is still UB. Always use unsigned types for shift operands. `1u << n`, not `1 << n`. [R1][R2]
- [ ] Right shift of a signed negative value? → **(C)** Right-shifting a negative signed integer is implementation-defined (usually arithmetic shift, but not guaranteed). Use unsigned types for shift operands or cast to unsigned before shifting. [R2][R3]
- [ ] Shift used to compute a mask or power-of-two? → **(C)** `(1 << n)` where `n` could be 31 on a 32-bit `int` platform causes UB (sign bit). Use `(1u << n)` or `(UINT32_C(1) << n)` to keep the operation in unsigned domain. [R2]

### 6. size_t vs int for Sizes, Indices, and Counts

Using `int` for sizes, indices, and loop counters is a persistent source of signed/unsigned mismatch, narrowing warnings, and overflow bugs. The C++ standard library uses `size_t` for sizes; matching those types eliminates a large class of bugs.

- [ ] Loop counter, array index, or size variable declared as `int`? → **(C)** Use `size_t` for all sizes, counts, and indices into standard containers. If signed arithmetic is needed (e.g., reverse loop), use `gsl::index` (a signed type specifically for indexing). [R2][R3]
- [ ] Reverse loop using `size_t` counter: `for (size_t i = n - 1; i >= 0; --i)`? → **(N)** This is an infinite loop because `size_t` is unsigned -- `i >= 0` is always true, and `--i` wraps to `SIZE_MAX` after 0. Use a sentinel pattern: `for (size_t i = n; i-- > 0; )` or `gsl::index` with signed arithmetic. [R2][R3]
- [ ] `std::ssize()` available (C++20) for loop bounds? → **(A)** Prefer `std::ssize(c)` which returns a signed size, enabling natural signed comparisons and reverse loops without the wraparound hazard. [R2]
- [ ] API boundary where a third-party C API returns `int` for sizes? → **(C)** Convert at the boundary with explicit validation. Check `api_size >= 0` before assigning to `size_t`. Never propagate `int` sizes into arithmetic-heavy code without first validating and converting. [R2][R3]
- [ ] `ptrdiff_t` vs `size_t` choice? → **(A)** `ptrdiff_t` is the signed counterpart of `size_t`. Use it when negative deltas are meaningful (pointer subtraction results). Use `size_t` when the value is inherently non-negative (allocation sizes). [R2]

### 7. Safe Arithmetic Abstractions

Raw integer arithmetic is fragile. Several library solutions provide checked, safe arithmetic that traps or signals on overflow rather than silently producing wrong results or UB.

- [ ] Arithmetic in security-critical or safety-critical code (crypto, bounds checks, allocation size computation)? → **(C)** Never use raw `+`, `-`, `*` on unchecked integers. Use a safe arithmetic library (Boost.SafeNumerics, `SafeInt`, or compiler builtins) that guarantees no silent overflow. [R2][R3]
- [ ] Addition with overflow check needed? → **(C)** Use `__builtin_add_overflow(a, b, &result)` (GCC/Clang) or `std::ckd_add(&result, a, b)` (C++23). These return a `bool` indicating overflow and are compiled to efficient branch-on-carry instructions. [R2][R4]
- [ ] Multiplication with overflow check needed? → **(C)** Use `__builtin_mul_overflow(a, b, &result)`. Never use the "check by dividing back" pattern (`if (a * b / b != a)`) -- the multiplication itself is UB before the check runs. [R1][R3]
- [ ] C++20 `std::cmp_less`, `std::cmp_greater`, `std::cmp_equal` for mixed-sign comparisons? → **(A)** These functions correctly compare signed and unsigned integers without the usual arithmetic conversions. `std::cmp_less(-1, 1u)` returns `true`. Prefer these over manual casts for comparisons. [R2]
- [ ] Boost.SafeNumerics used for whole-module integer safety? → **(A)** `boost::safe_numerics::safe<int>` provides drop-in integer types that throw or trap on overflow, underflow, and narrowing. Consider for modules with high correctness requirements. [R4]

### 8. Compiler Hardening Flags

Compiler flags provide baseline detection of integer misuse. A minimal set must be enabled in every build to catch integer bugs early.

- [ ] `-Wconversion` enabled as error (`-Werror=conversion`)? → **(C)** This catches implicit narrowing, sign conversions, and float-to-int conversions at compile time. Every build must have this on. False positives are suppressed with an explicit `static_cast` and documentation, never by disabling the warning. [R2]
- [ ] `-Wsign-conversion` enabled as error? → **(C)** Subset of `-Wconversion` that specifically catches signed/unsigned implicit conversions. Enable even if you enable the broader `-Wconversion`, for explicitness. [R2]
- [ ] `-Wsign-compare` enabled as error? → **(C)** Catches `int < size_t` comparisons. Critical for preventing the "negative becomes huge unsigned" bug. [R2]
- [ ] `-fsanitize=signed-integer-overflow` (or `-fsanitize=integer`) in CI test builds? → **(N)** Runtime detection of signed overflow. Must be clean in CI -- every report is a real bug. [R1][R3]
- [ ] `-ftrapv` considered? → **(A)** Traps (SIGABRT) on signed overflow at runtime. Higher overhead than UBSan but prevents execution past the overflow. Consider for release builds of safety-critical components. Do not combine with `-fwrapv`. [R5]
- [ ] `-fwrapv` absent from build? → **(C)** `-fwrapv` makes signed overflow well-defined (wraparound like unsigned). Only use with documented justification on specific translation units, never as a project-wide flag. It silences UBSan and hides real bugs. [R2][R5]

---

## Decision Tree

```
Integer operation review:
  ├─ Signed arithmetic (+, -, *) with potentially large operands?
  │     ├─ Overflow possible? → [Item 1] unsigned OR __builtin_add_overflow
  │     ├─ Mixing signed and unsigned? → [Item 2] convert to common type with range check
  │     └─ Security-sensitive bounds check? → [Item 1] checked arithmetic, NOT raw comparison
  │
  ├─ Assignment / initialization?
  │     ├─ Wider → narrower type? → [Item 3] {} init to catch; static_cast + range check if intentional
  │     └─ Float → integer? → [Item 3] range + isfinite check BEFORE cast
  │
  ├─ Division / modulo?
  │     └─ Variable divisor? → [Item 4] guard zero; guard INT_MIN / -1 for signed
  │
  ├─ Shift?
  │     ├─ Variable shift count? → [Item 5] validate 0 <= count < bit_width
  │     └─ Left operand signed? → [Item 5] use unsigned types for shift
  │
  ├─ Loop / index?
  │     ├─ Counter declared int? → [Item 6] size_t for sizes; gsl::index for signed needs
  │     └─ Reverse loop with size_t? → [Item 6] sentinel pattern OR gsl::index
  │
  ├─ Safety-critical arithmetic?
  │     └─ → [Item 7] Boost.SafeNumerics / __builtin_*_overflow / std::cmp_*
  │
  └─ Compiler flags gate:
        ├─ -Wconversion, -Wsign-conversion, -Wsign-compare as errors? → [Item 8]
        ├─ -fsanitize=signed-integer-overflow clean? → [Item 8]
        └─ -fwrapv absent (or documented per-TU)? → [Item 8]
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: "Unsigned Guarantees Non-Negative"

- **Appearance:** Function parameter `unsigned int age` or `size_t count` used to signal "must be >= 0." Code then does `count - 1` or `total - consumed`.
- **Trap:** Unsigned types guarantee wraparound, not non-negativity. When `count == 0`, `count - 1` silently becomes `UINT_MAX` (or `SIZE_MAX`). Comparisons like `if (a - b > 0)` are always true when `a` and `b` are unsigned.
- **Consequence:** Buffer overflows (huge size passed to `malloc` after wraparound), infinite loops (reverse `size_t` loop), incorrect bounds checks that always pass.
- **Fix:** Use `int` with `assert(value >= 0)` for semantic non-negativity. Reserve unsigned for modulo arithmetic, bit manipulation, and size/offset types. When you do need size-type subtraction, check ordering first: `if (a >= b) { size_t diff = a - b; }`.

### Anti-Pattern 2: "int for Everything"

- **Appearance:** All sizes, indices, counts, and loop variables declared as `int` -- `int size = vec.size()`, `for (int i = 0; i < n; ++i)`, `int buf_len = strlen(s)`.
- **Trap:** On 64-bit platforms, `int` is 32 bits but `size_t` is 64 bits. `int size = vec.size()` produces a narrowing conversion warning. The compiler's signed/unsigned promotion rules then create subtle bugs when `int` and `size_t` appear in the same expression.
- **Consequence:** Truncation of large sizes on 64-bit platforms. Sign-extension bugs when `int` is implicitly converted to `size_t`. Compiler warnings that developers suppress with casts rather than fixing the root type choice.
- **Fix:** Use `size_t` for sizes, counts, and standard-container indices. Use `gsl::index` (or `ptrdiff_t`) when signed arithmetic is needed. Convert API-returned `int` sizes at the boundary with validation, then use `size_t` internally.

### Anti-Pattern 3: "The Shift Can't Be That Large"

- **Appearance:** `x << n` where `n` comes from user input, a network packet, or a computed value. No range check on `n`. Assumption that "n will never exceed 31/63."
- **Trap:** UB when the shift count is `>=` the bit width of the promoted left operand. On x86, the hardware masks the shift count to the lower 5/6 bits, so `1 << 32` becomes `1 << 0 == 1`. On ARM, the behavior differs. The compiler may optimize assuming the shift is in range, producing surprising results.
- **Consequence:** Platform-dependent behavior -- code works on x86 (hardware masking) but breaks on ARM or under different optimization levels. Security bugs where crafted input triggers UB that becomes an exploitable condition.
- **Fix:** Always range-check the shift count before shifting: `if (n < 0 || n >= width) { /* handle error */ }`. Use unsigned types for both the value and the shift count: `value << shift` where both are `unsigned`. For mask generation, `(1u << n)` not `(1 << n)`.

### Anti-Pattern 4: "Division Check After the Fact"

- **Appearance:** `result = a / b; if (b == 0) { handle_error(); }` -- the division happens before the check, or the check is in a different scope.
- **Trap:** Division by zero is UB. The compiler may conclude `b != 0` at the division point and eliminate the subsequent null check as dead code (same optimization as null-pointer dereference elimination).
- **Consequence:** The error-handling code is silently removed. The program crashes or produces wrong results exactly when the divisor is zero -- precisely when the error handling was meant to save it.
- **Fix:** Place the divisor check before the division in the same basic block. Use a pattern like `if (divisor == 0) { return error; } result = a / divisor;` where the check dominates the division. For extra defense, `assert(divisor != 0)` before the division.

---

## See Also

- [Undefined Behavior Prevention](undefined-behavior.md) -- Signed overflow, division by zero, and shift UB are also covered in the general UB checklist ([Items 1, 5])
- [Type Safety and Implicit Conversions](type-safety.md) -- Narrowing, signed/unsigned, enum class, and C-style cast elimination ([Items 3, 4, 5, 6])

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [expr] (overflow, shift, division), [conv.integral] (promotion, narrowing), [expr.shift], [expr.mul] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | ES.100-ES.107 (integer arithmetic), ES.46-ES.49 (narrowing, conversions) | verified-2026 | 2026-06 |
| R3 | C | SEI/CERT C Coding Standard | INT30-C through INT36-C (integer safety rules) | verified-2026 | 2026-06 |
| R4 | A | Boost.SafeNumerics | Library documentation and rationale | verified-2026 | 2026-06 |
| R5 | A | GCC/Clang documentation | -fsanitize, -ftrapv, -fwrapv, -Wconversion flags | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft -- 8 checklist items covering signed overflow, unsigned mixing, narrowing, division/shift UB, size_t correctness, safe arithmetic libraries, and compiler hardening flags
