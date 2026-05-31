# Prompt: Create a New Harness

Use this template with an AI agent to create a new dev-guidelines harness.

## Template

```
Create a new harness for dev-guidelines on: "{TOPIC}"
Language: {cpp|common}
Category: {category}

Step 1: Identify 2-4 authoritative sources:
- At least one C-tier (Consensus) source
- Preferably one N-tier (Normative) if applicable
- A-tier for depth and examples

Step 2: Use the template format from templates/harness.template.md.

Step 3: Define 5-10 checklist items. Each:
- Has a clear yes/no condition
- Has an action for each branch
- Tagged (N), (C), or (A)
- References a specific source clause

Step 4: Include:
- Prerequisites/concepts section
- Quick decision tree (ASCII art)
- 2-3 anti-patterns: Appearance → Trap → Consequence → Fix
- Reference sources table with timeliness tags

Step 5: Cross-reference related harnesses (bidirectional).

Harness template:
{HARNESS_TEMPLATE_CONTENT}

Source registry:
{REFERENCES_SOURCES_CONTENT}
```

## Tips

- Items should be independently checkable — mark them one by one.
- Anti-patterns should describe things that SEEM correct — not obvious mistakes.
- Decision tree should be usable standalone — a reviewer follows it without reading every item.
- Cross-reference liberally. Harnesses form a knowledge graph, not isolated docs.
