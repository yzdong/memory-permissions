# 2025-08-11 Worker OOM Kill Loop

## Summary

The `worker` service entered a crash loop for ~1 hour 50 minutes after a memory-hungry migration job was triggered without resource limits. Kubernetes kept OOM-killing pods as they restarted, preventing normal job processing during the window.

## Timeline

| Time (UTC) | Event |
|---|---|
| 02:17 | Automated nightly data compaction job triggered by cron |
| 02:19 | First OOM kill observed in pod logs |
| 02:20 | Kubernetes restarts pod; job retried immediately |
| 02:20–04:05 | Crash loop continues; 47 pod restarts logged |
| 04:05 | On-call (Leila) woken by sustained alert; identifies loop |
| 04:12 | Job disabled via feature flag; pods stabilize |
| 04:07 | Normal `worker` queue processing resumes |

## Root Cause

The compaction job loads a full partition of the `events` table into memory for deduplication. With 14 months of accumulated data the in-memory set grew to ~9.2 GB, exceeding the pod memory limit of 4 GB. The job has no pagination or streaming path — it was written when the dataset was small.

No resource request/limit override was set for this specific job class.

## Impact

- ~1 h 50 min backlog in email and webhook delivery queues
- Maximum queue depth reached 230,000 jobs; cleared within 40 min of recovery
- No jobs were dropped (Kafka provides durability); all eventually processed
- Customer-facing: delayed transactional emails by up to 2 hours for some users

## Action Items

- [ ] **P0** Rewrite compaction job to operate in cursor-based batches of 50 k rows — owner: Leila, due 2025-08-22
- [ ] **P0** Add explicit memory limits per job class in `worker` Helm values — owner: Tomás, due 2025-08-18
- [ ] **P1** Create Grafana alert for sustained pod restart count > 5 within 10 min — owner: Damien, due 2025-08-25
- [ ] **P2** Document job resource profiling process in `runbooks/worker-jobs.md`

## Lessons Learned

Cron jobs need the same resource review as web services. We'll add a job-resource checklist to the PR template for the `worker` repo.
