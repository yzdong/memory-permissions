# Inference Cost Tracking

We track GPU cost for inference separately from training because the cost profiles are very different and require different optimization strategies.

## Current Monthly Spend Breakdown (Approximate)

| Resource | Usage | Est. Monthly Cost |
|---|---|---|
| ml-serving pool (4-12× A10G, autoscaled) | ~6 GPU-months avg | $9,800 |
| ml-batch pool (2× A100, fixed) | 2 GPU-months | $3,100 |
| GCS model artifact storage | ~200 GB | $40 |
| Egress (Triton → Platform) | ~50 TB | $600 |
| **Total** | | **~$13,540** |

Training costs tracked separately in `../training/cost-tracking.md`.

## Cost Reduction Wins (Last 6 Months)

- **FP16 quantization of ranker:** -38% GPU memory → could fit more instances per GPU → ~$1,200/mo saved
- **Batch job A100 → preemptible pricing:** Moved batch jobs to preemptible A100s. Increased failure rate slightly (handled by retry logic), saves ~$800/mo
- **Turned off intent_clf_v2 shadow replica:** Was running 2 replicas for redundancy; single replica with faster failover is sufficient. ~$400/mo saved

## Where Cost Comes From

The serving pool autoscales based on GPU utilization. Traffic peaks at ~14:00-18:00 UTC and scales up to 10 GPUs. Off-peak (02:00-08:00 UTC) drops to 4 GPUs.

Largest lever: **model latency**. Every 10ms reduction in p99 latency → ~8% reduction in required GPU count at peak. This is why latency optimization directly affects cost.

## Cost Attribution

We tag all inference GCP resources with `team=ml` and `workload=inference`. Finance dashboard is at `go/ml-gcp-cost` (internal).

Platform team is the primary consumer of online inference. We've discussed a chargeback model but haven't implemented it — their usage is hard to disaggregate from our own evaluation traffic.

## Watch Items

- TRT engine rebuild on every model update costs ~$15 in build-time GPU usage. Acceptable now, but if update frequency increases, consider caching intermediate ONNX → TRT steps.
- Triton metrics scraping via Prometheus adds non-trivial egress at high model count. Consider reducing scrape interval from 15s to 30s for non-critical metrics.

See `online-vs-batch-routing.md` for capacity allocation decisions.
