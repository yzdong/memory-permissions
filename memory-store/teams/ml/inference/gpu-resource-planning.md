# GPU Resource Planning — Inference

Owner: @ml-infra  
Last reviewed: 2024-11-08

## Current Fleet

| Cluster | GPU Type | Count | Usage |
|---|---|---|---|
| prod-online | NVIDIA A10G (24GB) | 8 nodes, 1 GPU each | Online inference |
| prod-batch | NVIDIA T4 (16GB) | 4 nodes, 1 GPU each | Nightly batch |
| staging | NVIDIA T4 (16GB) | 2 nodes, 1 GPU each | Pre-prod validation |

## Memory Allocation Per Node (prod-online)

| Component | GPU Memory |
|---|---|
| Ranker (FP16 + TRT) | 1.8 GB |
| Embedder (INT8) | 0.9 GB |
| TRT workspace | 4.0 GB |
| CUDA context + misc | 1.5 GB |
| **Total used** | **~8.2 GB** |
| **Available** | 24 GB |

We have significant headroom. If we add the content classifier to online
serving (currently being discussed), it would fit comfortably.

## Scaling Policy

- HPA scales on `nv_gpu_utilization` > 70% for 5 consecutive minutes.
- Min replicas: 3 (to survive 1 AZ failure).
- Max replicas: 10 (soft limit; requires approval above that).
- Scale-in is slow: 15-minute stabilization window to avoid thrash.

## Batch Cluster Sizing

Batch cluster runs nightly only. Nodes are scaled down to 0 during the day
via a CronJob that patches the node pool. This saves meaningful cost.

The scale-up CronJob runs at 01:30 UTC; batch DAG starts at 02:00 UTC,
giving 30 minutes for nodes to register and models to load.

## Upcoming Capacity Needs

- **Q1 next year**: New multimodal ranker is 2.1B params. Even quantized it won't
  fit alongside the current ranker on A10G. Will need A100 or H100 nodes, or
  a dedicated node per model.
- **Document embedding re-index**: Planned full re-embed of the corpus (~40M docs)
  will require a one-off batch job, estimated 18 hours on the current batch cluster.
  Might need to temporarily upsize.

## Cost Notes

We track GPU cost in the `#ml-cost` Slack channel (weekly summary from FinOps).
If nightly batch runs long and overlaps with business hours, spot preemption
can get expensive. Keep an eye on batch job duration.
