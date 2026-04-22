# API Database Migration Runbook

This covers how to safely run, monitor, and roll back Postgres migrations for the `api` service. This is specifically for production migration runs — staging migrations are handled automatically in CI.

## Before you run a migration in prod

- [ ] Migration has run successfully on staging at least 24 hours ago
- [ ] Migration is backwards-compatible (old code can run against new schema, and vice versa)
- [ ] If the table is large (>10M rows), estimate migration time using staging row count ratio
- [ ] Alert has been filed in `#engineering` with migration name and expected duration
- [ ] DBA or platform lead has reviewed if the migration adds an index or alters column type

## Running the migration

```bash
# Run as the api service user
kubectl exec -it deployment/api -n api -- \
  ./manage.py migrate --plan  # dry run first

kubectl exec -it deployment/api -n api -- \
  ./manage.py migrate
```

Monitor a long migration:

```sql
-- Watch progress on index creation (Postgres 12+)
SELECT phase, blocks_done, blocks_total,
       round(blocks_done::numeric / nullif(blocks_total, 0) * 100, 1) AS pct
FROM pg_stat_progress_create_index;
```

## Lock monitoring during migration

Migrations that add columns (nullable) or indexes (`CONCURRENTLY`) are low-risk. Column type changes or adding constraints can take locks.

```sql
-- See what is blocking what
SELECT
  blocked.pid AS blocked_pid,
  blocked.query AS blocked_query,
  blocking.pid AS blocking_pid,
  blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
  ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE blocked.pid != blocking.pid;
```

If the migration is blocked for >2 minutes, it's safe to kill the blocking query if it's a read — coordinate in `#platform-oncall` first.

## Rolling back a migration

Most migrations have a reverse operation:

```bash
kubectl exec -it deployment/api -n api -- \
  ./manage.py migrate <app_name> <previous_migration_number>
```

If the migration added a column with data and you need to reverse it, the data in that column will be lost. Dump it first:

```bash
kubectl exec -it deployment/api -n api -- \
  ./manage.py dumpdata --natural-foreign --natural-primary \
  app_name.ModelName > /tmp/pre-rollback-dump.json
```

## Related

- `postgres-slow-queries.md` — if migration causes query slowdown post-apply
- `postgres-connections.md` — migrations hold connections open
- `postgres-vacuum.md` — a large migration may warrant a VACUUM ANALYZE afterward
