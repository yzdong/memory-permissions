# Hyperparameter Sweep Guide

## When to Run a Sweep

Run a sweep when:
- Introducing a new model architecture component
- Offline metrics plateau and you suspect suboptimal learning rate or regularization
- Post-dataset-shift (new feature schema version, major data distribution change)

Don't run sweeps in the week before a planned production push — results won't be actionable in time.

## Tools

We use **Weights & Biases Sweeps** for orchestration. Config lives in `configs/sweep/`.

## Example Sweep Config

```yaml
# configs/sweep/lr_wd_sweep.yaml
program: src/train.py
method: bayes
metric:
  name: val/ndcg_at_20
  goal: maximize
parameters:
  learning_rate:
    distribution: log_uniform_values
    min: 1e-5
    max: 1e-2
  weight_decay:
    values: [0.0, 0.01, 0.1]
  dropout:
    distribution: uniform
    min: 0.0
    max: 0.4
  batch_size:
    values: [512, 1024, 2048]
```

## Launching a Sweep

```bash
# Initialize — do this once
wandb sweep configs/sweep/lr_wd_sweep.yaml
# Note the sweep ID printed (e.g. abc123)

# Start agents on the cluster — one per GPU node
sbatch --array=0-7 --partition=a100-40g scripts/sweep_agent.sh abc123
```

## Interpreting Results

- Primary metric: `val/ndcg_at_20` (normalized discounted cumulative gain, cutoff 20)
- Secondary gates before promotion:
  - `val/recall_at_50` ≥ 0.62
  - `val/mrr` ≥ 0.28
- Ignore runs with `train/loss` NaN — these are diverged runs, typically from too-high LR.

## Budget Guidance

- Aim for 60–80 runs for a Bayesian sweep to converge.
- Cap individual run time at 4 hours (set `--time=04:00:00`).
- Terminate the sweep early if the top-5 runs cluster within 0.5% on the primary metric after 40 runs.

## Logging Conventions

All sweep runs must log:
```python
wandb.log({"val/ndcg_at_20": ..., "val/recall_at_50": ..., "epoch": ...})
```
Use `wandb.config` to pull hyperparameters — don't hardcode them.

## After the Sweep

1. Export the best config: `scripts/export_best_sweep_config.py --sweep-id abc123`
2. Run a full training job with that config and verify metrics hold.
3. Document results in `../evaluations/sweep-results-<date>.md`.
4. Archive sweep configs in `configs/sweep/archive/`.

## See Also
- `gpu-cluster-access.md` — cluster submission details
- `training-image-build.md` — image to use for sweep agents
