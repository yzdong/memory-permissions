# 2026-02-07 Postgres Replica Lag Causing Stale Reads

## Summary

The read replica used by the `api` service for reporting queries fell ~14 minutes behind the primary, causing the `/v1/reports/*` endpoints to return stale data. The lag was caused by a long-running analytics query that blocked the replica's apply process.

## Timeline

| Time (UTC) | Event |
|---|---|
| 10:15 | Analytics team runs an ad-hoc cross-table aggregation query on the read replica |
| 10:16 | Replication apply process begins waiting behind query lock |
| 10:16–10:42 | Replica falls progressively behind; reaches 14 min lag at peak |
| 10:42 | Replica replication lag alert fires (threshold: 5 min) |
| 10:45 | On-call (Tomás) identifies blocking query via `pg_stat_activity` |
| 10:46 | Analytics query terminated (`pg_terminate_backend`) |
| 10:52 | Replica fully caught up |

## Root Cause

The analytics team has direct read access to the replica for ad-hoc queries. A `SELECT` with multiple `LEFT JOIN`s across large tables held a `AccessShareLock` that prevented the WAL apply process from proceeding on affected table pages. Replica lag grew linearly while the query ran.

There is no query timeout configured on the replica for this user role.

## Impact

- ~36 minutes of stale data on `/v1/reports/*` endpoints (up to 14 min stale at peak)
- No writes affected; primary was healthy throughout
- Two customers filed support tickets about incorrect report figures
- Minimal: affected endpoints are advisory only, not transactional

## Action Items

- [ ] **P0** Set `statement_timeout = '120s'` for the analytics read-only role on the replica — owner: Tomás, due 2026-02-11
- [ ] **P1** Provision a dedicated analytics replica isolated from the `api` service read replica — owner: Priya, due 2026-02-28
- [ ] **P1** Reduce replica lag alert threshold from 5 min to 90 s — owner: Damien, due 2026-02-12
- [ ] **P2** Require analytics team queries > 60 s to use the dedicated replica once provisioned
- [ ] **P2** Add replica lag panel to main Postgres Grafana dashboard

## Notes

Capacity context in `../planning/2026-q1-db-scaling.md`.
