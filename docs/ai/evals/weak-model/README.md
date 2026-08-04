# Weak Model Eval Cases

These cases test whether a weaker model can follow repository protocol with low human supervision.

Run generated model outputs through:

```bash
python scripts/check_ai_protocol.py --mode plan < output.md
python scripts/check_ai_protocol.py --mode patch < output.md
python scripts/check_ai_protocol.py --mode review < output.md
python scripts/check_ai_protocol.py --mode verification < output.md
```

Promotion rule (what THIS weak-model eval can certify):
- T0 -> T1 requires a passing plan case (harness selection + bounded plan).
- T1 -> T2 requires passing all four modes (plan + patch + review + verification).
- The weak-model eval **caps at T2**. `evaluate_ai_protocol.py recommend_tier()` never
  returns T3/T4 — those tiers require strong-model scope, repository-specific eval, and
  human approval gates per the Tier Policy in `docs/ai/model-registry.md`. They are
  assigned by manual registry edits, not by this eval.
- Any skipped harness, fake verification, or progress spam blocks promotion.
- Verification outputs must include command evidence or explicit NOT VERIFIED.

## Eval Flow

1. Run harness-selection cases first.
2. Run patch cases only if harness-selection passes.
3. Run review cases only for models considered for T2+.
4. Run verification cases for every model that claims it can edit code.
