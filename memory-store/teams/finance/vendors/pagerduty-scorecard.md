# PagerDuty Vendor Scorecard

**Review date:** 2024-09-15  
**Finance reviewer:** Amara Osei  
**Engineering input:** SRE Lead  
**Classification:** Confidential

## Scorecard

| Dimension | Score (1–5) | Comments |
|-----------|-------------|----------|
| Reliability of product | 4.7 | Uptime has been excellent; no P1 incidents |
| Pricing fairness | 3.1 | Per-user pricing is expensive at our scale |
| Support responsiveness | 3.6 | Tier 1 support slow; escalation to Tier 2 works well |
| Integration ecosystem | 4.4 | Excellent; connects to Datadog, Slack, Jira natively |
| Contract flexibility | 2.8 | Annual commit required; no monthly billing |
| **Composite** | **3.73** | |

## Contract Details

- **Plan:** Business
- **Users:** 210
- **Annual cost:** $126,000 ($600/user/yr)
- **Contract expiry:** 2025-07-31

## Cost Reduction Opportunities

SRE team reviewed PagerDuty user roster. Findings:
- ~40 users are "stakeholder" accounts receiving notifications only — these could move to a free observer role.
- 15 accounts are for offboarded employees (IT provisioning gap).
- Net: could reduce paid seats by ~55, saving approximately $33,000/yr.

## Alternative: Grafana OnCall

Grafana OnCall is included in our Grafana Cloud contract at no additional cost. SRE team prototyped a migration last quarter. Gap identified: escalation policy complexity and missing mobile app polish. SRE is not ready to migrate this cycle, but consensus is to re-evaluate in 12 months.

See `../evaluations/oncall-tools-comparison.md` for the detailed analysis.

## Renewal Recommendation

Renew for 1 year (not 2), with seat reduction to 155. Revisit after Grafana OnCall pilot in 2025.
