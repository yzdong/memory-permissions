# Eval Metric Definitions

Canonical definitions for every metric the ML team reports in quarterly evaluations. If a metric appears in any eval doc, it should conform to the definition here.

## Precision@k

**Definition:** Fraction of the top-k recommended items that are relevant.

```
Precision@k = |relevant ∩ top-k| / k
```

**Relevance label source:** Human annotations (gold set) or LLM judge (see `judge-prompt-v2.md`). Always note which was used.

**Aggregation:** Macro-average across users.

---

## Recall@k

See `recall-at-k-notes.md` for detailed discussion. Short form:

```
Recall@k = |relevant ∩ top-k| / min(|relevant|, 200)
```

---

## NDCG@k (Normalized Discounted Cumulative Gain)

**Definition:** Standard NDCG using log2 discounting. Relevance grades come from the 1–5 LLM judge scale (binary precision uses a binarized version at threshold ≥ 4).

```python
def dcg_at_k(scores, k):
    scores = scores[:k]
    return sum(s / np.log2(i + 2) for i, s in enumerate(scores))

def ndcg_at_k(scores, ideal_scores, k):
    return dcg_at_k(scores, k) / dcg_at_k(sorted(ideal_scores, reverse=True), k)
```

---

## MRR (Mean Reciprocal Rank)

The reciprocal of the rank of the first relevant item, averaged across queries.

```
MRR = (1/|Q|) * Σ (1 / rank_first_relevant_q)
```

If no relevant item appears in the top-k window, reciprocal rank is 0 for that query.

---

## P95 / P99 Latency

Measured from request receipt at the model server to first-byte of response. Excludes network transit to client. Computed over a 5-minute rolling window during load test or from production traces.

---

## Notes

- Always specify k when reporting @k metrics — "recall" alone is ambiguous
- When reporting on subsets (e.g., new users, cold items), label the subset explicitly
- Statistical significance tests: use paired t-test or Wilcoxon signed-rank; report p-values

## Related

- `recall-at-k-notes.md`
- `judge-prompt-v2.md`
- `holdout-set-methodology.md`
