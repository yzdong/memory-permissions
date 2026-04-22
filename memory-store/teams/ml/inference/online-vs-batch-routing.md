# Online vs Batch Routing Decisions

We have two inference paths and choosing the wrong one has caused both latency incidents and wasted GPU budget. This doc captures the decision logic.

## The Two Paths

**Online (Triton, real-time):**
- Invoked per-request by Platform's API service
- Latency SLA: p50 < 15ms, p99 < 50ms at the Triton boundary
- GPU pool: `ml-serving` — 4× A10G, autoscaled

**Batch (ORT direct, nightly):**
- Invoked by scheduled k8s CronJobs
- No latency SLA, throughput-optimized
- GPU pool: `ml-batch` — 2× A100, fixed (no autoscale needed)

## Decision Matrix

| Factor | Online | Batch |
|---|---|---|
| User-facing? | Yes | No |
| Can tolerate staleness? | No | Yes (up to 24h) |
| Payload size | Small (<100 items) | Large (millions) |
| Result needed before response? | Yes | No |
| Frequency | Continuous | Scheduled |

## Gray Areas

### Catalog Rescoring After Model Update
We used to do this online (lazy rescoring on cache miss). Switched to batch in Q2 — it was contributing ~8ms tail latency during the model transition window. Batch pre-scores the whole catalog; online path reads from BQ.

### A/B Experiments
Experiments run on the online path even if the model is also batch-scored. Reason: we need per-request control over which variant a user hits, which isn't possible with pre-scored batch results.

### Near-real-time Personalization
Currently online. We've discussed moving to a streaming batch approach (Dataflow + Triton) but the engineering investment is significant. Tracked in `../roadmap/personalization-infra.md`.

## Capacity Notes

- The `ml-serving` pool autoscales 4→12 A10G based on GPU util. Scale-up takes ~90 seconds — faster than Platform's traffic spike usually ramps.
- Don't schedule ad-hoc batch jobs on the serving pool. Use `ml-batch` or file a capacity request. We had an incident in July where a manual backfill job starved online serving.

## Handoff with Platform

Platform's API service calls Triton via gRPC at `triton-svc.ml-serving.svc.cluster.local:8001`. They are responsible for:
- Request shaping (max input length enforcement)
- Circuit breaking (they use Envoy)
- Client-side timeout (currently 200ms)

We are responsible for everything inside Triton.

See `batch-inference-nightly.md`, `triton-serving-setup.md`
