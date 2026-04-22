# Eval Harness — README

This is the main entry point for understanding how to run, configure, and extend the ML team's offline evaluation harness.

## What It Does

The eval harness:
1. Loads a frozen model checkpoint and serving config
2. Runs inference against a specified holdout set
3. Computes ranking metrics (Precision@k, Recall@k, NDCG@k, MRR)
4. Optionally invokes the LLM judge (see `judge-prompt-v2.md`) for relevance scoring
5. Writes results to BigQuery and posts a summary to #ml-eval-reports

## Quick Start

```bash
cd ml-platform/eval
pip install -r requirements.txt

python run_eval.py \
  --model-path gs://ml-models/recommender/checkpoints/latest/ \
  --holdout-path gs://ml-evals/holdout/2026-q1/ \
  --metrics precision_at_10 recall_at_50 ndcg_at_20 \
  --output-table ml_evals.results
```

## Configuration

All defaults live in `eval/config/defaults.yaml`. Override any field with `--config-override key=value`.

Key fields:
- `judge.enabled`: Set to `true` to use LLM-based relevance labels
- `judge.relevance_threshold`: Score cutoff for "relevant" (default: 4)
- `metrics.k_values`: List of k values for @k metrics
- `holdout.sample_rate`: Fraction of holdout to use (1.0 for full run, 0.1 for quick smoke test)

## Data Leakage Guard

Added in Q2 2025 after a near-miss: the harness now checks that no user in the holdout set appears in the training manifest for the given checkpoint. This runs automatically before inference.

```python
# eval/leakage_check.py
def assert_no_user_overlap(holdout_users, training_manifest_path):
    training_users = load_user_set(training_manifest_path)
    overlap = holdout_users & training_users
    if overlap:
        raise ValueError(f"Data leakage: {len(overlap)} users appear in both splits")
```

## Output Schema

Results are written to `ml_evals.results` with columns: `run_id`, `timestamp`, `model_version`, `holdout_id`, `metric_name`, `k`, `value`.

## Extending the Harness

- New metrics: add a class to `eval/metrics/` inheriting from `BaseMetric`
- New judge prompts: update `eval/judge_client.py` and document in `judge-prompt-v2.md`

## Runbook

If an eval run fails mid-way, see `../../runbooks/eval-recovery.md`.
