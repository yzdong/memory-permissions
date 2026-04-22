# Deprecated API Endpoints — 2025

**Last updated:** 2025-05-20  
**Owner:** Platform API team  
**Policy doc:** `docs/api-versioning-policy.md`

## Overview

This is the running list of endpoints scheduled for removal in 2025. Deprecation notices have been added to response headers (`Sunset`, `Deprecation`) per RFC 8594. Callers who ignore those headers will get broken integrations.

---

## Endpoints Being Removed

### `GET /v1/users/{id}/profile` → removed 2025-07-01

**Replacement:** `GET /v2/users/{id}`  
The v2 endpoint returns a superset of the v1 response; the field names are slightly different. See `docs/api/v2-user-migration.md` for the field mapping table.

Known callers (from API analytics, March 2025):
- Mobile app (iOS/Android) — they've committed to shipping v2 support by June 15
- Internal `services/crm-sync` — Platform to handle this one

### `POST /v1/events/batch` → removed 2025-08-15

**Replacement:** `POST /v2/events` with `Content-Type: application/x-ndjson`  
The new endpoint uses newline-delimited JSON and supports streaming. Max payload size stays at 10MB.

This change breaks any caller that sends `application/json` arrays. Check your clients.

### `GET /internal/health/legacy` → removed 2025-06-01

**Replacement:** `GET /healthz`  
This one should be painless. Anyone load-balancer health-checking against `/internal/health/legacy` needs to update their probe config.

### `DELETE /v1/sessions` → removed 2025-09-01

Related to the auth shim removal (see `legacy-auth-shim-removal.md`). The session cookie pattern goes away entirely.

---

## How to Check If You're Calling These

```bash
# Search service HTTP client definitions
grep -r "/v1/users" services/ --include="*.py" --include="*.ts" -n
```

Alternatively, check the Datadog dashboard `API Deprecated Endpoint Traffic` — it shows call volume per endpoint per service with a 30-day window.

---

## Process for Adding to This List

1. Announce in `#platform-api-changes` at least 90 days before removal
2. Add `Deprecation` and `Sunset` response headers immediately
3. File entries here with the removal date and replacement
4. Update `docs/api/changelog.md`
