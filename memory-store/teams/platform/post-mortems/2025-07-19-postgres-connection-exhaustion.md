# 2025-07-19 Postgres Connection Exhaustion

## Summary

All three platform services (`api`, `worker`, `gateway`) lost database connectivity for ~38 minutes after a connection pool misconfiguration was promoted to production during a routine deploy. The `max_connections` ceiling on our shared RDS instance was hit and new connections were refused.

## Timeline

| Time (UTC) | Event |
|---|---|
| 14:02 | Deploy of `api` v2.19.0 promoted to production |
| 14:06 | PagerDuty fires: DB connection errors on `api` |
| 14:09 | `worker` health checks start failing |
| 14:13 | On-call (Damien) identifies connection count at 498/500 in RDS console |
| 14:21 | Temporary mitigation: restart `worker` pods to drop idle connections |
| 14:40 | Permanent fix deployed: pool size reverted to `max: 10` per pod |
| 14:44 | All services reporting healthy |

## Root Cause

A config change in `api` v2.19.0 set `DATABASE_POOL_MAX` to `50` per pod (up from `10`) based on a misread of a load-testing recommendation intended for a *staging* environment with fewer pods. In production we run 20 `api` replicas, meaning peak possible connections jumped from 200 to 1,000 — well above the RDS `max_connections` of 500.

The change bypassed the normal config review step because it was bundled inside a larger PR.

## Impact

- 38-minute full database outage across all three services
- Approximately 8,500 requests failed with 503 during the window
- No data corruption; all in-flight transactions rolled back cleanly

## Action Items

- [ ] **P0** Add a pre-deploy check in the pipeline that validates `DATABASE_POOL_MAX * replica_count < rds_max_connections * 0.75` — owner: Damien, due 2025-07-25
- [ ] **P0** Separate config-only changes into their own diff category requiring infra review — owner: Sasha, due 2025-07-28
- [ ] **P1** Migrate to PgBouncer to decouple app-level pool sizes from RDS limits — owner: Priya, due 2025-08-30
- [ ] **P2** Update `runbooks/postgres-ops.md` with connection ceiling formulae

## Notes

Related capacity planning work tracked in `../planning/2025-q3-db-scaling.md`.
