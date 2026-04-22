# Legacy 2024 Deploy Procedure (Archived)

> **Status**: Superseded as of 2025-01-15. This runbook describes the pre-migration deploy process for the monolith era. Kept for historical reference and for teams still running the legacy `v1-compat` branch.

## Background

Prior to the service split in late 2024, all three services were deployed as a single artifact via the `platform-mono` pipeline. This file documents that procedure for:
- Rollbacks to pre-split versions
- Debugging incidents where root cause traces back to the monolith era
- The `v1-compat` compatibility shim still used by two internal partners

## Legacy Build

```bash
# From the platform-mono repo (not platform/services)
git checkout v1-compat
make build ENV=production TAG=$(git rev-parse --short HEAD)
```
Artifacts land in `s3://platform-artifacts/mono/<tag>/`.

## Legacy Deploy Targets

| Target | Host | Notes |
|--------|------|-------|
| mono-api | `mono-api-prod-01..03` | Still serving v1 auth endpoints |
| mono-worker | `mono-worker-prod-01` | Processes legacy event format |

Deploy via Ansible (not Kubernetes):
```bash
ansible-playbook -i inventories/production playbooks/mono-deploy.yml \
  --extra-vars "artifact_tag=<tag>"
```

## Health Check

```bash
curl -sf https://api-legacy.internal/healthz | jq .version
```
Expected: `{"version": "v1-compat", "status": "ok"}`

## Known Limitations of the Legacy System

- No rolling deploy — this is a stop-the-world restart. Coordinate a maintenance window.
- Legacy Redis schema is incompatible with the current Redis cluster. Uses a separate `redis-legacy-01` instance.
- Postgres migrations for the legacy schema are in `db/legacy_migrations/` — do not run these against the current schema.

## Deprecation Timeline

- **2025-Q3**: `v1-compat` branch enters security-only patch mode.
- **2025-Q4**: Scheduled sunset. See `../planning/legacy-sunset-plan.md`.

## Contacts

For legacy system questions, reach out to @legacy-owners in Slack. Do not file tickets in the main Platform board.
