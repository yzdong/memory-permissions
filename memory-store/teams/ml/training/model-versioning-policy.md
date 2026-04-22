# Model Versioning Policy

## Version Naming

Models follow the scheme: `recommender_v{MAJOR}_{YYYYMMDD}_{short_sha}`

Example: `recommender_v4_20241203_a3f9c1`

- **MAJOR** bumps when the architecture changes (e.g., new tower, different loss function)
- **Date** is the training run date (UTC)
- **short_sha** is the Git SHA of `src/` at training time

Never use a model artifact that lacks all three components — it means it was built outside CI.

## Registry

All promoted models are registered in MLflow at `https://mlflow.internal/models/recommender`. Stages:

| Stage | Meaning |
|-------|---------|
| `Staging` | Passed offline eval, not yet in A/B |
| `Production` | Active in at least one serving shard |
| `Archived` | Retired; kept for rollback reference |

## Promotion Checklist

- [ ] Offline NDCG@10 ≥ current production model's NDCG@10 (or within 0.5% with a strong online justification)
- [ ] Recall@50 ≥ 0.72
- [ ] Inference latency p99 < 40ms on `ml-serve` hardware
- [ ] No regressions on protected demographic slices (see `../evaluations/fairness_report.md`)
- [ ] Canary passed 24h with no elevated error rate
- [ ] Model card updated in `model-cards/recommender_v4.md`

## Rollback

If a production model needs immediate rollback:

```bash
python scripts/serve/rollback.py --model recommender_v4_20241110_b2d8a0 --env prod
```

This pins the previous `Production`-stage model. Alert `#ml-oncall` and open an incident.

## Artifact Storage

- Raw checkpoints: `gs://ml-checkpoints/{run_id}/`  (retained 60 days)
- Registered model weights: `gs://ml-models/registry/{model_version}/` (retained indefinitely)
- Evaluation artifacts: `gs://ml-models/evals/{model_version}/`

## See Also

- `hyperparameter-sweep-guide.md`
- `training-image-build.md`
- `../evaluations/offline_comparison.md`
