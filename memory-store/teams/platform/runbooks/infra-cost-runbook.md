# Infrastructure Cost Investigation Runbook

For when spend alerts fire or a budget review flags unexpected cost growth. This is an operational runbook, not a finance process doc.

## Alert Triggers

- Monthly spend projection exceeds 110% of budget baseline.
- Single-day AWS spend > $15,000.
- Untagged resource spend > $500/month (tagging policy violation).

## Initial Triage (15 minutes)

```bash
# Pull current month breakdown by service tag
just infra-cost breakdown --by-tag service --month current

# Compare to last month
just infra-cost diff --month current --baseline last-month
```

Common culprits:
- **RDS storage autoscaling**: Postgres storage can balloon if a runaway job produces large amounts of data. Check table sizes.
- **Kafka data transfer**: inter-AZ Kafka replication is charged. A topic retention increase can cause a spike.
- **EC2 right-sizing drift**: old workers left running after a scale-out event.
- **S3 request costs**: a logging bug can generate millions of unnecessary PUTs.

## Investigating RDS Cost Spike

```bash
just infra-cost breakdown --service rds --detail
```

If storage is growing unexpectedly:
```sql
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
```

See `postgres-vacuum.md` if bloat is the cause.

## Investigating EC2/EKS Cost Spike

```bash
# Find nodes that were running but shouldn't be
just infra-audit ec2 --state running --older-than 7d --not-in-asg
```

Terminate orphaned instances after confirming they're not in use:
```bash
aws ec2 terminate-instances --instance-ids <id1> <id2>
```

## Kafka Transfer Cost

If inter-AZ data transfer is spiking:
1. Identify topics with highest throughput: `just kafka-throughput --by-topic --env production`.
2. Check if any topics recently had retention extended.
3. Consider enabling rack-aware consumer assignment to reduce cross-AZ replication reads.

## Tagging Policy Violations

```bash
just infra-audit tags --missing required --output csv > /tmp/untagged.csv
```

File a Jira ticket per team with their untagged resources. SLA for tagging compliance: 5 business days.

## Escalation

If the cost anomaly exceeds $8,000 delta from baseline and the root cause isn't clear within 2 hours, escalate to the Platform lead and notify Finance via the cost-alerts email alias.
