# Postgres Connection Pool Runbook

Covers diagnosing and resolving connection pool exhaustion on our Postgres cluster. This is one of the most common causes of cascading failures across api, worker, and gateway.

## Background

We use PgBouncer in transaction-mode pooling in front of RDS. Each service connects to PgBouncer, not directly to Postgres. PgBouncer holds a fixed pool of backend connections.

- PgBouncer pool size: 100 connections to Postgres
- Per-service max clients: api=60, worker=30, gateway=20
- Postgres `max_connections`: 200 (100 reserved for PgBouncer + 100 direct slots for admin/migrations)

## Detecting exhaustion

```bash
# Check current PgBouncer state
psql -h pgbouncer -p 6432 -U pgbouncer pgbouncer -c 'SHOW POOLS;'
```

Look for `cl_waiting > 0` — clients waiting for a connection. Any nonzero value under load is a warning sign. Sustained waiting causes request timeouts.

## Quick relief: identify connection hogs

```sql
SELECT client_addr, count(*), max(now() - state_change) AS oldest
FROM pg_stat_activity
WHERE state != 'idle'
GROUP BY client_addr
ORDER BY count DESC;
```

If a single source is holding many long-running connections, that's your culprit.

## Terminating idle connections

```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle in transaction'
  AND state_change < now() - interval '5 minutes';
```

`idle in transaction` connections hold locks and waste pool slots. Terminate them first.

## Increasing pool size (temporary)

```bash
# Edit PgBouncer config live
psql -h pgbouncer -p 6432 -U pgbouncer pgbouncer -c 'SET pool_size=120;'
# Then reload
psql -h pgbouncer -p 6432 -U pgbouncer pgbouncer -c 'RELOAD;'
```

Don't go above 150 without increasing Postgres `max_connections` first.

## Root cause patterns

- **N+1 queries**: App code acquiring connections per-item in a loop
- **Missing connection release**: Bug causing connections not to be returned to pool
- **Long transactions**: Migrations or batch jobs holding connections too long
- **Sudden traffic spike**: More concurrent users than pool can serve

Check `../evaluations/connection-pool-analysis.md` for historical incidents.
