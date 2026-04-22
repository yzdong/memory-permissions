# Stripe Vendor Profile

**Last Updated:** 2024-11-10  
**Owner:** Finance / Payments  
**Classification:** Confidential — Revenue Sensitive

## Overview

Stripe is our primary payment processor, handling subscription billing, one-time payments, and connect payouts for marketplace transactions.

## Processing Volume & Cost

| Period | GMV Processed | Effective Rate | Total Fees |
|--------|--------------|----------------|------------|
| 2022   | $18.2M       | 2.41%          | $438,000   |
| 2023   | $26.4M       | 2.28%          | $602,000   |
| 2024E  | $34.1M       | 2.19%          | $747,000   |

Effective rate is declining as volume grows — Stripe gives volume discounts, but we are still above the negotiated rate floor available to us based on a competing proposal from Adyen.

## Products in Use

- **Stripe Payments:** Core processing
- **Stripe Billing:** Subscription lifecycle management for ~14,000 active subscriptions
- **Stripe Radar:** Fraud detection (included, no add-on cost)
- **Stripe Sigma:** Data querying — $750/month — used by Finance for revenue reconciliation
- **Stripe Connect:** Used for marketplace payouts; ~600 connected accounts

## Fraud & Chargebacks

- Chargeback rate: 0.41% of transactions (Stripe's threshold alert: 0.75%)
- Radar block rate: 1.8% of attempted transactions
- Notable: Q2 2024 had a fraud spike in the EU — Radar rules were updated; dispute rate returned to baseline by Q3

## Rate Negotiation Status

Adyen proposal received: ~2.05% effective rate at our current volume with a $25K implementation fee. Stripe has been informed. Stripe's counter: 2.12% if we sign a 2-year exclusivity commitment.

Finance's view: Don't take exclusivity. Use Adyen quote as leverage to get Stripe below 2.15% without commitment. Target outcome by end of Q4 2024.

## Related

- `../contracts/stripe-msa-2022.pdf` (restricted)
- `runbooks/payment-reconciliation.md`
