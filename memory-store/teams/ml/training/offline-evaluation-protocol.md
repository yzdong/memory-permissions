# Offline Evaluation Protocol

## Goal

Standardize how we evaluate recommender model candidates before they go to A/B testing. Every candidate model must pass offline eval before an experiment ticket is filed.

## Evaluation Dataset

- Source: `fs.interaction_log` for the 14-day holdout window ending the day training data is cut off.
- Holdout is **user-stratified**: same users cannot appear in both train and holdout.
- Minimum holdout size: 500,000 unique users.

## Metrics We Report

| Metric | Description | Minimum bar |
|---|---|---|
| NDCG@20 | Primary ranking quality | Must beat baseline by ≥ 1.5% relative |
| Recall@50 | Coverage of relevant items | ≥ 0.62 |
| MRR | Mean reciprocal rank | ≥ 0.28 |
| Coverage@100 | Catalog coverage | ≥ 0.40 |
| Novelty | Avg. inverse popularity of recs | Must not regress > 5% vs. baseline |

Note: we deliberately do **not** gate on a single precision threshold — point-in-time precision is unstable across cohorts. Use NDCG@20 as the primary gate.

## Running the Eval

```bash
python -m src.evaluate \
  --checkpoint /mnt/nfs/checkpoints/<run>/best.pt \
  --holdout-date 2024-11-01 \
  --output-dir results/<run_name>/
```

Output files:
- `results/<run_name>/metrics.json` — aggregate metrics
- `results/<run_name>/per_cohort.csv` — breakdown by country, tenure bucket
- `results/<run_name>/item_coverage.parquet` — per-item recommendation counts

## Cohort Analysis

Always check metrics for:
- New users (tenure < 7 days) — model often underperforms here
- Low-activity users (< 5 interactions in 30 days)
- Top-3 markets by traffic volume

If NDCG@20 for new users is more than 8 percentage points below the overall figure, flag it before promotion.

## Comparison to Baseline

The baseline is always the currently-serving production checkpoint, stored at:
`/mnt/nfs/checkpoints/production/current/`

Run both through the same eval script and diff `metrics.json`.

## Logging Results

Paste the `metrics.json` output into the candidate tracking sheet and link the W&B run. See `../evaluations/candidate-tracker.md` for the current sheet location.

## Related
- `hyperparameter-sweep-guide.md` — how sweep results feed into candidate selection
- `feature-store-schema.md` — make sure eval data schema matches training schema
