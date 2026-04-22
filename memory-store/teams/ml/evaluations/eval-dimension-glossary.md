# Eval Dimension Glossary

A reference for the metrics and concepts used across eval documents. Opinions are the ML team's; not all of these definitions are industry-standard.

---

## Precision@K

Fraction of the top-K recommended items that are relevant. "Relevant" means the user engaged with the item in the holdout window (click or long-click, configurable in harness).

```
Precision@K = |{top-K recommendations} ∩ {relevant items}| / K
```

We primarily track K=10. See `q1.md` for current target thresholds.

---

## Recall@K

See `recall-at-k-notes.md` for our specific implementation. Short version: we use capped Recall@K to handle users with very few relevant items.

---

## NDCG@K (Normalized Discounted Cumulative Gain)

Rank-sensitive metric. Rewards placing more relevant items higher in the list. We use binary relevance (clicked / not clicked) rather than graded relevance.

```
DCG@K = sum_{i=1}^{K} rel_i / log2(i+1)
NDCG@K = DCG@K / IDCG@K
```

NDCG tracks more signal about list ordering than Precision@K does and is more sensitive to cold-start regressions.

---

## MRR (Mean Reciprocal Rank)

Average of the reciprocal rank of the first relevant item. Useful for "did we surface *anything* useful near the top?" but less informative when users have multiple relevant items.

---

## p99 Latency

99th percentile inference latency, measured end-to-end from request to ranked list, in milliseconds. Measured in production shadow mode, not in the offline harness. Offline harness latency numbers are indicative only.

---

## Holdout Cohort

The frozen set of users and their future interactions used as ground truth in offline evals. Details in `holdout-set-methodology.md`.

---

## Cohort Bias

Systematic metric shift caused by cohort rotation, not model quality change. Accounted for using the delta-adjustment in `holdout-set-methodology.md`.

---

## LLM Judge Score

A supplementary 1–5 score from an LLM evaluator (see `judge-prompt-v2.md`). Not used in promotion gates; used for qualitative signal and catching issues in low-traffic categories.

---

## Offline/Online Delta

The difference between what offline metrics predict and what we observe in production A/B tests. Monitored weekly; see `offline-vs-online-delta.md`.

---

_Last updated: Jan 2026. If you add a new metric to the harness, add it here._
