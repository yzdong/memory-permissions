# Datadog Contract Renewal Notes

**Status:** Renewal in progress  
**Owner:** Tom Reyes (Finance)  
**Current Term Ends:** 2026-03-31  
**Vendor Contact:** Jamie Ortiz, Datadog Enterprise Sales  
**Last Updated:** 2025-12-02

## Background

We've been on Datadog since 2022. Current contract is a 2-year term signed March 2024. Usage has grown significantly — we're ~30% over our committed host count and burning overages at the per-host rate.

## Current Contract Snapshot

- **Hosts committed:** 180
- **Actual avg. hosts (trailing 90d):** ~235
- **APM hosts:** 60 committed, ~80 in use
- **Log ingestion:** 120 GB/day committed; averaging 175 GB/day
- **Overage rate:** Standard list price — needs to be renegotiated

## Renewal Options Under Discussion

1. **Option A — Expand and lock:** Commit to 280 hosts + 100 APM + 200 GB/day logs for 2 years. Vendor is offering 22% discount off list.
2. **Option B — Shorter term:** 1-year renewal at current commit + 10% buffer. Less discount (~14%) but more flexibility.
3. **Option C — Evaluate alternatives:** Grafana Cloud and New Relic have both been flagged by the Platform team. Would require 60-day migration effort (rough estimate from infra).

## Recommendation

Lean toward Option A if Datadog will sharpen the discount to 24%+. The migration cost for Option C likely outweighs savings in the 1-year window. Get legal to review auto-renewal language — prior contract had a 60-day notice window that we nearly missed.

## Redlines to Push

- Remove automatic price escalation clause (currently 7% YoY)
- Add usage credit carry-forward for any month under committed volume
- Cap overage rate at 80% of committed per-unit price, not list

## Next Steps

- [ ] Tom to send counter-proposal by 2026-01-10
- [ ] Legal review of draft by 2026-01-20
- [ ] Executive sign-off needed from CFO if TCV > $500K
- [ ] Reference `../budget.md` for headcount vs. tooling spend trade-off context

## Related Files

- `datadog-renewal-redlines-v2.docx` (SharePoint, Finance/Contracts)
- `../vendor-review-schedule.md`
