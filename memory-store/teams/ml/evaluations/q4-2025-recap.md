# Q4 2025 Eval Recap

## Summary

Q4 2025 was the first quarter we ran the full automated eval harness end-to-end without manual intervention on the holdout set. Overall a successful quarter with some notable regressions in the final two weeks tied to a training data pipeline change.

## Results Overview

| Metric | Target | Achieved | Status |
|--------|--------|----------|--------|
| Precision@10 | 0.80 | 0.81 | ✅ |
| Recall@50 | 0.72 | 0.70 | ⚠️ |
| P95 Latency (ms) | 120 | 113 | ✅ |
| NDCG@20 | 0.67 | 0.65 | ⚠️ |

## Notable Events

### November Training Data Incident
- Around Nov 14, a schema migration in the feature store dropped ~8% of user interaction signals
- Recall dropped noticeably in the following eval window before the pipeline team caught it
- Runbook at `runbooks/feature-store-recovery.md` was used to backfill

### Cold Start Improvements
- The new cold-start fallback model shipped in early November exceeded our cold-start precision target by ~4 points
- Worth carrying this momentum into Q1

## Lessons Learned

- We need schema validation checks at ingestion, not just at training time
- Eval cadence of every 3 days was too infrequent to catch the Nov regression quickly — moving to daily in Q1
- The offline-online delta widened in December; see `offline-vs-online-delta.md` for analysis

## Carry-forwards

- Set up alerting on eval score deltas > 2 points over a 7-day window
- Revisit holdout set composition before Q1 begins (see `holdout-set-methodology.md`)
- Coordinate with ranking team on shared NDCG baseline
