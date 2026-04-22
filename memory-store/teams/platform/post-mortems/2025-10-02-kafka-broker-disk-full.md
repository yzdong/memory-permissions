# 2025-10-02 Kafka Broker Disk Full

## Summary

One of three Kafka brokers ran out of disk space, causing it to go offline and triggering partition leadership re-elections across the cluster. Producer throughput dropped by ~60% for 1 hour 22 minutes while the cluster rebalanced and disk was freed.

## Timeline

| Time (UTC) | Event |
|---|---|
| 06:44 | Broker `kafka-2` disk utilization hits 100% |
| 06:44 | Broker self-fences; partitions begin re-electing leaders |
| 06:46 | Producer errors spike on `worker` and `api` services |
| 06:52 | On-call (Leila) paged |
| 07:01 | Root cause identified: `audit_events` topic retention not configured |
| 07:15 | Manually deleted oldest log segments; broker recovers |
| 07:23 | Retention policy set: 7-day size-based limit on `audit_events` |
| 08:06 | Cluster fully rebalanced; throughput normal |

## Root Cause

The `audit_events` topic was created three weeks prior with default retention settings (`retention.ms = -1`, unlimited). A new compliance feature began publishing ~2.3 GB/day to this topic. Over 22 days the broker hosting the majority of `audit_events` partitions accumulated ~49 GB of uncompacted log data, filling its 50 GB data volume.

Topic creation did not go through the standard infra review checklist, which would have caught the missing retention config.

## Impact

- 1 h 22 min of degraded Kafka throughput (~60% producer success rate)
- ~14,000 messages queued at producers with retries; all eventually delivered
- No message loss (producers have retry + idempotency enabled)
- Compliance audit trail complete; no data missing from `audit_events`

## Action Items

- [ ] **P0** Require retention policy in all topic creation PRs; add to `runbooks/kafka-topic-provisioning.md` — owner: Leila, due 2025-10-09
- [ ] **P0** Add disk utilization alert at 75% (currently only at 90%) — owner: Tomás, due 2025-10-07
- [ ] **P1** Expand broker data volumes from 50 GB to 150 GB — owner: Damien, due 2025-10-14
- [ ] **P1** Evaluate Kafka Tiered Storage to offload cold segments to S3
- [ ] **P2** Run quarterly capacity review for all Kafka topics — see `../planning/kafka-capacity.md`
