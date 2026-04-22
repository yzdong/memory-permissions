# Access Control Rules — Platform Team

Platform manages access to production infrastructure. Access is a liability; treat it like one.

## Principle of Least Privilege

Everyone — including Platform team members — gets the minimum access needed for their current role. Write access to production is not a perk.

## Access Tiers

| Tier | What it includes | Who has it |
|------|-----------------|------------|
| Read-only prod | Logs, metrics dashboards, k8s describe | All engineers |
| Deploy access | Trigger deploys via pipeline | All engineers (through pipeline only — no direct kubectl apply) |
| Platform infra write | Terraform apply, cluster admin | Platform team members |
| Break-glass prod | Direct DB access, manual k8s edits | Platform lead + on-call only, requires audit log |

## Requesting Access

- For read-only or deploy: self-serve via the internal access portal
- For platform infra write: open a ticket in `PLATACCESS` Jira project, approved by platform lead
- For break-glass: contact platform on-call directly; it's logged automatically in Vault audit

## Access Reviews

- **Quarterly**: Platform lead audits all Tier 3 and Tier 4 access holders
- **Offboarding**: Access revoked same day HR submits the offboarding ticket (automated)
- **Role change**: Previous access revoked within 5 business days

## Service Account Rules

- Every service account must have a named human owner (tracked in `infra/service-accounts/owners.yaml`)
- Service accounts must not have interactive login enabled
- Credentials rotate per the schedule in `secrets-handling.md`

## Shared Accounts

Prohibited. If you find one, file a `PLATACCESS` ticket and ping platform on-call.

## Audit

All Tier 3 and Tier 4 actions are logged to the SIEM with 90-day retention. Logs are reviewed automatically for anomalies; unusual patterns page the security rotation.

## Related

- `secrets-handling.md`
- `on-call-rotation.md`
- `infra/service-accounts/owners.yaml`
