# Embedding Dimension Sweep

**Status:** Complete  
**Owner:** @priya  
**Last updated:** 2025-11-14

## Motivation
After the dual encoder trial (see `2025-10-dual-encoder-trial.md`), we weren't sure if 128 dims was leaving quality on the table or wasting FLOPS. We swept 64 / 128 / 256 / 512 with everything else fixed.

## Setup
- Architecture: dual encoder v1 (Oct checkpoint as starting weights)
- Training: 2 epochs each, same data mix
- Evaluated on `../evaluations/nov2025-holdout.jsonl`
- ANN index rebuilt for each dim using FAISS flat for apples-to-apples quality; HNSW for latency numbers

## Quality vs Dim

| Dim | Recall@50 | Recall@100 | NDCG@10 |
|---|---|---|---|
| 64  | 0.68 | 0.74 | 0.39 |
| 128 | 0.75 | 0.81 | 0.44 |
| 256 | 0.77 | 0.83 | 0.46 |
| 512 | 0.77 | 0.83 | 0.46 |

Quality saturates at 256. 512 adds no signal.

## Latency vs Dim (HNSW, p50/p99 ms)

| Dim | p50 | p99 |
|---|---|---|
| 64  | 9  | 27 |
| 128 | 14 | 43 |
| 256 | 22 | 64 |
| 512 | 41 | 118 |

Latency roughly doubles with each doubling of dim. 256 at p99=64ms is on the edge of our SLO (75ms).

## Decision
Go with **256 dims** for the next production candidate. Gives best quality without busting SLO. Will need to re-evaluate if we add a reranker that eats budget.

## Index Storage
- 256-dim float32: ~120 GB for 120M items
- We can drop to float16 without measurable quality loss (checked, delta < 0.001 on Recall@100)
- float16 brings index to ~60 GB, fits in current ANN server fleet

## Open Questions
- Does dim interact with hard negative ratio? Probably not, but worth a quick ablation.
- Quantization to int8: not tested yet, assigned to @marco for Dec.
