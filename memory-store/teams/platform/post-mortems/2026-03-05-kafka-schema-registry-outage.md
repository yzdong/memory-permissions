# 2026-03-05 Kafka Schema Registry Outage

## Summary

The Confluent Schema Registry instance used by all three platform services went down for 1 hour 8 minutes after its backing ZooKeeper ensemble lost quorum. Producers and consumers using Avro serialization failed to fetch/register schemas and began erroring.

## Timeline

| Time (UTC) | Event |
|---|---|
| 14:30 | ZooKeeper node `zk-2` loses disk I/O; goes offline |
| 14:31 | ZooKeeper ensemble drops to 1/3 nodes; loses quorum |
| 14:31 | Schema Registry loses ZooKeeper connection; enters read-only mode |
| 14:32 | Schema-aware producers begin failing: `SchemaRegistryException: not leader` |
| 14:35 | Alerts fire; on-call (Leila) paged |
| 14:55 | `zk-2` disk I/O issue identified (full transaction log) |
| 15:10 | ZooKeeper transaction log pruned; `zk-2` restarted and rejoins |
| 15:22 | Quorum restored; Schema Registry back to read-write |
| 15:38 | All producers confirmed healthy |

## Root Cause

The ZooKeeper transaction log on `zk-2` was not subject to automatic pruning (`autopurge.purgeInterval` was set to `0`, disabled). Over 8 months of operation it accumulated ~47 GB of logs on a 50 GB volume. When the volume filled, ZooKeeper could no longer write and crashed, dropping quorum.

## Impact

- 1 h 8 min of failed Avro schema operations across `api`, `worker`, `gateway`
- Services gracefully degraded: producers that cache schemas locally continued; producers making first-time schema registration failed
- ~2,300 events dropped by producers with no local schema cache
- No data inconsistency; dropped events were non-critical notification payloads

## Action Items

- [ ] **P0** Enable ZooKeeper `autopurge.purgeInterval=24` and `autopurge.snapRetainCount=5` on all nodes — owner: Leila, due 2026-03-07
- [ ] **P0** Add disk utilization alert for ZooKeeper nodes at 70% — owner: Damien, due 2026-03-08
- [ ] **P1** Migrate Schema Registry from ZooKeeper to KRaft mode (Kafka-native metadata) — owner: Tomás, due 2026-04-30
- [ ] **P1** Require all producers to implement local schema caching with TTL — owner: Sasha, due 2026-03-20
- [ ] **P2** Document ZooKeeper log pruning procedure in `runbooks/kafka-zookeeper.md`
