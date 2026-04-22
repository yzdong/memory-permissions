# Hard Negative Mining Experiment — November 2025

## Background
In-batch negatives are cheap but produce easy negatives. The dual encoder from October still struggles on navigational queries where the correct item ranks ~150 in ANN search.

## Hypothesis
Mining hard negatives from the top-200 ANN results (excluding ground truth) and mixing them at 4:1 ratio with in-batch negatives will push recall@100 above 0.80.

## Experiment Config
```yaml
neg_mining:
  strategy: ann_top_k
  k: 200
  exclude_positives: true
  hard_neg_ratio: 0.8
  in_batch_ratio: 0.2
training:
  epochs: 3
  warmup_steps: 3000
  lr: 2e-4
```

## Runs
1. `run-hn-4to1` — 4 hard : 1 in-batch
2. `run-hn-2to1` — 2 hard : 1 in-batch (sanity check)
3. `run-hn-online` — real-time mining per batch (expensive, ran 1 epoch only)

## Results

| Run | Recall@100 | MRR@10 | Train loss (final) |
|---|---|---|---|
| baseline (Oct dual-enc) | 0.78 | 0.46 | 0.31 |
| run-hn-2to1 | 0.81 | 0.48 | 0.27 |
| run-hn-4to1 | 0.83 | 0.49 | 0.25 |
| run-hn-online | 0.82 | 0.48 | 0.24 |

The 4:1 ratio is the sweet spot. Online mining didn't improve over 4:1 static and cost 3× compute.

## Caveats
- Hard negatives make training brittle if the ANN index is stale. We refreshed index every 500k steps.
- Tail queries (< 5 impressions/month) still underperform. Separate cold-start work tracked in `cold-start-experiment.md`.

## Next Steps
- Merge run-hn-4to1 weights into `models/retrieval/dual-encoder-v2`
- Schedule a reranker comparison on top of this retrieval layer — see `2026-02-reranker-ablation.md`
