# Temperature Parameter Sweep — November 2025

**Owner:** Marcus Webb  
**Status:** Complete  
**Linked experiment:** `2025-10-dual-encoder-trial.md`

## Motivation

After the dual-encoder trial we noticed that changing τ (softmax temperature) had an outsized effect on hard-negative separation. We wanted to map the loss landscape systematically rather than hand-tune.

## Setup

Sweep τ ∈ {0.04, 0.05, 0.06, 0.07, 0.08, 0.10} with everything else fixed.

- Model checkpoint: `checkpoints/dual_encoder_v1_epoch4`
- Fine-tune for 1 additional epoch per τ value
- Eval: same held-out Q3 set

```python
for tau in [0.04, 0.05, 0.06, 0.07, 0.08, 0.10]:
    run_experiment(config_override={"temperature": tau}, tag=f"tau_{tau}")
```

## Results

| τ | Recall@50 (tail) | NDCG@10 | Loss (val) |
|---|---|---|---|
| 0.04 | 0.511 | 0.382 | 2.14 |
| 0.05 | 0.529 | 0.391 | 2.08 |
| 0.06 | 0.538 | 0.397 | 2.04 |
| 0.07 | 0.527 | 0.394 | 2.06 |
| 0.08 | 0.519 | 0.388 | 2.09 |
| 0.10 | 0.498 | 0.371 | 2.18 |

τ=0.06 is the clear winner on both metrics. The curve is fairly flat between 0.05–0.07 so we have some robustness.

## Observations

- Lower τ values push the model toward over-confident logits; training becomes unstable below τ=0.03 (not shown).
- The optimal τ likely shifts if we change the hard-negative mining strategy — worth revisiting if we adopt `runbooks/hard-neg-mining.md` approach.

## Decision

Set τ=0.06 as default in `configs/dual_enc_prod.yaml`. Merged via PR #1847.
