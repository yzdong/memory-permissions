# TensorRT Engine Notes

We use TensorRT engines for the embedding model in prod (lower latency than ORT for our input shapes). These notes capture what's non-obvious.

## Builder Settings

```python
import tensorrt as trt

builder = trt.Builder(logger)
config = builder.create_builder_config()
config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 4 * (1 << 30))  # 4 GB
config.set_flag(trt.BuilderFlag.FP16)

# For INT8 (needs calibrator):
# config.set_flag(trt.BuilderFlag.INT8)
# config.int8_calibrator = MyCalibrator(...)
```

## Engine Portability Warning

**TRT engines are NOT portable across:**
- GPU architectures (A10G engine won't run on T4)
- TensorRT major versions
- CUDA driver versions (sometimes minor versions too)

We build separate engines per target GPU type. Current targets: A100, A10G. T4 is being phased out.

## Optimization Profiles (Dynamic Shapes)

```python
profile = builder.create_optimization_profile()
profile.set_shape("input_ids", min=(1, 16), opt=(32, 256), max=(128, 512))
config.add_optimization_profile(profile)
```

The `opt` shape should reflect your most common production batch shape — TRT optimizes hardest for this.

## Debugging Poor TRT Performance

1. Check if the engine actually uses FP16 kernels — use `trtexec --verbose` and look for `DataType::kHALF`
2. Verify optimization profile matches actual runtime shapes; mismatches cause TRT to interpolate suboptimally
3. Use `trt.IInspector` to dump layer-level timing

```bash
trtexec \
  --onnx=models/onnx/embedder_v3.onnx \
  --fp16 \
  --minShapes=input_ids:1x16 \
  --optShapes=input_ids:32x256 \
  --maxShapes=input_ids:128x512 \
  --saveEngine=models/trt/embedder_v3_a100_fp16.plan \
  --verbose 2>&1 | tee /tmp/trtexec_build.log
```

## Engine Versioning

We store TRT version + GPU arch in the filename:

```
embedder_v3_trt103_a100_fp16.plan
```

This avoids the "which engine do I load" confusion that burned us in September.

## When to Fall Back to ONNX Runtime

- Development environments (no compatible GPU available)
- Models that are updated more than once per week (TRT build time is expensive)
- Models with highly variable input shapes where TRT profile interpolation hurts latency

See `quantization-tradeoffs.md` for accuracy impact of FP16 vs INT8 for TRT engines.
