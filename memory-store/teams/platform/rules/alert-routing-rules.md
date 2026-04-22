# Alert Routing Rules — Platform Team

We've had too many incidents where alerts fired into the void or the wrong team. This doc codifies who owns what alert and how it routes.

## Ownership Tiers

| Tier | Meaning | Who gets paged |
|------|---------|----------------|
| P1   | Platform infra / pipeline down | Platform on-call (PagerDuty) |
| P2   | Platform degraded, consumer impact | Platform on-call |
| P3   | Warning, no immediate consumer impact | `#platform-alerts` Slack only |
| P4   | Informational | Log sink only |

## Alert → Owner Mapping

This is a representative sample. Full mapping is in `infra/alerting/routing.yaml`.

| Alert name                   | Tier | Team         |
|------------------------------|------|--------------|
| `deploy_pipeline_down`       | P1   | Platform     |
| `vault_unreachable`          | P1   | Platform     |
| `canary_error_rate_high`     | P2   | Platform     |
| `terraform_plan_failed`      | P3   | Platform     |
| `node_disk_pressure`         | P2   | Platform     |
| `service_error_rate_high`    | P2   | Owning team  |
| `db_connection_pool_saturation` | P2 | Platform + DB team |

For alerts jointly owned, Platform is the **first responder** and involves the co-owner as needed.

## Routing Configuration

Alerts are defined in Prometheus alerting rules under `infra/alerting/rules/`. Routes are configured in the Alertmanager config at `infra/alerting/alertmanager.yaml`.

To add a new alert:
1. Add the rule to the appropriate file in `infra/alerting/rules/`
2. Update `infra/alerting/routing.yaml` with the owner and tier
3. PR with 2 platform approvals (this is infra)
4. Verify it fires correctly in staging before merging to prod config

## Silencing Policy

- Silences for known-flaky alerts: max 24h, must include a ticket link
- Extended silences (>24h): require platform-lead approval
- Never silence a P1 alert without an active incident declared

## Noise Reduction

We target fewer than 5 actionable pages per week per on-call. If we're exceeding that, the oncall should file tickets against noisy alerts during their rotation and we triage in the weekly platform sync.

## Related

- `on-call-rotation.md`
- `incident-severity.md`
- `infra/alerting/routing.yaml`
