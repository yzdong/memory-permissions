# Redis Failover Procedure

This covers unplanned Redis primary failure and manual sentinel/cluster failover. Does not cover routine Redis version upgrades (see `redis-upgrade.md`).

## Architecture Quick Reference

- **Mode**: Redis Sentinel, 1 primary + 2 replicas
- **Sentinel quorum**: 2
- **Used by**: api session store, worker rate-limiter, gateway feature-flag cache
- **RDB snapshot interval**: every 15 minutes to S3 `s3://infra-backups/redis/`

## Detecting a Failover Need

```bash
redis-cli -h redis-sentinel-0.internal -p 26379 SENTINEL masters
```
If `status` is not `ok` or the `num-slaves` count drops below 1, investigate.

## Automatic Sentinel Failover

Sentinel should trigger automatically within 30s of primary loss. Verify:
```bash
redis-cli -h redis-sentinel-0.internal -p 26379 SENTINEL get-master-addr-by-name mymaster
```
If the IP has changed from the old primary, sentinel already promoted a replica. Confirm services reconnected by checking api error rate in Grafana dashboard `Platform / Redis Connections`.

## Manual Failover

Only needed if sentinel failover did not complete automatically:
```bash
redis-cli -h redis-sentinel-0.internal -p 26379 SENTINEL failover mymaster
```
Then verify the new master:
```bash
redis-cli -h <new-primary-ip> -p 6379 INFO replication | grep role
```
Expected output: `role:master`

## Reconnecting Services

- **api**: reads `REDIS_SENTINEL_HOSTS` env var; rolling restart picks up new master automatically.
- **worker**: same sentinel config; no restart needed if lag < 500ms.
- **gateway**: uses a separate Redis instance for flag cache — check `gateway-config.md` before touching.

## Restoring from RDB Snapshot

If all nodes are lost (rare):
1. Download latest snapshot:
   ```bash
   aws s3 cp s3://infra-backups/redis/dump-latest.rdb /var/lib/redis/dump.rdb
   ```
2. Start Redis with the snapshot in place.
3. Validate key count vs. the snapshot manifest in `s3://infra-backups/redis/manifest.json`.

## After Failover

- Update `../infrastructure/redis-topology.md` with new primary IP.
- Verify session hit rate returns to > 95% within 5 minutes.
- Log the event in `../incidents/redis-log.md`.
