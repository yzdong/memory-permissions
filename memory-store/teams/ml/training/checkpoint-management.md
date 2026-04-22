# Checkpoint Management

## Storage Locations

- **Ephemeral (in-job)**: `/mnt/checkpoints/` on the training pod (500 GB limit, lost on job end)
- **Persistent**: `gs://ml-checkpoints/{run_id}/step_{n}.pt`
- **Promoted**: `gs://ml-models/registry/{model_version}/model.pt`

Always configure jobs to write to GCS — never rely on ephemeral storage as your only checkpoint.

## Checkpoint Frequency

Default: every 1,000 steps and at end of each epoch.  
For long runs (>24h), reduce to every 500 steps. If the job gets preempted, you lose at most 500 steps of work.

```yaml
# configs/train/recommender_v4.yaml
checkpointing:
  every_n_steps: 1000
  every_epoch: true
  backend: gcs
  gcs_path: gs://ml-checkpoints/${RUN_ID}/
  keep_last_n: 5
```

`keep_last_n: 5` means we only retain the 5 most recent step checkpoints to control storage costs. The epoch checkpoints are always retained.

## Resuming From a Checkpoint

```bash
python scripts/train.py \
  --config configs/train/recommender_v4.yaml \
  --resume-from gs://ml-checkpoints/run_20241203_001/step_15000.pt
```

The trainer will validate that the checkpoint's config hash matches the current config. If it doesn't match, you'll get a warning — investigate before proceeding.

## Checkpoint Retention Policy

| Location | Retention |
|----------|-----------|
| `gs://ml-checkpoints/` | 60 days, then auto-deleted |
| `gs://ml-models/registry/` | Indefinite |

If you need a checkpoint beyond 60 days, copy it to the registry bucket manually with appropriate naming.

## Inspecting a Checkpoint

```python
import torch
ckpt = torch.load("step_15000.pt", map_location="cpu")
print(ckpt.keys())  # ['model_state', 'optimizer_state', 'step', 'config_hash', 'metrics']
print(ckpt['step'])
print(ckpt['metrics'])  # {'train_loss': 0.312, 'val_ndcg10': 0.391}
```

## Common Issues

- **Checkpoint file not found**: The GCS path in `config.yaml` may use `${RUN_ID}` which wasn't exported — check your job submission script
- **Config hash mismatch**: You changed a config field after the checkpoint was saved; either revert or override with `--ignore-config-hash` (use cautiously)
