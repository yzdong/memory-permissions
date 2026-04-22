# Data Retention Schedule

**Owner:** Data Governance Team  
**Last Updated:** 2024-03-20  
**Classification:** Internal

## Overview

This schedule defines how long specific categories of data must be retained and when they must be deleted or archived. Retaining data longer than necessary increases legal exposure and storage costs; deleting it too early may violate regulatory obligations.

All teams responsible for data stores should review this document and confirm alignment at least once per year. Open a ticket in Jira under `COMPLIANCE` project to record your review.

## Retention Categories

### Customer Data

| Data Type | Retention Period | Legal Basis | Disposal Method |
|-----------|-----------------|-------------|----------------|
| PII (names, emails) | 3 years post-churn | GDPR Art. 17 | Cryptographic erasure |
| Transaction records | 7 years | SOX, local tax law | Secure archive then delete |
| Support tickets | 2 years | Legitimate interest | Automated purge |
| Usage telemetry (anonymized) | 5 years | Analytics | Standard deletion |

### Employee Data

| Data Type | Retention Period | Notes |
|-----------|-----------------|-------|
| Payroll records | 7 years post-departure | Required by FLSA and state law |
| Performance reviews | 3 years | HR discretion beyond 3 years |
| Background check results | Duration of employment + 1 year | FCRA |
| Access logs | 2 years | Security audit trail |

### System & Security Logs

- Application logs: **90 days** hot, **1 year** cold archive
- Audit logs (privileged access): **3 years** — do not delete early
- Network flow records: **6 months**
- Vulnerability scan reports: **2 years**

## Deletion Process

1. Identify datasets approaching end-of-retention via the `scripts/retention-scanner.py` tool
2. Confirm no legal hold is active (check with Legal before proceeding)
3. Execute deletion using approved tooling; log the action in the Data Governance tracker
4. For cloud data, verify deletion across all regions including backups

## Legal Holds

When litigation is reasonably anticipated, normal retention schedules are suspended for affected data. Legal will issue a Legal Hold Notice (LHN). Do **not** delete data subject to a hold.

See `../legal/legal-hold-procedures.md` for the full process.

## Related Documents

- `acceptable-use-policy.md`
- `third-party-risk-policy.md`
- `../privacy/privacy-impact-assessment-template.md`
