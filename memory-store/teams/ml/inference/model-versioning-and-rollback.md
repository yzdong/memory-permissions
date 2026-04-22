# Model Versioning and Rollback

How we version models in Triton and how to roll back when things go wrong.

## Triton Version Directories

Triton uses numeric version directories. Higher number = newer version.

```
ranker_onnx/
  config.pbtxt
  41/
    model.onnx
  42/         ← current serving version
    model.onnx
```

`config.pbtxt` controls which version serves traffic:

```protobuf
version_policy {
  specific {
    versions: 42
  }
}
```

We never use `latest` in production — it causes surprise version bumps.

## Version Promotion

1. Export pipeline writes new version directory to GCS.
2. CD pipeline syncs GCS → Triton pod's local model repo via `gsutil rsync`.
3. Triton detects the new directory and loads the model (hot-swap, no restart).
4. Config is updated to point `versions: [new_version]`.
5. Triton unloads the old version after drain.

The config update is the atomic flip. We keep the previous version directory
on disk for at least 48 hours for fast rollback.

## Rollback Procedure

### Fast rollback (< 2 min)

If the previous version directory is still on disk:

```bash
# Update config.pbtxt to point back to previous version
kubectl exec -n ml-system deploy/triton -- \
  sed -i 's/versions: \[42\]/versions: [41]/' \
  /model-repository/ranker_onnx/config.pbtxt

# Triton picks up the config change via inotify — no restart needed
# Verify:
curl triton-svc:8000/v2/models/ranker_onnx | jq .versions
```

### Full rollback (if directory is gone)

Re-sync from GCS. The GCS bucket retains 30 versions. See `runbooks/deploy.md`.

## Canary Traffic Splits

We don't use Triton's built-in ensemble for canary. Instead, the inference
service handles it: `configs/inference-service/canary.yaml` controls the
percentage of requests routed to each model version. Default: 100% to primary.

Changing canary split doesn't require a Triton restart.

## Tracking Which Version Is Live

```bash
curl -s triton-svc:8000/v2/models/ranker_onnx | jq '.versions'
```

Also visible in Grafana panel "Model Version" on the Triton dashboard.
