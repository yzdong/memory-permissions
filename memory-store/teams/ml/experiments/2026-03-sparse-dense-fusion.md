# Sparse-Dense Fusion Experiment — March 2026

**Owner:** @jan, @priya  
**Status:** Completed

## Background
Dense retrieval (our dual encoder) excels at semantic matching but sometimes misses exact keyword matches. A user searching for a specific SKU or product code gets poor results because the dense encoder focuses on semantic neighborhoods.

## Hypothesis
Fusing BM25 (sparse) scores with dense retrieval scores using a learned interpolation weight will improve exact-match queries without hurting semantic queries.

## Fusion Strategies

### Strategy 1: Linear interpolation (RRF)
Reciprocal Rank Fusion — no learned weights, pure heuristic:
```
score(d) = Σ_r 1 / (k + rank_r(d))
```
with k=60. Fast, no training needed.

### Strategy 2: Learned score fusion
- Train a lightweight regression head on (dense_score, sparse_score, query_type_features) → final score
- Query type features: contains digits?, contains special chars?, query length

## Results

| Condition | Recall@100 (semantic) | Recall@100 (exact-match) | MRR@10 |
|---|---|---|---|
| Dense only | 0.83 | 0.61 | 0.55 |
| Sparse only (BM25) | 0.49 | 0.88 | 0.41 |
| RRF fusion | 0.82 | 0.87 | 0.57 |
| Learned fusion | 0.83 | 0.89 | 0.59 |

Both fusion approaches recover near-perfect exact-match recall while preserving semantic quality. Learned fusion is marginally better (+2pp exact, +2pp MRR).

## Latency Impact
BM25 adds 6ms p50 (running on Elasticsearch). Fusion logic itself is negligible.

## Deployment Complexity
- Now have two retrieval systems to maintain and keep in sync (catalog updates must propagate to both)
- ES cluster sizing: current cluster handles load, but will need to scale during catalog refresh windows
- See `runbooks/elasticsearch-ops.md` for operational notes

## Decision
Ship RRF for now (simpler, no retraining needed). Revisit learned fusion in Q3 2026 once operational burden of running two retrieval systems is better understood.
