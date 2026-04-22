# Cost Optimization Review Playbook

Run this monthly. The goal is to surface easy wins before waste compounds. This is not an audit — it's a standing hygiene practice.

## Data sources
- AWS Cost Explorer export: `s3://platform-billing/exports/monthly/`
- Internal cost allocation dashboard: Grafana > Platform > Cost Allocation
- Unused resource report: `./scripts/infra/find-orphans.sh`

## Review checklist

### Compute
- [ ] Identify instances running at < 10% average CPU over the past 30 days → rightsizing candidates
- [ ] Check Reserved Instance and Savings Plan coverage; target ≥ 70% coverage for steady-state workloads
- [ ] Review spot usage. Are we using spot where we can?
- [ ] Idle node pools (scale to zero if workload permits)

### Storage
- [ ] S3 buckets: check lifecycle policies are in place. Data older than 90 days should be in Infrequent Access unless there's a reason
- [ ] Unattached EBS volumes — run `find-orphans.sh --type ebs` and delete or snapshot-then-delete
- [ ] RDS storage autoscaling — confirm it's enabled and max isn't set irrationally high

### Network
- [ ] Data transfer costs trending up? Cross-AZ traffic is a common culprit; check service topology
- [ ] NAT Gateway costs — anything egressing that shouldn't be?

### Licensing
- [ ] Any tooling seats not used in 60+ days? Ping the user; reclaim if no response

## Escalation path
Wins under $5k/month can be actioned directly by Platform. Over $5k, loop in Finance and Engineering director before any architectural changes.

## Tracking
Log findings and actions in `cost/monthly-reviews/YYYY-MM.md`. Include:
- Total monthly spend vs. prior month
- Actions taken with estimated savings
- Items deferred and why

## Reporting
Post a 3-sentence summary in #platform-cost after each review. Nobody reads long reports in Slack.
