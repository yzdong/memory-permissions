# Quarterly Capacity Planning Playbook

Run this every quarter, ideally starting 6 weeks before quarter-end so procurement has runway.

## Owners
- Platform lead + on-call rotation rep
- Coordinate with Finance (ping #finance-ops) for budget sign-off

## Steps

### 1. Pull current utilization
```bash
./scripts/infra/utilization-report.sh --window 90d --output csv > /tmp/util-$(date +%Y%m).csv
```
Look at p95 CPU and memory per cluster, not averages. Averages lie.

### 2. Gather growth projections
- Pull traffic forecasts from Growth team (see `../forecasts/traffic-model.md`)
- Check any planned launches from the roadmap doc shared in #platform-sync

### 3. Headroom targets
| Resource | Minimum headroom | Target headroom |
|----------|------------------|-----------------|
| CPU      | 20%              | 35%             |
| Memory   | 15%              | 30%             |
| Disk     | 25%              | 40%             |

### 4. Draft capacity request
- Fill out `templates/capacity-request.md`
- Include cluster-level breakdown, not just aggregate numbers
- Attach the utilization CSV

### 5. Review & approval
- Engineering director approves instance changes
- Finance approves any new commitments over $50k
- Committed Reserved Instance purchases need 2-week lead time with AWS

### 6. Implement
- Terraform PRs for node pool changes go through normal review (`runbooks/terraform-apply.md`)
- Schedule any disruptive changes during low-traffic windows (see `../oncall/change-windows.md`)

## Common mistakes
- Forgetting spot instance interruption rate when sizing critical workloads
- Using monthly averages instead of peak-day numbers for storage
- Not accounting for holiday traffic spikes in Q4 planning

## Outputs
- Capacity request doc (linked in quarterly planning ticket)
- Updated `infra/node-pools/` Terraform vars
- Summary posted to #platform-capacity Slack channel
