# Listwise Loss Functions — March 2026

**Owner:** Tariq Al-Rashid  
**Status:** Complete  
**Related:** `2025-11-temperature-sweep.md`

## Background

We've been using pointwise and pairwise losses. Listwise losses (e.g., ListNet, LambdaRank) optimize ranking metrics directly and might better align training with our NDCG@10 eval metric.

## Experiment Design

Three loss variants compared:

1. **Pointwise BCE** (current baseline)
2. **Pairwise BPR** (Bayesian Personalized Ranking)
3. **Listwise LambdaRank** (NDCG-approximating)

All trained on the same data with the same architecture (dual_encoder_v2, τ=0.06, mixed negatives). 5-fold cross-validation to reduce variance.

## Results (mean ± std across folds)

| Loss | Recall@50 | NDCG@10 | Training hrs/fold |
|---|---|---|---|
| Pointwise BCE | 0.559 ± 0.008 | 0.388 ± 0.006 | 6.1 |
| Pairwise BPR | 0.563 ± 0.007 | 0.397 ± 0.005 | 7.4 |
| LambdaRank | 0.558 ± 0.009 | 0.411 ± 0.006 | 8.9 |

## Interpretation

- LambdaRank wins on NDCG (as expected — it directly optimizes it) but barely changes Recall.
- BPR is a reasonable middle ground: small NDCG improvement, modest Recall improvement, less training overhead than LambdaRank.
- For our reranker (where NDCG is primary), LambdaRank is worth the cost. For first-stage retrieval (where Recall dominates), BPR is better.

## Decisions

- First-stage retrieval: switch to BPR from BCE
- Reranker: switch to LambdaRank
- Update `configs/retrieval_loss.yaml` and `configs/reranker_loss.yaml`

## PR

PR #2134 (retrieval) and PR #2135 (reranker) — both under review.
