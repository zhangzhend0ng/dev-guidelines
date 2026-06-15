# Model Registry

This registry records model capability for this repository. Capability is assigned by local eval results, not by model branding.

| Model | Version | Default Tier | Approved Tasks | Blocked Tasks | Last Eval | Notes |
|-------|---------|--------------|----------------|---------------|-----------|-------|
| unknown / unevaluated | n/a | T0/T1 | summarize, classify, harness selection draft | code edits, autonomous tools, approval verdicts | n/a | Must use weak-model workflow |
| dsv4pro | TBD | T1 | harness selection, short plans, bounded explanations | autonomous edits, approval verdicts, unverified patch claims | TBD | Promote only after eval report |

## Tier Policy

- T0/T1: no code edits without approval.
- T2: small bounded patch allowed after plan approval and protocol check.
- T3: multi-file subsystem work allowed only after repository-specific eval pass.
- T4: autonomous tool workflow requires tool-control harness, CI evidence, and human approval gates.

## Promotion Rule

1. Run weak-model eval cases.
2. Generate an evaluation report.
3. Update this registry in the same change.
4. Promote only the task class that passed; do not generalize.

