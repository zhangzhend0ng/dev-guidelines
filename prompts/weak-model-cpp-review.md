# Prompt: Weak-Model C++ Review

Use this to make a weaker model review a bounded diff without producing broad commentary.

```
Review this C++ diff against the listed harnesses.

Rules:
- Findings first, ordered by severity.
- Every finding must cite file:line.
- Every finding must name the harness and checklist item.
- Start each finding line with its checklist item, exactly:
  "Item N: PASS" or "Item N: FAIL — <reason with file:line>".
  Lines that only say "FAIL ..." without the Item N prefix cannot be
  matched back to a checklist item and are logged as protocol gaps.
- Do not include pass-only checklist items unless needed for coverage.
- Do not give a verdict unless every applicable harness item was checked.
- If evidence is missing, say NOT VERIFIED.

Harnesses:
{HARNESSES}

Diff:
{DIFF}

Required output:
Blocking findings:
High findings:
Suggestions:
Harness coverage:
Verdict:
```

