# Disaster Recovery Drill Playbook

We run a DR drill twice a year: once as a tabletop exercise, once as a live failover test. The live test is the one that matters; the tabletop is prep for it.

## Objectives

1. Validate that RTO and RPO targets are achievable in practice, not just in theory
2. Identify gaps between the DR plan (on paper) and operational reality
3. Give the team practice — the first time you fail over to the DR region should not be during an actual disaster

## Current RTO/RPO Targets

| Tier | RPO | RTO |
|---|---|---|
| Tier 1 (customer-critical) | 15 min | 1 hour |
| Tier 2 (internal tools) | 4 hours | 8 hours |
| Tier 3 (non-critical) | 24 hours | 48 hours |

## Tabletop Exercise

Schedule: 90-minute session with Platform team + service leads.

Scenario: "us-east-1 is completely unavailable. What do we do?"

Work through:
- Who decides to declare a DR event?
- What's the communication chain (internal, customer-facing, status page)?
- Which services fail over automatically vs. manually?
- What's the order of operations for manual failovers?
- What data loss is acceptable for each tier? Who approves accepting that loss?

Output: list of gaps found, owners assigned.

## Live Failover Test

### Pre-Test Requirements

- [ ] Cross-region replication verified for all Tier 1 databases (lag < 30s)
- [ ] DR environment Terraform applied and validated within last 30 days
- [ ] DNS failover records configured and tested in isolation
- [ ] Synthetic monitors pointed at DR region endpoints
- [ ] All engineers who will participate have DR region console access

### Test Execution

```bash
# Step 1: Pause writes in primary region
./scripts/dr/pause-primary-writes.sh --confirm

# Step 2: Promote DR read replica
./scripts/dr/promote-replica.sh --region us-west-2 --db core-db

# Step 3: Flip DNS
./scripts/dr/dns-failover.sh --target us-west-2 --dry-run  # review first
./scripts/dr/dns-failover.sh --target us-west-2

# Step 4: Validate
python scripts/dr/validate-dr.py --region us-west-2 --tier 1
```

### Success Criteria
- All Tier 1 services responding in DR region within RTO
- Data loss verified to be within RPO (compare record counts pre/post)
- End-to-end synthetic test passing in DR region

### Failback
Don't rush failback. Confirm the primary region is genuinely healthy before returning. Failback order is reverse of failover order.

## Post-Drill

- Measure actual RTO/RPO vs. targets
- Document every manual step that wasn't scripted — each is a candidate for automation
- Update `docs/dr-plan.md` with findings
