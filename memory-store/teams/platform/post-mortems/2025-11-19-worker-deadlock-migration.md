# 2025-11-19 Worker Deadlock During Schema Migration

## Summary

A zero-downtime schema migration on the `jobs` table caused a 22-minute deadlock window that stopped the `worker` service from dequeuing new jobs. The migration added a non-null column without a default, which PostgreSQL locked the table for while backfilling existing rows.

## Timeline

- **11:00** — Migration `0048_add_priority_column.sql` starts via CI/CD pipeline
- **11:02** — `worker` processes slow; dequeue rate drops from 800/s to 0
- **11:04** — Job queue depth alert fires
- **11:11** — On-call identifies table lock contention via `pg_locks`
- **11:18** — Migration still running (large table, ~42M rows)
- **11:22** — Migration completes; lock released; `worker` recovers automatically
- **11:24** — Dequeue rate back to 850/s

## Root Cause

The migration used `ALTER TABLE jobs ADD COLUMN priority INT NOT NULL DEFAULT 0`. Despite having a DEFAULT, PostgreSQL versions before 11 would rewrite the table; our primary is on PG 14 which handles this in-place. However, the `NOT NULL` + backfill still required an `ACCESS EXCLUSIVE` lock that blocked all concurrent DML for the duration.

The real mistake: no one checked the table row count before scheduling during business hours. 42M rows took ~20 minutes to migrate.

See `db/migrations/0048_add_priority_column.sql` and `docs/migration-safety.md` for context.

## Impact

- 22 minutes of zero job processing
- ~17,600 jobs queued but not dropped; all processed within 40 minutes of recovery
- No user-facing errors on `api` (job results are async)
- Internal SLA for background job latency breached

## Action Items

- [ ] Add row-count check to migration CI step; require approval if table > 5M rows — owner: @dana, due 2025-12-03
- [ ] Schedule large migrations in low-traffic windows (02:00–05:00 UTC) — update `runbooks/schema-migrations.md`
- [ ] Evaluate `pg_repack` or `pglogical` for large table changes — owner: @priya, due 2025-12-15
- [ ] Add job queue depth alert with tighter threshold (500 queued, not 2000) — owner: @ryo, due 2025-11-26
