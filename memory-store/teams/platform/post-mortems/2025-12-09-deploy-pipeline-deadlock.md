# 2025-12-09 Deploy Pipeline Deadlock

## Summary

The internal `just` CLI's deploy pipeline entered a deadlock state that blocked all production deployments for 3 hours 17 minutes. Two concurrent deploys acquired overlapping locks in opposite order, causing both to wait indefinitely.

## Timeline

| Time (UTC) | Event |
|---|---|
| 13:45 | Engineer A triggers `worker` deploy |
| 13:45 | Engineer B (simultaneously) triggers `api` deploy |
| 13:46 | Both deploys hang at "Waiting for deploy lock" |
| 13:52 | Engineers notice and ping #platform-team |
| 14:00 | On-call (Damien) joins; confirms deadlock via deploy state store |
| 15:02 | Manual lock release performed via `just lock release --force` |
| 15:15 | Deploys re-run sequentially; complete successfully |
| 17:02 | Root cause confirmed and fix merged |

## Root Cause

The `just` CLI acquires two locks during a deploy: a per-service lock and a shared infrastructure lock. `worker` deploys acquire them in order `[service, infra]`; `api` deploys (due to a code path difference) acquired them in order `[infra, service]`. With both deploys running simultaneously, each held the first lock and waited for the second — classic deadlock.

This ordering inconsistency was introduced in `just` v0.14.0 (shipped 3 weeks prior) when the API deploy path was refactored.

## Impact

- 3 h 17 min freeze on all production deployments
- Two security patches queued for release were delayed
- No production traffic impact (existing deployments were healthy)

## Action Items

- [ ] **P0** Enforce canonical lock acquisition order in `just` CLI (alphabetical by lock name) — owner: Damien, due 2025-12-13
- [ ] **P0** Add deadlock detection with 60-second timeout + automatic retry with backoff — owner: Leila, due 2025-12-17
- [ ] **P1** Integration test for concurrent deploys of all service pairs — owner: Tomás, due 2025-12-20
- [ ] **P2** Document lock hierarchy in `../just-cli/architecture.md`

## Notes

Lock release runbook added to `runbooks/deploy.md` post-incident.
