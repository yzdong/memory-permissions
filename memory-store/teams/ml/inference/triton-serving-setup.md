# Triton Inference Server Setup

This covers how we configure and run Triton for our ML model serving. Platform's API service calls our Triton endpoints — we own the serving infra, they own the routing layer.

## Repository Layout

```
triton/
  model_repository/
    ranker_v8/
      config.pbtxt
      1/
        model.onnx
    embedder_v3/
      config.pbtxt
      1/
        model.plan   # TensorRT engine
  docker/
    Dockerfile.triton
    entrypoint.sh
```

## Config Template

```protobuf
name: "ranker_v8"
backend: "onnxruntime"
max_batch_size: 128

input [
  { name: "input_ids" data_type: TYPE_INT64 dims: [-1, 512] },
  { name: "attention_mask" data_type: TYPE_INT64 dims: [-1, 512] }
]
output [
  { name: "logits" data_type: TYPE_FP32 dims: [-1, 1] }
]

dynamic_batching {
  preferred_batch_size: [32, 64, 128]
  max_queue_delay_microseconds: 5000
}

instance_group [
  { kind: KIND_GPU count: 2 }
]
```

## Starting Triton Locally (dev)

```bash
docker run --gpus all --rm \
  -p 8000:8000 -p 8001:8001 -p 8002:8002 \
  -v $(pwd)/triton/model_repository:/models \
  nvcr.io/nvidia/tritonserver:24.04-py3 \
  tritonserver --model-repository=/models --log-verbose=1
```

## Health and Readiness

- Readiness: `GET /v2/health/ready`
- Per-model stats: `GET /v2/models/ranker_v8/stats`
- Prometheus metrics endpoint: `:8002/metrics`

We scrape `:8002` in our internal Grafana — dashboard is `ML Inference / Triton Overview`.

## Model Loading Strategy

We use explicit model control mode (`--model-control-mode=explicit`) so that new model versions don't auto-load in prod. Deployment is gated by our CI:

1. Push ONNX/TRT artifact to GCS
2. CI runs equivalence + latency regression test
3. On pass, CI calls `POST /v2/repository/models/ranker_v8/load`

## Troubleshooting

- **Model stuck in LOADING** — usually a bad ONNX file. Check Triton logs with `kubectl logs -l app=triton --tail=200`
- **OOM on GPU** — reduce `instance_group count` or check if multiple versions are loaded
- **High queue time** — increase `max_queue_delay_microseconds` OR check if batching is saturated

See `latency-debugging-cheatsheet.md` for a deeper dive.
