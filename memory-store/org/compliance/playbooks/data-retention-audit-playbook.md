# Data Retention Audit Playbook

## Purpose

Verify that we are actually deleting data we committed to deleting, on the schedule in our retention policy. This is required for SOC 2, GDPR accountability, and just basic hygiene. Last time we skipped this, we found customer email addresses in a log bucket from three years prior — not a good look.

## Frequency

- Full audit: annually (aligned with SOC 2 audit prep)
- Spot-check: quarterly for high-risk data stores (those containing PII or PHI)

## Data Stores in Scope

| System | Retention Policy | Owner |
|---|---|---|
| Prod PostgreSQL | Per data class (see policy) | Engineering |
| Data warehouse (BigQuery) | 24 months for raw events | Data Engineering |
| Application logs (GCS) | 90 days | Platform Engineering |
| Backups | 1 year; encrypted | IT / Infra |
| Email archive | 3 years | IT |
| Support tickets (Zendesk) | 5 years | Customer Success |
| Candidate records (Greenhouse) | Jurisdiction-dependent | HR / Legal |

## Audit Steps

### 1. Inventory Data Stores
- Pull current list from `../assets/data-inventory.csv`
- Confirm no new stores added without retention classification (Engineering should notify Compliance on new data stores — check Jira project `DSGOV`)

### 2. Verify Automated Deletion Jobs

```sql
-- Example: check last run of deletion job in audit log table
SELECT job_name, last_run_at, records_deleted, status
FROM retention_job_audit_log
WHERE last_run_at < NOW() - INTERVAL '8 days'
ORDER BY last_run_at ASC;
```

- Any job not run in the last 7 days → page the owning team immediately
- Spot-check that deleted records are actually gone (query for records beyond retention window)

### 3. Check Legal Holds
- Pull current hold list from Legal (`../legal/active-holds.md`)
- Confirm deletion jobs respect hold flags — records under legal hold must not be auto-deleted

### 4. Third-Party Deletion Verification
- For DSR erasures processed in the past quarter, sample 10 requests and confirm deletion was propagated to sub-processors
- Request deletion confirmation emails from vendors and attach to audit ticket

### 5. Document Findings
- Any data found beyond its retention window: severity, root cause, remediation with owner and date
- Green/yellow/red status per data store
- Evidence package to `gs://compliance-vault/retention-audits/<year>/`

## What Gets Reported

- Executive summary to CISO and CPO
- Detailed findings to system owners
- Material gaps escalated to Legal and DPO

## References

- `gdpr-data-subject-request.md`
- `ccpa-consumer-rights-playbook.md`
- `../policies/data-retention-policy.md`
- `../assets/data-inventory.csv`
