# Financial Controls Overview

**Owner:** Finance & Internal Audit  
**Classification:** Confidential  
**Last Updated:** 2025-10-15

---

## Purpose

This document summarizes the key internal controls the Finance team maintains to ensure accuracy of financial reporting, prevent fraud, and support external audit readiness. It is not a substitute for the full controls matrix (maintained in `../audit/controls-matrix-fy2025.xlsx`).

## Control Categories

### 1. Segregation of Duties

- No single employee may both **initiate and approve** a payment.
- Employees who can create vendors in our ERP cannot also approve payments to those vendors.
- The payroll team has read-only access to Finance dashboards; they cannot post journal entries.

### 2. Authorization Controls

All transactions above defined thresholds require multi-party approval. See `invoice-approval-chain.md` for specifics. Authorization matrices are reviewed annually by Internal Audit.

### 3. Reconciliation Controls

| Account Type | Reconciliation Frequency | Owner |
|---|---|---|
| Bank accounts | Daily (automated) + monthly sign-off | Treasury |
| AR aging | Weekly | Revenue Ops |
| AP subledger | Monthly | AP Manager |
| Intercompany | Monthly | Consolidations team |
| Fixed assets | Quarterly | Accounting |

### 4. System Access Controls

- ERP access is provisioned via IT on Finance approval; access reviews run **quarterly**.
- Terminated employees are deprovisioned within **4 hours** of HR confirming offboarding.
- Finance systems are excluded from self-service IT provisioning.

### 5. Exception Reporting

The following automated reports run weekly and are reviewed by Finance Ops:

- Invoices approved by the same person who created the vendor record
- Payments to vendors added within the last 30 days
- Expense reports with no receipts over $25
- Transactions posted outside of business hours

## Audit Readiness

We target a **clean opinion** from external auditors with zero material weaknesses. Any control deficiency identified internally must be logged in the audit tracker and remediated within 60 days (significant) or 90 days (other).

## Related Documents

- `../audit/controls-matrix-fy2025.xlsx`
- `invoice-approval-chain.md`
- `expense-policy-2026.md`
- `corporate-card-issuance.md`
