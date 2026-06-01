---
type: harness
id: "cpp-performance-patterns"
title: "C++ Performance Patterns Checklist"
language: "cpp"
category: "performance"
tier: "N"
scope: "Apply performance-critical C++ patterns: copy elision, data-oriented design, and benchmarking methodology"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-01"
review_cycle: "12m"
tags: [performance, optimization, cpp, benchmarking]
based_on:
  - "[N] ISO C++ [class.copy.elision] — Guaranteed RVO in C++17"
  - "[C] C++ Core Guidelines Per.1-Per.19"
  - "[A] Optimized C++ (Guntheroth, 2016)"
  - "[A] Chandler Carruth — CppCon Performance Talks"
related:
  - "cpp/memory/move-semantics.md"
  - "cpp/memory/raii.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# C++ Performance Patterns Checklist

**Based on:** ISO C++ [class.copy.elision] ([N]), C++ Core Guidelines Per ([C]), Optimized C++ ([A]), Carruth CppCon ([A]).
**Scope:** C++-specific performance patterns. Apply after profiling, not before.

---

## Concepts

| Pattern | Mechanism |
|---------|-----------|
| RVO/NRVO | Compiler elides return copy; guaranteed in C++17 |
| Sink params | Pass by value + `std::move`; one overload for lvalue+rvalue |
| Data-oriented | SoA over AoS; cache line alignment; group hot fields |
| Benchmarking | Profile first; isolate; trust data over intuition |

---

## Checklist

### 1. Rely on Copy Elision  **(N)** [R1]

- [ ] Return local by value; never `std::move` the return → **(N)** [R1]
- [ ] `return std::move(x)` disables RVO → **(N)** [R1]

### 2. Move on Ownership Transfer  **(N)** [R1]

- [ ] `std::move` at last use when transferring to sink → **(N)** [R1]
- [ ] Moved-from object in valid-but-unspecified state → **(C)** [R2]

### 3. Pre-increment Iterators  **(C)** [R2]

- [ ] `++it`, not `it++` in loops → **(C)** [R2]
- [ ] Post-increment creates unnecessary temporary → **(C)** [R2]

### 4. Sink Parameters  **(C)** [R2]

- [ ] Pass by value + `std::move` for sinks → **(C)** [R2]
- [ ] Amortizes copy + move into single move for rvalues → **(C)** [R2]

### 5. Data-Oriented Design  **(A)** [R3]

- [ ] SoA over AoS for sequential access → **(A)** [R3]
- [ ] Hot fields grouped; aligned to cache line → **(A)** [R3]
- [ ] `vector<Point>` over `vector<shared_ptr<Point>>` → **(A)** [R3]

### 6. False Sharing Prevention  **(C)** [R2][R3]

- [ ] Per-thread hot data ≥64 bytes apart → **(C)** [R2]
- [ ] `alignas(64)` or padding for thread-local writes → **(C)** [R3]

### 7. Benchmarking Methodology  **(C)** [R2][R4]

- [ ] Profile BEFORE optimizing → **(C)** [R2]
- [ ] Microbenchmark with representative data → **(C)** [R4]
- [ ] No measurement = speculation → **(C)** [R2]

---

## Decision Tree

```
Profiler says hot?
  → Return by value? → RVO [1]
  → Ownership transfer? → std::move [2]
  → Loop? → ++it [3]
  → Sink param? → pass by value + move [4]
  → Sequential data? → SoA + cache align [5]
  → Multi-thread hot? → 64-byte gap [6]
  → Before any fix: benchmark [7]
```

---

## Anti-Patterns

### 1. Premature Optimization

- **Appearance:** Micro-optimizing loops before profiling.
- **Trap:** Feels like discipline.
- **Consequence:** Obfuscated cold paths. Real bottlenecks ignored.
- **Fix:** Profile. Fix 3% of code taking 97% of time.

### 2. `std::move` on Return

- **Appearance:** `return std::move(result);`
- **Trap:** "Explicitly moving to avoid copy."
- **Consequence:** Disables RVO. Forces move where compiler would elide entirely.
- **Fix:** `return result;` — compiler elides. `std::move` only for non-return transfers.

---

## See Also

- [Move Semantics](../memory/move-semantics.md) — Rule of Five, std::move, perfect forwarding
- [RAII](../memory/raii.md) — Exception-safe resource management

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [class.copy.elision] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | Per.1-Per.19 | verified-2026 | 2026-06 |
| R3 | A | Optimized C++ (Guntheroth) | Ch.4-6,9 | verified-2026 | 2026-06 |
| R4 | A | Carruth — CppCon | Benchmarking | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft
