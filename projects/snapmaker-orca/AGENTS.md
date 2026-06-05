# AGENTS.md — SnapmakerOrca Project Guidelines

You are working on SnapmakerOrca (OrcaSlicer fork for Snapmaker). Apply shared `dev-guidelines` harnesses at `../../INDEX.md` plus the project-specific harness below.

## Inherited Harnesses (always apply)

- `cpp/memory/raii.md`
- `cpp/memory/ownership.md`
- `cpp/correctness/const-correctness.md`
- `cpp/correctness/type-safety.md`
- `cpp/correctness/undefined-behavior.md`
- `cpp/correctness/integer-safety.md`
- `cpp/concurrency/thread-safety.md`
- `cpp/functions/parameter-validation.md`
- `common/security/input-validation.md`

## Project-Specific Harness

[SnapmakerOrca Coding Standards](coding-standards.md) — overrides:

| Shared Rule | SnapmakerOrca Override |
|------------|----------------------|
| C++20 allowed | **C++11/14 only** |
| Exceptions allowed | **Disabled — error codes only** |
| Brace style unspecified | **Allman mandatory** |
| Function <40 lines | **≤150 lines** |
| auto OK where clear | **Avoid where type unclear** |
| strcpy discouraged | **Forbidden — use strcpy_s** |
| malloc/free discouraged | **Forbidden in application code** |

## Key Differences

1. No exceptions — bool/int return codes
2. C++11/14 — no C++17 structured bindings, CTAD, if-init
3. Allman braces — each brace on own line
4. No Chinese in source; UTF-8 BOM encoding
5. Doxygen comments on all functions/classes
6. Win32 safe APIs: strcpy_s, sprintf_s, memcpy_s
