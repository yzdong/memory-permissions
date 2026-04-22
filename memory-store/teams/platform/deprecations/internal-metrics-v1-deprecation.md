# Internal Metrics V1 API Deprecation

**Status:** Sunset scheduled 2025-09-01  
**Owner:** Platform (Observability Sub-team)  
**Slack:** #observability

## What Is the V1 Metrics API?

The V1 metrics API (`/internal/metrics/v1/query`) was a thin wrapper around InfluxDB 1.x that predates our move to Prometheus/Thanos. It accepted InfluxQL queries and returned a proprietary JSON envelope.

We've been running it alongside the V2 API (PromQL-backed) since 2023. V1 traffic has dropped significantly but about 12 services still hit it, mostly older scripts and some legacy alert rules.

## Migration to V2

V2 endpoint: `/internal/metrics/v2/query`

V2 accepts PromQL. If you were using InfluxQL, you'll need to rewrite your queries.

### InfluxQL → PromQL Quick Reference

| InfluxQL | PromQL equivalent |
|---|---|
| `SELECT mean("value") FROM "cpu" WHERE time > now()-1h` | `avg_over_time(cpu_usage[1h])` |
| `SELECT count("errors") FROM "api" GROUP BY service` | `sum by (service) (increase(api_errors_total[5m]))` |
| `SELECT last("memory") FROM "process"` | `process_resident_memory_bytes` |

### Auth Change

V1 used a static API key passed as `?api_key=`. V2 uses service account tokens via the `Authorization: Bearer` header. Tokens are provisioned in Vault at `secret/metrics/service-accounts/<service-name>`.

## Checking Current Usage

Grafana dashboard: `Observability → Metrics API Usage by Version`. Filter by `version=v1` to see your service's call count.

Alternatively, check server logs:
```bash
ssh metrics-api.internal
grep 'v1/query' /var/log/metrics-api/access.log | awk '{print $7}' | sort | uniq -c
```

## What Happens After Sunset

The V1 endpoint will return `410 Gone`. InfluxDB 1.x will be decommissioned the same week (saves ~$1,200/month in compute).

## Related

- `runbooks/promql-query-guide.md`
- `../observability/thanos-architecture.md`
