# Dependency Update Rules — Platform Team

Stale dependencies are a security risk and a maintenance burden. Platform has an opinionated stance on how to handle them.

## Automated Updates (Dependabot)

Dependabot is enabled on all Platform-owned repos. PRs are auto-created for:
- **Patch updates**: Auto-merged if CI is green (no human review needed)
- **Minor updates**: Require 1 approval from any platform team member
- **Major updates**: Require 2 approvals + manual testing against staging

Config lives at `.github/dependabot.yml` in each repo.

## Grouping

We group AWS SDK updates together (there are a lot of them) to avoid PR spam. Similarly, Terraform provider updates are batched weekly. See the dependabot config for current grouping rules.

## Security Advisories

Critical or high-severity advisories are treated differently:

- CRITICAL: Must be patched within **48 hours** regardless of freeze windows
- HIGH: Must be patched within **7 days**
- MEDIUM/LOW: Normal cadence, next sprint

GitHub Security Alerts ping `#platform-security`. If you see one there, don't ignore it.

## Major Version Upgrades

For major upgrades of foundational deps (Node.js runtime, Python version, Terraform, EKS Kubernetes version):

1. File a migration ticket in `PLATINFRA` 30 days before the target date
2. Test in `sandbox` first, then `staging` with a 1-week bake time
3. Coordinate with affected teams if the upgrade changes any shared interface
4. Upgrade `prod` during a change window (see `change-management-rules.md`)

## Lock Files

- Lock files (`package-lock.json`, `Pipfile.lock`, `go.sum`) MUST be committed
- PRs that delete lock files without explanation are blocked
- Never use `--no-lock` or equivalent flags in production builds

## Related

- `change-management-rules.md`
- `code-review-rules.md`
- `../runbooks/dependency-incident.md`
