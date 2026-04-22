# Access Exceptions Register

This file documents approved deviations from our standard access controls. Every entry requires:
- A business justification
- An expiry date (no indefinite exceptions)
- An approving manager
- A linked Jira ticket

Security Engineering reviews this file as part of the quarterly access review. See `access-review-quarterly.md`.

## Current Exceptions

### EXC-001 — Direct DB Access: Analytics Team

| Field | Value |
|---|---|
| Granted to | @priya, @dan-w (Analytics) |
| Resource | `prod-replica.db.internal` read-only role |
| Justification | BI tooling doesn't support Vault credential brokering yet. Migration planned for Q2. |
| Approved by | @vp-engineering |
| Expires | 2025-06-30 |
| Ticket | SEC-312 |

### EXC-002 — Non-SSO Auth: Legacy CRM

| Field | Value |
|---|---|
| Granted to | All CRM users (~14 people) |
| Resource | `crm.legacy.internal` (SugarCRM instance) |
| Justification | SugarCRM SAML integration is broken upstream; vendor fix ETA Q3. |
| Approved by | @ciso |
| Expires | 2025-09-01 |
| Ticket | SEC-389 |
| Compensating control | VPN required to reach the service; MFA enforced at VPN layer. |

### EXC-003 — Cross-Account IAM Role: ML Training

| Field | Value |
|---|---|
| Granted to | `ml-training-prod` service role |
| Resource | `s3://raw-data-lake` in `data-prod` AWS account |
| Justification | Cross-account S3 access needed for training jobs; no alternative until data mesh migration completes. |
| Approved by | @head-of-ml |
| Expires | 2025-08-15 |
| Ticket | SEC-421 |

## Requesting a New Exception

1. Open a Jira ticket in the `SEC` project with label `access-exception`.
2. Fill in all fields from the table above.
3. Security Engineering will respond within 5 business days.
4. Approved exceptions are added here by Security Engineering — do not self-merge.

## Expired Exceptions (to be cleaned up)

_Move entries here once expired; delete after confirming the access is revoked._

| EXC | Description | Expired | Revoked |
|---|---|---|---|
| EXC-098 | Contractor direct S3 access | 2024-09-01 | ✅ 2024-09-03 |
