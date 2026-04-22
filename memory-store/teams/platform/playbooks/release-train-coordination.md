# Release Train Coordination Playbook

Platform coordinates the monthly release train for service teams that want a scheduled deployment rather than self-serve continuous deployment. Not all teams use this — check `docs/release-process-by-team.md`.

## Why this exists

Some teams (particularly those with compliance requirements) need a scheduled, structured release with sign-off. The release train gives them a repeatable process without requiring Platform to custom-babysit each deployment.

## Schedule

- Release train deploys on the **third Wednesday of each month**
- Cut-off for inclusion: previous Friday at 17:00 local
- Anything that misses cut-off rides the next train — no exceptions without VP approval

## For service teams

1. Submit your release by opening a PR against `release-train/manifest/YYYY-MM.yaml` with your service version pinned
2. Include a link to your own team's release notes
3. Confirm your staging deployment is green before submitting
4. Assign the PR to the Platform on-call for that week

## Platform responsibilities

### Pre-release (Monday–Tuesday before deploy day)
- [ ] Collect all manifests; verify each service's staging is healthy
- [ ] Resolve any version conflicts (two services depending on incompatible shared library versions)
- [ ] Run compatibility checks: `./scripts/release-train/pre-flight.sh YYYY-MM`
- [ ] Send release summary to #deployments: what's going out, which teams, any notable changes
- [ ] Confirm deploy window is free of other high-risk changes

### Deploy day (Wednesday)
- Deploy in order defined in `release-train/deploy-order.yaml` (load-bearing services first)
- Each service gets a 15-minute smoke test window after deploy
- Platform engineer stays available for 2 hours post-completion

### Post-release
- [ ] Confirm all services healthy in Grafana
- [ ] Post completion notice in #deployments
- [ ] Archive the manifest to `release-train/history/`
- [ ] Log any issues in `release-train/retros/YYYY-MM.md`

## Rollback
If a service fails its smoke test: roll back that service independently. The release train doesn't roll back en masse unless there's a systemic issue.
