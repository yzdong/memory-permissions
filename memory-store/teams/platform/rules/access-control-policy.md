# Access Control Policy — Platform Team

Platform manages access to infra systems. This document covers how access is granted, reviewed, and revoked.

## Principle of Least Privilege

Every service account and human user should have exactly the permissions needed to do their job — nothing more. If you're not sure what's needed, start minimal and expand.

## Access Request Process

1. Open a ticket in Jira (project: `PLAT`) using the "Access Request" template.
2. Specify: system, permission level, business justification, and duration.
3. A Platform Lead approves or denies within 2 business days.
4. Access is provisioned via Terraform — no manual IAM or RBAC changes.

## Access Levels

| Level | Description |
|-------|-------------|
| `read` | View resources, read logs and metrics |
| `write` | Create/update resources; cannot delete or modify IAM |
| `admin` | Full control; restricted to Platform leads and CI service accounts |

## Access Reviews

- All access is reviewed quarterly by the Platform Lead.
- Any access not explicitly re-confirmed during review is revoked.
- Service accounts unused for > 60 days are suspended automatically.

## Offboarding

When someone leaves the team:

1. Their access is revoked within **4 hours** of departure confirmation.
2. Any service accounts they owned are rotated and re-assigned.
3. Their entries are removed from PagerDuty and the on-call rotation.

Offboarding checklist: `runbooks/offboarding.md`

## External Contractors

- Contractors get time-bounded access (max 90 days, renewable with justification).
- No contractor gets `admin` level without a VP exception.
- All contractor actions are logged and auditable.
