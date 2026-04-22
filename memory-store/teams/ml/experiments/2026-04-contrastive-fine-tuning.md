# Contrastive Fine-Tuning on User Feedback — April 2026

**Owner:** @marco, @lena  
**Hypothesis:** Fine-tuning the dual encoder on explicit negative feedback (thumbs down, "not relevant" flags) via contrastive loss will reduce bad-fit recommendations.

## Data
- Positive signal: clicks with dwell time > 30s, purchases, add-to-wishlist
- Negative signal: explicit "not relevant" flags + clicks with immediate back-navigation (< 3s)
- Dataset: 8.4M positive pairs, 1.2M explicit negatives, 6.1M implied negatives
- Ratio concern: negatives are sparse. Used oversampling for explicit negatives.

## Loss Function
SupCon loss with temperature τ = 0.07:
```
L = -log [ exp(sim(q, p+)/τ) / Σ_k exp(sim(q, n_k)/τ) ]
```
where n_k includes both hard negatives and explicit negatives.

## Results After 3 Epochs

| Metric | Before | After |
|---|---|---|
| Recall@100 | 0.83 | 0.82 |
| MRR@10 | 0.55 | 0.57 |
| Explicit negative hit rate (bad recs shown) | 3.2% | 1.8% |
| User-reported irrelevance rate (A/B) | — | −22% relative |

Small recall regression (−1pp) is a reasonable trade for the irrelevance reduction. MRR improves because avoiding known-bad results surfaces better ones.

## The Regression
Investigated the −1pp recall drop. It concentrates in the "discovery" query bucket (broad, non-specific queries like "gift for dad"). Our explicit negatives skew toward navigational queries, so the model learned to be too conservative on broad queries.

Mitigation: re-weight training so discovery queries contribute at least 20% of contrastive pairs. Will test in v2.

## Next Steps
- v2 with discovery query reweighting
- Check interaction with poly-encoder reranker — does it also see quality improvement?
- Report to `../reports/user-satisfaction-q2-2026.md`
