# Inference Observability

How we monitor the ML inference stack in production. If you're being paged,
you probably want `latency-debugging-cheatsheet.md` first, then come back here.

## Metrics Stack

- **Triton native metrics**: Prometheus endpoint at `:8002/metrics`.
- **Inference service metrics**: Custom Prometheus metrics from our FastAPI app,
  scraped at `:9090/metrics`.
- **Redis client metrics**: `redis_client_request_latency_seconds` histogram.
- **Feature miss rate**: `feature_cache_miss_total` counter.

All scraped by the cluster Prometheus; dashboards in Grafana.

## Critical Alerts

| Alert | Condition | Severity | Runbook |
|---|---|---|---|
| InferenceP99High | p99 > 200ms for 5min | P1 | `runbooks/latency-incident.md` |
| TritonQueueBacklog | queue_duration_us p99 > 20ms | P2 | `latency-debugging-cheatsheet.md` |
| ModelLoadFailure | any model not in READY state | P1 | `runbooks/model-load-failure.md` |
| FeatureMissRateHigh | miss rate > 5% for 10min | P2 | `feature-store-integration.md` |
| BatchJobOverrun | nightly job runs past 04:30 UTC | P3 | `batch-inference-nightly.md` |

## Distributed Tracing

We propagate `X-Request-ID` from Platform's api service through to Triton.
Traces are sent to Jaeger (`http://jaeger.internal:16686`).

To find a specific request trace:
```
Service: ml-inference-service
Tags: request_id=<id from Platform's logs>
```

This lets us correlate a slow response in Platform's logs with the specific
Triton model execution.

## Logging

Structured JSON logs from the inference service. Key fields:

```json
{
  "level": "INFO",
  "request_id": "...",
  "model_version": 42,
  "total_latency_ms": 87.3,
  "triton_latency_ms": 71.2,
  "feature_lookup_ms": 1.8,
  "tokenizer_ms": 4.1,
  "cache_miss": false
}
```

Logs shipped to BigQuery via Dataflow. Query them at:
`bq query --project=ml-prod 'SELECT * FROM ml_logs.inference_requests WHERE ...'`

## Monthly Review

We do a monthly inference review covering p50/p90/p99 trends, cache miss rate,
model version history, and any latency regressions. Notes go in
`../reviews/inference-monthly.md`.
