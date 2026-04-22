# Worker Job Failure Modes and Recovery

This covers specific failure patterns we've seen in the worker service and how to recover from them. General worker deploy notes are in `worker-deploy.md`.

## Failure mode 1: Job stuck in `processing` state

Cause: Worker pod was killed mid-job (OOMKilled, node eviction, deploy without graceful drain).

The job remains locked in `processing` in the database and never retries because the lock holder is gone.

Detect:
```sql
SELECT id, job_type, locked_at, locked_by, attempts
FROM jobs
WHERE status = 'processing'
  AND locked_at < now() - interval '30 minutes'
ORDER BY locked_at;
```

Recover (unlock and re-enqueue):
```sql
UPDATE jobs
SET status = 'queued', locked_at = NULL, locked_by = NULL
WHERE status = 'processing'
  AND locked_at < now() - interval '30 minutes';
```

Review why pods were killed before re-enqueuing if it was OOM — the job may just OOM again.

## Failure mode 2: Retry storm

A bad batch of messages causes rapid retries, flooding the retry topic and consuming all worker capacity.

Detect: Grafana → Worker → Retry Queue Depth spike + job throughput drop on primary queue.

Mitigation:
1. Identify the bad job type:
   ```sql
   SELECT job_type, count(*), max(attempts) FROM jobs
   WHERE status = 'failed' AND updated_at > now() - interval '1 hour'
   GROUP BY job_type ORDER BY count DESC;
   ```
2. Temporarily pause that job type's Kafka consumer:
   ```bash
   kafka-consumer-groups.sh --bootstrap-server kafka-0:9092 \
     --group worker-retry --topic platform.<job-type>.retry --reset-offsets \
     --to-latest --execute
   ```
3. Fix the root cause, then replay from the dead-letter topic.

## Failure mode 3: Memory leak on long-running jobs

Some jobs accumulate memory over multiple iterations. Worker pods grow until OOMKilled.

We have a workaround: `WORKER_MAX_JOBS_PER_PROCESS=500` env var causes the worker to gracefully restart after 500 jobs. Set this via:
```bash
kubectl set env deployment/worker WORKER_MAX_JOBS_PER_PROCESS=500 -n worker
```

This is a stopgap. File a ticket with the worker team to profile and fix the leak.

## Failure mode 4: Database connection exhaustion

Workers are the biggest consumer of DB connections. If Postgres connections are exhausted and workers can't connect, jobs queue up.

See `postgres-connections.md` for diagnosis and recovery.

## Related

- `kafka-lag-runbook.md` — if job failures are causing consumer lag
- `worker-deploy.md` — if failure appeared after a deploy
