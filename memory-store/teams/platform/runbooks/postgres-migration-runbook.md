# Postgres Migration Runbook

Covers running, monitoring, and recovering from database migrations in production. Our migration tool is Flyway, invoked as part of the deploy pipeline, but sometimes you need to intervene manually.

## When you'd use this

- A migration is running too long and blocking other queries
- A migration failed partway through and left a partial state
- You need to run a migration outside the normal pipeline (e.g., emergency schema fix)

## Checking migration status

```sql
SELECT version, description, installed_on, success
FROM flyway_schema_history
ORDER BY installed_rank DESC
LIMIT 10;
```

A `success = false` row means a migration failed and Flyway will refuse to run further migrations until it's resolved.

## Handling a failed migration

1. Identify what the migration did before it failed (check the SQL in `db/migrations/`)
2. Manually roll back any partial changes
3. Mark the failed migration as repaired:

```bash
just db-repair
```

This calls `flyway repair` which removes failed entries from the history table.

4. Fix the migration SQL and redeploy

## Long-running migrations

If a migration is blocking:

```sql
-- Find blocking queries
SELECT pid, now() - query_start AS duration, query, state
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;
```

For index creation on large tables, use `CREATE INDEX CONCURRENTLY` in the migration SQL — this is non-blocking but Flyway cannot run it in a transaction. Add `-- flyway:nontransactional` comment at the top of the migration file.

## Emergency schema change (bypassing pipeline)

Only for true emergencies. Connect to the primary directly:

```bash
just db-console prod
```

Make your change, then manually insert a row in `flyway_schema_history` so the pipeline doesn't try to run it again. Document what you did in `../post-mortems/` immediately.

## Lock timeouts

All migrations should set a lock timeout to avoid indefinite waits:

```sql
SET lock_timeout = '10s';
ALTER TABLE events ADD COLUMN processed_at timestamptz;
```

If the lock timeout fires, the migration fails cleanly. Better than hanging.
