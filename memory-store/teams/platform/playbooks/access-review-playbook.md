# Quarterly Access Review Playbook

Platform runs the infra access review as part of our security posture. We coordinate with the Security team but own the execution.

## Scope

- AWS IAM users and roles (production accounts only)
- Bastion host access (SSH public keys)
- PagerDuty admin access
- Terraform state S3 bucket access
- Datadog admin users

## Schedule

Reviews happen within the first 3 weeks of each quarter. The Security team sends a compliance reminder; we should not need that reminder — calendar it.

## Step 1: Export Current Access

```bash
# AWS
python scripts/access/export-iam-report.py \
  --accounts prod,prod-data,prod-shared \
  --output reports/iam-access-$(date +%F).csv

# Bastion keys
python scripts/access/export-bastion-keys.py > reports/bastion-keys-$(date +%F).txt
```

## Step 2: Cross-Reference with HR Data

The People team exports a CSV of active employees weekly to `s3://internal-hr-exports/active-employees-latest.csv`. Any IAM user or bastion key belonging to someone NOT in that export is suspect.

Automated check:
```bash
python scripts/access/cross-ref-hr.py \
  --iam-report reports/iam-access-$(date +%F).csv \
  --hr-export s3://internal-hr-exports/active-employees-latest.csv \
  --output reports/access-gaps-$(date +%F).csv
```

## Step 3: Privilege Review

For each identity with AdministratorAccess or PowerUserAccess:
- Confirm the role is still necessary
- Check last-used date — if > 60 days, flag for removal or downgrade
- `aws iam generate-service-last-accessed-details` is your friend

## Step 4: Remediation

For departed employees: immediate revocation, no grace period.
For active employees with excess privilege: 5-business-day notice before downgrade, giving them a chance to raise a legitimate need.

All removals logged in `reports/access-removals-YYYY-Qn.md`.

## Step 5: Sign-Off

The completed access report (with remediation summary) goes to:
1. Platform lead (technical review)
2. Security team (compliance sign-off)
3. Stored in `s3://platform-compliance/access-reviews/`

## Things That Always Come Up

- Service accounts with human-style names: confirm they're actually non-human
- Old CI/CD machine users from deprecated pipelines — clean these up aggressively
- Roles assumed cross-account that aren't documented — add them to `docs/cross-account-roles.md` or remove them
