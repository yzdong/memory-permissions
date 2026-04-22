# 2025-10-28 Gateway 502 Storm

## Summary

The `gateway` service began returning 502 errors to approximately 40% of traffic for 28 minutes after an upstream timeout misconfiguration was deployed. Mobile and web clients showed "Service Unavailable" banners during the window.

## Timeline

| Time (UTC) | Event |
|---|---|
| 16:05 | `gateway` v1.8.3 deployed |
| 16:07 | 502 error rate climbs to 38% |
| 16:09 | Customer support begins receiving reports |
| 16:11 | On-call (Sasha) alerted via PagerDuty |
| 16:19 | Config diff reviewed; `upstream_read_timeout` found set to `50ms` (was `5000ms`) |
| 16:27 | Hotfix deploy initiated with corrected timeout value |
| 16:33 | Error rate drops to baseline |

## Root Cause

A YAML config value for `upstream_read_timeout` was accidentally expressed as `50` (milliseconds) after a copy-paste from a latency budget document that used seconds. The PR reviewer did not catch the unit mismatch because the field name doesn't encode units and there's no schema validation on the config file.

## Impact

- 28 minutes of ~38% 502 rate on all gateway-proxied endpoints
- Estimated 19,000 failed requests based on traffic replay analysis
- No data loss; all failed requests were safe to retry
- Three high-value B2B customers noticed and emailed account managers

## Action Items

- [ ] **P0** Add JSON Schema validation for `gateway` config with unit annotations — owner: Sasha, due 2025-11-04
- [ ] **P0** Canary deployment required for `gateway` config changes (10% traffic, 5-min soak) — owner: Priya, due 2025-11-07
- [ ] **P1** Add synthetic monitor that asserts p99 < 800 ms from external probe — owner: Leila, due 2025-11-10
- [ ] **P2** Rename config key to `upstream_read_timeout_ms` for clarity

## Notes

Timeout configuration reference lives in `../architecture/gateway-timeouts.md`.
