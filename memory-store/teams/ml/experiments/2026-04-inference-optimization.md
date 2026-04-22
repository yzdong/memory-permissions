# Inference Optimization Experiment — April 2026

**Owner:** @jan, @marco  
**Goal:** Reduce serving cost and p99 latency without quality regression

## Current State
- Query encoder: 110M params, runs on GPU, p50=14ms, p99=43ms
- Item index: 256-dim float16, 60 GB, HNSW on CPU
- Reranker (poly-encoder): p50=48ms, p99=140ms
- Total pipeline p99: ~200ms (close to our 220ms budget)

## Optimizations Tested

### OPT-1: INT8 quantization of query encoder
- Used dynamic quantization via `torch.quantization.quantize_dynamic`
- Query encoder p50: 14ms → 9ms (-36%)
- Recall@100 delta: −0.002 (negligible)
- MRR@10 delta: −0.003 (negligible)
- ✅ Shipping this

### OPT-2: Query encoder distillation (12→6 layers)
- Distilled from full 12-layer encoder using intermediate layer matching
- Query encoder p50: 14ms → 6ms (-57%)
- Recall@100 delta: −0.012 (borderline — more work needed)
- ❌ Not shipping yet; need 2 more weeks of distillation tuning

### OPT-3: HNSW ef_search tuning
- Reduced ef_search from 200 to 120
- ANN search p50: 18ms → 11ms
- Recall@100 delta: −0.007
- Acceptable trade. ✅ Shipping.

### OPT-4: Reranker early exit
- Stop reranking once top-1 score exceeds a confidence threshold
- Effectively reduces candidates rescored on high-confidence queries
- Reranker p50: 48ms → 31ms on 40% of queries
- MRR@10 on early-exit queries: no change (confidence threshold well-calibrated)
- ✅ Shipping.

## Projected Pipeline After Optimizations
- Total p99: ~155ms (down from ~200ms)
- GPU fleet reduction: ~22% fewer query encoder GPUs needed at current QPS
- No quality regression at ship threshold

## Notes
- OPT-2 distillation work continues in `2026-05-encoder-distillation.md` (forthcoming)
- All latency numbers measured at 50k QPS on staging — see `runbooks/load-testing.md`
