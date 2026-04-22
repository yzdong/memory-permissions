# Security Controls Overview

Owner: Security Engineering
Audience: All engineers

This is the "where to find things" map for our security control landscape. Each section links to the canonical doc rather than repeating details.

## Identity & Access

- **SSO:** Okta SAML for all Tier-1 systems. See `saml-sso-runbook.md`.
- **MFA:** Hardware key (YubiKey) required for `eng-infra-prod` group. TOTP acceptable for other groups.
- **Access reviews:** Quarterly. See `access-review-quarterly.md`.
- **Least privilege:** IAM roles scoped per service; no shared `admin` accounts in prod.

## Secrets Management

- AWS Secrets Manager for application secrets.
- 1Password Teams for human-accessible credentials.
- Rotation schedule: `secrets-rotation-schedule.md`.
- **Never** commit secrets to git. Pre-commit hook `git-secrets` is mandatory; enforced in CI.

## Network Security

- All external traffic terminates at the WAF (AWS WAF v2).
- Internal service-to-service traffic uses mTLS within the VPC.
- Egress filtering via VPC endpoints; unexpected egress triggers CloudWatch alarm.
- No SSH to production — use AWS Systems Manager Session Manager.

## Endpoint Security

- All corporate laptops enrolled in Jamf (Mac) or Intune (Windows).
- CrowdStrike Falcon deployed; any detection auto-creates a Jira ticket in the SEC project.
- Full-disk encryption required; verified by MDM compliance policy.

## Application Security

- SAST: Semgrep runs in CI on every PR; High findings block merge.
- SCA: Dependabot PRs for dependency updates; Critical CVEs must be patched within 7 days.
- Container images scanned by Trivy at build time; Critical findings block image push.
- Bug bounty program for external researchers: `bug-bounty-program.md`.
- Threat models maintained per service: see `threat-model-user-service.md` as the reference format.

## Data Protection

- Classification levels and tagging requirements: `data-classification-policy.md`.
- PII handling rules: `../pii-handling.md`.
- Encryption at rest: AES-256 for all datastores. Encryption in transit: TLS 1.2 minimum, 1.3 preferred.

## Logging & Monitoring

- Centralized log aggregation in CloudWatch; shipped to Datadog for alerting.
- 13-month log retention for Critical and High data sources.
- SIEM: Panther consumes CloudTrail, VPC Flow Logs, and app audit logs.
- On-call rotation handles security alerts; escalation path in PagerDuty service `security-oncall`.

## Incident Response

- Template: `incident-response-template.md`.
- Severity definitions and escalation matrix: internal wiki page `Security / Severity Definitions`.
- Post-mortems required for all P1 and P2 security incidents.
