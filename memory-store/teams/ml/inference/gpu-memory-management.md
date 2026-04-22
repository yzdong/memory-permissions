# GPU Memory Management

GPU OOM is one of the most disruptive failure modes in inference. This doc covers how we size memory, what to do when things go wrong, and some non-obvious gotchas.

## Memory Budget per Model (A10G, 24 GB)

| Model | Weights (FP16) | KV / Activation Budget | Reserved | Total |
|---|---|---|---|---|
| ranker_v8 | 2.8 GB | 4 GB | 1 GB | ~8 GB |
| embedder_v3 | 1.1 GB | 2 GB | 0.5 GB | ~4 GB |
| intent_clf_v2 | 0.4 GB | 1 GB | 0.5 GB | ~2 GB |

We run ranker + embedder on the same GPU in dev (fits comfortably). In prod, they're on separate instances for isolation.

## CUDA Memory Fragmentation

After days of sustained traffic with variable batch sizes, the CUDA allocator can fragment memory enough to cause OOM even when `nvidia-smi` shows plenty of free memory.

Mitigation:
```python
# In ORT session warmup, pre-allocate a range of buffer sizes
import torch
torch.cuda.memory.set_per_process_memory_fraction(0.90)  # Don't let ORT grab everything
```

Longer-term: weekly rolling restart of Triton pods (scheduled Sunday 04:00 UTC, low traffic).

## Triton Memory Pool Config

```protobuf
# In triton startup flags:
--cuda-memory-pool-byte-size=0:4294967296  # 4 GB for GPU 0
```

Be conservative here — if you give Triton the whole GPU, there's no slack for driver overhead.

## OOM Runbook

1. Check `nvidia-smi` on affected node — is it actually fully utilized or just fragmented?
2. `kubectl describe pod <triton-pod>` — look for recent OOM kills in events
3. If fragmented (high `Reserved` but low `Allocated` in pytorch): rolling restart
4. If genuinely OOM: reduce `instance_group count` in `config.pbtxt` and redeploy
5. If neither: check if a batch job got scheduled on the serving pool (see `online-vs-batch-routing.md`)

## Multi-Instance GPU (MIG)

We evaluated MIG on A100s for the batch pool — the isolation is great but the setup overhead for our use case (variable model sizes) wasn't worth it. Revisit if we add more models to batch pool.

## Useful Commands

```bash
# Detailed CUDA memory breakdown for a running ORT process
python -c "import torch; print(torch.cuda.memory_summary())"

# Watch GPU memory live
watch -n 1 nvidia-smi --query-gpu=memory.used,memory.free --format=csv

# Triton per-model memory usage via metrics API
curl triton-svc:8002/metrics | grep nv_gpu_memory
```
