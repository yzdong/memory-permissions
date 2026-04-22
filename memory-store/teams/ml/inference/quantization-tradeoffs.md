# Quantization Tradeoffs

Notes from our Q3 evaluation of INT8 and FP16 quantization on the ranking and embedding models.

## TL;DR

- FP16 is nearly free for GPU workloads — do it by default.
- INT8 PTQ (post-training quantization) saves ~40% memory but costs 1-3% recall on tail queries.
- INT8 QAT (quantization-aware training) recovers most of that loss but adds ~2 weeks of training overhead.
- Do NOT quantize the final projection layer of the embedding model — accuracy drop is unacceptable there.

## Benchmarks (ranker_v8, 512-dim, A100)

| Mode | Latency p50 | Latency p99 | Model Size | Recall@10 |
|---|---|---|---|---|
| FP32 baseline | 18 ms | 47 ms | 1.4 GB | 0.91 |
| FP16 | 11 ms | 29 ms | 700 MB | 0.91 |
| INT8 PTQ | 7 ms | 19 ms | 350 MB | 0.88 |
| INT8 QAT | 8 ms | 21 ms | 350 MB | 0.90 |

Recall threshold for prod promotion is 0.89 — INT8 PTQ barely misses it on certain verticals.

## When to Use What

**Use FP16 when:**
- Deploying to any NVIDIA GPU with Tensor Cores (Ampere, Hopper)
- Model is already in mixed-precision training regime

**Use INT8 PTQ when:**
- Serving on edge or CPU-only nodes
- Latency SLA is < 10 ms p50 and accuracy budget allows

**Use INT8 QAT when:**
- PTQ accuracy loss is above budget AND latency matters
- Plan for at least 3 extra weeks (2 training + 1 validation)

## Calibration Dataset

INT8 PTQ requires a calibration dataset. We use 5,000 samples from production logs, stratified by query category. Script:

```bash
python tools/calibrate_int8.py \
  --model models/onnx/ranker_v8.onnx \
  --calibration-data data/calib/prod_sample_5k.jsonl \
  --output models/onnx/ranker_v8_int8.onnx
```

## Known Issues

- TensorRT INT8 engine build is non-deterministic across driver versions — always lock driver in the Triton Docker image.
- Quantizing the cross-attention QK matmul introduces >2% error on long sequences (>512 tokens). We exclude those ops.

See: `onnx-export-notes.md`, `triton-serving-setup.md`, `../evaluations/ranker-q3-eval.md`
