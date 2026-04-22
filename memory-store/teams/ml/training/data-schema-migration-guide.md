# Feature Store Schema Migration Guide

When a new feature schema version is cut (e.g., v4.2 → v4.3), there are several moving parts across the training pipeline, eval pipeline, and serving stack. This doc is the checklist.

## Who Needs to Know

Before starting a migration, loop in:
- ML training team (this team)
- ML serving team (`#ml-serving`) — they need compatible model exports
- Data platform (`#ml-data-eng`) — they manage the Hive tables
- Offline eval team — the eval harness must match the new schema

## Pre-Migration Checklist

- [ ] New schema version defined in `ml-platform/feature-store-defs` and merged
- [ ] Backfill for new columns completed for at least 30 days of history
- [ ] `fs.item_features` and `fs.user_embeddings` tables confirmed healthy (check Datadog)
- [ ] Model config updated: `configs/features/features_v<N+1>.yaml` created
- [ ] Training image rebuilds confirmed not needed (or triggered — see `training-image-build.md`)
- [ ] Offline eval harness updated to use new schema version

## Migration Steps

### 1. Update Feature Config

Create `configs/features/features_v4.3.yaml` with the new columns. Update `prod_v5.yaml` to reference it:
```yaml
data:
  feature_schema_version: v4.3
  features_config: features/features_v4.3
```

### 2. Train a Shadow Model

Train a model on the new schema without promoting it:
```bash
sbatch scripts/train.sh --config configs/prod_v5.yaml \
  data.feature_schema_version=v4.3 \
  run_name=schema-migration-v4.3-shadow
```

### 3. Offline Eval on Shadow Model

Run eval with the **new** schema holdout data. Compare against baseline (which uses v4.2). Both NDCG@20 and Recall@50 must meet or exceed baseline thresholds.

### 4. Update `metadata.json`

Ensure the promoted checkpoint's `metadata.json` reflects `feature_schema_version: v4.3`.

### 5. Coordinate Serving Cutover

Serving reads `metadata.json` to know which feature schema to request at inference time. The serving team must deploy the new feature fetcher before the model goes live. **Do not promote the model before confirming serving is ready.**

### 6. Update `feature-store-schema.md`

Update the canonical schema doc with the new columns and version number.

### 7. Archive Old Schema

Models trained on the old schema should be moved to `/mnt/nfs/checkpoints/archive/` per the versioning conventions in `model-versioning-conventions.md`.

## Rollback

If anything goes wrong post-promotion:
1. Revert `production/current` symlink to the v4.2-schema model.
2. Serving team reverts feature fetcher config.
3. File a post-mortem in this directory under `YYYY-MM-DD-schema-migration-incident.md`.

## See Also
- `feature-store-schema.md`
- `model-versioning-conventions.md`
- `offline-evaluation-protocol.md`
