# Python 3.11 Migration Guide

**Status:** In progress  
**Owner:** Platform  
**Deadline:** 2025-08-01  

## Background

We've been running Python 3.9 across most services since late 2022. Python 3.9 hits end-of-life in October 2025, and we want a buffer. 3.11 gives us ~15% performance improvements on CPU-bound workloads plus better error messages, which alone is worth the upgrade.

## Scope

- All services under `services/` that specify `python_version = "3.9"` in their `Pipfile` or `pyproject.toml`
- Shared libs in `libs/platform-utils` and `libs/data-connectors`
- Lambda functions deployed via `infra/lambdas/`

## Migration Steps

1. **Update base images** — swap `python:3.9-slim` for `python:3.11-slim` in all Dockerfiles
2. **Pin dependencies** — run `pip-compile --upgrade` and audit the diff
3. **Run test suite locally** on 3.11 before pushing
4. **Fix deprecations** — notably `asyncio.get_event_loop()` warns loudly in 3.10+; replace with `asyncio.get_running_loop()` where appropriate
5. **Update CI matrix** in `.github/workflows/ci.yml` to test on 3.11
6. **Deploy to staging** and soak for 48 hours minimum

## Known Breakages

- `distutils` is gone in 3.12 but still present in 3.11 — don't rely on it, treat it as already gone
- `datetime.utcnow()` is deprecated; switch to `datetime.now(timezone.utc)`
- Some older `cryptography` versions don't build cleanly; pin to `>=41.0.0`

## Service Tracker

| Service | Owner | Status |
|---|---|---|
| api-gateway | platform | ✅ Done |
| billing-worker | billing-team | 🔄 In progress |
| notification-service | comms | ⏳ Not started |
| data-pipeline | data-eng | 🔄 In progress |

## Rollback

If a service breaks post-deploy, revert the image tag in `infra/helm/values-prod.yaml` and re-deploy. See `runbooks/rollback-service.md` for the standard rollback procedure.

## References

- [Python 3.11 What's New](https://docs.python.org/3.11/whatsnew/3.11.html)
- `../evaluations/dependency-audit-2024.md`
- `runbooks/deploy.md`
