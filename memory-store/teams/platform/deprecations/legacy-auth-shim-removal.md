# Legacy Auth Shim Removal

**Status:** Removal targeted for 2025-09-30  
**Owner:** Platform (coordinate with Security team)  
**Slack:** `#platform-auth-migration`

## What Is the Auth Shim

The auth shim lives in `libs/auth-shim/` and was written in 2020 to bridge the old LDAP-based session auth with the JWT system we adopted. It intercepts requests in the API gateway middleware stack, checks for legacy session cookies, and if found, mints a short-lived JWT on behalf of the caller.

It was supposed to be temporary. It is now five years old.

## Why Remove It

1. It holds a persistent LDAP connection that has caused cascading timeouts twice in the past year (see incident `INC-2041`, `INC-2198`)
2. It bypasses the standard token refresh logic, meaning shim-authenticated sessions don't get rotated MFA checks
3. It's blocking a security requirement to enforce per-request signing by Q3 2025
4. Nobody on the current team wrote it or wants to maintain it

## Who Still Uses It

Run the following to find active callers:

```bash
grep -r "auth-shim" services/ --include="*.py" -l
```

As of the last audit (2025-05-01):
- `services/internal-admin-portal` — highest priority to migrate
- `services/reporting-api` — low traffic, but sensitive data
- `services/partner-gateway` — owned by partnerships team

## Migration Path

Each service should:

1. Switch to the standard `libs/auth-client` SDK (docs: `libs/auth-client/README.md`)
2. Register a service client ID in Vault: `vault write auth/jwt/clients/...`
3. Update integration tests to use JWT fixtures, not session cookies
4. Remove any `X-Legacy-Session` header handling

## Timeline

| Milestone | Date |
|---|---|
| All internal services migrated | 2025-07-31 |
| Partner-gateway migrated (partnerships team) | 2025-08-31 |
| Shim disabled (feature flag off) | 2025-09-15 |
| Shim code deleted | 2025-09-30 |

## Contacts

- Platform lead: ask in `#platform-help`
- Security sign-off required before final deletion — file a ticket with the Security team referencing this doc
