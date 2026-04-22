# FX Hedging Policy

**Owner:** Treasury / Finance  
**Classification:** Confidential  
**Last Reviewed:** 2025-08-30  
**Next Review:** 2026-08-30

---

## Scope

This policy governs how the company manages foreign currency exposure arising from:

- International revenue contracts denominated in non-USD currencies
- Vendor and payroll obligations in foreign currencies
- Intercompany transactions across subsidiaries

## Hedging Objectives

Our goal is **not** to profit from currency movements. Hedging is strictly a risk-reduction tool. Target outcomes:

- Reduce earnings volatility from FX fluctuations to below **8%** of operating margin variance
- Protect against adverse moves of > **10%** in any single currency pair over a rolling 90-day window

## Eligible Instruments

The treasury team may use the following instruments only:

- **Forward contracts** — preferred instrument for predictable cash flows
- **Vanilla options (puts/calls)** — for uncertain cash flow timing
- **Cross-currency swaps** — for intercompany loan exposures > $5M USD equivalent

Exotic derivatives, structured products, and speculative positions are **prohibited**.

## Hedge Ratios by Exposure Type

| Exposure Type | Hedge Ratio Target | Tenor |
|---|---|---|
| Contracted revenue (firm) | 70–90% | Up to 12 months |
| Forecasted revenue (probable) | 40–60% | Up to 6 months |
| Vendor payables | 50–80% | Up to 3 months |
| Payroll obligations | 90–100% | Rolling 2-month |

## Governance & Authorization

- All hedging transactions must be approved by the **Treasurer** and documented in the FX log (maintained in `../treasury/fx-transaction-log.xlsx`).
- Transactions above $2M USD equivalent require **CFO co-approval**.
- Hedge positions are reviewed monthly by the Finance Leadership Team.
- No individual trader or analyst may execute hedges unilaterally.

## Counterparty Requirements

Only banks with a credit rating of **A- or above** (S&P) or equivalent are eligible counterparties. Current approved counterparties are listed in `../treasury/approved-counterparties.md`.

## Reporting

- Monthly mark-to-market report delivered to CFO and Finance VP by the 5th business day of each month.
- Quarterly summary included in Board Finance package.

## Related Documents

- `../treasury/approved-counterparties.md`
- `../treasury/fx-transaction-log.xlsx`
- `invoice-approval-chain.md`
