# GitHub Enterprise — Spend Profile

**Period:** FY2024  
**Owner:** Finance / Engineering Tooling  
**Classification:** Confidential

## License Summary

- **Product:** GitHub Enterprise Cloud
- **Seat count:** 680
- **Annual cost:** $163,200 ($240/seat/yr)
- **Contract term:** 2024-09-01 — 2025-08-31
- **Renewal owner:** Engineering VP + Finance

## Additional Products & Spend

| Product | Annual Cost | Notes |
|---------|-------------|-------|
| GitHub Advanced Security | $48,960 | 204 committer seats |
| GitHub Copilot Business | $38,400 | 160 seats, growing |
| Actions compute (overage) | ~$11,000 | Billed monthly; inconsistent |

**Total GitHub annual spend:** ~$261,560

## Copilot Expansion Notes

Eng leadership wants to expand Copilot to all 680 developers. At current pricing that's $204,000/yr incremental — a significant jump. Finance is requesting productivity data before approving. See `../evaluations/copilot-roi-analysis.md` for the draft model.

## Actions Spend

Actions compute overages are inconsistently tracked. Spike in August traced to a misconfigured CI pipeline running redundant test suites. Infra team has since added a concurrency cap. Expected overages going forward: ~$4,000–6,000/mo.

## Negotiation Notes

- GitHub (Microsoft) offered a 5% multi-year discount for a 3-year commit. Legal is reviewing lock-in implications.
- Competitor: GitLab Ultimate at ~$99/user/yr. Migration effort estimated at 9 months minimum — not realistic this cycle.

## Open Actions

- [ ] Eng tooling: audit inactive Enterprise seats (last login > 90 days) by 2024-12-01
- [ ] Finance: model Copilot full-rollout NPV scenario
- [ ] Legal: respond to GitHub's 3-year term proposal
