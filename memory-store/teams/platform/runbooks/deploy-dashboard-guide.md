# Deploy Dashboard Guide

This guide explains how to read and use the Grafana deploy dashboard during and after a deploy. It is not a deploy procedure; it's a reference for interpreting what you're seeing.

## Dashboard Location

Grafana → `Platform` folder → `Deploy Overview`

Direct link (internal): `https://grafana.internal/d/platform-deploy-overview`

## Key Panels

### 1. Error Rate by Service

- **What it shows**: 1-minute rolling error rate (5xx / total requests) per service.
- **Normal range**: api < 0.8%, gateway < 0.3%, worker N/A (no HTTP).
- **Deploy spike**: a brief spike to < 2% during rolling restarts is acceptable. Anything sustained > 2% warrants investigation or rollback.

### 2. Deploy Annotations

Vertical lines on all panels. Each annotation shows:
- Service name
- Short SHA
- Who triggered the deploy

If annotations are missing, the deploy was likely triggered outside the normal pipeline. Check `../deploys/manual-deploys.md`.

### 3. Replica Readiness

Shows the count of `Ready` vs `Total` pods per service during rollout. You want to see a smooth staircase pattern. If readiness stalls, the new pods are failing health checks — check pod logs.

### 4. Kafka Consumer Lag (Worker Panel)

Visible during worker deploys. Lag will spike during partition rebalance. Expected recovery: < 3 minutes. If it doesn't recover, see `kafka-lag-runbook.md`.

### 5. P99 Latency

Breakout by service and endpoint. Watch for latency increases on endpoints that touch the database — these sometimes regress after deploys that add unindexed queries.

## Deploy Annotation Variables

The dashboard exposes a `$service` variable so you can filter to a single service. During a worker-only deploy, set `$service=worker` to reduce noise.

## Saved Views

| View Name | Use Case |
|-----------|----------|
| `Deploy - All Services` | Full deploy monitoring |
| `Deploy - Gateway Focus` | Gateway rollout or rollback |
| `Deploy - Post-Deploy 15m` | 15-minute observation window view |
| `Rollback Watch` | Pre-configured for rollback scenarios |

## Common Misreadings

- **Flat error rate line**: usually means metrics stopped flowing, not that errors are zero. Check the `platform-metrics-agent` pods.
- **Lag spike before deploy starts**: pre-existing issue, not caused by the deploy. Investigate separately.
- **Latency spike on gateway after api deploy**: gateway caches route tables; it may take 30s to pick up new api pod IPs.
