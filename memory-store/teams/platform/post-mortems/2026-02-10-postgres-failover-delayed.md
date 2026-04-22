# 2026-02-10 Postgres Primary Failover Delayed

## Summary

The Postgres primary suffered a kernel OOM at 07:43 UTC. Automatic failover to the replica was expected within 30 seconds but took 9 minutes due to a misconfigured `patroni` health check interval. Services were degraded for the full duration.

## Timeline

- **07:43** — Postgres primary process killed by kernel OOM killer
- **07:43** — Patroni detects primary unresponsive
- **07:43–07:52** — Patroni waits through 18 × 30s health check cycles before declaring primary dead (expected: 3 × 10s)
- **07:52** — Replica promoted to primary
- **07:54** — `api` and `worker` reconnect; error rates drop
- **07:58** — Full recovery; all services healthy

## Root Cause

A Patroni config change in November 2025 set `loop_wait: 30` and `ttl: 540` to reduce false-positive failovers during a noisy deployment window. The change was never reverted. The production values should be `loop_wait: 10` and `ttl: 30`.

Config file: `infra/patroni/patroni.yaml`.

The root cause of the kernel OOM on the primary was a runaway `VACUUM ANALYZE` on a table with bloat that hasn't been addressed since Q3 2025. That's a separate but related issue.

## Impact

- 9 minutes of database unavailability
- All writes to `api` and `worker` failed during window
- ~7,400 requests returned 500
- Replica promotion successful; no data loss (synchronous replication was active)

## Action Items

- [ ] Restore Patroni `loop_wait: 10`, `ttl: 30` immediately — DONE (same day)
- [ ] Add config drift detection for Patroni settings — owner: @priya, due 2026-02-17
- [ ] Address table bloat on `public.events` — owner: @priya, due 2026-02-24
- [ ] Require TTL/revert plan for any Patroni tuning changes — update `runbooks/patroni-operations.md`
- [ ] Add failover time SLO alert: if failover takes > 60s, page immediately — owner: @ryo, due 2026-02-24
