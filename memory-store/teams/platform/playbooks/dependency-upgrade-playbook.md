# Dependency Upgrade Playbook

Applies to: shared libraries, base images, Kubernetes version, Terraform provider versions.

Not for emergency patching — use `runbooks/security-patch.md` for CVEs with active exploits.

## Deciding when to upgrade

We track versions in `infra/versions.yaml`. Dependabot PRs land weekly. A dependency should be prioritized for upgrade if:
- It's more than 2 minor versions behind latest stable
- A CVE with CVSS ≥ 7.0 is present, even if not actively exploited
- The current version is EOL or enters EOL within 90 days

## Process

### 1. Assess impact
```bash
./scripts/dep-impact.sh --package <name> --current <ver> --target <ver>
```
This outputs which services depend on the package and flags any known breaking changes.

### 2. Read the changelog
Seriouslydo this. We have been burned by silent behavior changes more than once. Look for anything touching serialization, connection pooling, or retry logic.

### 3. Stage the upgrade
- Update `infra/versions.yaml`
- Open a draft PR; tag `#platform-review`
- Run the integration test suite in CI: `make test-integration`

### 4. Canary rollout
- Deploy to `staging` first and let it soak for at least 24 hours
- For Kubernetes or Terraform provider upgrades, soak for 72 hours minimum
- Check error rates and latency in Grafana before promoting

### 5. Broad rollout
- Merge and deploy to production in off-peak hours
- Keep the old version available to roll back for 48 hours if feasible

### 6. Communicate
- Post upgrade notice in #platform-announcements with the version change and any action items for service teams
- Update `infra/versions.yaml` with upgrade date and notes

## Rollback
If something goes wrong post-upgrade, revert the `versions.yaml` PR and re-deploy. Do not try to fix-forward under production pressure unless the old version is truly unavailable.
