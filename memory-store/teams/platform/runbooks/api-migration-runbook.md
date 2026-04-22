# API Database Migration Runbook

This covers the execution and monitoring of database migrations for the `api` service. Schema migrations are the highest-risk part of most api deploys.

## Migration Philosophy

All migrations must be backward-compatible (expand-contract pattern). A deploy may not include a migration that breaks the currently running version of the api. If you're unsure whether a migration is safe, consult `../procedures/migration-safety-checklist.md`.

## Before Running a Migration

```bash
# Preview what will run
just db-migrate api --env production --dry-run

# Check estimated table size (large tables need CONCURRENTLY or batching)
just db-table-size api --env production --table <table-name>
```

If the target table is > 10GB, the migration needs special handling. Do not run a standard `ALTER TABLE` — it will lock the table. Use `pg_repack` or a shadow-table approach instead.

## Running the Migration

```bash
just db-migrate api --env production
```

This connects to the Postgres primary via pgbouncer in session mode (bypasses transaction pooling for the duration of the migration).

## Monitoring Progress

For long-running DDL operations, watch progress in Postgres:
```sql
SELECT phase, blocks_done, blocks_total,
       tuples_done, tuples_total
FROM pg_stat_progress_cluster; -- for CLUSTER/VACUUM FULL

SELECT phase, blocks_done, blocks_total
FROM pg_stat_progress_create_index; -- for index builds
```

Also watch for lock contention:
```sql
SELECT wait_event_type, wait_event, count(*)
FROM pg_stat_activity
WHERE wait_event IS NOT NULL
GROUP BY 1, 2
ORDER BY 3 DESC;
```

## Rolling Back a Migration

Most migrations are not automatically reversible. Before running any migration, confirm the down-migration is written and tested:
```bash
just db-migrate api --env production --rollback --steps 1
```

If no rollback migration exists, you may need to write one manually. Coordinate with the service owner.

## Post-Migration

- Run `ANALYZE <table>` on the migrated table to update planner statistics.
- Check `pg_stat_user_tables` for the table to confirm `last_analyze` updated.
- Monitor query latency on endpoints that touch the migrated table for 15 minutes post-migration.
- Log the migration in `../infrastructure/postgres-migration-log.md`.

## Failed Migration Recovery

If a migration fails partway through:
1. Check `schema_migrations` table for partial state.
2. Manually resolve any partial DDL (Postgres DDL is transactional, so partial failure usually means the transaction was rolled back cleanly).
3. Fix the migration file and re-run after reviewing with the team.
