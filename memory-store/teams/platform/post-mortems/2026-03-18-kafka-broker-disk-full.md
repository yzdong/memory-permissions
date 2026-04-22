# 2026-03-18 Kafka Broker Disk Full

## Summary

Broker 2 in the production Kafka cluster ran out of disk at 16:33 UTC after a topic retention misconfiguration caused log segments to accumulate without compaction. Producers began receiving `RecordTooLargeException` (actually a disk-full error surfacing oddly) and the `worker` service fell behind on three topics.

## Timeline

- **14:00** — Kafka topic `audit-log` retention policy accidentally set to `compact` instead of `delete` during a routine topic config update
- **14:00–16:33** — Compaction log accumulates; no segments deleted
- **16:33** — Broker 2 disk hits 100%; producer errors begin
- **16:38** — Lag alert fires on `order-events`, `user-events`, `audit-log`
- **16:41** — On-call identifies broker 2 disk full via Kafka JMX metrics
- **16:49** — Retention policy corrected on `audit-log`; old segments eligible for deletion
- **17:02** — Log cleaner removes eligible segments; disk drops to 71%
- **17:11** — Producer errors stop; all consumers catch up within 22 minutes

## Root Cause

The `audit-log` topic received a config update via `kafka-configs.sh` with `--add-config cleanup.policy=compact`. The operator intended to update a different topic (`audit-log-archive`). No review step exists for topic config changes.

Compact-only topics never have segments deleted, only deduplicated by key. The `audit-log` topic has very high cardinality keys so compaction was effectively useless at reducing size.

## Impact

- 30 minutes of producer errors and consumer lag
- `audit-log` data fully preserved (compaction doesn't lose data)
- No user-facing errors on `api` or `gateway`
- `worker` audit emission had partial failures; 3,400 audit events reprocessed from dead-letter queue

## Action Items

- [ ] Require peer review + infra approval for all `kafka-configs.sh` topic mutations in production — owner: @farah, due 2026-03-25
- [ ] Add Kafka disk utilization alert at 75% per broker — owner: @ryo, due 2026-03-25
- [ ] Document topic naming convention to disambiguate `audit-log` vs `audit-log-archive` — owner: @farah
- [ ] Add topic config drift detection to weekly infra health check — owner: @marco, due 2026-04-01
