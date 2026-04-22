# Jira & Confluence Spend Profile

**Last Updated:** 2024-10-28  
**Owner:** Finance / Engineering Operations  
**Classification:** Confidential

## Overview

Atlassian products (Jira Software, Confluence, Jira Service Management) are the backbone of engineering project management and internal documentation.

## License Breakdown

| Product                 | Users | Annual Cost |
|-------------------------|-------|-------------|
| Jira Software (Cloud)   | 420   | $126,000    |
| Confluence (Cloud)      | 420   | $84,000     |
| Jira Service Management | 35    | $52,500     |
| Atlassian Access (SSO)  | 420   | $42,000     |
| **Total**               |       | **$304,500**|

## Pricing Model Notes

Atlassian Cloud pricing is tiered by user band. We're currently in the 201-500 band. At 501 users, we jump to the next tier with a ~15% per-user increase. **This is a hard threshold to watch** — we're 80 users away.

## Usage Reality Check

- Jira: 378 of 420 users active in last 60 days (90%)
- Confluence: 291 of 420 users active (69%) — Confluence adoption is soft; some teams use Notion instead
- JSM: 35 agents, all active; support ticket volume healthy

## Atlassian Access

Access is required for SAML SSO through Okta. It's not optional given our security requirements. Cost is $8/user/month at 420 users.

## Consolidation Opportunity

If we standardized documentation on Confluence and eliminated Notion (currently ~$28K/yr for ~200 users), we'd net roughly flat after the Confluence seat bump. Proposal is in `../evaluations/documentation-platform-consolidation.md` — not yet approved.

## OpsGenie

We have an OpsGenie Standard license (180 users, $54,000/yr) evaluated separately in context of PagerDuty renewal — see `pagerduty-scorecard.md`.

## Renewal

- Atlassian Cloud is annual, auto-renews February 2025
- Atlassian doesn't negotiate much at our scale — pricing is what it is
- One lever: reduce Confluence seats to active users (say 300) and right-size Atlassian Access accordingly
