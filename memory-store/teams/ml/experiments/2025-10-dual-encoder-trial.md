# Dual Encoder Trial — October 2025

## Hypothesis
Replacing the single tower with a dual encoder (query tower + item tower) should improve retrieval recall at top-100 by separating representation concerns.

## Setup
- Base model: `models/retrieval/single-tower-v4`
- New model: `models/retrieval/dual-encoder-v1`
- Training data: 60M query-item pairs from Sept 2025 logs
- Negative sampling: in-batch negatives + 10 hard negatives per query
- Embedding dim: 128 (both towers)
- Batch size: 4096, learning rate: 3e-4 with linear warmup over 5k steps
- Eval set: `../evaluations/oct2025-holdout.jsonl` (2.1M queries)

## Infra
- Training run on 8×A100 cluster, ~18h per full epoch
- See `runbooks/training-cluster.md` for job submission details
- Index built with FAISS HNSW (ef_construction=200, M=32)

## Results

| Metric | Single Tower | Dual Encoder |
|---|---|---|
| Recall@100 | 0.71 | 0.78 |
| MRR@10 | 0.41 | 0.46 |
| Latency p50 (ms) | 12 | 14 |
| Latency p99 (ms) | 38 | 43 |

Recall improvement is real and consistent across query length buckets. Latency increase is acceptable.

## Issues Encountered
- First training run diverged at step ~22k — traced to a bad batch of synthetic negatives in the Aug data slice. Filtered those out and restarted.
- Item tower embeddings had cosine similarity > 0.99 for ~0.3% of item pairs — likely duplicate catalog entries. Filed ticket with data-eng.

## Next Steps
- Sweep embedding dims (64, 128, 256, 512) — see `embedding-dim-sweep.md`
- Try asymmetric tower depths (deeper query tower)
- Hand off to ranking team once recall@100 ≥ 0.80
