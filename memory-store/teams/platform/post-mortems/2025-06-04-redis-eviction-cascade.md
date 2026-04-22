# 2025-06-04 Redis Eviction Cascade

## Summary

A spike in memory usage on the shared Redis cluster caused aggressive key eviction, which cascaded into failed session lookups across the `api` and `gateway` services. The incident lasted approximately 2 hours and 14 minutes before caches were sufficiently warmed.

## Timeline

| Time (UTC) | Event |
|---|---|
| 09:12 | Alerts fire: `api` p99 latency exceeds 4 s threshold |
| 09:15 | On-call (Priya) pages secondary (Tomás) |
| 09:22 | Redis dashboard shows eviction rate at ~18 k keys/min |
| 09:40 | Decision made to increase `maxmemory` from 8 GB to 12 GB via config reload |
| 10:05 | Eviction rate drops; cache hit rate begins recovering |
| 11:26 | Latency back within SLO; incident closed |

## Root Cause

A poorly-scoped background job in the `worker` service was caching full serialized order objects (averaging 42 KB each) without a TTL. Over 48 hours these accumulated to fill ~7.4 GB of the 8 GB limit. Once memory pressure hit, Redis began evicting LRU keys indiscriminately — including hot session tokens.

The job was introduced in `worker` commit `a3f88c1` two days prior and had not been reviewed for cache hygiene.

## Impact

- Roughly 34% of API requests returned 5xx errors during peak eviction window (09:18–09:55 UTC)
- Approximately 12,000 unique users experienced session drops or failed checkouts
- No data loss; all affected carts were recoverable from Postgres

## Action Items

- [ ] **P0** Add TTL enforcement lint rule in `worker` job framework — owner: Tomás, due 2025-06-11
- [ ] **P1** Set Redis `maxmemory-policy` to `allkeys-lru` with alerting on eviction rate > 2 k/min — owner: Priya, due 2025-06-18
- [ ] **P2** Document cache sizing expectations in `runbooks/redis-sizing.md`
- [ ] **P2** Add integration test asserting cache entries from background jobs have a non-zero TTL

## Follow-up

See also `runbooks/redis-ops.md` for runbook updates made post-incident.
