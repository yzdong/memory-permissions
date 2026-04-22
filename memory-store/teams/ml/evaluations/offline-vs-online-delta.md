# Offline vs. Online Delta Analysis

## Background

There's a persistent gap between our offline eval metrics and the online A/B results for the same model version. This document tracks that delta over time and hypothesizes causes.

## Observed Deltas (by quarter)

| Quarter | Offline Precision@10 | Online CTR Lift (proxy) | Delta Notes |
|---------|----------------------|-------------------------|-------------|
| Q2 2025 | 0.78 | +1.2% | Reasonable alignment |
| Q3 2025 | 0.79 | +0.6% | Gap widened — position bias suspected |
| Q4 2025 | 0.81 | +0.9% | Partial recovery after debiasing |

## Root Cause Hypotheses

### 1. Position Bias
Offline metrics assume uniform exposure, but online users heavily favor top-3 positions. Our recall@k metrics may be overstating actual user discovery.

**Mitigation tried:** Inverse propensity scoring on offline labels (Q3 2025). Helped somewhat.

### 2. Feedback Loop Drift
The model trained on data that itself was influenced by a prior model version. Offline eval on "natural" holdout data doesn't capture this.

### 3. Feature Freshness
Online serving uses near-real-time features; offline eval uses features materialized at training time. Staleness is a known issue for user-state features (recency, last click).

```
Estimated staleness window in Q4 offline eval: ~4 hours average
Estimated staleness window online: ~15 minutes
```

## Recommendations

- Add online shadow logging to the eval harness to enable counterfactual estimates
- Don't over-index on offline precision as a launch gate — use it as a directional signal
- Document the expected delta range so stakeholders aren't surprised; current expectation is ±0.3–0.8 CTR points per 0.01 offline precision

## Related Docs

- `q4-2025-recap.md`
- `eval-harness-readme.md`
- `../runbooks/ab-test-launch.md`
