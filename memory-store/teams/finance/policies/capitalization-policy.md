# Capitalization Policy

**Owner:** Accounting  
**Last Updated:** 2025-07-22  
**Standard Reference:** ASC 350 (internal-use software), ASC 360 (property, plant & equipment)

---

## Why This Matters

Miscategorizing capital expenditures as operating expenses (or vice versa) directly affects our income statement, balance sheet, and tax position. When in doubt, ask Accounting before the purchase — not after.

## Capitalization Thresholds

| Asset Type | Capitalize If Cost ≥ | Useful Life |
|---|---|---|
| Computer hardware | $2,500 | 3 years |
| Furniture & fixtures | $3,000 | 7 years |
| Leasehold improvements | $5,000 | Lease term |
| Purchased software licenses (perpetual) | $3,000 | 3–5 years |
| Internally developed software | $5,000 (per project phase) | 3 years |

Amounts below these thresholds are **expensed immediately** in the period incurred.

## Internally Developed Software (IDS)

This is the most frequently misapplied area. Costs are capitalized only during the **application development stage** — not during preliminary design or post-implementation.

**Capitalizable costs:**
- Direct labor (engineering time coding the new capability)
- Third-party development fees tied to a specific deliverable

**Not capitalizable:**
- Bug fixes and maintenance
- Training costs
- Research / proof-of-concept work
- General overhead or team management time

Engineering teams are asked to log hours by project phase in Jira. Finance and Engineering leads review IDS capitalization quarterly.

## How to Flag a Potential Capital Purchase

1. Before submitting a PO or contract above $2,500, email `accounting@company.internal` with: item description, vendor, total cost, expected useful life.
2. Accounting responds within 2 business days with a CapEx/OpEx determination.
3. The determination is logged and attached to the invoice in Ramp.

## Depreciation Method

All fixed assets use **straight-line depreciation** with no salvage value unless otherwise documented. Accelerated depreciation requires CFO approval.

## Disposals and Write-Offs

Assets disposed of or written off must be reported to Accounting within the same month. See `../accounting/asset-disposal-form.md` for the process.

## Related Documents

- `../accounting/asset-disposal-form.md`
- `invoice-approval-chain.md`
- `budget-amendment-process.md`
