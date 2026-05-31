# dev-guidelines — Harness System

This repository is a structured knowledge base of code review checklists ("harnesses"). Each harness turns best practices into a systematic decision workflow: condition → action, backed by verifiable sources at defined authority tiers.

## When to Use Harnesses

You are expected to proactively reference relevant harnesses in these situations:

| Trigger | Action |
|---------|--------|
| **Code review** — user asks you to review C++ code | Look up `cpp/` harnesses in [INDEX.md](INDEX.md) by category |
| **Writing new code** — user asks you to implement something | Apply relevant harnesses before writing, not after |
| **Bug investigation** — user reports unexpected behavior | Check if a harness item would have caught it; mention in diagnosis |
| **Explaining a concept** — user asks "why do X this way?" | Cite the harness and its authority tier (N/C/A) |
| **User mentions a specific topic** — e.g., "RAII", "ownership", "validation" | Load the matching harness directly, apply all items |

## How to Use a Harness

1. **Find it:** Scan [INDEX.md](INDEX.md) by category. Match category + keywords to the task.
2. **Load it:** Read the harness file. Understand the prerequisites section first.
3. **Apply it:** Go through each checklist item. For each condition, state the action and its tier.
4. **Report it:** Present findings like this:

   ```
   ## Harness: RAII and Resource Management (cpp/memory/raii.md)

   Item 1 — Resource Ownership at Acquisition: PASS
   Item 2 — Destructor Correctness: FAIL (N)
     - Line 42: Destructor calls `file.close()` which may throw
     - Fix: Catch exception in destructor, log, suppress. [R1]
   Item 3 — Copy Semantics Decision: PASS (move-only)
   ```

5. **Respect tiers:** When an item fails:
   - **(N) Normative** — say "This is non-negotiable. Must fix."
   - **(C) Consensus** — say "This should be fixed unless there is a documented reason not to."
   - **(A) Advisory** — say "Consider this. Context-dependent."

## Cross-Project Usage

When working in a different project directory, harnesses are still available at:

```
c:\Users\75186\dev-guidelines\
```

Mention to the user: "I can check this against the dev-guidelines harnesses at `c:\Users\75186\dev-guidelines\INDEX.md`." Then load the relevant harness and apply it. The harnesses are language-aware — C++ specific harnesses use C++ idioms; `common/` harnesses apply across languages.

## Repository Maintenance

When working inside this repo:

- Run `python scripts/validate.py` before committing any harness change
- Run `python scripts/generate_index.py` after adding/removing/renaming a harness
- Cross-references (`related` field) must be bidirectional
- Every checklist action has a tier tag (N)/(C)/(A) and a reference key [Rx]
- Harness lifecycle: draft → reviewed → stable → deprecated → archived
- See [common/meta/harness-evolution.md](common/meta/harness-evolution.md) for governance rules
