# Shared Session Store Deprecation

**Status:** In Progress — Target 2025-08-01  
**Owner:** Platform (Security Subteam)  
**Related:** `legacy-auth-shim-removal.md`

## What Is the Shared Session Store?

A Redis instance at `redis-sessions.internal:6379` (no auth, no TLS) that a handful of services use to share user session state. It was a pragmatic shortcut from 2020 when we needed multiple services to recognize the same user session without implementing a proper token exchange.

The problems:
- No TLS: session tokens in plaintext on the internal network
- No per-service isolation: a bug in any one service can read or corrupt sessions for all others
- No ACL: literally any service that knows the host can connect
- Sessions never expire cleanly — we have stale session keys from 2021 still sitting in the keyspace

## What Replaces It

Stateless JWT-based sessions via the IdP. Each service validates tokens independently. No shared state needed.

For services that truly need cross-service user context, the IdP's token introspection endpoint (`https://idp.internal/oauth/introspect`) is the right tool.

## Affected Services

- `admin-portal` — currently reads sessions for user lookup
- `reporting-service` — reads sessions to check permissions
- `legacy-export-job` — writes session flags as a hack for job-ownership tracking

## Migration Plan per Service

### admin-portal
Switch to JWT validation middleware. The `platform-auth-client` SDK v2.4 includes this. See `lib/auth/README.md`.

### reporting-service
Permissions should come from token claims, not session state. Work with the identity team to add the needed claims to the token scope.

### legacy-export-job
Job ownership should be tracked in the job's own database row (already has an `owner_user_id` column that was never used). Stop using session flags.

## After Migration

The Redis instance at `redis-sessions.internal` will be decommissioned. The hostname will resolve to nothing. Any service still connecting will fail immediately with a connection refused error — that's intentional and will surface any missed migrations.

## Related

- `legacy-auth-shim-removal.md`
- `runbooks/oauth-token-debugging.md`
- `../security/zero-trust-network-policy.md`
