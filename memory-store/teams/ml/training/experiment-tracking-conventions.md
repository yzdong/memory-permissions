# Experiment Tracking Conventions

We track all training runs in MLflow at `https://mlflow.internal`. This doc explains what to log, how to name things, and how to find results later.

## Naming Experiments

MLflow experiment name format: `{team}/{model}/{purpose}`

Examples:
- `ml/recommender/baseline`
- `ml/recommender/hyperparam-sweep-v4`
- `ml/recommender/feature-ablation`

Do not create experiments with generic names like `test` or `debug` — they pollute the namespace and we can't clean them up without losing run history.

## Required Tags

Every run **must** have these MLflow tags set:

```python
mlflow.set_tags({
    "git_sha": get_git_sha(),
    "config_path": args.config,
    "dataset_date": cfg.dataset.date,
    "model_version": cfg.model.version,
    "author": os.environ["LDAP_USER"],
})
```

This is enforced by `src/training/mlflow_setup.py` — don't bypass it.

## What to Log

### Metrics (every N steps)
- `train/loss`
- `val/ndcg_10`
- `val/recall_50`
- `val/mrr`
- `train/learning_rate`
- `system/gpu_util_pct` (if available)

### Artifacts
- Final model checkpoint
- `slice_metrics.json` from offline eval
- The resolved config YAML (not the template)
- Training curve plot (PNG)

## Finding a Previous Run

Filter in the MLflow UI by tag `git_sha` or `dataset_date`. Alternatively:

```python
import mlflow
client = mlflow.tracking.MlflowClient()
runs = client.search_runs(
    experiment_ids=["12"],
    filter_string="tags.model_version = 'v4' and tags.dataset_date = '2024-11-18'",
    order_by=["metrics.val/ndcg_10 DESC"],
)
```

## Comparing Runs

Use the MLflow UI's comparison view. For command-line comparisons, use `scripts/compare_runs.py` which outputs a markdown table suitable for PRs.

## Archiving Old Experiments

Experiments older than 6 months with no `Production` model promotions are moved to the `_archive` namespace by a quarterly cleanup job. Runs are not deleted; just reorganized.
