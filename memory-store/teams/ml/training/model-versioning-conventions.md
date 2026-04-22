# Model Versioning Conventions

## Why We Have This

We've had at least two incidents caused by loading a checkpoint trained on an old feature schema into a serving container expecting a newer schema. This doc establishes the rules so that doesn't happen again.

## Version Format

```
rec-v<MAJOR>.<MINOR>.<PATCH>
```

| Component | Increment when |
|---|---|
| MAJOR | Architecture change — incompatible checkpoint format |
| MINOR | Feature schema version bump or new training dataset split |
| PATCH | Hyperparameter-only change, bug fix, regularization tweak |

Current production model: `rec-v5.2.1`

## Checkpoint Metadata

Every checkpoint must include a `metadata.json` at its root:

```json
{
  "model_version": "rec-v5.2.1",
  "feature_schema_version": "v4.2",
  "training_data_cutoff": "2024-10-31",
  "numpy_version": "1.26.4",
  "torch_version": "2.3.1+cu121",
  "wandb_run_id": "abc123xyz"
}
```

`numpy_version` is explicitly logged because we pin `numpy<2.0` in the training image and need to catch any accidental upgrade.

## Directory Structure

```
/mnt/nfs/checkpoints/
  production/
    current/          → symlink to active prod checkpoint dir
    rec-v5.2.1/
      best.pt
      metadata.json
  staging/
    rec-v5.3.0-rc1/
      best.pt
      metadata.json
  archive/
    rec-v4.x/         → retained for 90 days, then deleted
```

## Promoting a Checkpoint

1. Confirm offline eval passes (see `offline-evaluation-protocol.md`).
2. Update the `production/current` symlink:
```bash
ln -sfn /mnt/nfs/checkpoints/production/rec-v5.3.0/ \
         /mnt/nfs/checkpoints/production/current
```
3. Notify serving team in `#ml-serving` with the new version string and `metadata.json` diff.
4. Tag the commit in `ml-models` repo: `git tag rec-v5.3.0 && git push --tags`

## Rollback

```bash
ln -sfn /mnt/nfs/checkpoints/production/rec-v5.2.1/ \
         /mnt/nfs/checkpoints/production/current
```
Notify `#ml-serving` immediately.

## Compatibility Matrix

| Model version | Feature schema | Notes |
|---|---|---|
| rec-v5.x | v4.2 | Current |
| rec-v4.x | v3.1 | Archived |
| rec-v3.x | v2.0 | Deleted |
