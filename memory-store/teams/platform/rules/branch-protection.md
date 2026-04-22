# Branch Protection Rules — Platform Team

These rules apply to all Platform-owned repositories. They are enforced via GitHub rulesets and are not optional.

## Protected Branches

- `main`
- `release/*`
- `hotfix/*`

## Rules on `main`

- **Required status checks** (must pass before merge):
  - `ci/lint`
  - `ci/test`
  - `ci/terraform-plan` (for repos with infra)
- **Required approvals**: 2 (see `code-review-rules.md`)
- **Dismiss stale reviews**: enabled — a new push invalidates previous approvals
- **Require signed commits**: enabled
- **No force push**: enforced, no exceptions (use revert commits)
- **No deletion**: enforced

## Rules on `release/*` and `hotfix/*`

- Same as `main` except:
  - 1 approval sufficient for `hotfix/*` during active incident (SEV-1 or SEV-2)
  - Stale review dismissal still applies

## Admin Override Policy

Admins CAN bypass protection in declared incidents. They MUST:
1. Post in `#platform-oncall` before bypassing
2. Open a follow-up PR to revert or re-apply any direct push within 24h
3. Note the bypass in the incident postmortem

Admin bypass should be the absolute last resort.

## Adding New Protected Branches

Open a PR against `infra/github-rulesets/platform.tf`. Changes go through the normal infra review process (2 approvals).

## Tooling Notes

We manage rulesets via Terraform, not the GitHub UI, to keep config in code. If you see a drift between the UI and the Terraform state, file a ticket — don't fix it manually in the UI.

```bash
# Check current ruleset state
terraform -chdir=infra/github-rulesets plan
```

## Related

- `code-review-rules.md`
- `../runbooks/hotfix-deploy.md`
- `infra/github-rulesets/platform.tf`
