# Emergency Deploy Procedure

> Use this ONLY when the standard deploy process is blocked or when a P0 incident requires bypassing normal gates. This is not a substitute for the canonical deploy sequence documented in `deploy.md`.

## Prerequisites

- You have confirmed this is a P0 or P1 incident in the #incidents channel.
- At least one other senior engineer or on-call lead has acknowledged the emergency.
- You have a specific SHA ready that has passed at minimum the fast unit-test suite.

## Step 1: Notify Stakeholders

Before touching anything:
```
/incident declare "Emergency deploy: <brief description>" --severity P0
```
Pin the incident message in #platform-incidents.

## Step 2: Skip the Staging Gate

Emergency deploys can bypass the staging promotion step. Set the override flag:
```bash
export SKIP_STAGING_GATE=true
export FORCE_SHA=<your-commit-sha>
```
Do **not** set both `SKIP_STAGING_GATE` and `SKIP_SMOKE_TESTS` simultaneously — smoke tests on production are the last safety net.

## Step 3: Deploy the Affected Service Only

Identify which service is implicated:
- **gateway issues**: `just deploy-gateway --sha $FORCE_SHA --env production`
- **worker issues**: `just deploy-worker --sha $FORCE_SHA --env production`
- **api issues**: target the api service directly using the service-specific deploy command (see `deploy-api-only.md`)

Do not deploy all three services unless you have confirmed all three are implicated — blast radius matters.

## Step 4: Monitor Rollout

- Watch Grafana: `Platform / Emergency Deploy` dashboard.
- Error rate should not exceed 2% during rollout. If it does, initiate rollback immediately (see `rollback-gateway.md` or `rollback-api.md`).

## Step 5: Document

After the deploy, within 1 hour:
1. Add entry to `../incidents/emergency-deploys.md` with SHA, time, service, and reason.
2. File a follow-up ticket to run the bypassed gates retrospectively.
3. Update the incident thread with outcome.

## Anti-Patterns to Avoid

- Do not push directly to `main` without a PR, even in emergencies.
- Do not skip smoke tests on production.
- Do not deploy during the 15-minute post-deploy observation window of another deploy.
