# Serving SLOs and Alerts

This documents the SLOs we've committed to Platform and how our alerting is configured.

## Agreed SLOs

These are at the Triton boundary (not end-to-end — Platform adds their own budget):

| Model | p50 target | p99 target | Error rate target |
|---|---|---|---|
| ranker_v8 | 15 ms | 50 ms | < 0.5% |
| embedder_v3 | 8 ms | 25 ms | < 0.5% |
| intent_clf_v2 | 5 ms | 18 ms | < 1.0% |

SLO review happens quarterly with Platform. Current SLO doc: `../agreements/platform-ml-slos.md`

## Alert Configuration

Alerts are defined in `infra/monitoring/alerts/ml-inference.yaml`.

Key alerts:

```yaml
- alert: TritonP99LatencyHigh
  expr: histogram_quantile(0.99, rate(nv_inference_request_duration_us_bucket[5m])) > 55000
  for: 3m
  severity: page
  labels:
    team: ml

- alert: TritonErrorRateHigh
  expr: rate(nv_inference_request_failure_total[5m]) / rate(nv_inference_request_success_total[5m]) > 0.01
  for: 2m
  severity: page
  labels:
    team: ml

- alert: TritonGPUUtilSustained
  expr: avg(nv_gpu_utilization) > 88
  for: 10m
  severity: warning
  labels:
    team: ml
```

## On-Call Response

- P99 alert → check `latency-debugging-cheatsheet.md` first
- Error rate alert → check Triton logs immediately; common cause is malformed inputs from Platform
- GPU util warning → not an emergency, but open a capacity request if it persists > 1 hour

## SLO Burn Rate

We track 1-hour and 6-hour burn rates. Dashboard: `ML Inference / SLO Burn Rates`. If 6-hour burn rate > 5×, we send a Slack message to `#ml-oncall` even if no alert fires.

## Error Budget Policy

We have ~3.5 days of error budget per month (99.5% uptime target). Current policy:
- If we burn > 50% in the first two weeks → freeze non-critical deployments
- If we burn > 75% in a month → post-mortem required

Hadn't triggered the 75% threshold in the past 6 months — one close call in March due to the TRT driver upgrade.
