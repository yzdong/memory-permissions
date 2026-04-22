# 2025-11-21 API TLS Certificate Rotation Failure

## Summary

The automated TLS certificate rotation job for the `api` service failed silently for 11 days, causing the certificate to expire and resulting in 22 minutes of HTTPS failures before a manual hotfix was applied.

## Timeline

| Time (UTC) | Event |
|---|---|
| 2025-11-10 03:00 | Cert rotation cron job runs; fails due to expired Vault token |
| 2025-11-10–2025-11-20 | Job fails daily with no alert; nobody notices |
| 2025-11-21 03:00 | TLS certificate expires |
| 2025-11-21 03:01 | HTTPS connections to `api` fail with `SSL_ERROR_RX_RECORD_TOO_LONG` |
| 2025-11-21 03:04 | Uptime monitor fires; on-call (Priya) paged |
| 2025-11-21 03:09 | Root cause identified: expired cert + broken rotation |
| 2025-11-21 03:26 | Manual cert renewal and reload completed |

## Root Cause

The Vault AppRole token used by the cert rotation job had a `ttl` of 30 days and a `max_ttl` of 90 days. It was initially provisioned in August but never renewed. When it expired on November 10th, the rotation job began failing. The job only logged to stdout; there was no alerting on cron job failure exit codes.

## Impact

- 22 minutes of complete HTTPS unavailability on the `api` service
- All web and mobile clients affected; API consumers received TLS handshake errors
- No data loss or security compromise
- One enterprise customer filed a severity-1 support ticket

## Action Items

- [ ] **P0** Alert on any cron job non-zero exit within 5 minutes — owner: Damien, due 2025-11-25
- [ ] **P0** Switch cert rotation to use Vault's `periodic` token type with auto-renewal — owner: Priya, due 2025-11-28
- [ ] **P0** Add cert expiry monitoring with 30-day and 7-day advance alerts — owner: Tomás, due 2025-11-26
- [ ] **P1** Audit all cron job Vault tokens for approaching `max_ttl` — owner: Sasha, due 2025-11-30
- [ ] **P2** Document Vault token lifecycle in `runbooks/vault-tokens.md`
