# Redis Key Eviction Runbook

Covers diagnosing and responding to Redis memory pressure and key eviction events. Eviction can silently break rate limiting and session caching.

## Detection

- Alert: `Redis Eviction Rate High` (fires when `evicted_keys` delta > 500/min)
- Symptom: Users report being unexpectedly logged out
- Symptom: Rate limits appear to reset randomly

## Checking memory usage

```bash
redis-cli -h redis-primary INFO memory | grep -E 'used_memory_human|maxmemory_human|mem_fragmentation_ratio'
```

Also check eviction policy:

```bash
redis-cli -h redis-primary CONFIG GET maxmemory-policy
```

Our policy is `allkeys-lru`. This means Redis will evict the least-recently-used keys across all keyspaces when memory is full — including session keys, which is bad.

## Immediate actions

### Option A: Increase maxmemory

Check current allocation and whether the instance has headroom:

```bash
redis-cli -h redis-primary CONFIG SET maxmemory 8gb
```

This is a live change but will revert on restart. Update the config file at `infra/redis/redis.conf` and apply via Terraform.

### Option B: Identify and flush large key groups

```bash
# Find keyspace sizes by prefix
redis-cli -h redis-primary --scan --pattern 'session:*' | wc -l
redis-cli -h redis-primary --scan --pattern 'ratelimit:*' | wc -l
redis-cli -h redis-primary --scan --pattern 'cache:*' | wc -l
```

If cache keys are disproportionately large, lower their TTL in the application config and flush existing ones:

```bash
redis-cli -h redis-primary --scan --pattern 'cache:*' | xargs redis-cli DEL
```

## Key TTL audit

Regularly check for keys with no TTL (they never expire and accumulate):

```sql
-- Not SQL, just a pattern to check via redis-cli:
```

```bash
redis-cli -h redis-primary DEBUG SLEEP 0  # wake up if paused
redis-cli -h redis-primary --scan | \
  xargs -L 1 redis-cli TTL | sort -n | head -20
```

Keys with TTL `-1` are persistent and should be reviewed.

## Long-term fix

Consider separating session store from cache store into two Redis instances. This is tracked in `PLAT-5201`. Until then, session keys must be given shorter TTLs than cache keys.
