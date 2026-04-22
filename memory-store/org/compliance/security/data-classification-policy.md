# Data Classification Policy

Owner: Security Engineering + Legal
Approved: 2024-09
Next review: 2025-09

This document defines how we classify data at rest and in motion. Rules for handling PII specifically live in `../pii-handling.md` — don't look here for those.

## Classification Levels

### Critical

Exposure would cause severe harm to users, the company, or both. Examples: private keys, password hashes, payment card data, OAuth tokens.

Controls required:
- Encryption at rest (AES-256) and in transit (TLS 1.2+)
- Access limited to specific roles; no broad group grants
- Audit log on every read and write
- Cannot leave production environment in plaintext — ever

### High

Exposure would cause significant harm but is recoverable. Examples: email addresses, internal financial data, HR records, security findings.

Controls required:
- Encryption at rest and in transit
- Role-based access with quarterly review (see `access-review-quarterly.md`)
- Audit log on writes; read logging encouraged

### Medium

Exposure is embarrassing or mildly harmful. Examples: internal project names, non-public roadmaps, vendor contract terms.

Controls required:
- Not publicly accessible
- Reasonable access controls (Okta group gates are sufficient)
- No special logging requirement

### Low / Public

Intentionally public or effectively harmless if leaked. Examples: marketing copy, open-source code, published blog posts.

No special controls required.

## Tagging

All Snowflake tables must have a `sensitivity` tag applied:

```sql
ALTER TABLE analytics.users SET TAG governance.sensitivity = 'high';
```

S3 buckets must have a `DataClassification` resource tag. Untagged buckets trigger an alert in our AWS Config rules within 1 hour.

## Handling in Code

- Log lines **must not** contain Critical or High fields. Use the `scrub()` helper in `libs/logging`.
- API responses **must** strip fields the calling role isn't entitled to — never return and filter on the client.
- When in doubt, classify higher and ask Security Eng to review.

## Violations

Report suspected misclassification or exposure to #security-alerts or security@example.org. Violations are tracked in the SEC Jira project.
