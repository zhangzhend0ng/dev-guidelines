# Roadmap

For the larger multi-language, planning, debugging, and pack distribution strategy, see [Capability Roadmap](docs/strategy/2026-06-15-capability-roadmap.md).
For the execution checklist, see [AI Task Checklist](docs/strategy/2026-06-15-ai-task-checklist.md).

## Phase 1 (Current)

| Priority | Topic | Language | Category | Effort |
|----------|-------|----------|----------|--------|
| 1 | RAII and Resource Management | cpp | resource-management | M |
| 2 | Smart Pointer and Ownership | cpp | resource-management | M |
| 3 | Const Correctness | cpp | correctness | M |
| 4 | Input Validation | common | security | M |
| 5 | Error Handling Strategy | common | design | L |
| 6 | AI-Assisted C++ Development | common | ai | M |
| 7 | Tool Calling and Agent Control | common | ai | M |
| 8 | Model Capability and Instruction Adherence | common | ai | M |
| 9 | C++ Static Analysis | cpp | testing | M |
| 10 | C++ Toolchain and Compiler Flags | cpp | build | M |
| 11 | C++ Secure Coding | cpp | security | M |
| 12 | C++ ABI Compatibility | cpp | api | M |
| 13 | C++ Module Boundaries | cpp | architecture | M |
| 14 | C++ Result vs Exception | cpp | design | M |
| 15 | C++ Fuzzing | cpp | testing | M |
| 16 | C++ Property-Based Testing | cpp | testing | M |
| 17 | C++ Parsing and Validation | cpp | serialization | M |
| 18 | C++ Mutation Testing | cpp | testing | M |
| 19 | C++ Runtime Observability and Diagnostics | cpp | runtime | M |
| 20 | C++ Sanitizer Triage | cpp | debugging | M |
| 21 | C++ Crash Dump Analysis | cpp | debugging | M |
| 22 | C++ Flaky Test Triage | cpp | debugging | M |

## Phase 2 (Next)

| Priority | Topic | Language | Category | Effort |
|----------|-------|----------|----------|--------|
| 23 | Undefined Behavior Prevention | cpp | correctness | L |
| 24 | Exception Safety Guarantees | cpp | correctness | L |
| 25 | Move Semantics / Rule of Five | cpp | resource-management | M |
| 26 | Concurrency and Thread Safety | cpp | correctness | XL |
| 27 | Object Lifetime and Dangling | cpp | correctness | M |

## Phase 3+

Pack export workflow, Python core pack, Rust core pack, Go core pack.
Future AI modules: RAG and context management, model selection and change management, AI UX and disclosure.

## Planned Languages

| Language | Status |
|----------|--------|
| python | planned |
| go | planned |
| rust | planned |
