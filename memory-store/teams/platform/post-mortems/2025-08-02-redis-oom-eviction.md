# 2025-08-02 Redis OOM Eviction Cascade

## Summary

At 09:17 UTC a Redis memory spike caused aggressive key eviction under the `allkeys-lru` policy. Session tokens were evicted, logging out a large portion of active users. The spike traced back to a batch job in the `worker` service that stored uncompressed intermediate results in Redis without a TTL.

## Timeline

- **08:50** — Nightly recommendation-score batch job starts (worker service)
- **09:17** — Redis memory hits 95% of `maxmemory` (12 GB); eviction begins
- **09:19** — Auth errors spike; users report being logged out
- **09:23** — On-call paged via PagerDuty
- **09:31** — Batch job identified as memory culprit; job manually killed
- **09:44** — Redis memory drops to 61%; session evictions stop
- **10:02** — Error rate normalizes; incident downgraded

## Root Cause

The batch job wrote ~3.8 GB of raw score vectors into Redis as a caching layer. Each key had no expiry set. Under memory pressure, Redis evicted whatever LRU keys it could, which happened to include session tokens (shorter lived, frequently accessed, but older in LRU terms due to a timing quirk).

The engineer who wrote the batch job wasn't aware that session data shared the same Redis instance. See `infra/redis/instance-map.md` for the current tenant layout.

## Impact

- Estimated 9,200 active sessions terminated unexpectedly
- 27 minutes of elevated auth failure rate
- No data loss; sessions can be re-established on login
- Downstream `gateway` saw elevated 401 responses during window

## Action Items

- [ ] Split Redis into dedicated instances: one for session/auth, one for batch/ephemeral workloads — owner: @ryo, due 2025-09-01
- [ ] Mandate TTL on all Redis writes in `worker` service; add linter rule — owner: @farah, due 2025-08-15
- [ ] Add memory utilization alert at 80% (not just 95%) — owner: @ryo, due 2025-08-09
- [ ] Update `runbooks/redis-operations.md` with multi-tenant risk section
- [ ] Schedule cross-team session with Data Engineering about shared infra usage policies
