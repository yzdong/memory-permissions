# 2026-03-18 API Rate Limiter Misconfiguration

## Summary

An incorrect rate limit configuration deployed to the `api` service set per-IP limits 100x too low, causing legitimate users to be throttled with 429 responses for ~55 minutes. The issue was triggered by a unit confusion (requests/second vs requests/minute) in the config.

## Timeline

| Time (UTC) | Event |
|---|---|
| 09:00 | `api` v2.31.0 deployed with new rate limiter config |
| 09:01 | 429 error rate climbs to 28% across all endpoints |
| 09:04 | Customer support queue spikes; first escalations arrive |
| 09:07 | On-call (Priya) paged by alert: 429 rate > 5% |
| 09:14 | Config diff reviewed; `rate_limit_per_ip` found set to `1` (was `100`) |
| 09:22 | Hotfix deployed setting `rate_limit_per_ip` to `100` with correct unit label |
| 09:55 | 429 rate back to baseline (<0.1%) |

## Root Cause

The rate limiter config was migrated from requests/minute to requests/second as part of v2.31.0. The value was updated from `6000` (req/min) to `100` (req/s), which is equivalent. However, the PR author accidentally used `1` instead of `100` — a transcription error. The config has no unit annotation and no bounds-checking validation.

The code review passed without catching the value change because the PR was large (17 files) and the config change was on line 312.

## Impact

- 55 minutes of excessive 429 throttling
- ~22% of authenticated users hit limits during peak traffic
- Support received 47 tickets; all resolved with explanation and session refresh
- No data loss; all throttled requests were retried successfully by clients

## Action Items

- [ ] **P0** Add config schema validation: `rate_limit_per_ip` must be > 10 and < 10,000 — owner: Priya, due 2026-03-22
- [ ] **P0** Annotate all rate limit config fields with unit in key name (e.g. `rate_limit_per_ip_rps`) — owner: Sasha, due 2026-03-22
- [ ] **P1** Rate limit config changes must be deployed with canary (5% traffic) and 10-min soak before full rollout — owner: Damien, due 2026-03-25
- [ ] **P1** Add 429 rate alert at 5% threshold (currently fires but was slow; reduce evaluation window to 2 min) — owner: Tomás, due 2026-03-24
- [ ] **P2** Add large-PR checklist requiring config-change summary in PR description

## References

- Rate limiting architecture: `../architecture/api-rate-limiting.md`
- `runbooks/deploy.md` for canary rollout procedures
