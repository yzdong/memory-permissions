# GPU Cluster Access Runbook

## Cluster Overview

We run training jobs on the `ml-gpu-prod` cluster managed by the Infra team. There's also `ml-gpu-dev` for experimentation — please use dev for anything under 4 hours.

**Contact:** `#infra-gpu-oncall` for quota increases or node failures.

## Getting Access

1. File an access request in the internal IAM portal under **Group: ml-training-users**.
2. Infra will add you within one business day.
3. Verify with:
```bash
ssh <your-ldap>@gateway.ml-gpu-prod.internal
nvidia-smi
```

## Available Node Pools

| Pool | GPU | Count | VRAM | Intended use |
|---|---|---|---|---|
| `a100-40g` | A100 40 GB | 32 | 40 GB | Large model sweeps |
| `a100-80g` | A100 80 GB | 8 | 80 GB | Full-batch training |
| `t4-16g` | T4 16 GB | 64 | 16 GB | Eval, small experiments |

## Submitting a Job

```bash
# Example: 8-GPU training run
sbatch --partition=a100-40g \
       --gres=gpu:8 \
       --time=12:00:00 \
       --job-name=rec-train-sweep \
       scripts/train.sh --config configs/prod_v5.yaml
```

## Priority & Fairshare

- Production training jobs: use `--qos=high`
- Research / sweep jobs: use `--qos=normal` (default)
- Jobs exceeding their walltime are killed without checkpoint. **Set `--time` conservatively.**

## Common Issues

- **NCCL timeout during all-reduce:** Usually a bad node. Run `sinfo -N -l` and exclude it with `--exclude=<node>`.
- **OOM on 40 GB node:** Try gradient checkpointing (`trainer.gradient_checkpointing = true` in config).
- **Job stuck in PD state >10 min:** Check quota with `sshare -u $USER`; ping `#infra-gpu-oncall`.

## Checkpoints

Checkpoints are written to `/mnt/nfs/checkpoints/<job_name>/`. NFS quota per team is 20 TB. Clean up old runs — see `scripts/cleanup_old_checkpoints.sh`.

## See Also

- `training-image-build.md` — ensure your image is pushed before submitting
- `training-failure-modes.md` — diagnostic guide for failed runs
