# Weak Model Eval Cases

These cases test whether a weaker model can follow repository protocol with low human supervision.

Run generated model outputs through:

```bash
python scripts/check_ai_protocol.py --mode plan < output.md
python scripts/check_ai_protocol.py --mode patch < output.md
python scripts/check_ai_protocol.py --mode review < output.md
python scripts/check_ai_protocol.py --mode verification < output.md
```

Promotion rule:
- T1 -> T2 requires passing all plan cases and at least one bounded patch case.
- T2 -> T3 requires passing patch and review cases with verification evidence.
- Any skipped harness, fake verification, or progress spam blocks promotion.
- Verification outputs must include command evidence or explicit NOT VERIFIED.

## Eval Flow

1. Run harness-selection cases first.
2. Run patch cases only if harness-selection passes.
3. Run review cases only for models considered for T2+.
4. Run verification cases for every model that claims it can edit code.
