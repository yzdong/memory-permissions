# Infrastructure Cost Alert Runbook

What to do when cost anomaly alerts fire or monthly spend is tracking above budget. This is an operational guide, not a finance document.

## Alert sources

- AWS Cost Anomaly Detection: fires in `#platform-alerts` when daily spend deviates > 20% from the 14-day baseline
- Monthly budget alert: fires at 80% and 100% of monthly budget thresholds (configured in AWS Budgets)

## Initial triage

```bash
# Get cost breakdown by service for last 7 days
aws ce get-cost-and-usage \
  --time-period Start=$(date -d '7 days ago' +%Y-%m-%d),End=$(date +%Y-%m-%d) \
  --granularity DAILY \
  --metrics BlendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

Common culprits:
- RDS: runaway query causing high IOPS
- EC2/EKS: over-scaled node groups that weren't scaled back
- Data Transfer: unexpected cross-region traffic
- Kafka (MSK): partition count increase multiplied broker costs

## Immediate actions by service

### EC2/EKS over-scaling

```bash
# Check current node group sizes
eksctl get nodegroup --cluster platform-prod

# Scale down if appropriate
eksctl scale nodegroup --cluster platform-prod --name workers --nodes 4
```

Don't scale below minimum needed for current traffic — check the `Worker / Throughput` Grafana panel first.

### RDS IOPS spike

- Check `Platform / Postgres Health` for slow query counts
- Look for a missing index on a recently added query pattern
- Check if a VACUUM FULL was triggered (it causes massive IOPS)

### Data transfer costs

```bash
# Check VPC Flow Logs for cross-AZ or cross-region traffic patterns
# (Athena query — use the saved query 'cross-az-traffic-7d' in Athena console)
```

## Tagging issues

If costs show up under `No Tag` in the breakdown, resources are missing required tags. Required tags: `team`, `service`, `env`. Tag enforcement runs via AWS Config — check the Config console for non-compliant resources.

## Escalation

If spend is more than 15% over monthly budget with no obvious cause, bring in `@infra-ops` and `@platform-lead`. Do not make architecture changes without lead approval during a cost incident.
