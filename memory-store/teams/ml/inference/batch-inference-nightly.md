# Batch Inference — Nightly Jobs

We run several nightly batch inference jobs that are separate from the online serving path. These use larger batch sizes and more aggressive quantization since latency SLAs don't apply.

## Jobs Overview

| Job Name | Schedule | Model | Output |
|---|---|---|---|
| `embed-catalog` | 02:00 UTC | embedder_v3 | Catalog embedding index |
| `score-candidates` | 03:30 UTC | ranker_v8 | Pre-scored candidate lists |
| `intent-classify` | 01:00 UTC | intent_clf_v2 | Query intent labels for logging |

All jobs run on the `ml-batch` k8s namespace using GPU node pools.

## Running a Job Manually

```bash
# Trigger embed-catalog for a specific date
kubectl create job --from=cronjob/embed-catalog embed-catalog-manual-$(date +%Y%m%d) \
  -n ml-batch
```

## Architecture

```
GCS (input shards)
     │
     ▼
 Spark reader (ml-batch pod)
     │
     ▼
 ONNX Runtime (no Triton — direct ORT for batch)
     │
     ▼
GCS (output parquet)
     │
     ▼
 BQ table (consumed by downstream teams)
```

We deliberately do NOT route batch jobs through Triton — dynamic batching overhead isn't worth it when we're controlling batch sizes directly.

## Batch Size Tuning

- `embed-catalog`: batch_size=512 on A10G; larger sizes cause OOM due to catalog item length variance
- `score-candidates`: batch_size=256; bottleneck is actually GCS read speed, not GPU
- `intent-classify`: batch_size=1024 (short sequences, fits easily)

## Failure Handling

- Jobs have `backoffLimit: 2` — two retries before alerting.
- Alert fires to `#ml-batch-alerts` in Slack.
- Common failure: GCS permissions expiry (service account token). Check `runbooks/gcs-sa-refresh.md`.

## Output Schema

The `score-candidates` parquet output schema:

```
root
 |-- query_id: string
 |-- candidate_id: string
 |-- score: float
 |-- model_version: string
 |-- run_date: date
```

Downstream consumers (Platform data team) should never hard-code model_version — use the `latest` symlink in GCS.

## Monitoring

- Job duration tracked in Grafana: `ML Inference / Batch Jobs`
- p99 embed-catalog job should complete in < 90 minutes. If it's exceeding 2 hours, something is wrong — likely shard imbalance.

See `onnx-export-notes.md` for how batch models are exported differently from online models.
