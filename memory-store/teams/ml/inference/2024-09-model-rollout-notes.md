# Sept 2024 — ranker_v8 Rollout Notes

Practical notes from the ranker_v8 production rollout. Written during the rollout so nothing gets forgotten for next time.

## Timeline

| Date | Event |
|---|---|---|
| Sep 10 | ONNX export + validation passed |
| Sep 11 | TRT engine built (A10G target) |
| Sep 12 | Canary deployed at 5% traffic |
| Sep 14 | Canary at 25%, latency regression noted |
| Sep 15 | Rollback to 5%, investigation |
| Sep 17 | Fix merged, canary at 25% again |
| Sep 19 | Full production cutover |

## Latency Regression (Sep 14)

At 25% canary, p99 went from 31ms to 58ms. Root cause: the v8 architecture added a cross-attention block that's much slower on TRT with short sequences (< 64 tokens). The optimization profile had `opt` shape set to batch=32, seq=512 — wrong for our actual distribution which skews short (median seq len ~80 tokens).

Fix: Rebuilt TRT engine with `opt` shape at batch=32, seq=96. P99 dropped to 33ms.

Lesson: **Always profile with production-representative sequence length distribution before building TRT engine.**

## Traffic Splitting Mechanism

We used Triton's built-in ensemble feature to shadow traffic:

```
platform request → ensemble model → [ranker_v7 (primary), ranker_v8 (shadow)]
```

Shadow results logged to BigQuery for offline comparison. This is way cleaner than the feature flag approach we used in previous rollouts.

## Offline Metrics Before Cutover

On the holdout evaluation set (Sep 18 snapshot):

- ranker_v7 NDCG@10: 0.742
- ranker_v8 NDCG@10: 0.761 (+2.6%)
- ranker_v8 MRR: 0.683 vs v7's 0.661 (+3.3%)

Online A/B data from canary (Sep 17-19) showed +1.8% CTR, which is above our 1.0% threshold for full rollout.

## What Went Well

- Shadow traffic setup meant we had 7 days of quality signal before full cutover
- Automated latency regression gate caught the TRT profile issue before it hit > 25% of traffic
- Platform team was great about the extended canary period

## What to Improve

- TRT engine profiling step should be codified in the export pipeline, not done manually
- We didn't have a runbook for the "shadow mode" rollout strategy — writing one now: `runbooks/shadow-rollout.md`
- The rollout took 9 days total; target for future major model updates is ≤ 6 days

See `model-export-pipeline.md`, `triton-serving-setup.md`
