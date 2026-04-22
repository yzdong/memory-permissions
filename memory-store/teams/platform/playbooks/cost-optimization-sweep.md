# Cost Optimization Sweep Playbook

Run this every 6 months or when cloud spend growth exceeds 15% MoM for two consecutive months. This is a structured program, not a one-off ticket.

## Context

Platform owns the shared infra budget and is accountable for cost efficiency. Individual service teams own their service-level spend. We work together on this — Platform provides tooling and analysis; service teams make the changes.

## Step 1: Spend Baseline

```bash
# Pull cost by service tag for last 90 days
python scripts/cost/tag-breakdown.py \
  --start-date $(date -d '90 days ago' +%F) \
  --end-date $(date +%F) \
  --group-by service \
  --output reports/cost-by-service.csv
```

Also pull by resource type: EC2, RDS, data transfer, and S3 are usually the top 4.

## Step 2: Quick Wins Scan

These can usually be done without service team involvement:

- **Idle resources:** EC2 instances with < 5% CPU over 14 days → candidate for termination or downsizing
- **Unattached EBS volumes:** `aws ec2 describe-volumes --filters Name=status,Values=available`
- **Snapshot retention:** Any snapshot older than 90 days on non-critical accounts
- **Old AMIs:** Deregister AMIs not used in any launch template
- **NAT Gateway:** Check if traffic is routing through NAT unnecessarily vs. VPC endpoints

## Step 3: Compute Rightsizing

For each service with > $2,000/mo compute:
1. Pull average and p95 CPU + memory from Datadog
2. Compare to provisioned instance size
3. If p95 CPU < 40% and p95 memory < 55%, recommend downsizing by one instance class

Document recommendations in `reports/rightsizing-YYYY-MM.md`. Don't just resize unilaterally — service teams need to validate.

## Step 4: Reserved Instance / Savings Plan Review

- Run the RI utilization report in Cost Explorer
- Any RI at < 75% utilization is a problem — either terminate the workload or sell on marketplace
- Propose new RI purchases based on the capacity plan from `quarterly-capacity-planning.md`

## Step 5: Data Transfer Costs

This one always surprises people. Check:
- Cross-AZ traffic (often fixable by pinning clients to the same AZ)
- Cross-region replication that's no longer needed
- CloudFront cache hit rate — if < 70%, tuning the cache behavior can significantly cut origin traffic

## Step 6: Findings Report

Deliver a concise report to Engineering leadership:
- Total identified savings opportunity ($X/mo)
- Quick wins (Platform-owned, < 1 week to implement)
- Service team recommendations with estimated effort
- Items requiring architectural changes (longer horizon)

## Guardrails

- Never terminate a resource without checking the `do-not-delete` tag
- Any change affecting a production database requires a change window
- RI purchase decisions > $10,000 require VP approval
