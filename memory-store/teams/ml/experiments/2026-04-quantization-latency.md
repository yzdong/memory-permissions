# INT8 Quantization for Item Tower — April 2026

**Owner:** Tariq Al-Rashid  
**Status:** Complete  
**Linked to:** `2025-10-dual-encoder-trial.md` (latency concern), `embedding-dim-sweep.md`

## Motivation

The dual encoder's p99 latency of 27 ms was flagged as a blocker for the online A/B test. INT8 quantization was identified as the most promising latency reduction lever without architecture changes.

## Method

- Quantization toolkit: TensorRT 9.1 + PyTorch export
- Calibration set: 50K random queries from 2025-Q4 traffic
- Quantized layers: all linear projections in item tower
- Query tower kept at FP16 (it's on the hot path differently)

## Results

| Config | Recall@50 | p50 latency | p99 latency | Throughput (QPS) |
|---|---|---|---|---|
| FP16 baseline | 0.561 | 9 ms | 27 ms | 1,820 |
| INT8 item tower | 0.557 | 7 ms | 19 ms | 2,490 |
| INT8 both towers | 0.541 | 5 ms | 14 ms | 3,310 |

Quantizing only the item tower hits the target (<22 ms p99) with minimal recall degradation (-0.7%).

Quantizing both towers recovers more latency but costs 3.6% recall — too much.

## Decision

Ship INT8 item tower to staging. Green-light the A/B test.

## Notes

- Calibration set size matters: using <10K samples caused noticeable accuracy drop. 50K felt stable.
- Latency measured on `ml-serving-bench-01`; production hardware (`ml-serving-prod-*`) is slightly faster — p99 should land around 17 ms.
- TensorRT engine is saved to `models/retrieval/dual_encoder_v2_int8_item/`.
