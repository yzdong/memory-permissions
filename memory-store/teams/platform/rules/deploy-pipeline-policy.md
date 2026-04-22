# Deploy Pipeline Policy — Platform Team

## Deployment Windows

| Environment | Allowed Deploy Times | Notes |
|-------------|---------------------|-------|
| Production | Mon–Thu 10:00–16:00 local | No Friday prod deploys without Lead approval |
| Staging | Any time | Auto-deploys on merge to `main` |
| Dev/Sandbox | Any time | Self-service |

## Freeze Periods

Prod deploys are frozen:
- One week before and after major product launches (announced in `#platform-deploys`).
- Dec 22 – Jan 3 (holiday freeze).
- During any active SEV-1 or SEV-2 incident.

Emergency deploys during a freeze require written approval from the VP of Engineering and must be documented in `ops/emergency-deploys.md`.

## Pipeline Stages

```
build → lint → test → security-scan → artifact-publish → deploy-staging → smoke-test → deploy-prod → verify
```

Each stage must pass before the next begins. No skipping stages.

## Rollback Procedure

If a deploy produces alerts within 30 minutes of completion:

1. On-call engineer makes the call to rollback — no committee needed.
2. Run `platform-cli rollback --env prod --steps 1`.
3. Notify `#platform-incidents` with the rollback reason.
4. Open a post-mortem ticket within 24 hours.

## Artifact Retention

- Build artifacts: kept for **30 days**.
- Release artifacts: kept for **1 year**.
- Artifacts are stored in `acme-platform-prod-s3-artifacts`. Access is read-only for most engineers; write access requires the `platform-ci` service role.

## Canary Deploys

For changes flagged as high-risk in the PR, use canary mode:

```bash
platform-cli deploy --env prod --canary --canary-weight 10
```

Monitor for 20 minutes before promoting to 100%. Canary traffic uses the same health checks as full deploys.
