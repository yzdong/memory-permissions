# Distributed Training Setup

## Overview

For production training runs we use PyTorch DDP (DistributedDataParallel) across multiple A100 nodes. This doc covers how to set it up correctly and the gotchas we've hit.

## Architecture

- **Communication backend:** NCCL (InfiniBand fabric on the A100 nodes)
- **Launch method:** `torchrun` via SLURM `srun`
- **Typical config:** 4 nodes × 8 GPUs = 32 GPUs total

## SLURM Script Template

```bash
#!/bin/bash
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --gres=gpu:8
#SBATCH --partition=a100-40g
#SBATCH --time=08:00:00
#SBATCH --job-name=rec-train-prod
#SBATCH --output=logs/%x-%j.out

export MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)
export MASTER_PORT=29500
export NCCL_IB_DISABLE=0
export NCCL_DEBUG=WARN

srun torchrun \
  --nnodes=$SLURM_NNODES \
  --nproc_per_node=8 \
  --rdzv_id=$SLURM_JOB_ID \
  --rdzv_backend=c10d \
  --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \
  -m src.train --config-name prod_v5
```

## Key Environment Variables

| Variable | Purpose | Our setting |
|---|---|---|
| `NCCL_IB_DISABLE` | Use InfiniBand | `0` (enabled) |
| `NCCL_DEBUG` | NCCL logging | `WARN` (use `INFO` when debugging) |
| `OMP_NUM_THREADS` | CPU threads per worker | `4` |
| `TOKENIZERS_PARALLELISM` | Avoid HuggingFace deadlock | `false` |

## Gradient Synchronization Notes

- DDP performs all-reduce after each backward pass. With 32 GPUs and large embeddings (~500M parameters), this adds ~800ms overhead per step.
- We use `find_unused_parameters=False` — make sure all model parameters participate in the forward pass or you'll get hangs.
- The item embedding table is sharded with `torch.nn.parallel.DistributedDataParallel` — don't accidentally put it on a single GPU.

## Debugging Distributed Hangs

```bash
# Check which ranks are alive
squeue -j $JOB_ID -o "%N %T"

# Increase NCCL verbosity in a single run
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=ALL
```

Common hang causes:
1. Unequal batch sizes across ranks (ensure dataset is divisible by world size, or use `drop_last=True`).
2. One rank throws an exception but others keep waiting at the barrier.
3. Firewall blocking the rendezvous port — check with `#infra-gpu-oncall`.

## See Also
- `gpu-cluster-access.md` — cluster prerequisites
- `training-failure-modes.md` — NCCL failure mode (#2)
- `training-config-reference.md` — training config options
