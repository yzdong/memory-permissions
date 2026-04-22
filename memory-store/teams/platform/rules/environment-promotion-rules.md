# Environment Promotion Rules — Platform Team

This doc defines how code and configuration move between environments. The promotion path is always dev → staging → prod. No skipping.

## Promotion Path

```
dev (local / feature branches)
  ↓  PR merged to main
staging (auto-deployed from main)
  ↓  Manual promotion gate
prod (promoted by pipeline)
```

There is no mechanism to deploy directly to prod from a feature branch. If you think you need one, talk to the platform lead first.

## Staging Promotion (main → staging)

Automatic on every merge to `main`. No human gate. Staging should always reflect `main` within 10 minutes of a merge.

If staging is behind by more than 30 minutes, check the `#platform-deploys` channel and the pipeline dashboard.

## Production Promotion Gates

Before a build can go to prod, the pipeline checks:

1. Staging has been running the build for at least **15 minutes** (configurable per service, this is the floor)
2. Error rate in staging has not exceeded **1.5%** during that window
3. No active incidents tagged with the service name
4. A human clicked the promotion button (pipeline config: `require_approval: true`)

## Configuration Differences Between Environments

Environment-specific config is stored in `infra/deploy-config/{service}/{env}.yaml`. Common differences:

- Replica counts (staging runs at reduced capacity)
- Log levels (staging: debug, prod: info)
- Feature flags (some features are staging-only during rollout)

Never hardcode environment names in application code. Use the injected `DEPLOY_ENV` variable.

## Rollback Across Environments

Rolling back prod does NOT automatically roll back staging. Staging stays on the newer build for debugging purposes unless you explicitly want to roll it back too.

## Sandbox

Sandbox is outside the promotion path. It's for experimentation and is not a gate to anything. Treat it as ephemeral — resources are reaped after 14 days of inactivity.

## Related

- `deploy-pipeline-rules.md`
- `change-management-rules.md`
- `../runbooks/deploy.md`
