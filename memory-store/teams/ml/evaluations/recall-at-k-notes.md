# Recall@k — Notes and Gotchas

This doc is a working reference for anyone interpreting or modifying recall@k metrics in our eval pipeline.

## Definition We Use

For a given user query, recall@k is:

```
Recall@k = |relevant items in top-k| / |total relevant items for user|
```

We cap the denominator at 200 to avoid pathologically low scores for power users with huge interaction histories.

## Why k Matters So Much

Our retrieval model returns a candidate set of 500 items that gets ranked down to 20. Recall@k at different k values tells very different stories:

- **Recall@20**: How well does the ranker surface relevant items in final display? Reflects end-user experience.
- **Recall@100**: How well does the retrieval model feed the ranker? Ranker can't rescue items not in the candidate set.
- **Recall@500**: Upper bound — reflects retrieval ceiling before any ranking.

We track all three. Missing a Recall@500 target is a retrieval problem; missing Recall@20 while hitting Recall@100 is a ranking problem.

## Variance at Small k

For users with few relevant items (e.g., new users with <5 known relevant items), recall@k estimates are very noisy. A single miss can tank the score by 20+ points.

Recommendation: **always report recall@k separately for new vs. established users**. The aggregate number can mask serious new-user recall failures.

## Bootstrap CI Code

```python
import numpy as np

def bootstrap_recall_ci(per_user_recalls, n_boot=1000, ci=0.95):
    bootstraps = [
        np.mean(np.random.choice(per_user_recalls, size=len(per_user_recalls), replace=True))
        for _ in range(n_boot)
    ]
    lo = np.percentile(bootstraps, (1 - ci) / 2 * 100)
    hi = np.percentile(bootstraps, (1 + ci) / 2 * 100)
    return lo, hi
```

We report 95% CIs on all recall@k numbers in quarterly summaries.

## Historical Recall@50 Values

| Quarter | Recall@50 (all users) | Recall@50 (new users) |
|---------|----------------------|----------------------|
| Q2 2025 | 0.71 | 0.54 |
| Q3 2025 | 0.73 | 0.57 |
| Q4 2025 | 0.70 | 0.53 |

The Q4 dip was caused by the training data incident described in `q4-2025-recap.md`.

## Related

- `holdout-set-methodology.md` — sample sizes and stratification affect CI width
- `regression-tracking.md` — recall is one of the signals used for regression detection
