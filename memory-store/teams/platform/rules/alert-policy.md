# Alert Policy — Platform Team

## Alert Philosophy

Every alert that pages someone should require a human decision. If it can be auto-remediated, auto-remediate it. If it's informational, make it a Slack notification, not a page.

**Alert fatigue is a safety issue.** Noisy alerts get ignored.

## Alert Tiers

| Tier | Channel | Response SLA | Example |
|------|---------|-------------|--------|
| P1 | PagerDuty (phone call) | 5 min ack | Pipeline fully down |
| P2 | PagerDuty (push notification) | 30 min ack | Canary error rate > 5% |
| P3 | `#platform-alerts` Slack | Next business day | Disk usage > 80% |
| Info | `#platform-monitoring` Slack | No SLA | Successful deploy notification |

## Creating New Alerts

Before adding an alert:

1. Confirm what action the on-call engineer should take when it fires.
2. Document the runbook link in the alert annotation.
3. Get a review from one other Platform engineer.
4. Shadow the alert for one week (set to non-paging) to validate the threshold.

Alerts without runbook links will be disabled after 14 days.

## Threshold Guidelines

- Error rate alerts: fire after the rate sustains for **5 minutes** (avoid transient spikes).
- Latency alerts: use p99 latency, not mean.
- Disk/memory: alert at 80%, critical page at 92%.

Do not set thresholds below what you can act on. A 0.1% error rate during a quiet period is not actionable if your normal floor is 0.08%.

## Alert Review Cadence

Review all Platform alerts quarterly. Retire any alert that has:
- Fired zero times in the past 6 months
- Fired more than 30 times in a week without a corresponding incident

See `../evaluations/alert-review.md` for the last review results.
