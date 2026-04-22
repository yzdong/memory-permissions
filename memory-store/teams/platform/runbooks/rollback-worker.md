# Worker Service Rollback

This covers rolling back the `worker` service. Worker rollbacks have additional considerations compared to stateless services because of Kafka offset state.

## Decision Checklist Before Rolling Back

- [ ] Confirmed the issue is caused by the current worker version (not a Kafka or DB issue).
- [ ] Checked schema compatibility: does the previous worker version handle messages produced by current producers? (See `../kafka/schema-compatibility.md`.)
- [ ] Is there data that the current worker version has already processed that the old version would re-process incorrectly? If yes, rollback may cause data corruption — escalate to #platform-leads.

## Finding the Previous SHA

```bash
just deploy-history --service worker --env production --limit 5
```

## Executing the Rollback

```bash
just rollback worker --to-sha <previous-sha> --env production
```

This performs a rolling update. Because worker is a Kubernetes Deployment, Kafka partitions will rebalance twice (during scale-down of new pods and scale-up of old pods). Expect a lag spike of up to 5 minutes.

## Monitoring During Rollback

```bash
# Watch pod transitions
kubectl rollout status deployment/worker -n workers

# Monitor lag
watch -n 15 'just kafka-lag --group worker-group'

# Watch for handler errors from the old version
just logs worker --env production --tail 100 --follow
```

## If the Rollback Is Also Failing

If both the new and old worker versions are failing on the same messages, the issue is likely in the message payload or a downstream dependency, not the worker code. Steps:

1. Pause the affected consumer group to stop processing:
   ```bash
   just feature-flag set PAUSE_CONSUMER_WORKER_GROUP true --env production
   ```
2. Investigate the failing message using the DLQ (see `worker-stuck-jobs.md`).
3. Fix the root cause (data issue or downstream), then unpause.

## Post-Rollback

- Confirm lag returns to < 5k within 10 minutes.
- Post in #platform-incidents with the rollback SHA and reason.
- Open a tracking issue to root-cause before re-attempting the forward deploy.
- Update `../incidents/worker-rollbacks.md`.
