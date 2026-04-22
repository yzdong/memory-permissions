# 2026-01-22 Gateway Certificate Expiry

## Summary

The TLS certificate for the `gateway` service expired at 00:00 UTC, causing all HTTPS traffic to be rejected with certificate errors. The outage lasted 51 minutes. This is a partial recurrence of the `api` cert expiry on 2025-11-21 — the action items from that incident were only applied to `api`, not `gateway`.

## Timeline

| Time (UTC) | Event |
|---|---|
| 00:00 | `gateway` TLS certificate expires |
| 00:00 | All HTTPS handshakes fail; clients receive `ERR_CERT_DATE_INVALID` |
| 00:03 | Uptime monitor fires; on-call (Sasha) paged |
| 00:11 | Sasha confirms cert expiry; begins manual renewal |
| 00:38 | New cert issued from internal CA |
| 00:51 | `gateway` reloaded with new cert; HTTPS restored |

## Root Cause

The certificate monitoring and auto-rotation improvements made after the November 21 incident were scoped to the `api` service only. `gateway` still relied on a manually-renewed certificate with no automated rotation and no expiry alert. The cert had been issued January 22, 2025 with a 1-year validity.

There was no tracking item to apply the November fixes to `gateway` — the post-mortem action items were service-specific rather than fleet-wide.

## Impact

- 51 minutes of complete HTTPS unavailability on the public `gateway` endpoint
- All external API clients and web frontend affected
- Internal service-to-service traffic (mTLS via separate cert) was unaffected
- Estimated 28,000 failed requests during the window

## Action Items

- [ ] **P0** Apply automated cert rotation (from `2025-11-21` remediation) to `gateway` and `worker` immediately — owner: Sasha, due 2026-01-23
- [ ] **P0** Audit all services for certificate expiry dates; add to central monitoring dashboard — owner: Priya, due 2026-01-25
- [ ] **P0** Post-mortem action items must explicitly enumerate all affected services, not just the one that failed — process change, owner: Damien, due 2026-01-28
- [ ] **P1** Certificate rotation runbook in `runbooks/tls-cert-rotation.md` to cover all three services
- [ ] **P2** Evaluate cert-manager for cluster-wide automated cert lifecycle management

## Cross-reference

See `2025-11-21-api-cert-rotation-failure.md` for the prior related incident.
