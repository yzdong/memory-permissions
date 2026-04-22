# Inference Service Architecture

The ML inference service is the gRPC/HTTP service that sits between Platform's
api service and Triton. It handles preprocessing, routing, and postprocessing.

## Why Not Call Triton Directly?

Platform could technically call Triton directly, but:
- Triton's HTTP API is low-level (raw tensors). We handle tokenization here.
- We do request validation, feature augmentation, and A/B model routing.
- Postprocessing (score calibration, filtering) belongs with the model team.

## Service Diagram

```
Platform API (gRPC)
  │
  ▼
ML Inference Service (Python, FastAPI + gRPC server)
  │  ├─ Tokenizer (HuggingFace, runs in thread pool)
  │  ├─ Feature augmentation (lookup from Redis)
  │  ├─ Triton client (tritonclient.grpc)
  │  └─ Postprocessor (score calibration, threshold application)
  │
  ▼
Triton Inference Server
  │
  ▼
GPU (ONNX/TRT)
```

## Key Config

All tunable settings are in `configs/inference-service/production.yaml`:

```yaml
tokenizer:
  model_name: "bert-base-uncased"
  max_length: 512
  workers: 4

triton:
  host: "triton-svc"
  grpc_port: 8001
  timeout_ms: 150

feature_store:
  redis_host: "redis-svc"
  redis_port: 6379
  ttl_seconds: 300

scoring:
  calibration_method: "platt"
  threshold: 0.72
```

Note: threshold was recalibrated after the Q4 model update. Previous value was 0.68.

## Request Flow (Timing Budget)

Our p99 budget to Platform is 120ms end-to-end from their perspective.

| Stage | Budget |
|---|---|
| Tokenization | 5ms |
| Feature lookup (Redis) | 3ms |
| Triton queue + compute | 80ms |
| Postprocessing | 2ms |
| Network overhead | 10ms |
| **Total** | **100ms** (20ms buffer) |

If any stage consistently exceeds its budget, check `latency-debugging-cheatsheet.md`.

## Deployment

Helm chart: `helm/inference-service/`. Container image built in `Dockerfile.inference`.
See `runbooks/deploy.md` for the rollout procedure.
