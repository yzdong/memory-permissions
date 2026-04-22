# TLS Certificate Rotation

Covers manual and semi-automated rotation of TLS certificates for the three services (api, gateway, worker internal mTLS). Automated rotation via cert-manager handles 90% of cases; this runbook is for the exceptions.

## Certificate Inventory

| Certificate | CN | Expiry Check | Managed By |
|-------------|----|--------------|------------|
| gateway external | `*.platform.example.com` | `just cert-status gateway-external` | cert-manager (Let's Encrypt) |
| api internal | `api.internal` | `just cert-status api-internal` | cert-manager (internal CA) |
| worker mTLS | `worker.internal` | `just cert-status worker-mtls` | manual (see below) |
| Postgres client cert | `db-client` | `just cert-status db-client` | manual |

## Checking Expiry

```bash
openssl s_client -connect gateway.prod.internal:443 -servername platform.example.com \
  </dev/null 2>/dev/null | openssl x509 -noout -dates
```

Alert fires at 30 days remaining. Do not wait until < 7 days.

## cert-manager Managed Certs

If a cert-manager cert is stuck:
```bash
kubectl describe certificate gateway-tls -n gateway
kubectl describe certificaterequest -n gateway
```
Common fix — delete the failed `CertificateRequest` resource and let cert-manager retry:
```bash
kubectl delete certificaterequest -n gateway --field-selector status.conditions[0].reason=Failed
```

## Manual Rotation: Worker mTLS

1. Generate new cert from internal CA:
   ```bash
   just gen-cert worker.internal --ca internal-ca --days 365 --out certs/worker-new.pem
   ```
2. Upload to Vault:
   ```bash
   vault kv put secret/platform/worker-mtls cert=@certs/worker-new.pem key=@certs/worker-new-key.pem
   ```
3. Trigger worker secret rotation (rolls pods without full deploy):
   ```bash
   kubectl rollout restart deployment/worker -n workers
   ```
4. Verify mTLS handshakes are succeeding:
   ```bash
   just mtls-check worker --env production
   ```

## Manual Rotation: Postgres Client Cert

See `../procedures/postgres-client-cert-rotation.md` for the full sequence — it involves coordinating with the DBA to update `pg_hba.conf`.

## Post-Rotation Checklist

- [ ] Old cert removed from Vault after 48-hour grace period.
- [ ] Cert expiry alert reset in PagerDuty.
- [ ] Updated `../infrastructure/cert-inventory.md` with new expiry dates.
- [ ] Notified #platform-infra of rotation completion.
