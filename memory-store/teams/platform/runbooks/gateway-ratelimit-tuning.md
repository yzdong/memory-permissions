# Gateway Rate Limit Tuning

Operational guide for adjusting rate limits on the gateway service. Incorrectly tuned limits can either fail to protect downstream services or block legitimate traffic.

## How rate limiting works

- Gateway uses a token bucket algorithm per API key
- State is stored in Redis (key format: `ratelimit:<api_key_hash>:<window>`)
- Limits are configured per route group in `config/gateway/ratelimits.yaml`
- Changes to config require a gateway config reload (no full redeploy needed)

## Reloading config without restart

```bash
just gateway-reload-config
```

This sends SIGHUP to the gateway process via the Kubernetes exec endpoint. Verify the reload succeeded:

```bash
kubectl logs -n platform -l app=gateway --since=30s | grep 'config reloaded'
```

## Raising limits for a specific API key

Some partners get elevated limits. These are configured in `config/gateway/partner-overrides.yaml`:

```yaml
overrides:
  - api_key_prefix: "pk_partner_acme"
    requests_per_minute: 2000
    burst: 400
```

After editing, reload config with the command above. No restart needed.

## Temporary limit bypass (for load tests)

```bash
# Allowlist an IP for 1 hour (rate limit bypass)
redis-cli -h redis-primary SET ratelimit:bypass:<ip_hash> 1 EX 3600
```

Document the bypass in `#platform-deploys` with a time window and reason. Do not leave bypasses in place permanently.

## Diagnosing false positives (legitimate traffic being blocked)

```bash
# Check which keys are being throttled
kubectl logs -n platform -l app=gateway | grep 'rate_limit_exceeded' | \
  awk '{print $NF}' | sort | uniq -c | sort -rn | head -20
```

If a key appears unexpectedly, check if there's a bug causing requests to share a key inadvertently.

## Rate limit metrics

- Dashboard: `Platform / Gateway Rate Limits`
- Key panel: `Throttled Requests / min` — should normally be near zero
- Alert: `RateLimitThrottleSpike` fires when throttled requests exceed 500/min

## Historical context

We tightened limits in 2024-09 after a partner's runaway client caused a Redis memory spike. The incident post-mortem is at `../post-mortems/2024-09-ratelimit-incident.md`.
