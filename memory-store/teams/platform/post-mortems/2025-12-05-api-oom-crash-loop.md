# 2025-12-05 API Service OOM Crash Loop

## Summary

The `api` service entered a crash loop between 03:14 and 04:51 UTC after a memory leak introduced in v3.7.2 caused each pod to exceed its 2 GB memory limit within ~12 minutes of startup. Kubernetes repeatedly restarted pods, leading to intermittent 503s for end users.

## Timeline

| Time (UTC) | Event |
|---|---|
| 03:00 | api v3.7.2 rolled out (10% canary) |
| 03:14 | First OOMKilled event on canary pod |
| 03:17 | Canary promotion proceeds (OOM not yet visible in alerts) |
| 03:22 | Full rollout complete; all pods begin leaking |
| 03:31 | Error rate alert fires at 8% 5xx |
| 03:38 | On-call initiates rollback to v3.7.1 |
| 04:51 | All pods on v3.7.1; memory stable; 503s stop |

## Root Cause

v3.7.2 introduced a request-scoped cache that was mistakenly registered as a module-level singleton. Each request appended to the cache without ever evicting. The cache grew linearly with request count until the pod was OOM-killed.

File: `api/src/cache/request_cache.py`, introduced in PR #4501.

## Impact

- ~97 minutes of degraded service; peak 5xx rate 22%
- Estimated 31,000 failed requests
- Canary promotion process did not catch OOM fast enough (12-min leak vs. 5-min canary bake window)

## Action Items

- [ ] Increase canary bake window to 20 minutes before auto-promotion — owner: @marco, due 2025-12-12
- [ ] Add memory growth rate alert: if any pod grows >150 MB/min, hold deployment — owner: @lena, due 2025-12-19
- [ ] Code review checklist item: flag any module-level mutable state — owner: API team, due 2025-12-31
- [ ] Add memory profiling to load tests in CI — owner: @farah, due 2026-01-09
- [ ] Post-mortem linked from `../api/deploys/v3.7.2-rollback.md`
