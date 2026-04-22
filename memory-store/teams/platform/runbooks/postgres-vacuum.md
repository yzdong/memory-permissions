# Postgres Manual Vacuum & Bloat Runbook

Autovacuum handles most cases. This runbook is for situations where autovacuum is falling behind, causing table bloat, or where we've hit transaction ID (XID) wraparound risk.

## Identifying Bloat

```sql
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
       n_dead_tup,
       last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;
```
Tables with `n_dead_tup` > 5 million and no recent `last_autovacuum` are candidates for manual intervention.

## XID Wraparound Risk

```sql
SELECT datname,
       age(datfrozenxid) AS xid_age,
       2147483647 - age(datfrozenxid) AS xids_remaining
FROM pg_database
ORDER BY xid_age DESC;
```
If `xids_remaining` drops below 50 million, treat as P1. Page the on-call DBA immediately.

## Running Manual VACUUM

### Non-blocking vacuum (safe in production)
```sql
VACUUM VERBOSE ANALYZE events;
```
This does not lock the table. Monitor progress:
```sql
SELECT phase, heap_blks_scanned, heap_blks_vacuumed
FROM pg_stat_progress_vacuum;
```

### VACUUM FULL (requires downtime window)
`VACUUM FULL` takes an exclusive lock. Coordinate with the api team before running on any high-traffic table. See `../procedures/downtime-window-request.md`.

## Tuning Autovacuum for Problematic Tables

```sql
ALTER TABLE events SET (
  autovacuum_vacuum_scale_factor = 0.01,
  autovacuum_analyze_scale_factor = 0.005,
  autovacuum_vacuum_cost_delay = 10
);
```
Document any per-table autovacuum overrides in `../infrastructure/postgres-table-settings.md`.

## Reindex After Vacuum

Index bloat can persist after a VACUUM. For the worst offenders:
```sql
REINDEX TABLE CONCURRENTLY events;
```
Run during off-peak hours. This operation can take 30–90 minutes on large tables.

## Contacts

- **Primary DBA**: listed in `../on-call/rotation.md`
- **Escalation**: #platform-infra Slack channel
