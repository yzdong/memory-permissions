# 2026-06-01 Multi-Region Split-Brain During Network Partition

## Summary

A 14-minute network partition between `us-east-1` and `eu-west-1` caused both regions to independently elect Patroni primaries. When the partition healed, conflicting writes from both regions needed manual reconciliation. This is the most complex incident the Platform team has handled to date.

## Timeline

| Time (UTC) | Event |
|---|---|
| 02:11 | Network partition begins between regions (cause: upstream provider maintenance with no notice) |
| 02:13 | `eu-west-1` replica loses connection to `us-east-1` primary; Patroni timeout begins |
| 02:14 | `us-east-1` Patroni still healthy; continues accepting writes |
| 02:21 | `eu-west-1` Patroni promotes local replica to primary (TTL elapsed) |
| 02:21–02:25 | Both regions accept writes independently |
| 02:25 | Network partition heals |
| 02:25 | Patroni detects two primaries; both pause write acceptance |
| 02:27 | On-call paged; services begin returning errors |
| 02:44 | Manual reconciliation started by DBA |
| 04:18 | Reconciliation complete; single primary restored in `us-east-1` |
| 04:23 | Services resume normal operation |

## Root Cause

Patroni's default split-brain protection (`synchronous_standby_names`) was not enabled for the cross-region replica. The replica was running in async mode to reduce cross-region write latency. Without synchronous replication, Patroni has no mechanism to prevent a secondary region from promoting during a partition.

This tradeoff was documented in `infra/patroni/architecture-decisions.md` ADR-007 but the risk of concurrent promotions was underestimated.

## Impact

- ~113 minutes of total incident duration
- 4 minutes of split-brain (conflicting writes)
- 1 hour 56 minutes for reconciliation
- 847 rows with conflicting primary keys identified; 801 auto-reconciled, 46 required manual review
- Services were read-only or unavailable for ~1h 56m during reconciliation
- All three services (`api`, `worker`, `gateway`) affected

## Action Items

- [ ] Enable synchronous replication to cross-region replica for critical tables (accept latency tradeoff) — owner: @priya, due 2026-06-15; requires Infra + Product sign-off
- [ ] Implement application-level fencing token to reject writes when Patroni is in uncertain state — owner: @dana, due 2026-07-01
- [ ] Set up automated conflict detection job that runs every 5 minutes when multi-region replication is active — owner: @priya, due 2026-06-22
- [ ] Conduct chaos engineering exercise for network partition scenarios quarterly — owner: @marco, starting Q3 2026
- [ ] Revisit ADR-007 with updated risk assessment; publish updated version to `infra/patroni/architecture-decisions.md`
- [ ] Full blameless post-mortem presentation to engineering org scheduled for 2026-06-08
- [ ] Coordinate with cloud provider on advance notice for maintenance windows — owner: @lena
