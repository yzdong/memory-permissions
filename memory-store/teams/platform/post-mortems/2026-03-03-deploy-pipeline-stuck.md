# 2026-03-03 Deploy Pipeline Frozen for 4 Hours

## Summary

The CI/CD deploy pipeline became completely stuck from 09:15 to 13:22 UTC. No new builds could be queued or run. The cause was a stale lock file in the pipeline state store (backed by Redis) that was never released after a runner process was SIGKILL'd during a prior infrastructure maintenance window.

## Timeline

| Time (UTC) | Event |
|---|---|
| 09:15 | Engineers begin reporting that pipeline jobs are queued but never start |
| 09:28 | Platform on-call investigates; pipeline queue depth growing |
| 09:45 | Redis pipeline lock key inspected: `pipeline:global:lock` has TTL of -1 (no expiry) |
| 09:52 | Lock traced to runner PID that no longer exists |
| 10:05 | Decision made to manually delete lock key (requires two approvals per runbook) |
| 10:19 | Approval obtained; lock deleted |
| 10:21 | Pipeline resumes; queued jobs begin processing |
| 13:22 | Backlog of 47 queued builds drained |

## Root Cause

The pipeline coordinator uses a Redis distributed lock to prevent concurrent global state mutations. The lock is acquired with `SET NX` and is supposed to set a TTL of 300s. A bug introduced in pipeline-coordinator v0.9.1 called `SET NX` without the `EX` argument when the runner was in "maintenance pause" mode — so the lock had no expiry.

When the runner was SIGKILL'd during the Feb 28 maintenance window, the lock was never released and persisted indefinitely.

## Impact

- 4 hours 7 minutes of zero deploys across all three services
- 47 builds queued; all eventually processed
- Two teams missed their planned release windows
- No production services affected (existing deployments kept running)

## Action Items

- [ ] Fix: always set TTL on pipeline lock acquisition regardless of runner mode — owner: @marco, PR #4788, merged 2026-03-04
- [ ] Add monitor: alert if `pipeline:global:lock` TTL is -1 for more than 60 seconds — owner: @ryo, due 2026-03-10
- [ ] Add lock inspection command to `just` CLI (`just pipeline lock-status`) — owner: @dana, due 2026-03-17
- [ ] Update `runbooks/deploy-pipeline.md` with lock recovery procedure
