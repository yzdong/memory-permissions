# Q1 2026 Eval Methodology Notes

_These are process and methodology notes for Q1 2026 evals. Metric thresholds are defined in `q1.md` — not here._

## What's New in Q1 2026 Eval Setup

### Cohort

Active cohort for Q1 2026 is `hs-2026-01`. It covers user activity from Oct–Dec 2025 and was frozen on 2026-01-06. See `eval-set-rotation.md` for how it was built.

### Harness Version

All Q1 2026 evals run on harness `v2.0.3`. The main differences from the v1.x harness used through Q3 2025:
- Distributed batch inference (Ray-based) — runs ~4x faster on the same cohort size.
- Slice analysis is now automatic; no more manual slice scripts.
- BigQuery output replaces CSV, enabling the new regression dashboard.

### LLM Judge

We're running the LLM judge pass (`judge-prompt-v2.md`) on 3,000 sampled lists per eval run in Q1. Judge scores are informational only — promotion decisions are still based on Precision@K, Recall@K, and latency as defined in `q1.md`.

## Known Methodology Gaps

- **Geo-stratification**: Still not implemented in the cohort builder. Geo-specific regressions can go undetected. Tracking in `../roadmap/2026-h1.md`.
- **Catalog freshness**: Items added in December 2025 have sparse engagement signals in the holdout window. Expect slightly deflated Precision scores on new-catalog items.
- **Session context**: Our current Precision@10 and Recall@10 computations treat each evaluation as context-free. Session-aware metrics are on the H2 roadmap.

## Eval Run Schedule

| Run Type | Frequency | Trigger |
|----------|-----------|--------|
| Pre-promotion eval | Per checkpoint | Manual via `eval/run.py` |
| Weekly regression sweep | Weekly | Cron, Mondays 6am UTC |
| Judge pass | Per promotion candidate | Automatic when `--judge true` |

## Contact

Eval methodology questions → `#ml-eval` Slack or file an issue in `github.com/company/ml-platform`.
