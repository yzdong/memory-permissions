# Security Audit Preparation Playbook

We go through external security audits annually. This playbook covers how Platform prepares our scope of the audit without scrambling at the last minute.

## Timeline

Start 8 weeks before the audit kickoff date.

| Week | Activity |
|------|----------|
| -8   | Confirm scope with Security team; identify new systems since last audit |
| -6   | Evidence collection begins |
| -4   | Internal pre-audit review |
| -2   | Evidence package delivered to auditors |
| 0    | Audit kickoff |

## Scope confirmation

Work with Security to confirm which systems are in scope. Platform typically covers:
- Deploy pipeline and CI/CD tooling
- Secrets management (Vault)
- Network controls (VPC, security groups, NACLs)
- IAM structure and privilege access management
- Kubernetes cluster configuration

## Evidence collection

### Access control
- Export IAM role and policy inventory: `./scripts/iam-report.sh > evidence/iam-inventory.json`
- Privileged access list with business justification for each account
- Access review records (we do quarterly reviews; confirm last one is documented in `access-reviews/`)

### Change management
- Sample of recent Terraform PRs showing approval process
- Deploy pipeline config showing required approvals before production
- Evidence of change window enforcement

### Encryption
- Confirm all S3 buckets have default encryption (our config check: `./scripts/s3-encryption-audit.sh`)
- RDS encryption at rest — screenshot or API output
- TLS versions in use for all public-facing endpoints

### Vulnerability management
- Container image scan results from the past 90 days (exported from our CI output)
- Evidence of patch cadence for base OS images

## Internal pre-audit review

Run a tabletop with Platform lead and at least two engineers:
- Walk through each evidence item: is it accurate? Is it complete?
- Are there known gaps? Better to know now than during the audit
- Check that contact info for auditor questions is current

## Common failure modes
- Evidence that's technically accurate but unclear — auditors will ask follow-up questions for everything that needs interpretation. Add context notes.
- Stale access review records — do the review, don't back-date it
- Inconsistency between policy docs and actual config — fix the config, update the doc, or both
