# Secrets Handling — Platform Team

This doc covers how Platform manages secrets. It is prescriptive. Deviations need a written exception approved by the platform lead.

## Where Secrets Live

- **Vault** (HashiCorp): all production and staging secrets
- **GitHub Actions Secrets**: CI/CD secrets only (e.g. deploy tokens, registry credentials)
- **AWS Secrets Manager**: used for RDS credentials and a few legacy integrations

Do NOT store secrets in:
- Environment variable files committed to the repo (`.env`, `config.local.yaml`, etc.)
- S3 buckets without encryption-at-rest enabled
- Slack, Confluence, Notion, or any collaboration tool
- Terraform state without remote state encryption configured

## Naming Convention for Vault Paths

```
secret/{env}/{service}/{key-name}
```

Examples:
- `secret/prod/deployer/github-token`
- `secret/staging/metrics/datadog-api-key`

## Rotation Policy

| Secret type           | Max age  | Rotation method          |
|-----------------------|----------|--------------------------|
| Service account tokens| 90 days  | Automated (Vault leases) |
| Deploy tokens         | 30 days  | Semi-automated script     |
| Database passwords    | 60 days  | Automated via RDS plugin  |
| Personal API keys     | 30 days  | Manual, owner responsible |

## Incident Response for Leaked Secrets

1. Revoke immediately — don't wait to confirm the leak
2. Rotate and re-issue
3. Audit access logs for the 30 days before revocation
4. File SEV-2 (minimum) in `#incidents`
5. Add to postmortem

## Audit Logging

All Vault access is logged to our SIEM. Unusual access patterns trigger an alert in `#platform-security`. If you get paged for this, check the runbook at `../runbooks/vault-audit-alert.md`.

## Temporary Secrets for Dev/Testing

Use the `sandbox` Vault namespace. Secrets there expire after 7 days automatically. Never use real credentials in dev environments.

## Related

- `naming-conventions.md`
- `../runbooks/secret-rotation.md`
- `../runbooks/vault-audit-alert.md`
