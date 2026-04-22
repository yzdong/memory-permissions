# Worker: Stuck and Zombie Job Investigation

## What "Stuck" Means Here

A job is considered stuck when:
- It has been in `processing` state for > 10 minutes (normal max is ~2 minutes).
- The worker holding the job has since restarted, leaving the job unclaimed.
- A job has been retried > 5 times without success.

## Finding Stuck Jobs

```sql
SELECT id, job_type, status, started_at, attempts, last_error
FROM job_queue
WHERE status = 'processing'
  AND started_at < now() - interval '10 minutes'
ORDER BY started_at ASC;
```

Also check the dead-letter queue:
```sql
SELECT id, job_type, failed_at, last_error
FROM job_queue_dlq
ORDER BY failed_at DESC
LIMIT 20;
```

## Releasing a Stuck Job for Retry

```sql
UPDATE job_queue
SET status = 'pending', started_at = NULL, worker_id = NULL
WHERE id = '<job-id>';
```

Only do this after confirming the worker that claimed the job is no longer running (check pod status).

## Bulk Release (with caution)

```sql
UPDATE job_queue
SET status = 'pending', started_at = NULL, worker_id = NULL
WHERE status = 'processing'
  AND started_at < now() - interval '15 minutes'
  AND attempts < 5;
```

Do not bulk-release jobs that have already hit 5 attempts — those go to DLQ investigation.

## Investigating Repeated Failures

1. Pull the `last_error` from the DB.
2. Find the worker log entry for that job ID:
   ```bash
   just logs worker --grep '<job-id>' --env production --hours 2
   ```
3. Common failure patterns:
   - **Serialization error**: job payload doesn't match current schema — may need a data fix.
   - **Downstream timeout**: external API or internal service down — check dependency status.
   - **Duplicate key**: job produces a DB record that already exists — investigate idempotency.

## Replaying DLQ Jobs

```bash
just worker-replay-dlq --job-type <type> --limit 50 --env production
```
This moves jobs from DLQ back to `pending`. Use `--dry-run` first to see what would be replayed.

## Escalation

If stuck jobs are caused by a code bug in a recently deployed worker version, roll back first (see `rollback-worker.md`), then release the stuck jobs.
