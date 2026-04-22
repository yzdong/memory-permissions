# Training Image Build

## Overview

All training jobs run inside a Docker image defined at `docker/training/Dockerfile`. The image is built by CI on merges to `main` and pushed to the internal registry at `registry.internal/ml/training`.

## Key Constraints

> **numpy must stay pinned to `<2.0`.**  
> The base CUDA image uses a native extension that segfaults with numpy 2.x. This is tracked in [infra issue #4821](http://internal-jira/INFRA-4821). Do not bump this pin without coordinating with the Infra team.

## Dockerfile Summary

```dockerfile
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04

RUN apt-get update && apt-get install -y python3.11 python3-pip git

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Training source
COPY src/ /workspace/src/
WORKDIR /workspace
ENTRYPOINT ["python", "-m", "src.train"]
```

## requirements.txt Highlights

```
torch==2.3.1+cu121
numpy<2.0          # DO NOT CHANGE — see note above
scikit-learn==1.4.2
hydra-core==1.3.2
wandb==0.17.0
pyarrow==16.0.0
```

## Building Locally

```bash
cd docker/training
docker build -t ml-training:local .
# Quick smoke test
docker run --gpus all ml-training:local python -c "import torch; print(torch.cuda.is_available())"
```

## CI/CD Pipeline

- Triggered on pushes to `main` that touch `docker/training/**` or `requirements.txt`.
- Pipeline: `.github/workflows/build-training-image.yml`
- Tags pushed: `latest`, `sha-<short-commit>`, `<semver>` (when tagged)

## Pinning a Specific Image in Job Scripts

Always pin by digest for production training:
```bash
#SBATCH --container-image=registry.internal/ml/training@sha256:<digest>
```
Never use `:latest` in production jobs — it makes runs non-reproducible.

## Updating the Image

1. Modify `Dockerfile` or `requirements.txt`.
2. Open a PR; CI will build and run `tests/smoke_test_image.py`.
3. After merge, note the new digest and update `configs/prod_v5.yaml` → `container_image`.
4. Announce in `#ml-training` with the diff summary.

## See Also
- `gpu-cluster-access.md` — how to submit jobs using this image
- `hyperparameter-sweep-guide.md` — sweep-specific image notes
