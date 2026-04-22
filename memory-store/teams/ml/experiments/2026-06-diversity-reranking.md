# Diversity-Aware Reranking — June 2026

**Owner:** Priya Nair  
**Status:** Pilot

## Background

User research (shared by the product team in `../product/user-research-june2026.pdf`) found that result pages dominated by a single brand or format frustrate users even when individual items are highly relevant. We want to incorporate diversity into the reranking stage.

## Approach

Maximal Marginal Relevance (MMR) post-processing on top of the cross-encoder reranker scores:

```
score_mmr(d) = λ · relevance(d) - (1 - λ) · max_{d' in S} sim(d, d')
```

Tuning λ on held-out set with human preference labels from our annotation team.

## λ Sweep Results

| λ | NDCG@10 | Brand Coverage@10 | User Preference (annotator) |
|---|---|---|---|
| 1.0 (no diversity) | 0.431 | 2.1 brands | 3.41/5 |
| 0.8 | 0.419 | 3.4 brands | 3.67/5 |
| 0.7 | 0.408 | 4.1 brands | 3.78/5 |
| 0.6 | 0.389 | 5.0 brands | 3.71/5 |

λ=0.7 maximizes annotator preference while keeping NDCG degradation under 6%.

## Trade-off Discussion

There's genuine tension here. Some stakeholders (merchandising) care about promoting specific brands. Need alignment from Product on acceptable NDCG sacrifice before we ship. Raised in eng-product sync 2026-06-04.

## Next Steps

- [ ] A/B test λ=0.7 vs. λ=1.0 on 5% of traffic
- [ ] Instrument brand diversity metrics in the serving dashboard
- [ ] Check if per-category λ tuning makes sense (apparel may prefer more diversity than electronics)
