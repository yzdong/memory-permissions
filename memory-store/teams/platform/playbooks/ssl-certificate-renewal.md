# TLS Certificate Renewal Playbook

Most certs are managed via ACM with auto-renewal. This playbook covers the edge cases: self-managed certs, third-party CA certs, and the annual review of what we actually have.

## Annual Certificate Audit

Run this in January before any certs expire in Q2 (our historically bad quarter for expiry incidents).

```bash
python scripts/certs/audit-certs.py \
  --sources acm,nginx-configs,k8s-secrets \
  --warn-days 90 \
  --output reports/cert-audit-$(date +%Y).csv
```

Expected output columns: domain, issuer, expiry date, days remaining, managed-by, auto-renew status.

## ACM-Managed Certs (Automated)

These should renew automatically if:
- Domain validation records are in Route 53 (owned by Platform)
- Certificate is associated with a CloudFront distribution or ALB

If auto-renewal fails (it does happen), the ACM console shows a "Pending validation" status. Fix by re-adding the CNAME validation record — DNS propagation can take up to 72h.

## Third-Party CA Certs (Manual Process)

We have a handful of these for partners who require specific CA chains.

1. Generate CSR:
```bash
openssl req -new -newkey rsa:2048 -nodes \
  -keyout certs/<domain>.key \
  -out certs/<domain>.csr \
  -subj "/CN=<domain>/O=Platform Co/C=US"
```

2. Submit CSR to CA portal (credentials in 1Password vault `platform-certs`)
3. Download the full chain: cert + intermediates
4. Verify chain before deploying:
```bash
openssl verify -CAfile intermediate.pem domain.pem
```
5. Upload to Secrets Manager: `/<env>/tls/<domain>/cert` and `/<env>/tls/<domain>/key`

## Deployment

For NGINX-terminated certs:
- Update the cert path in `nginx/conf.d/<site>.conf`
- Deploy via standard pipeline — do NOT restart NGINX manually in production
- Verify: `echo | openssl s_client -connect <domain>:443 | openssl x509 -noout -dates`

## Monitoring

Datadog cert expiry monitors are configured for all public-facing domains. Threshold: warn at 45 days, critical at 14 days. If you're seeing a critical alert, work the renewal immediately — 14 days sounds like a lot until you're waiting for CA validation.

## Common Failures

- **CAA record mismatch:** Check `dig CAA <domain>` before submitting to a new CA
- **SAN mismatch:** CSR must include all subdomains the cert will serve
- **Private key loss:** Never store keys only in CI/CD env vars — always back up to Secrets Manager
