# Training Failure Modes

This is a living doc. Add new failure modes as you encounter them — include the symptom, root cause, and the fix.

---

## 1. Loss Goes to NaN After N Steps

**Symptom:** `train/loss` suddenly becomes `nan`, usually around step 200–500.

**Causes (in order of frequency):**
1. Learning rate too high — gradients explode.
2. Bad batch containing all-zero or all-padding items (rare, see data cleaning issue #312).
3. `fp16` mixed-precision with a loss scale that overflowed.

**Fixes:**
- Reduce LR by 5× and restart from last checkpoint.
- Add gradient clipping: `trainer.max_grad_norm = 1.0`.
- Switch to `bf16` if on A100 hardware — more numerically stable than `fp16`.

---

## 2. NCCL Timeout / Hang During Distributed Training

**Symptom:** Job hangs at an all-reduce step; workers eventually timeout with `NCCL error: unhandled system error`.

**Cause:** Usually a bad NIC or a flaky node in the job allocation.

**Fix:**
```bash
sinfo -N -l | grep drain   # find drained/bad nodes
scancel <job_id>
sbatch --exclude=<bad-node> <original-script>
```
If it recurs, report the node to `#infra-gpu-oncall`.

---

## 3. Checkpoint Corruption

**Symptom:** `torch.load` raises an error when resuming; checkpoint file is 0 bytes or truncated.

**Cause:** Job was killed mid-write (walltime exceeded, preemption, node failure).

**Fix:** Roll back to the previous checkpoint. We save every 1000 steps; worst case you lose 1000 steps.

**Prevention:** Enable atomic checkpoint writes — see `src/training/checkpoint.py:save_atomic()`.

---

## 4. Feature Mismatch at Training Time

**Symptom:** `KeyError` or shape mismatch in the feature preprocessing step; usually right after a schema change.

**Cause:** Model config references a feature column that was renamed or dropped in the feature store.

**Fix:**
1. Check `feature-store-schema.md` for the current schema version.
2. Update `configs/features_v<N>.yaml` to match.
3. If you need to run on old data, pin the schema version in the dataset loader.

---

## 5. OOM on GPU Despite Small Batch Size

**Symptom:** `CUDA out of memory` even with `batch_size=64`.

**Causes:**
- Activation memory not freed — you may have a graph retained somewhere.
- Embedding table too large for single GPU; need model parallel.
- Memory leak in a custom CUDA kernel.

**Quick diagnostics:**
```python
print(torch.cuda.memory_summary())
```

**Fix:** Enable gradient checkpointing first — it trades compute for memory. If that's not enough, open a ticket with the model-parallel flag.

---

## 6. Slow DataLoader (GPU Starvation)

**Symptom:** GPU utilization < 30% between batches; `data_time` in logs >> `compute_time`.

**Fix:**
- Increase `num_workers` (try 8–16 on A100 nodes).
- Move feature prefetching to a background thread.
- Check NFS mount latency: `df -h /mnt/nfs && iostat -x 5`.

---

## See Also
- `gpu-cluster-access.md`
- `data-cleaning-pipeline.md`
