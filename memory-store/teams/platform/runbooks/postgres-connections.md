# Postgres Connection Exhaustion

We run PgBouncer in front of Postgres. This doc covers both PgBouncer saturation and actual Postgres connection limit issues.

## Architecture reminder

```
api / worker / gateway
       │
    PgBouncer (transaction pooling, :5432)
       │
    Postgres primary (:5433)
```

Max Postgres connections: `max_connections = 200` (set in `../docs/postgres-config.md`)
PgBouncer pool size: 20 per database (see `/etc/pgbouncer/pgbouncer.ini`)

## Symptoms

- Services log: `FATAL: remaining connection slots are reserved for non-replication superuser connections`
- PgBouncer logs: `no more connections allowed (max_client_conn)`
- API latency spike with P99 > 2s but Postgres CPU is low

## Check current connection count

```sql
-- Total connections by state and user
SELECT usename, state, count(*)
FROM pg_stat_activity
GROUP BY usename, state
ORDER BY count DESC;
```

```bash
# PgBouncer stats
psql -h pgbouncer.internal -p 5432 -U pgbouncer pgbouncer -c 'SHOW POOLS;'
psql -h pgbouncer.internal -p 5432 -U pgbouncer pgbouncer -c 'SHOW CLIENTS;'
```

## Immediate relief

If connections are exhausted:

1. Kill idle connections first (safe):
   ```sql
   SELECT pg_terminate_backend(pid)
   FROM pg_stat_activity
   WHERE state = 'idle'
     AND now() - state_change > interval '10 minutes'
     AND usename != 'replication';
   ```

2. If still exhausted, look for connection leaks:
   ```sql
   SELECT usename, application_name, client_addr, count(*)
   FROM pg_stat_activity
   GROUP BY 1, 2, 3
   ORDER BY count DESC
   LIMIT 10;
   ```
   One application with 50+ connections is almost certainly a connection pool misconfiguration.

3. Restart PgBouncer to clear stuck connections (brief interruption ~2s):
   ```bash
   sudo systemctl restart pgbouncer
   ```

## Longer term

- Connection pool size per service is configured in each service's `DATABASE_POOL_SIZE` env var
- If legitimate traffic is outgrowing the pool, raise a PR against `infra/postgres/pgbouncer.ini`
- Do NOT increase `max_connections` without checking shared_buffers and memory impact first

## Related

- `postgres-slow-queries.md` — sometimes slow queries hold connections open
- `postgres-vacuum.md` — autovacuum workers also consume connections
