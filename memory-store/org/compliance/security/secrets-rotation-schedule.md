# Secrets Rotation Schedule

Maintained by: Security Engineering  
Source of truth for all credential rotation timelines across the org.

If a secret is not on this list, that's a gap — open a ticket in `SEC`.

## Rotation Policy

| Secret Type | Max Lifetime | Method |
|---|---|---|
| AWS IAM user keys | 90 days | Automated (Lambda + Secrets Manager) |
| Database passwords | 180 days | Vault dynamic secrets preferred; manual otherwise |
| API keys (third-party) | 365 days | Manual — owner team responsible |
| JWT signing keys | 90 days | Automated key rollover |
| Okta API tokens | 180 days | Manual |
| SSH host keys | 2 years | Manual |
| TLS certificates | 90 days (Let's Encrypt auto) | Automated via cert-manager |
| SAML IdP signing cert | 2 years | See `saml-sso-runbook.md` |

## Upcoming Rotations

| Secret | Owner Team | Due Date | Ticket |
|---|---|---|---|
| `prod/payments-service/stripe-api-key` | Payments | 2025-03-01 | SEC-441 |
| `prod/data-pipeline/snowflake-svc-acct` | Data Eng | 2025-02-15 | SEC-438 |
| JWT signing key (user-service) | Platform | 2025-04-10 | SEC-450 |
| Okta API token (IT automation) | IT/Ops | 2025-05-30 | SEC-452 |

## How to Rotate

### AWS IAM keys (automated)

The `secrets-rotation` Lambda runs every Sunday at 02:00 UTC. It rotates keys older than 80 days, gives services 10 days to pick up the new key, then deletes the old one. Monitor in `#security-rotation-alerts`.

### Vault dynamic secrets (preferred for DB)

```bash
# Verify dynamic secret config for a service
vault read database/roles/user-service-role

# Manually force rotation if needed
vault write -f database/rotate-role/user-service-role
```

### Manual rotation

1. Generate new credential in the target system.
2. Write to Vault: `vault kv put secret/<path> value=<new-value>`
3. Update any hardcoded references (there shouldn't be any — if there are, fix them).
4. Verify service is using new credential before revoking old one.
5. Revoke old credential.
6. Update this file and close the tracking ticket.

## Emergency Rotation

If a secret is believed to be compromised, treat it as an active incident:

1. Declare an incident — use `incident-response-template.md`.
2. Rotate immediately, don't wait for the normal process.
3. Review audit logs for the compromised credential's usage in the prior 30 days.
4. Notify `#security-incidents`.

## Audit Trail

All Vault reads/writes are logged to CloudWatch Logs group `/vault/audit`. Retention: 1 year.
