# Datadog Vendor Scorecard

**Review period:** Q3 2024  
**Reviewer:** Priya Nair, Finance  
**Classification:** Confidential

## Scoring Summary

| Category | Weight | Score (1–5) | Weighted |
|----------|--------|-------------|----------|
| Price competitiveness | 25% | 3.2 | 0.80 |
| Feature coverage | 30% | 4.5 | 1.35 |
| Support quality | 20% | 3.8 | 0.76 |
| Contract flexibility | 15% | 2.9 | 0.44 |
| Vendor stability | 10% | 4.0 | 0.40 |
| **Total** | | | **3.75** |

## Contract Details

- **Annual spend:** $580,000
- **Seats / hosts licensed:** 1,400 hosts
- **Contract end:** 2025-08-31
- **Renewal window opens:** 2025-05-01

## Notes from Engineering

Datadog APM is deeply integrated — migration cost is non-trivial. Infra team estimates a 6-month effort to switch to Grafana Cloud. That context should inform any negotiation leverage claim.

Log indexing costs grew 34% YoY primarily due to verbose application logging from the recommendations service. Eng committed to a retention-policy change in Q4 that should reduce indexed log volume by ~20%.

## Negotiation Priorities for Renewal

1. Push for host-based to usage-based pricing model
2. Request 15% discount given 3-year commitment
3. Negotiate SLA for support response time (currently 4-hour, want 1-hour)
4. Clarify data residency guarantees for EU hosts

## Recommendation

Renew with a 2-year term contingent on pricing concessions. Escalate to VP Finance if discount floor isn't met.

See also: `../evaluations/observability-tools-eval.md`
