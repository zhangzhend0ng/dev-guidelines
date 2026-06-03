---
type: harness
id: "cpp-stl-containers"
title: "STL Algorithms and Containers Checklist"
language: "cpp"
category: "correctness"
tier: "N"
scope: "Apply STL algorithms correctly, choose the right container, avoid iterator invalidation, respect algorithm preconditions, and avoid misuse patterns like inheriting from STL containers"
version: "2026.06"
status: "draft"
stable_since: ""
last_validated: "2026-06-03"
review_cycle: "12m"
tags: [stl, algorithms, containers, iterators, erase-remove, bounds-checking, pmr]
based_on:
  - "[N] ISO C++ [algorithms], [containers], [sequence.reqmts], [associative.reqmts], [unord.req]"
  - "[C] C++ Core Guidelines SL.con.1-SL.con.4, SL.str.1-SL.str.5, SL.io.1-SL.io.5"
  - "[C] SEI/CERT CTR50-CPP through CTR58-CPP"
  - "[A] Effective STL (Scott Meyers, 2001)"
related:
  - "cpp/correctness/undefined-behavior.md"
  - "cpp/correctness/type-safety.md"
  - "cpp/lifetime/dangling-references.md"
supersedes: []
changelog:
  - "2026.06: Initial draft"
---

# STL Algorithms and Containers Checklist

**Based on:** ISO C++ [algorithms]/[containers] ([N]), C++ Core Guidelines SL.con-SL.str ([C]), SEI/CERT CTR50-CTR58 ([C]), Effective STL by Scott Meyers ([A]).

**Scope:** Apply STL algorithms correctly, choose the right container for the task, avoid iterator invalidation and bounds errors, respect algorithm preconditions, and avoid inheritance and misuse patterns. The STL is the most powerful and most misused library in C++. Most raw loops and hand-rolled data structures are both less expressive and less correct than their STL equivalents.

---

## Prerequisites / Concepts

### The STL Philosophy

The STL separates containers (data storage), algorithms (operations), and iterators (the glue between them). Writing a raw loop replicates algorithm logic inline, hiding intent and introducing opportunities for off-by-one errors, bounds violations, and iterator invalidation. A named algorithm documents what the code does; a raw loop documents only how.

| Concept | Definition |
|---------|-----------|
| **Container** | Owns a sequence of elements. `vector`, `list`, `map`, `unordered_set`, etc. |
| **Algorithm** | A generic function operating on iterator ranges. `std::find`, `std::sort`, `std::for_each`, etc. |
| **Iterator** | An abstraction of a position in a range. Input, output, forward, bidirectional, random-access. |
| **Iterator Invalidation** | A container operation that renders existing iterators, pointers, or references to elements invalid. Rules vary by container. |
| **Algorithm Precondition** | A requirement the caller must satisfy before invoking an algorithm (e.g., sorted range for `binary_search`). Violating a precondition is UB. |
| **Erase-Remove Idiom** | `c.erase(std::remove_if(c.begin(), c.end(), pred), c.end())` -- the correct way to conditionally remove elements from a sequence container. |
| **PMR (Polymorphic Memory Resources)** | C++17 allocator abstraction that allows switching memory strategies at runtime without changing container type. |

### Container Invalidation Quick Reference

| Container | Insert (reallocation) | Insert (no realloc) | Erase | Other |
|-----------|----------------------|---------------------|-------|-------|
| `vector` | All iterators/refs | Only if after insertion point | After erased element | `reserve` prevents realloc |
| `deque` | All iterators (refs to existing elements valid) | All iterators (middle); end only (front/back) | All (middle); end only (front/back) | |
| `list` | Never | Never | Only erased element | |
| `forward_list` | Never | Never | Only erased element | |
| `set`/`map` | Never | Never | Only erased element | |
| `unordered_set`/`map` | All if rehash | Never | Only erased element | Refs/pointers always valid |

---

## Checklist

### 1. Prefer Algorithms Over Raw Loops

Named algorithms express intent. Raw loops express mechanics. The reader must reverse-engineer the algorithm from the loop body, which is error-prone and obscures the purpose.

- [ ] A raw `for`/`while` loop traverses a container to find, count, transform, or accumulate elements? → **(N)** Replace with the named algorithm: `std::find`/`find_if`, `std::count`/`count_if`, `std::transform`, `std::accumulate`, `std::for_each`. [R1][R2]
- [ ] A raw loop copies elements that satisfy a predicate to an output container? → **(N)** Replace with `std::copy_if`. [R1]
- [ ] A raw loop removes elements matching a condition from a sequence container? → **(N)** Use the erase-remove idiom (Item 3). [R1][R2]
- [ ] A raw loop checks if any/all/none of the elements satisfy a predicate? → **(C)** Replace with `std::any_of`/`std::all_of`/`std::none_of`. [R2]
- [ ] Algorithm exists in C++17/20 parallel/range form that would improve performance or readability? → **(A)** Use `std::execution::par` or `std::ranges` equivalents where appropriate. [R4]

```cpp
// Good -- algorithm expresses intent
auto it = std::find_if(users.begin(), users.end(),
                       [](const auto& u) { return u.is_admin(); });

// Bad -- raw loop obscures intent; manual index management
User* admin = nullptr;
for (size_t i = 0; i < users.size(); ++i) {
    if (users[i].is_admin()) { admin = &users[i]; break; }
}
```

---

### 2. Iterator Invalidation Rules by Container Type

Every container documents which operations invalidate iterators, pointers, and references. Assuming "iterators are like pointers into stable memory" leads to use-after-free UB.

- [ ] Modifying a `std::vector` or `std::string` (push_back, emplace_back, insert, resize, erase) while holding iterators or references to its elements? → **(N)** Reallocation invalidates ALL iterators, pointers, and references. Insert/erase invalidates everything at or after the modification point. Use indices instead, or pre-reserve capacity. [R1][R3]
- [ ] Inserting into a `std::deque` anywhere except front/back? → **(N)** All iterators invalidated. Insert at front/back invalidates only `end()` iterator. References to existing elements remain valid. [R1]
- [ ] Erasing from `std::set`/`std::map`/`std::list`? → **(C)** Only iterators/references to the erased element are invalidated. Others are safe. Use `it = container.erase(it)` to advance correctly. [R2]
- [ ] Inserting into `std::unordered_map`/`std::unordered_set` triggering a rehash? → **(N)** All iterators invalidated (pointers and references to elements remain valid). Check `max_load_factor` and pre-reserve with `reserve()`. [R1]
- [ ] Storing an iterator as a long-lived member or cached value? → **(C)** Store an index or key instead. Recompute the iterator each time. [R2]

```cpp
// Good -- erase returns next valid iterator
for (auto it = m.begin(); it != m.end(); /* no increment here */) {
    if (should_remove(it->first))
        it = m.erase(it);  // returns next valid iterator
    else
        ++it;
}

// Bad -- erase then increment invalidated iterator = UB
for (auto it = v.begin(); it != v.end(); ++it) {
    if (it->expired())
        v.erase(it);  // it invalidated; ++it on next loop = UB
}
```

---

### 3. Erase-Remove Idiom

Calling `container.erase()` in a loop or on individual elements is verbose, error-prone (invalidation), and O(n^2) for vector. The erase-remove idiom is the canonical one-pass solution for conditionally removing elements from sequence containers.

- [ ] Removing elements from a `vector`, `deque`, or `string` by calling `erase()` on individual elements in a loop? → **(N)** Replace with `c.erase(std::remove_if(c.begin(), c.end(), pred), c.end())`. [R1][R2]
- [ ] Calling `std::remove()` or `std::remove_if()` without following with `.erase()`? → **(N)** `remove` only shifts elements; it does not change the container size. The trailing elements are in a moved-from state. Always pair with `.erase()`. [R1]
- [ ] Removing elements from associative containers (`map`, `set`)? → **(C)** Use member `erase(it)` in a loop with `it = container.erase(it)`, not the erase-remove idiom (which does not work for associative containers). [R2]
- [ ] C++20 available? → **(A)** Use `std::erase_if(container, pred)` -- a unified non-member function that works for all standard containers. [R4]

```cpp
// Good -- erase-remove idiom; O(n), correct
v.erase(std::remove_if(v.begin(), v.end(),
        [](int x) { return x < 0; }), v.end());

// C++20 -- even better
std::erase_if(v, [](int x) { return x < 0; });

// Bad -- erase in loop; O(n^2) for vector, invalidation risk
for (auto it = v.begin(); it != v.end();) {
    if (*it < 0)
        it = v.erase(it);  // each erase shifts remaining elements
    else
        ++it;
}
```

---

### 4. Bounds Checking

`operator[]` on `vector` and `array` has no bounds checking. Out-of-bounds access is UB. Defensive code should use bounds-checked access or verify indices explicitly.

- [ ] `operator[]` used with a runtime-computed index that could exceed the container size? → **(N)** Validate the index against `.size()` first, or use `.at()` which throws `std::out_of_range` on bounds violation. [R1][R2]
- [ ] Raw pointer plus offset from `.data()` used without bounds verification? → **(N)** Validate `offset < size` before dereference. Same UB risk as raw arrays. [R1]
- [ ] Function receives a pointer and a count (C-style API pattern)? → **(C)** Wrap in `std::span<T>` at the boundary. Spans carry the size but do not perform bounds checking themselves; pair with explicit checks. [R2]
- [ ] Iterator arithmetic (`it + n`) where `n` is not provably within `[0, distance(it, end)]`? → **(C)** Compute `distance(it, end())` first. Advancing past-the-end is UB for most iterator categories. [R2]
- [ ] **(A)** For release builds where `.at()` overhead is a concern, use `assert(index < size())` before `operator[]` to catch bounds errors in debug while removing the check in optimized builds. [R4]

```cpp
// Good -- bounds-checked access
if (index < v.size())
    process(v[index]);
else
    handle_error();

// Or equivalently
try {
    process(v.at(index));
} catch (const std::out_of_range&) {
    handle_error();
}

// Bad -- no bounds check; UB if index >= size
process(v[index]);  // compiler assumes index is always valid
```

---

### 5. Choosing the Right Container

The default container choice has a large impact on correctness and performance. `std::vector` is the correct default for the vast majority of cases. Other containers exist for specific access patterns.

- [ ] Need a dynamic sequence of elements? → **(C)** `std::vector` is the default. Contiguous storage, cache-friendly, amortized O(1) push_back. [R1][R2]
- [ ] Need key-value lookup with ordering requirements (enumeration in sorted order, range queries)? → **(C)** `std::map` (tree-based, O(log n)). If only `operator[]`/`find` is needed and ordering does not matter, use `std::unordered_map` (hash-based, amortized O(1)). [R2][R4]
- [ ] Need FIFO/LIFO queue behavior? → **(C)** Use `std::deque` as the default backing store for `std::queue` and `std::stack`. `deque` avoids the per-element allocation overhead of `list` and the reallocation cost of `vector` at the front. [R2][R4]
- [ ] Need stable iterators/pointers to elements after insertion? → **(N)** Do not use `vector` or `deque` without reserving capacity. Use `std::list` (sequential) or `std::map`/`std::set` (associative) where insert/erase never invalidates other iterators. [R1]
- [ ] Need a fixed-size array whose size is known at compile time? → **(C)** Prefer `std::array<T, N>` over C-style arrays. It does not decay to a pointer, preserves size information, and supports STL algorithms. [R2]
- [ ] Using `std::list` as the default sequential container? → **(A)** Re-evaluate. `std::list` has per-element allocation overhead, poor cache locality, and O(n) random access. `vector` is almost always the right choice even when "inserting in the middle." Profile before switching. [R4]

---

### 6. Algorithm Preconditions

Many STL algorithms have preconditions that, when violated, produce undefined behavior. The compiler cannot check these -- the caller is responsible.

- [ ] Calling `std::binary_search`, `std::lower_bound`, `std::upper_bound`, `std::equal_range` on an unsorted range? → **(N)** UB. The range must be partitioned with respect to the comparison. Call `std::sort` or `std::stable_sort` first, or check `std::is_sorted` before invoking. [R1][R3]
- [ ] Calling `std::push_heap`, `std::pop_heap`, `std::sort_heap` on a range that is not a valid max-heap? → **(N)** UB. The range `[first, last-1)` must already be a valid heap. Build it with `std::make_heap` first. Verify with `std::is_heap` in debug. [R1]
- [ ] Calling `std::merge`, `std::set_union`, `std::set_intersection`, `std::set_difference` on unsorted input ranges? → **(N)** Both input ranges must be sorted. Same requirement as binary search. [R1]
- [ ] Calling `std::next_permutation`, `std::prev_permutation` on an unsorted range? → **(C)** The range must be sorted in the appropriate order for the first call to enumerate all permutations. [R2]
- [ ] Passing an empty range to `std::min_element`, `std::max_element`, or `std::minmax_element`? → **(N)** Dereference of the returned iterator is UB. Always check `first != last` or test the result against `end()`. [R1]
- [ ] Passing a range to `std::nth_element` or `std::partial_sort` with `nth` or `middle` out of bounds? → **(N)** `nth` and `middle` must be dereferenceable iterators within the range. [R1]

```cpp
// Good -- ensure sorted preconditions before binary search
std::sort(v.begin(), v.end());
if (std::binary_search(v.begin(), v.end(), target))
    handle_found();

// Debug-mode precondition check
assert(std::is_sorted(v.begin(), v.end()));
auto it = std::lower_bound(v.begin(), v.end(), target);

// Bad -- binary search on unsorted range = UB
auto found = std::binary_search(v.begin(), v.end(), target);  // range may be unsorted
```

---

### 7. Avoid Inheriting from STL Containers

STL container destructors are not virtual. Public inheritance from an STL container invites deletion through a base pointer, which is UB. It also couples client code to the container's concrete type, reducing flexibility.

- [ ] Defining a class that publicly inherits from `std::vector`, `std::map`, or any STL container? → **(N)** STL containers have non-virtual destructors. Deletion through a base pointer is UB per [expr.delete]. Use composition (container as a private member) or non-member functions instead. [R1][R2]
- [ ] Need to add convenience methods to container-like behavior? → **(C)** Use free functions operating on the standard container type, or (if encapsulation is required) wrap the container in a class with private inheritance or a member variable. [R2]
- [ ] Private inheritance from an STL container? → **(C)** Acceptable only if no external code can delete through a pointer to the base class. Composition is clearer and preferred. [R2][R4]

```cpp
// Good -- composition over inheritance
class UserCache {
public:
    void add(User u) {
        auto it = std::find_if(users_.begin(), users_.end(),
                              [&](const auto& e) { return e.id == u.id; });
        if (it != users_.end()) *it = std::move(u);
        else users_.push_back(std::move(u));
    }
private:
    std::vector<User> users_;  // owned by value, not inherited
};

// Bad -- inheriting from non-virtual-dtor base
class UserList : public std::vector<User> {  // vector has no virtual dtor
public:
    User* find_by_id(int id) {
        auto it = std::find_if(begin(), end(),
                              [id](const auto& u) { return u.id == id; });
        return it != end() ? &*it : nullptr;
    }
};
// std::vector<User>* p = new UserList; delete p;  // UB: ~vector() called, not ~UserList()
```

---

### 8. Custom Allocators and PMR

Most STL containers use the default heap allocator (`std::allocator<T>`). For performance-critical or memory-constrained scenarios, custom allocators and C++17 PMR allow tuning memory strategies without changing container types.

- [ ] Performance profiling shows allocation/deallocation as a bottleneck? → **(A)** Consider a pool allocator, arena allocator, or `std::pmr::monotonic_buffer_resource` for monotonic workloads. PMR allows switching strategies at runtime without recompiling. [R4]
- [ ] Container elements are allocated from shared memory, memory-mapped files, or device memory? → **(C)** Use a custom allocator that maps to the specific memory region. PMR's `std::pmr::polymorphic_allocator` is the modern approach. [R2]
- [ ] Need to switch allocation strategy per-call-site without changing container type? → **(C)** Use `std::pmr::vector<T>` (alias for `std::vector<T, std::pmr::polymorphic_allocator<T>>`) with `std::pmr::memory_resource*` passed at construction. The same container type works with any memory resource. [R4]
- [ ] Allocator is stateful and propagated inconsistently across copies/moves? → **(N)** Allocator propagation traits (`propagate_on_container_copy_assignment`, `propagate_on_container_move_assignment`, `propagate_on_container_swap`) must be correct. Inconsistent propagation leads to elements owned by the wrong allocator -- UB on deallocation. [R1]
- [ ] **(A)** Reserve `std::pmr::synchronized_pool_resource` for multi-threaded allocation scenarios; `std::pmr::unsynchronized_pool_resource` for single-threaded. The default `std::pmr::new_delete_resource` simply wraps `new`/`delete` and provides no performance benefit. [R4]

```cpp
// Good -- PMR for scoped, predictable allocation
std::array<std::byte, 4096> buffer;  // stack-based arena
std::pmr::monotonic_buffer_resource arena(buffer.data(), buffer.size());
std::pmr::vector<std::pmr::string> strings(&arena);
// All allocations for strings and their elements come from the arena.
// No heap interaction; all memory freed when buffer goes out of scope.

// Bad -- default allocator for thousands of small, short-lived containers
for (int i = 0; i < 100000; ++i) {
    std::vector<int> v = build_small_vector();  // heap alloc + free each iteration
    process(v);
}
// Consider an arena allocator reused across iterations.
```

---

## Decision Tree

```
STL decision point:
  │
  ├─ Writing a loop over a container?
  │     ├─ Finding/counting/transforming? → [Item 1] Named algorithm
  │     ├─ Removing by condition? → [Item 3] Erase-remove idiom
  │     └─ Truly custom per-element logic? → OK, but check invalidation [Item 2]
  │
  ├─ Choosing a container type?
  │     ├─ Default sequence? → [Item 5] std::vector
  │     ├─ Insert/erase in middle, need stable iterators? → [Item 5] std::list
  │     ├─ Key-value, ordered? → [Item 5] std::map
  │     ├─ Key-value, unordered? → [Item 5] std::unordered_map
  │     ├─ FIFO/LIFO? → [Item 5] std::deque (backing std::queue/stack)
  │     └─ Fixed compile-time size? → [Item 5] std::array
  │
  ├─ Accessing elements by index?
  │     └─ Runtime-computed index? → [Item 4] Bounds-check with .at() or explicit check
  │
  ├─ Calling a named algorithm?
  │     ├─ binary_search/lower_bound/merge? → [Item 6] Ensure sorted precondition
  │     ├─ push_heap/pop_heap? → [Item 6] Ensure valid heap precondition
  │     └─ min_element/max_element? → [Item 6] Check range non-empty first
  │
  ├─ Extending container behavior?
  │     └─ Considering inheritance? → [Item 7] Composition over inheritance
  │
  └─ Allocation a bottleneck?
        └─ Profile shows overhead? → [Item 8] Consider PMR or custom allocator
```

---

## Anti-Patterns / Common Mistakes

### Anti-Pattern 1: The Raw Loop Reflex

- **Appearance:** Every traversal, search, filter, or transformation is written as a `for` loop. The developer knows STL algorithms exist but "a loop is easier to write."
- **Trap:** Writing a loop is faster in the moment but slower to review, test, and maintain. The loop encodes the "how" but obscures the "what." Each loop re-invents bounds checking, iteration logic, and termination conditions.
- **Consequence:** Off-by-one errors. Invalidation bugs when loops modify containers. Reviewers must mentally execute the loop to understand its purpose. Optimization opportunities (parallel algorithms, range views) are invisible.
- **Fix:** Train the reflex to ask "is there an algorithm for this?" before typing `for`. If the algorithm name (`find_if`, `any_of`, `transform`, `remove_if`) describes the intent, use it.

### Anti-Pattern 2: Vector as the Universal Container

- **Appearance:** `std::vector` used for everything: queues, sorted key-value lookups, frequent middle insertions, graphs represented as vector-of-vectors.
- **Trap:** `vector` is the right default, but not the right universal container. Using `vector` for queue semantics means `erase(begin())` which is O(n). Using `vector` for maps means manual sorted-insert or linear search which is O(n) or O(n^2).
- **Consequence:** Accidental quadratic complexity. Code that works correctly for small N but degrades catastrophically at scale. Iterator invalidation surprises from reallocation.
- **Fix:** Match the container to the dominant access pattern (Item 5). Use `std::queue<T>` (backed by `deque`) for FIFO, not `vector`. Use `std::map` or `std::unordered_map` for associative lookup, not a sorted vector with binary_search.

### Anti-Pattern 3: Inheriting to Add Methods

- **Appearance:** `class StringList : public std::vector<std::string> { ... };` to add `find_case_insensitive`, `join`, `split` methods.
- **Trap:** Inheritance feels like the natural OOP way to extend a container with domain methods. The base class destructor is non-virtual, but the developer never intends `delete` through a base pointer, so "it's fine."
- **Consequence:** Another developer, or even the same developer months later, stores the object as `std::vector<std::string>*` and calls `delete`. Non-virtual destructor = UB. Separately, public inheritance exposes the entire `vector` API permanently -- changing to a different container later requires rewriting all callers.
- **Fix:** Wrap the container as a private member. Expose only the needed operations. Free functions can also add convenience without coupling to the container type.

### Anti-Pattern 4: Assuming Algorithms Check Preconditions

- **Appearance:** `std::binary_search(v.begin(), v.end(), x)` called on a vector, assuming the algorithm handles both sorted and unsorted inputs correctly.
- **Trap:** The name "binary_search" sounds like it just "searches binary." The developer may not realize "binary" refers to the algorithm technique (binary subdivision of a sorted range), not the data type.
- **Consequence:** Binary search on an unsorted range returns arbitrary results (not "not found"). It does not error, crash, or warn. It silently produces wrong answers -- the worst kind of bug.
- **Fix:** For any algorithm with a sorted-range or valid-heap precondition, audit the call sites. Add `std::is_sorted` assertions in debug builds. Sort the range before the algorithm call if it may not be sorted.

---

## See Also

- [Undefined Behavior Prevention](undefined-behavior.md) -- Algorithm precondition violations, out-of-bounds access, and iterator invalidation all produce UB
- [Type Safety and Implicit Conversions](type-safety.md) -- Container value types, comparison functors, and allocator types interact with the type safety rules
- [Object Lifetime and Dangling References](../lifetime/dangling-references.md) -- Iterator/reference invalidation is a lifetime problem; dangling views and captures intersect with STL usage

---

## Reference Sources

| Label | Tier | Source | Clause | Timeliness | Last Verified |
|-------|------|--------|--------|------------|---------------|
| R1 | N | ISO C++ Standard | [algorithms], [containers.general], [sequence.reqmts], [associative.reqmts], [unord.req], [expr.delete] | verified-2026 | 2026-06 |
| R2 | C | C++ Core Guidelines | SL.con.1-SL.con.4, SL.str.1-SL.str.5, SL.io.1-SL.io.5, ES.70-ES.76 | verified-2026 | 2026-06 |
| R3 | C | SEI/CERT C++ Coding Standard | CTR50-CPP through CTR58-CPP | verified-2026 | 2026-06 |
| R4 | A | Effective STL (Scott Meyers, 2001) | Items 1-50 | verified-2026 | 2026-06 |

---

## Changelog

- 2026.06: Initial draft -- 8 checklist items covering algorithm preference, iterator invalidation, erase-remove, bounds checking, container selection, algorithm preconditions, inheritance avoidance, and custom allocators/PMR
