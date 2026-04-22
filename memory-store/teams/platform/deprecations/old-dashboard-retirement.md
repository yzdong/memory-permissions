# Old Dashboard Retirement

**Status:** Retired 2025-04-30  
**What was it:** The Grafana v7 instance at `dashboards.internal.legacy/`  
**Replacement:** Grafana v10 at `dashboards.internal/`

## Background

We ran two Grafana instances in parallel for about eight months longer than planned. The legacy instance was kept alive because three teams had bespoke dashboards that weren't migrated in the original v10 rollout. Those teams finally signed off, so we pulled the plug on April 30.

## What Was Migrated

| Dashboard | Old UID | New UID | Owner |
|---|---|---|---|
| Platform Infra Overview | `infra-001` | `plt-infra-v2` | Platform |
| Billing Pipeline | `bill-dash-07` | `billing-main` | Billing |
| Event Bus Throughput | `eb-tput-v3` | `events-throughput` | Data Eng |
| Deployment Frequency | `depfreq-legacy` | `platform-delivery` | Platform |

Two dashboards were intentionally not migrated — they had no viewers in 90 days and were archived as JSON at `s3://platform-dashboard-archive/grafana-v7/`.

## What Broke During Cutover

- Alerting rules referencing the old instance datasource UID `legacy-prom-01` had to be rewritten; the new datasource UID is `prometheus-prod`
- Several PagerDuty alerts had hardcoded links to `dashboards.internal.legacy/` — platform updated these in PD on cutover day
- The `provisioning/dashboards/` directory in the old Terraform module (`infra/terraform/grafana-legacy/`) was left intact temporarily for rollback; it was deleted in the 2025-05-07 infra PR

## Lessons

The 8-month parallel-run was too long. Next time we should set a firm cutover date at migration kickoff and build migration tooling (dashboard JSON export + import scripts) from the start rather than doing it manually per team.

Migration scripts we wrote are saved at `tools/grafana-migrate/` if anyone needs them for future Grafana major-version upgrades.

## References

- `runbooks/grafana-provisioning.md`
- `infra/terraform/grafana/README.md`
