# Postgres Slow Query Investigation

## Symptoms That Bring You Here

- `pg_stat_statements` showing queries > 500ms average.
- Worker handlers timing out on DB writes.
- Grafana `DB Query Duration` panel spiking.
- PagerDuty alert `postgres.slow_query_threshold_exceeded`.

## Finding the Culprits

```sql
SELECT query,
       calls,
       round(mean_exec_time::numeric, 2) AS mean_ms,
       round(total_exec_time::numeric, 2) AS total_ms,
       rows
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC
LIMIT 15;
```

Note the query text (may be truncated). Get the full query from application logs if needed:
```bash
just logs api --grep 'slow_query' --env production --tail 100
```

## Analyzing with EXPLAIN

Always use `EXPLAIN (ANALYZE, BUFFERS)` on a **replica** unless the query is write-only:
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM events WHERE user_id = 12345 AND created_at > now() - interval '7 days';
```

Look for:
- **Seq Scan on large tables**: missing index.
- **Hash Join with high rows**: row estimate way off, stale statistics.
- **Nested Loop with many iterations**: N+1 query pattern from application.

## Quick Fixes

### Add a missing index (concurrent — no lock)
```sql
CREATE INDEX CONCURRENTLY idx_events_user_created
  ON events (user_id, created_at);
```
Monitor index build progress:
```sql
SELECT phase, blocks_done, blocks_total
FROM pg_stat_progress_create_index;
```

### Update stale statistics
```sql
ANALYZE events;
```

### Kill a runaway query
```sql
SELECT pg_cancel_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > interval '5 minutes'
  AND query NOT LIKE '%autovacuum%';
```
Use `pg_terminate_backend` only if cancel doesn't work within 30 seconds.

## Longer-Term Fixes

- If a specific query pattern is consistently slow, file a ticket with the owning service team to optimize the ORM query.
- For complex reporting queries, consider routing to the read replica (`POSTGRES_READ_REPLICA_URL`).
- Document index additions in `../infrastructure/postgres-indexes.md`.

## Escalation

If slow queries are causing connection pool exhaustion (pgbouncer queue depth > 50), this becomes a P1. See `postgres-connection-pool.md`.
