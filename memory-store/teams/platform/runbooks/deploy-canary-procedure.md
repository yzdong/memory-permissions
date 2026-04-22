# Canary Deploy Procedure

Documents how canary deploys work in our pipeline and what to do when a canary behaves unexpectedly. The standard deploy flow includes canary by default — this file covers the monitoring and decision-making layer, not the invocation.

## What canary means here

We route 5% of production traffic to the new version for 10 minutes before promoting. The canary pod set runs alongside the current stable pods.

Canary traffic selection is done at the gateway layer using a weighted routing rule in Envoy config.

## Canary metrics

During the canary window, watch:

| Metric | Stable baseline | Canary threshold to abort |
|---|---|---|
| 5xx error rate | < 0.1% | > 0.4% |
| p99 latency | < 300ms | > 600ms |
| Auth failure rate | < 0.05% | > 0.2% |

Thresholds are configured in `infra/canary/thresholds.yaml`. Do not adjust them inline during a deploy.

## Manual abort

If you see canary metrics crossing thresholds before the automated system catches it:

```bash
just canary-abort <service>
```

This immediately shifts 100% of traffic back to stable and deletes the canary pod set.

## Manual promote

If you're confident before the 10 minutes are up:

```bash
just canary-promote <service>
```

This skips the remaining canary window. Use only if delay is causing business impact.

## Canary for worker

Worker doesn't receive HTTP traffic, so canary works differently:
- Canary worker gets 10% of Kafka partition assignments
- Monitored via job error rate and processing duration
- The same abort/promote commands apply

## Edge case: canary and migrations

If a deploy includes a database migration, the migration runs before canary starts. This means the new schema is live for both canary and stable. Ensure all migrations are backward-compatible with the previous binary version. See `postgres-migration-runbook.md`.

## Logging canary decisions

All canary promote/abort decisions are logged to the deploy audit log in S3: `s3://platform-deploy-logs/canary/`. Retention is 1 year.
