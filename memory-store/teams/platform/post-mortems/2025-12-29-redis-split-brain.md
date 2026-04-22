# 2025-12-29 Redis Sentinel Split-Brain

## Summary

A network partition between availability zones caused Redis Sentinel to promote a replica to primary while the original primary was still serving writes. The resulting split-brain lasted ~18 minutes and caused a burst of write conflicts and session invalidations.

## Timeline

| Time (UTC) | Event |
|---|---|
| 22:11 | AZ-b to AZ-a network latency spikes to ~4 s |
| 22:12 | Sentinel quorum in AZ-b promotes `redis-replica-2` to primary |
| 22:12 | `api` pods in AZ-a continue writing to old primary |
| 22:12 | `api` pods in AZ-b start writing to new primary |
| 22:13 | Conflicting writes begin; some session tokens overwritten |
| 22:18 | Network partition resolves; old primary detects new primary |
| 22:18 | Old primary demotes itself; ~11,000 writes from old primary discarded |
| 22:29 | All Sentinel nodes agree on topology; stable |

## Root Cause

Sentinel was configured with `min-slaves-to-write 0`, meaning the old primary continued accepting writes even after losing replication connectivity. Combined with a quorum of 2 out of 3 sentinels being reachable within AZ-b, the split-brain condition was met and sustained until the partition healed.

## Impact

- ~11,000 write operations on the old primary were lost on merge
- ~4,200 user sessions silently invalidated (users had to log in again)
- No payment or order data affected (Redis is not source of truth for those)
- Approximately 18 minutes of potential stale-read exposure

## Action Items

- [ ] **P0** Set `min-slaves-to-write 1` on Redis primary to prevent isolated-primary writes — owner: Priya, due 2026-01-05
- [ ] **P0** Configure Sentinel with 5 nodes across 3 AZs to improve quorum resilience — owner: Damien, due 2026-01-12
- [ ] **P1** Add split-brain detection metric (compare write counters across nodes) — owner: Tomás, due 2026-01-15
- [ ] **P2** Evaluate migration to Redis Cluster for better partition tolerance
- [ ] **P2** Update `runbooks/redis-ops.md` with split-brain diagnosis steps
