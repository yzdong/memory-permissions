# ONNX Export Notes

> Last updated by @priya, after we migrated the ranker to ONNX in the staging env.

## Why ONNX

- Decouples training framework (PyTorch) from inference runtime
- Allows Triton to load models without a Python dependency chain at serving time
- Enables hardware-specific optimizations (TensorRT backend, ONNX Runtime providers)

## Export Checklist

1. **Pin opset version** — we standardize on opset 17. Older opsets miss some ops we use in attention layers.
2. **Trace vs. script** — use `torch.onnx.export` with `dynamo=True` for models that have data-dependent control flow.
3. **Input shape validation** — always export with `dynamic_axes` for batch and sequence dims.
4. **Operator coverage check** — run `python tools/check_onnx_ops.py <model>.onnx` before pushing.

```bash
python tools/export_to_onnx.py \
  --checkpoint checkpoints/ranker_v8.pt \
  --output models/onnx/ranker_v8.onnx \
  --opset 17 \
  --dynamic-axes batch seq_len
```

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `Unsupported op: aten::upsample_bilinear2d` | Opset too low | Bump opset to 17+ |
| Shape mismatch at runtime | Static axes exported | Re-export with `dynamic_axes` |
| Numerical diff > 1e-4 | Mixed-precision training artifacts | Cast to fp32 before export |
| Slow ORT inference | CPU EP used instead of CUDA | Set `providers=['CUDAExecutionProvider']` |

## Validation

After export, always run the equivalence check:

```bash
python tools/validate_onnx.py \
  --pytorch checkpoints/ranker_v8.pt \
  --onnx models/onnx/ranker_v8.onnx \
  --tolerance 1e-4
```

If the validator fails, check `logs/onnx_validation/` for per-layer diff reports.

## Where Exported Models Live

- **Staging:** `gs://ml-models-staging/onnx/`
- **Production:** `gs://ml-models-prod/onnx/`

Do not manually push to prod bucket — CI pipeline handles promotion after validation passes.

See also: `triton-serving-setup.md`, `quantization-tradeoffs.md`
