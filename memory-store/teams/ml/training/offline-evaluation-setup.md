# Offline Evaluation Setup

## What We Measure

For the recommender, offline evaluation runs against a held-out test set constructed from the last 14 days of cleaned events (excluding the training window).

### Primary Metrics

| Metric | Description | Minimum bar |
|--------|-------------|-------------|
| NDCG@10 | Normalized discounted cumulative gain, top-10 | Beat current prod |
| Recall@50 | Fraction of relevant items in top-50 | ≥ 0.72 |
| MRR | Mean reciprocal rank | Informational only |

### Slice Metrics

We always report metrics broken down by:
- User activity tier (cold: <5 sessions/month, warm: 5–50, hot: >50)
- Content category (top-10 categories)
- Platform (iOS, Android, Web)

Slice results live in `gs://ml-models/evals/{model_version}/slice_metrics.json`.

## Running Evaluation

```bash
python scripts/evaluate.py \
  --model-uri gs://ml-models/registry/recommender_v4_20241203_a3f9c1/ \
  --eval-date 2024-12-01 \
  --output-dir gs://ml-models/evals/recommender_v4_20241203_a3f9c1/
```

This takes ~25 minutes on a 4×T4 node.

## Test Set Construction

The test set is constructed by `src/eval/build_test_set.py`. Key decisions:

- **Temporal split**: test events are always strictly after training events to prevent leakage
- **User holdout**: 5% of users are fully held out (never seen during training) to measure cold-start
- **Negative sampling**: 500 random negatives per positive, stratified by popularity bucket

If you change the test set construction, the previous comparisons are no longer valid. Bump the eval dataset version in `configs/eval/test_set.yaml` and re-evaluate the current production model first.

## Comparing Two Models

```python
from src.eval.comparison import compare_models

results = compare_models(
    baseline="recommender_v4_20241110_b2d8a0",
    candidate="recommender_v4_20241203_a3f9c1",
    eval_date="2024-12-01",
)
results.to_markdown()  # prints comparison table
```

## Known Issues

- Cold-start users (0 features) show artificially low recall; this is expected and tracked separately
- The evaluation script does not currently support models with custom tokenizers — open issue ML-318
