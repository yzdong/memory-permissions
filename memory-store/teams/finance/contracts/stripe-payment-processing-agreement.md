# Stripe Payment Processing Agreement

**Status:** Active  
**Agreement Type:** Stripe Services Agreement (standard) + custom rate addendum  
**Rate Addendum Signed:** 2024-09-01  
**Owner:** Tom Reyes  
**Stripe Account Manager:** Riley Chu

## Overview

Stripe is our primary payment processor for all customer-facing revenue (subscription billing and one-time purchases). The standard Stripe Services Agreement governs; we negotiated a custom rate addendum based on volume.

## Rate Structure (Custom Addendum)

| Transaction Type | Rate |
|---|---|
| US card (not present) | 2.1% + $0.30 |
| International card | 2.7% + $0.30 |
| ACH Debit | 0.75%, max $5.00 |
| Stripe Billing (subscription management) | Included |
| Stripe Radar (fraud, standard) | Included |
| Stripe Radar (custom rules) | +$0.04/transaction |

List rates for our volume tier would be 2.7% + $0.30 for US cards — the addendum represents meaningful savings.

## Key Terms

- Stripe may update rates with 30 days notice; we have right to terminate within that window if rates increase
- Dispute/chargeback fee: $15 per dispute (not negotiable per Stripe standard policy)
- Funds settlement: 2-business-day rolling (standard)
- PCI compliance: Stripe maintains PCI DSS Level 1; our obligations limited to SAQ A if using Stripe.js

## Volume Commitment

There is no hard volume commitment in the addendum. Stripe indicated informally that custom rates are reviewed annually; if volume drops significantly, rates may revert. Flag to Finance if GMV trends down more than 20% QoQ.

## Annual Review

- Schedule review with Riley by 2025-08-01 each year
- Pull processing fee report from Stripe Dashboard (Finance access only) and compare effective rate to addendum rate
- Explore ACH promotion to reduce card transaction mix

## Open Items

- [ ] Evaluate Stripe Tax for sales tax compliance (currently using Avalara)
- [ ] Review chargeback rate — if > 0.5% of transactions, flag to Risk
- [ ] Confirm 3DS2 enforcement settings with Engineering
