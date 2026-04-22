# Popularity Bias Audit — September 2025

**Owner:** @dani  
**Type:** Audit / diagnostic (not a training experiment)

## Why This Exists
We noticed long-tail items have disproportionately low recall. Before running experiments to fix it, wanted to quantify how bad it is and understand root causes.

## Methodology
Segmented the Nov 2025 holdout by item popularity decile (D1=top 10% most popular, D10=bottom 10%). Computed Recall@100 and NDCG@10 per decile.

## Findings

| Decile | Item count | Recall@100 | NDCG@10 |
|---|---|---|---|
| D1 (most popular) | 12M | 0.91 | 0.61 |
| D2 | 12M | 0.88 | 0.57 |
| D3 | 12M | 0.86 | 0.53 |
| D4–D6 | 36M | 0.81 | 0.46 |
| D7–D9 | 36M | 0.71 | 0.36 |
| D10 (least popular) | 12M | 0.53 | 0.24 |

D10 recall is half of D1. This is severe.

## Root Causes
1. **Training frequency imbalance**: popular items appear far more often as positives and as hard negatives — the item tower gets much more gradient signal for them.
2. **ANN graph connectivity**: popular items end up as hubs in the HNSW graph, crowding out tail items during search.
3. **Feature sparsity**: tail items have fewer co-click features, so content features dominate — but we under-train on content.

## Proposed Fixes
- Popularity-based upsampling of tail items in training batches
- Separate evaluation budget for tail items in all future experiments (added to eval harness in `../evaluations/eval-harness.md`)
- Consider IVF-based index with popularity-aware cluster assignment

## Status
Fixes being tested in `2026-01-tail-item-boosting.md` (not yet written as of this audit).
