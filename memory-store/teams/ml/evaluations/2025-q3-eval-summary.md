# Q3 2025 Eval Summary

**Period:** July 1 – September 30, 2025

## Highlights

Q3 was relatively stable. We shipped two model updates:
- `rec-v2.4.1` in mid-July (lightweight tuning on new user cohort)
- `rec-v2.5.0` in mid-September (new item embedding tower with contrastive loss)

`rec-v2.5.0` was the more significant change and showed clear improvements in tail-item coverage.

## Metric Summary (end-of-quarter, rec-v2.5.0)

| Metric | Q2 2025 | Q3 2025 | Change |
|--------|---------|---------|--------|
| Precision@10 | 0.78 | 0.79 | +0.01 |
| Recall@50 | 0.71 | 0.73 | +0.02 |
| NDCG@20 | 0.63 | 0.64 | +0.01 |
| Tail-item Recall@50 | 0.48 | 0.56 | +0.08 ✅ |
| P95 Latency (ms) | 118 | 121 | -3ms ⚠️ |

The tail-item recall jump is the standout number. The contrastive loss in the new item tower is doing what we hoped.

Latency uptick is minor but worth monitoring — the new embedding tower is slightly larger.

## Issues

### Position Bias Investigation
Started a formal investigation into offline-online delta widening (see `offline-vs-online-delta.md`). No concrete fix landed in Q3 but we validated the hypothesis and IPS labels are being generated for Q4.

### Holdout Set Age
The Q3 holdout set was still the July window by end of September — we didn't rotate mid-quarter as discussed. This should not repeat. See `eval-set-rotation.md`.

## Q4 Intentions

- Land IPS debiasing
- Deploy `rec-v2.6.0` targeting NDCG improvements
- Do not let holdout set go stale again

## Artifacts

- Holdout set: `gs://ml-evals/holdout/2025-q3/`
- Full metric tables: `ml_evals.results` where `holdout_id = '2025-q3'`
