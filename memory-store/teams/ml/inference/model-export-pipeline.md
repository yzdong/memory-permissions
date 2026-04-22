# Model Export Pipeline

This documents the automated pipeline that takes a trained PyTorch checkpoint and produces a Triton-ready artifact. The pipeline lives in `ml/pipelines/export/`.

## Pipeline Stages

```
[1] Checkpoint validation
       │
[2] ONNX export (opset 17)
       │
[3] Equivalence test (PyTorch vs ONNX)
       │
[4] Optional: TensorRT engine build
       │
[5] Latency regression test
       │
[6] Artifact upload to GCS
       │
[7] Triton model-repository PR (auto-generated)
```

## Triggering an Export

Exports are triggered by tagging a W&B run:

```bash
python ml/pipelines/export/trigger.py \
  --wandb-run-id abc123def \
  --model-name ranker \
  --target onnx tensorrt
```

This kicks off a Cloud Build job. Status visible in `#ml-model-export` Slack channel.

## Configuration File

Each model has an export config at `ml/configs/export/<model_name>.yaml`:

```yaml
model_name: ranker_v8
opset_version: 17
dynamic_axes:
  input_ids: [0, 1]
  attention_mask: [0, 1]
tolerance: 1e-4
latency_regression_threshold_ms:
  p50: 20
  p99: 55
tensorrt:
  enabled: true
  precision: fp16
  workspace_gb: 4
```

## Latency Regression Gate

If the new ONNX model's p99 exceeds the threshold by >10%, the pipeline fails and sends an alert. This has caught two regressions in the past quarter — once from an accidental opset downgrade, once from a model architecture change that added a dense layer.

## Artifact Naming Convention

```
gs://ml-models-staging/onnx/ranker/ranker_v8_20240918_abc123.onnx
gs://ml-models-staging/trt/ranker/ranker_v8_20240918_abc123_fp16.plan
```

The `abc123` is the first 6 chars of the W&B run ID — keeps things traceable.

## Known Limitations

- TRT engine build takes ~25 minutes on T4; we've been talking about moving to A10G builders but haven't prioritized it.
- The pipeline doesn't yet support multi-model ensembles — those are exported manually. See `onnx-export-notes.md`.
- Python version in the Cloud Build image must match training environment exactly — this bit us in August when training moved to 3.11 and the export job was still on 3.10.

Related: `triton-serving-setup.md`, `onnx-export-notes.md`
