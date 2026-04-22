# 2026-01-07 Gateway Rate Limit Misconfiguration

## Summary

A configuration push to `gateway` accidentally set the global rate limit to 10 req/s per IP instead of 10,000 req/s. Normal users were throttled as though they were abusers. The misconfiguration was live for 31 minutes before detection.

## Timeline

- **14:02** — Config push lands: `gateway/config/rate-limits.yaml` v1.9.3
- **14:02** — Rate limiting begins aggressively throttling all IPs
- **14:06** — Support channel lights up with 429 reports
- **14:09** — On-call paged
- **14:14** — Config diff reviewed; typo identified (`10` vs `10000`)
- **14:17** — Corrected config pushed to gateway
- **14:33** — 429 rate fully normalizes (some clients in backoff loops)

## Root Cause

The config value `requests_per_second` was specified as `10` in a YAML file. The intended value was `10_000`. The reviewer and author both read the value as "ten" without noticing the missing thousands. There is no validation step that checks rate-limit values against a reasonable range.

YAML file: `gateway/config/rate-limits.yaml`. The type is `int` so `10_000` (Python-style underscores) is not valid YAML — the author meant to type `10000` and missed the extra zeros.

## Impact

- 31 minutes of widespread 429 responses for legitimate traffic
- Estimated 240,000 throttled requests
- Mobile clients with exponential backoff took up to 8 additional minutes to recover after config fix
- No data loss

## Action Items

- [ ] Add config validation: reject `requests_per_second` values below 100 — owner: @lena, due 2026-01-14
- [ ] Add a staging smoke test that validates rate limits are not absurdly low before gateway config promotion — owner: @lena, due 2026-01-21
- [ ] Consider using YAML anchors or a typed config schema with explicit ranges — owner: @marco, due 2026-01-28
- [ ] Add rate-limit value to canary dashboard so operators can sanity-check visually — owner: @ryo, due 2026-01-21
