# Gateway Rate Limit Tuning

The gateway enforces per-client and global rate limits via a Redis-backed token bucket. This runbook covers emergency adjustments, not the configuration process (see `../gateway/rate-limit-config.md` for the full configuration guide).

## Current Limits (as of 2025-01)

| Tier | Requests/min | Burst | Notes |
|------|-------------|-------|-------|
| free | 60 | 10 | Per API key |
| pro | 600 | 100 | Per API key |
| internal | 6000 | 500 | Per service identity |
| global | 50000 | 5000 | Across all traffic |

## Checking Current Rate Limit State

```bash
# See hit rate per tier
just metrics gateway.ratelimit.hit_rate --by-tier --env production --window 5m

# Inspect a specific API key's current bucket
redis-cli -h redis.internal GET ratelimit:apikey:<key-prefix>
```

## Emergency: Increase Global Limit

If legitimate traffic is being rate-limited during a traffic spike (e.g., a marketing event):

```bash
just config-set gateway RATELIMIT_GLOBAL_RPM=80000 --env production
# No restart needed — gateway polls config every 30s
```

Document the change in the #platform-incidents channel and set a reminder to revert it.

## Emergency: Block an Abusive Client

If a client is causing disruption and rate limits aren't enough:
```bash
just gateway-blocklist add --api-key <key> --reason 'abuse - see incident XYZ' --env production
```
This takes effect within 30 seconds (next config poll).

## Emergency: Temporarily Disable Rate Limiting

Last resort. Only for internal traffic issues or a rate-limit bug causing false positives:
```bash
just feature-flag set GATEWAY_RATELIMIT_ENABLED false --env production
```
⚠️ This removes all rate limiting. Revert as soon as possible.

## Diagnosing False Positives

If clients report being blocked but their usage looks normal:
1. Check if their API key was accidentally assigned the wrong tier:
   ```bash
   just gateway-keyinfo --api-key <key>
   ```
2. Check for shared IP NAT causing multiple clients to appear as one:
   ```bash
   just metrics gateway.ratelimit.by_ip --env production --window 15m | sort -rn | head
   ```
3. Verify Redis is not returning stale counter values (after a Redis failover, counters reset; this would lower limits, not raise them).

## Reverting Changes

Always revert emergency limit changes within 24 hours or after the incident resolves. Log the revert in the same incident thread.
