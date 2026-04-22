# Kafka Consumer Lag Runbook

## When to Use This

Triggered when consumer lag on any topic exceeds 50k messages, or when the `worker` service emits `consumer_lag_critical` alerts.

## Diagnosing the Problem

1. Check current lag across consumer groups:
   ```bash
   kafka-consumer-groups.sh --bootstrap-server kafka:9092 \
     --describe --all-groups
   ```
2. Identify which partition(s) are behind. Uneven lag often points to a hot partition rather than a slow consumer overall.
3. Verify worker pod count:
   ```bash
   kubectl get pods -n workers -l app=worker
   ```
4. Pull recent worker logs for deserialization errors or slow handler traces:
   ```bash
   kubectl logs -n workers -l app=worker --tail=200 | grep -E 'ERROR|lag|slow'
   ```

## Common Causes

- **Hot partition**: a single key dominates traffic. Check producer side — see `../kafka/partition-strategy.md`.
- **Downstream DB slowness**: worker handlers that write to Postgres are blocking. Check `postgres-slow-queries.md`.
- **Worker OOM**: pod restarts drop in-flight messages temporarily. Look for `OOMKilled` in pod events.
- **Schema mismatch**: a new producer is emitting a schema version the worker hasn't deployed yet.

## Remediation Steps

### Scale out workers temporarily
```bash
kubectl scale deployment worker -n workers --replicas=12
```
Watch lag trend for 5 minutes. Revert once lag drops below 5k.

### Reset offset (use with extreme caution)
Only do this if messages are confirmed replayable and the topic has retention > 48h:
```bash
kafka-consumer-groups.sh --bootstrap-server kafka:9092 \
  --group worker-group --reset-offsets \
  --to-datetime 2024-06-01T00:00:00.000 \
  --topic events.ingested --execute
```
Document the reset in the #platform-incidents Slack channel with timestamp and reason.

### Pause non-critical topic consumption
The `worker` supports runtime feature flags to skip low-priority handlers:
```bash
just feature-flag set SKIP_ANALYTICS_HANDLER true --env production
```

## Escalation

- If lag hasn't moved in 20 minutes after scaling: page the on-call DBA (Postgres issue likely).
- If schema mismatch: loop in the team that owns the producer service.

## Post-Incident

- File a lag event entry in `../incidents/kafka-lag-log.md`.
- Review partition key strategy if the same key caused the hot partition.
