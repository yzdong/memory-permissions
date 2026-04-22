# Redis 3.x Cluster Decommission

**Status:** Decommissioned 2024-10-15  
**Owner:** Platform  
**Replacement:** Redis 7.2 Cluster (ElastiCache)

## History

The Redis 3.x cluster was provisioned in 2018 and has been running non-stop. Redis 3 lacks:

- WAIT command for semi-synchronous replication
- ACL support (introduced in Redis 6)
- LMPOP / ZMPOP commands used by newer client libraries
- TLS for in-transit encryption

By early 2024 we had three separate services hacking around missing ACL support by sharing a single no-auth Redis connection. That's not acceptable.

## Migration Steps Taken

1. Provisioned Redis 7.2 cluster on ElastiCache with TLS and AUTH enabled
2. Enabled TLS in all client configs (see `services/*/config/redis.yaml`)
3. Migrated data using `redis-cli --cluster` MIGRATE commands where needed (mostly session data and rate-limit counters — ephemeral by design, so most could just be cold-started)
4. Updated all services to use per-service ACL users (`secret/redis/acl/<service-name>` in Vault)
5. Ran parallel for two weeks, then cut DNS over
6. Monitored keyspace hit rates and eviction metrics in Grafana

## ACL User Setup

Each service now has a Redis user with minimal permissions:

```
ACL SETUSER ingestion-worker on >strong-password ~ingestion:* &* +get +set +del +expire
```

ACL definitions are managed in Terraform at `terraform/redis/acl-users.tf`.

## What to Do If Redis Commands Fail

If you get `NOPERM this user has no permissions to run the X command`, your service is trying to do something outside its ACL. Check the ACL definition in Vault and open a PR to `terraform/redis/acl-users.tf` with the needed permission addition — don't use the admin user as a workaround.

## Related

- `runbooks/redis-failover-procedure.md`
- `terraform/redis/`
- `../infrastructure/elasticache-sizing.md`
