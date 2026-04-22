# Slack Vendor Review

**Date:** 2024-10-01  
**Owner:** Finance — SaaS Portfolio  
**Classification:** Confidential

## Current Contract

- **Tier:** Slack Business+
- **Seats:** 2,300 (purchased) / ~1,950 (active MAU)
- **Annual cost:** $244,000
- **Cost per active user/yr:** ~$125 (effective)
- **Contract expiry:** 2025-04-30

## Utilization Concern

We're paying for ~350 seats above actual active usage. This has been a recurring gap since the 2022 contract. IT Ops hasn't implemented automated seat reclamation — tracked in `jira/IT-4421`.

Recommendation: Before next renewal, run the Okta + Slack reconciliation report to identify dormant accounts. Estimated recoverable savings: $43,750/yr.

## Vendor Sentiment

Slack (Salesforce) has been moderately flexible in past renewals. They applied a 7% increase on our last renewal despite industry benchmarks suggesting 3–4% for our volume tier. We pushed back and settled at 4%. Same tactic likely viable this cycle.

## Competitive Landscape

| Option | Cost/seat/yr | Migration Risk |
|--------|-------------|----------------|
| Slack Business+ | $106 | — (incumbent) |
| Microsoft Teams | ~$72 (bundled) | High (culture) |
| Google Chat | ~$60 (bundled) | Moderate |

Migration to Teams would save ~$78K/yr but would require significant change management. Not recommended this cycle.

## Action Items

- [ ] IT Ops: run seat reconciliation before 2025-01-15
- [ ] Finance: open renewal discussion by 2025-02-01
- [ ] Legal: review DPA for Slack AI data handling

## Next Review Date

2025-02-15
