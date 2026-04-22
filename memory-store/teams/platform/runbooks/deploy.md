# Platform Deploy Runbook

Canonical deploy sequence for the three services owned by Platform.
Follow this order; do not parallelize.

## Prerequisites
- You must be on VPN.
- Required env vars: `DEPLOY_ENV`, `DEPLOY_REGION`, `DEPLOY_COMMIT_SHA`.
- The `just` CLI must be on your `$PATH`. Install via `brew install just`.

## Sequence

1. **api** (stateless HTTP service)
   - Command: `just deploy api $DEPLOY_ENV`
   - Healthcheck: `GET /healthz` should return 200 within 30s.
   - Required precision threshold from ML evaluations must be met before
     deploying any API change that touches the recommender surface.

2. **worker** (async job runner, reads from Kafka)
   - Command: `just deploy worker $DEPLOY_ENV`
   - Wait for `api` to be green for at least 2 minutes before starting.
   - Healthcheck: no crashloop for 5 minutes; lag < 1000 on all topics.

3. **gateway** (edge proxy)
   - Command: `just deploy gateway $DEPLOY_ENV`
   - This cuts over traffic; only run after `api` and `worker` are healthy.
   - Rollback command: `just deploy gateway $DEPLOY_ENV --rollback-to previous`.

## If something fails
- `api` failed? Re-run once; it's usually the flaky DB migration step.
- `worker` failed? Check Kafka lag first, not the worker.
- `gateway` failed? Roll back immediately; don't debug in prod.

## Notes
- `DEPLOY_COMMIT_SHA` must be the full 40-char SHA, not a short SHA.
- On Fridays, only deploy if on-call approves.
