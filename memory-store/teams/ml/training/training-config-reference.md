# Training Config Reference

All training jobs are configured via YAML files under `configs/`. We use Hydra for config composition. This page documents the key knobs and what they do.

## Config Hierarchy

```
configs/
  base.yaml           # Defaults for all runs
  prod_v5.yaml        # Production training config
  dev.yaml            # Lightweight config for local iteration
  sweep/              # Sweep configs (see hyperparameter-sweep-guide.md)
  features/           # Feature set configs
    features_v4.yaml
```

## Key Parameters

### Model
```yaml
model:
  architecture: two_tower      # Options: two_tower, cross_attention
  embedding_dim: 256
  user_tower_layers: [512, 256]
  item_tower_layers: [512, 256]
  dropout: 0.15
  l2_norm_embeddings: true
```

### Training Loop
```yaml
training:
  batch_size: 1024
  learning_rate: 3.0e-4
  weight_decay: 0.01
  max_epochs: 20
  warmup_steps: 2000
  lr_scheduler: cosine
  max_grad_norm: 1.0
  precision: bf16          # Use fp32 on non-A100 hardware
  gradient_checkpointing: false
```

### Data
```yaml
data:
  feature_schema_version: v4.2
  train_start_date: "2024-05-01"
  train_end_date: "2024-10-31"
  holdout_days: 14
  num_workers: 12
  prefetch_factor: 4
  negative_sampling_ratio: 4    # Negatives per positive
```

### Checkpointing
```yaml
checkpointing:
  save_every_n_steps: 1000
  keep_last_n: 3
  checkpoint_dir: /mnt/nfs/checkpoints/${run_name}/
  atomic_writes: true
```

### Logging
```yaml
logging:
  wandb_project: rec-training
  log_every_n_steps: 50
  eval_every_n_steps: 500
```

## Overriding via CLI

```bash
python -m src.train \
  --config-name prod_v5 \
  training.learning_rate=1e-3 \
  training.batch_size=2048
```

## Gotchas

- `precision: bf16` requires A100 or newer. Set to `fp32` on T4 nodes.
- `negative_sampling_ratio` values above 8 slow down the dataloader significantly on NFS-backed datasets.
- `data.num_workers` should not exceed the number of CPUs on the node minus 2. Check with `nproc`.

## See Also
- `training-image-build.md` — runtime environment
- `hyperparameter-sweep-guide.md` — how to search over these params
