# Redis Cluster v4 Sunset

**Status:** Sunset complete — 2025-03-01  
**Owner:** Platform  
**Replaced by:** ElastiCache Redis 7.x cluster

## Background

We self-managed a Redis 4.0 cluster on EC2 (`redis-cluster-prod-01` through `-03`) from 2019 to 2025. Redis 4 has been EOL since 2022. The cluster ran fine, but:

- No TLS support in Redis 4 — all cache traffic was unencrypted on the internal network
- Missing ACL support (added in Redis 6) — everyone used the same no-password connection
- Self-managed replication meant Platform was on-call for failovers
- A 2024 incident (`INC-2309`) showed a 20-minute manual failover was unacceptable

## Migration Path Taken

1. Provisioned ElastiCache Redis 7.x cluster with Multi-AZ (`prod-cache-main`)
2. Identified all services using the old cluster via `CLUSTER INFO` client list
3. Migrated services one at a time using a feature flag pointing to old vs. new endpoint
4. Ran both clusters in parallel for 6 weeks
5. Decommissioned EC2 Redis nodes on 2025-03-01

## Connection String Changes

```python
# Old (do not use)
REDIS_URL = "redis://redis-cluster-prod-01.internal:6379"

# New
REDIS_URL = "rediss://prod-cache-main.abc123.cfg.use1.cache.amazonaws.com:6380"  # TLS on port 6380
```

Note: `rediss://` (double-s) for TLS. If your Redis client doesn't support `rediss://` scheme, upgrade the client library.

## ACL Setup

Each service now has its own Redis user with scoped permissions. Credentials are in Vault at `secret/redis/prod/<service-name>`. Request access via the standard Vault policy in `infra/vault/policies/redis-read.hcl`.

## Cache Warming

ElastiCache was not pre-warmed from the old cluster — Redis 4 to 7 has no compatible snapshot restore. Plan for elevated cache miss rates for 2-4 hours after initial cutover of each service. We didn't see meaningful downstream impact due to low read latencies on the backing DB.

## References

- `runbooks/elasticache-failover.md`
- `infra/terraform/elasticache/main.tf`
