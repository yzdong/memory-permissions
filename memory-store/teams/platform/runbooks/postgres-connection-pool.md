# Postgres Connection Pool (pgbouncer) Runbook

## Overview

We run pgbouncer in transaction-mode pooling between all application services and the Postgres primary. Default pool size per service: api=40, worker=15, gateway=10.

## Detecting Pool Exhaustion

```bash
# Connect to pgbouncer admin
psql -h pgbouncer.internal -p 6432 -U pgbouncer pgbouncer

SHOW POOLS;
```

Key columns: `cl_waiting` (clients waiting for a connection). If this is consistently > 5, the pool is saturated.

Also check:
```
SHOW STATS;
```
`avg_wait_time` above 50ms is a warning sign.

## Immediate Relief

### Temporarily increase pool size
Edit `pgbouncer.ini` and reload (no restart needed):
```ini
[databases]
platform_api = host=postgres.internal pool_size=60
```
```bash
kill -HUP $(pgrep pgbouncer)
```
Do not exceed 80 total connections without checking Postgres `max_connections` setting first:
```sql
SHOW max_connections;
SELECT count(*) FROM pg_stat_activity;
```

### Kill idle connections hogging the pool
```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
  AND query_start < now() - interval '10 minutes'
  AND usename != 'postgres';
```

## Root Cause Investigation

Pool exhaustion is usually a symptom, not the cause:

1. **Long-running transactions**: check `pg_stat_activity` for transactions open > 30 seconds.
2. **Slow queries blocking others**: see `postgres-slow-queries.md`.
3. **Application connection leak**: look for a spike in `cl_active` without a corresponding spike in traffic. Likely a recent deploy introduced a connection leak.
4. **Lock contention**: 
   ```sql
   SELECT * FROM pg_locks l JOIN pg_stat_activity a ON l.pid = a.pid
   WHERE NOT granted;
   ```

## Connection Leak from a Deploy

If a recent deploy is suspected:
1. Identify the service (check which pool is saturated in `SHOW POOLS`).
2. Rolling restart of that service will recycle its connections:
   ```bash
   kubectl rollout restart deployment/<service> -n <namespace>
   ```
3. If the leak is confirmed, roll back via `rollback-api.md` or `rollback-gateway.md`.

## Metrics

Grafana: `Platform / Database / pgbouncer` — watch `cl_waiting` and `avg_wait_time` panels.
