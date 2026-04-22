# Gateway Rate Limiting: Operational Notes

The gateway enforces rate limits using a sliding window algorithm backed by Redis. This doc covers tuning, bypassing, and debugging rate limit behavior in production. Architecture details are in `../docs/gateway-rate-limits.md`.

## Checking current limits

Rate limit configs live in `infra/gateway/rate-limits.yaml`. Current production values:

| Tier | Limit | Window |
|------|-------|--------|
| anonymous | 60 req | 1 min |
| authenticated | 1000 req | 1 min |
| partner | 5000 req | 1 min |
| internal | unlimited | — |

## Temporarily raising a limit for a customer

For urgent situations (customer demo, batch migration):

```bash
# Set a per-client override in Redis directly
# Key format: ratelimit:override:<client_id>
redis-cli -h redis-primary.internal \
  SET ratelimit:override:client_12345 10000 EX 7200
# This overrides to 10000/min for 2 hours
```

File a ticket to remove the override or make it permanent in config. Don't leave Redis overrides without a paper trail.

## Customer hitting rate limits unexpectedly

```bash
# Check current window count for a client
redis-cli -h redis-primary.internal \
  ZCARD ratelimit:sliding:<client_id>

# Check their tier in the database
psql -h pgbouncer.internal -U api -d appdb \
  -c "SELECT id, tier, rate_limit_override FROM clients WHERE id = '<client_id>';"
```

If the tier is wrong, fix it in the database and flush their Redis state:

```bash
redis-cli -h redis-primary.internal DEL ratelimit:sliding:<client_id>
```

## Rate limit bypass for internal services

Internal services (worker calling API internally) should use the `X-Internal-Token` header. Verify the secret is correctly configured:

```bash
kubectl get secret gateway-internal-token -n gateway -o jsonpath='{.data.token}' | base64 -d
```

If the token is wrong or missing, gateway will rate-limit internal calls — this shows up as 429s in worker logs.

## Redis failover impact on rate limits

During a Redis failover, rate limit state is temporarily lost. Gateway falls back to in-memory counting (per-pod, not distributed) for the duration of the failover. This means limits are effectively multiplied by the number of gateway pods — users may see higher-than-normal throughput for a brief period. This is the accepted tradeoff over refusing traffic.

See `redis-failover.md` for failover procedure.

## Monitoring

- Grafana → Gateway → Rate Limiting: shows 429 rate by client tier
- Alert: `GatewayRateLimitHigh429Rate` fires if 429s exceed 5% of total requests
