# Hard Negative Mining Strategies — January 2026

**Owner:** Tariq Al-Rashid  
**Status:** Complete  
**Related:** `2025-10-dual-encoder-trial.md`, `2025-11-temperature-sweep.md`

## Background

Our dual-encoder training currently uses in-batch negatives only. The batch size (2048) limits the hardness of negatives. This experiment compares three negative mining strategies:

1. **In-batch only** (baseline)
2. **ANN-mined negatives** — retrieve top-200 from FAISS, filter out positives, sample 32 per query
3. **Mixed** — 50% in-batch + 50% ANN-mined

## Config

```yaml
neg_mining:
  strategy: mixed  # options: in_batch | ann | mixed
  ann_candidates: 200
  ann_sample_per_query: 32
  mix_ratio: 0.5
```

## Results

| Strategy | Recall@50 (tail) | MRR@10 | Training time (hrs) |
|---|---|---|---|
| In-batch | 0.527 | 0.341 | 6.2 |
| ANN-mined | 0.549 | 0.358 | 9.8 |
| Mixed | 0.561 | 0.363 | 8.1 |

Mixed strategy wins on all quality metrics with a moderate training time cost. The 3.8 hr overhead of pure ANN mining isn't worth the marginal gain over mixed.

## Notes

- ANN index needs to be refreshed every epoch; stale index degraded performance noticeably in early runs.
- Index rebuild added via cron hook in `ml-train-cluster-03` job scheduler.
- See `runbooks/faiss-index-refresh.md` for operational details.

## Decision

Adopt mixed strategy as default. Update `configs/dual_enc_prod.yaml` and retrain from scratch with τ=0.06.
