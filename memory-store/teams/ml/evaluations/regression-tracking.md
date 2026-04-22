# Regression Tracking

## Overview

This document describes how we detect, triage, and resolve eval metric regressions in the recommender system.

## What Counts as a Regression

We define a regression as a statistically significant degradation (p < 0.05, two-tailed) in any of the following metrics relative to the previous eval run:

- Precision@10
- Recall@50
- NDCG@20
- P95 latency

A "soft regression" alert fires if any metric drops more than 0.015 absolute even without statistical significance — this catches cases where the holdout set was too small to reach significance.

## Alerting Setup

The eval harness writes results to BigQuery. A scheduled query (runs hourly) computes rolling deltas and writes to `ml_evals.regression_alerts`. A Cloud Function then posts to #ml-eval-alerts if any threshold is breached.

For alert configuration, see `../../infra/monitoring/eval-alerts.tf`.

## Triage Runbook

1. **Check if holdout set changed** — a rotation (see `eval-set-rotation.md`) can cause apparent regressions; compare on old holdout too
2. **Check training data freshness** — was there a pipeline incident? Check `#data-platform-incidents`
3. **Check feature store staleness** — see `../../runbooks/feature-store-recovery.md`
4. **Bisect model checkpoints** — use `eval/bisect_checkpoints.py` to find the checkpoint where the regression appeared
5. **If regression is confirmed**: file a P1 in Linear under ML > Regressions and page the on-call

## Historical Regressions

| Date | Metric | Drop | Root Cause | Resolution |
|------|--------|------|------------|------------|
| 2025-05-12 | Precision@10 | -0.03 | Data leakage bug (false positive — harness bug) | Fixed in harness |
| 2025-11-17 | Recall@50 | -0.04 | Feature store schema migration dropped 8% of signals | Backfill + retrain |
| 2025-12-03 | P95 latency | +28ms | Serialization bottleneck introduced in serving layer | Hotfix in 2h |

## Policies

- A regression on the main model branch blocks deployment until resolved or explicitly waived
- Waivers require sign-off from ML lead + product stakeholder
- Regression records must be kept for 12 months for audit purposes

## Related

- `offline-vs-online-delta.md` — online regressions may not surface in offline tracking
- `q4-2025-recap.md` — detailed post-mortem on the November regression
