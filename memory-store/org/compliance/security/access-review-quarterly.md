# Quarterly Access Review Procedure

Owner: Security Engineering  
Cadence: Every 13 weeks (roughly calendar-quarter-aligned)  
Last completed: 2024-Q4  
Next due: 2025-Q1

## Why We Do This

Regulatory frameworks we're bound by (SOC 2 Type II, ISO 27001 annex A.9) require periodic review of who has access to what. We've found real over-provisioned accounts every single quarter — don't skip this.

## Scope

- All production AWS accounts
- GitHub org membership and team assignments
- Okta application assignments
- Database direct-access grants (Postgres, Redis)
- Any service account with >read permissions

## Steps

### 1. Pull current access snapshots

```bash
# AWS IAM
python scripts/access_review/dump_iam.py --output reports/iam-$(date +%Y%m%d).csv

# GitHub
gh api /orgs/our-org/members --paginate > reports/gh-members-$(date +%Y%m%d).json

# Okta — use the Okta admin console export or the script:
python scripts/access_review/dump_okta.py
```

### 2. Compare against HR roster

HR exports a CSV of active employees. Any account not in that list is flagged for removal unless there's an approved exception in `access-exceptions.md`.

### 3. Review privileged roles specifically

For any account with admin/owner/superuser roles, get explicit manager sign-off in the review ticket.

### 4. Remediate

- Deactivate terminated-employee accounts within **24 hours** of flag.
- Downscope over-provisioned accounts within **5 business days**.
- Document exceptions with a linked Jira ticket and expiry date.

### 5. Archive results

Commit the final report to `reports/access-review/YYYY-QN/` and close the tracking ticket.

## Roles & Contacts

| Role | Team |
|---|---|
| Review coordinator | Security Eng |
| AWS account owners | Platform Infra |
| GitHub org admin | DevEx |
| Okta admin | IT/Ops |

## Related

- `saml-sso-runbook.md` — SSO configuration details
- `secrets-rotation-schedule.md` — service account credential rotation
