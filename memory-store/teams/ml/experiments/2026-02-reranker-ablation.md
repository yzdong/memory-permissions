# Reranker Ablation — February 2026

**Owner:** @priya, @marco  
**Hypothesis:** A cross-attention reranker over the top-100 retrieved candidates will improve MRR@10 and CTR without unacceptable latency cost.

## Context
Retrieval (dual-encoder-v2) gives us solid recall but MRR@10 is capped at ~0.49 because the ANN stage can't model query-item interactions. A reranker sees both query and item together.

## Models Tested

### R1: BERT-base cross-encoder
- 12-layer transformer, query+item concatenated with [SEP]
- Fine-tuned on top-100 lists with click labels
- Latency: 210ms p50 for 100 candidates (sequential) — too slow

### R2: Poly-encoder (sparse attention)
- 6-layer, 16 query codes
- Latency: 48ms p50 for 100 candidates
- Quality lower than R1 but usable

### R3: ListMLE reranker (R1 architecture, listwise loss)
- Same model as R1 but trained with ListMLE on ranked lists
- Marginal quality gain over pointwise R1 (+0.01 NDCG@10)
- Not worth the training complexity for now

### R4: Lightweight MLP over concatenated embeddings
- Fast (3ms p50) but quality improvement barely detectable
- Useful as a cheap baseline but not production-worthy

## Quality Summary

| Model | MRR@10 | NDCG@10 | p50 latency |
|---|---|---|---|
| No reranker | 0.49 | 0.46 | 0 ms |
| R4 MLP | 0.51 | 0.47 | 3 ms |
| R2 Poly-enc | 0.55 | 0.52 | 48 ms |
| R1 BERT cross-enc | 0.59 | 0.57 | 210 ms |
| R3 ListMLE | 0.60 | 0.58 | 215 ms |

## Decision
**R2 Poly-encoder** for immediate production use. R1/R3 quality is compelling but 210ms is over our 150ms total budget when combined with retrieval.

Logging full R1 scores in shadow mode — will use them as training signal for distilling into a smaller model (see `2026-03-reranker-distillation.md` once written).

## Deployment Notes
- Reranker deployed as a sidecar to retrieval service
- See `runbooks/reranker-deploy.md` for rollout steps
- Feature flags: `reranker_enabled`, `reranker_model_version`
