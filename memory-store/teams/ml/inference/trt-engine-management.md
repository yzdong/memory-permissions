# TensorRT Engine Management

TRT plan files are expensive to build and environment-specific. This doc tracks
how we manage them so we don't rebuild unnecessarily (or use stale ones).

## Why Plan Files Are Annoying

- A plan compiled on one GPU architecture (e.g., Ampere) is **not** portable to
  another (e.g., Ada Lovelace). It will silently fall back to ONNX execution.
- A plan compiled against TRT 8.x doesn't work with TRT 9.x.
- Shape profiles are baked in. If we change `dynamic_axes` ranges, rebuild.

## Plan Naming Convention

```
gs://ml-models-prod/trt-plans/
  <model_name>/
    <model_version>/
      <trt_version>_<gpu_arch>/
        model.plan
```

Example: `ranker/v42/trt9.2_ampere/model.plan`

GPU arch is derived from `nvidia-smi --query-gpu=compute_cap --format=csv,noheader`.

## Build Process

Building happens inside the Triton container at startup via Triton's native
TensorRT integration, OR we can pre-build with `trtexec`:

```bash
trtexec \
  --onnx=model.onnx \
  --saveEngine=model.plan \
  --fp16 \
  --minShapes=input_ids:1x8 \
  --optShapes=input_ids:16x128 \
  --maxShapes=input_ids:64x512 \
  --workspace=4096
```

Pre-building is preferred for prod — it moves the compilation cost out of
the critical path for pod startup.

## Cache Warming

The export pipeline does a warm-up inference pass after building the plan.
This fills the CUDA cache and ensures the first real request isn't slow.
See `model-export-pipeline.md` for where this fits in.

## Invalidation

Plans are invalidated (and must be rebuilt) when:
- TRT minor or major version changes.
- GPU fleet changes architecture.
- ONNX model graph changes (new ops, shape changes).
- Input shape profiles change.

We track the current expected plan signature in the model registry under
`trt_plan_signature`. If the signature on disk doesn't match, the export
pipeline forces a rebuild.

## Incident History

- **2024-09-12**: Prod pods started falling back to ONNX after a node pool
  upgrade changed GPU from A10G to L4 (different compute cap). Plans needed
  rebuild. Added compute_cap check to deploy validation.
