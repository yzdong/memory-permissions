# Worker Service Deploy Notes

> This supplements `deploy.md` with worker-specific considerations. It does not restate the general deploy sequence.

## Why Worker Deploys Are Different

The worker service consumes from Kafka. A rolling restart during a deploy will cause some partitions to be temporarily unassigned, leading to a short lag spike. This is usually acceptable (< 2 minutes) but requires monitoring.

## Pre-Deploy Checks

1. Confirm current Kafka lag is below 10k on all consumer groups:
   ```bash
   just kafka-lag --group worker-group
   ```
   If lag is elevated, wait or investigate before deploying (see `kafka-lag-runbook.md`).

2. Check for any pending schema migrations:
   ```bash
   just db-status --service worker
   ```
   Migrations that add non-nullable columns without defaults must run *before* the new worker pods come up.

3. Verify the worker feature flags are in the expected state for this release:
   ```bash
   just flags list --env production --service worker
   ```

## Deploy Considerations

- **Max unavailable**: set to 1 (not default 25%) to avoid mass partition rebalance.
- **Termination grace period**: 90 seconds — workers need time to finish in-flight message processing. Do not reduce this.
- **Readiness probe**: the worker registers with Kafka only after its readiness probe passes. New pods will not receive partitions until healthy.

## Post-Deploy Validation

```bash
# Watch lag recover
watch -n 10 'just kafka-lag --group worker-group'

# Check handler error rate
just metrics worker.handler.error_rate --window 5m --env production
```

Expect lag to normalize within 3 minutes. Error rate should be < 0.5% post-deploy.

## Rollback

Worker rollback follows the same pattern as the general rollback procedure but has an additional step: verify the rolled-back version can still process any messages produced by the current producer versions. Check the schema compatibility matrix in `../kafka/schema-compatibility.md`.

## Canary Strategy

For high-risk worker changes, deploy to one node first:
```bash
just deploy-worker --strategy canary --canary-replicas 1 --env production
```
Monitor for 10 minutes before promoting the canary to full rollout.
