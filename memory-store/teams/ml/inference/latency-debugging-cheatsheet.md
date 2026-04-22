# Latency Debugging Cheatsheet

A quick reference when someone pages about high inference latency. Written from experience — not theoretical.

## First 5 Minutes

```bash
# Check Triton queue time vs compute time breakdown
curl -s http://triton-svc:8002/metrics | grep -E 'nv_inference_(queue|compute)_duration'

# Tail Triton logs for slow requests
kubectl logs -l app=triton -n ml-serving --tail=500 | grep 'WARN\|ERROR\|slow'

# Check GPU utilization
nvidia-smi dmon -s u -d 2
```

## Latency Taxonomy

Break latency into layers:

1. **Network (client → Triton)** — check Platform's outbound latency metrics first
2. **Triton queue time** — how long request waited before a model instance picked it up
3. **Triton compute time** — actual GPU kernel execution
4. **Triton response time** — serialization + network back to client

## Common Culprits

### Culprit: Batching queue is too aggressive
Symptom: p50 is fine, p99 spikes. Queue delay set too high.
```
# Reduce max_queue_delay_microseconds in config.pbtxt
max_queue_delay_microseconds: 2000  # was 10000
```

### Culprit: Wrong CUDA execution provider
Symptom: GPU idle but latency high. ORT falling back to CPU.
```python
sess_options = ort.SessionOptions()
providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
# Verify with:
print(sess.get_providers())
```

### Culprit: Model not warmed up
Symptom: First N requests after deploy are 10-20x slower.
Fix: Add warmup config to `config.pbtxt`:
```protobuf
model_warmup [
  {
    name: "warmup"
    batch_size: 32
    inputs { key: "input_ids" value { data_type: TYPE_INT64 dims: [32, 512] zero_data: true } }
  }
]
```

### Culprit: Memory fragmentation after long uptime
Symptom: Gradual latency increase over days, resolved by pod restart.
Mitigation: Schedule weekly rolling restarts via `kubectl rollout restart`.

### Culprit: Tokenizer on CPU in hot path
Symptom: High CPU usage, GPU compute time looks fine.
Fix: Pre-tokenize inputs upstream (at Platform's API layer) and send token IDs directly to Triton.

## Profiling with Nsight

```bash
# Attach to running Triton pod (requires privileged)
nsys profile -t cuda,nvtx \
  --output /tmp/triton_profile \
  curl -X POST http://localhost:8000/v2/models/ranker_v8/infer -d @sample_payload.json
```

Then pull the `.nsys-rep` file and open in Nsight Systems on your laptop.

## When to Escalate

- If GPU compute time looks correct but e2e latency is still high → escalate to Platform (check their service mesh / LB)
- If CUDA OOM errors accompany latency → see `triton-serving-setup.md` for instance count tuning

See also: `../monitoring/slo-definitions.md`
