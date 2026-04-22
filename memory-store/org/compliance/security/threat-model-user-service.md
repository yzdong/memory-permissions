# Threat Model: User Service

Version: 1.3  
Last updated: 2025-01-15  
Authors: @mireille, @tobias-k  
Review cycle: 6 months or after major architectural change

## Scope

Covers the `user-service` microservice: account creation, authentication, profile management, and session lifecycle. Does **not** cover downstream services that consume user data — those have their own models.

## Architecture Summary

```
[Browser / Mobile] → [API Gateway] → [user-service] → [users-db (Postgres)]
                                              ↓
                                       [auth-cache (Redis)]
                                              ↓
                                       [event-bus (Kafka)]
```

The service runs in our internal VPC. API Gateway handles TLS termination and rate limiting.

## Assets & Trust Boundaries

| Asset | Classification | Trust Boundary |
|---|---|---|
| User credentials (hashed) | Confidential | DB network segment |
| Session tokens | Sensitive | Memory + Redis |
| Profile data | Internal | Service-to-service |
| Audit logs | Internal | Log aggregator |

## Threats (STRIDE)

### Spoofing
- **T-01**: Attacker replays a stolen session token.
  - Mitigations: short TTL (15 min), token rotation on use, Redis-side invalidation list.

### Tampering
- **T-02**: SQL injection via profile update endpoint.
  - Mitigations: parameterized queries enforced via ORM, SAST in CI (semgrep rule `sql-injection`).

### Repudiation
- **T-03**: User denies performing account action.
  - Mitigations: signed audit log entries, append-only CloudWatch log group.

### Information Disclosure
- **T-04**: Error responses leak internal stack traces.
  - Mitigations: generic error messages in prod; full traces only in structured internal logs.
- **T-05**: Bulk user enumeration via login endpoint timing.
  - Mitigations: constant-time comparison, generic "invalid credentials" message.

### Denial of Service
- **T-06**: Credential stuffing floods auth endpoint.
  - Mitigations: CAPTCHA after 5 failures, per-IP rate limit at gateway (100 req/min).

### Elevation of Privilege
- **T-07**: Horizontal privilege escalation — user A reads user B's data.
  - Mitigations: ownership check middleware applied to all profile routes; integration test suite covers this.

## Open Issues

- [ ] **T-08** (draft): Evaluate risk of Kafka consumer lag allowing stale auth events — assigned @tobias-k, due 2025-02-28.

## References

- `../pii-handling.md` — rules on how PII fields must be treated
- `incident-response-template.md` — use when a threat is realized
- OWASP Top 10 2021
