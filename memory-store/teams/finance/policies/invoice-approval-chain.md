# Invoice Approval Chain

**Owner:** Accounts Payable / Finance Operations  
**Last Updated:** 2025-10-22  
**Applies To:** All vendor invoices payable by the company

---

## Guiding Principle

Every invoice needs a human who can confirm the work was done, the amount is correct, and the vendor is legitimate. The chain below is designed to minimize bottlenecks while maintaining audit integrity.

## Approval Thresholds

| Invoice Amount (USD) | Required Approvers |
|---|---|
| < $500 | Budget owner (self-serve in Ramp) |
| $500 – $4,999 | Budget owner + Manager |
| $5,000 – $49,999 | Budget owner + Manager + Finance Business Partner |
| $50,000 – $249,999 | Above + VP of Finance |
| $250,000+ | Above + CFO |

## PO-Backed Invoices

Invoices referencing an approved Purchase Order (PO) with sufficient remaining balance skip the standard chain and route directly to AP for matching. Three-way match (PO → receipt → invoice) is required.

If the invoice exceeds the PO by more than **5%** or **$500** (whichever is smaller), it falls back into the standard approval chain for the delta amount.

## How to Submit an Invoice for Approval

1. Vendor sends invoice to `ap@company.internal` or uploads via the Ramp vendor portal.
2. AP team codes the invoice to the correct GL account and cost center.
3. Approval request is routed automatically based on the thresholds above.
4. Approvers receive a Slack notification in `#ap-approvals` and an email.
5. Payment is batched and processed on **Tuesdays and Thursdays** (ACH) or last business day of the month (wire).

## SLA Commitments

- AP acknowledges receipt within **1 business day**.
- Standard payment terms: **Net 30** unless contract specifies otherwise.
- Expedited payment (Net 5 or Net 10) requires Finance VP approval and a written justification from the requesting team.

## Common Rejection Reasons

- Missing PO reference when one is required
- Invoice date more than 180 days in the past
- Vendor not in approved vendor registry (`../procurement/approved-vendors.md`)
- Duplicate invoice number

## Related Documents

- `corporate-card-issuance.md`
- `../procurement/approved-vendors.md`
- `../procurement/vendor-onboarding.md`
