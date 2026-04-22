# Gateway Rollback Runbook

This covers rolling back the `gateway` service specifically. For api or worker rollback procedures, see `rollback-api.md` and `rollback-worker.md`.

## When to Roll Back

- Error rate on gateway > 5% sustained for 3+ minutes post-deploy.
- P99 latency exceeds 800ms (baseline is ~120ms).
- TLS handshake failures appearing in logs.
- Any routing misconfiguration causing 502/504 at the load balancer.

## Identifying the Previous Good SHA

```bash
just deploy-history --service gateway --env production --limit 5
```
Pick the last SHA that was stable. Cross-reference with the Grafana annotation on the `Platform / Gateway` dashboard.

## Rolling Back

```bash
just rollback gateway --to-sha <previous-sha> --env production
```

This triggers a rolling update back to the specified image. The gateway is stateless so rollback is fast (< 2 minutes for 6 replicas).

## Verifying the Rollback

```bash
# Confirm running image
kubectl get pods -n gateway -o jsonpath='{.items[*].spec.containers[0].image}'

# Hit a canary health endpoint
curl -sf https://gateway-internal.prod/health | jq .

# Watch error rate
just metrics gateway.upstream.error_rate --window 2m --env production
```

Error rate should drop below 1% within 90 seconds of rollback completing.

## Gateway-Specific Gotchas

- **TLS cert state**: the gateway holds TLS cert cache in memory. After rollback, cert rotation state may differ from the rolled-back version's expectations. Check `certificate-rotation.md` if TLS issues persist.
- **Rate limit counters**: stored in Redis; rollback does not reset them. This is usually fine, but if the old version had a rate limit bug, counters may be in a weird state. Flush with:
  ```bash
  redis-cli -h redis.internal DEL ratelimit:*
  ```
  (Use cautiously — this resets all rate limits temporarily.)
- **Config map version**: ensure the rollback SHA is compatible with the current `gateway-config` ConfigMap. If the ConfigMap was updated as part of the bad deploy, roll that back too:
  ```bash
  kubectl rollout undo configmap gateway-config -n gateway
  ```

## Post-Rollback

- Post outcome in #platform-incidents.
- Add entry in `../incidents/gateway-rollbacks.md`.
- Open a ticket to root-cause the bad deploy before re-attempting.
