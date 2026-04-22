# Dependency Update Policy — Platform Team

## Motivation

Stale dependencies are a security risk and a tech debt source. Platform sets the standard for how regularly we stay current — other teams look to us.

## Dependabot Configuration

All Platform repos have Dependabot enabled. Config is templated from `infra-tooling/dependabot-template.yaml`.

- **npm/pip/go:** weekly PR generation, patch and minor bumps only auto-raised.
- **GitHub Actions:** monthly.
- **Terraform providers:** monthly.
- **Docker base images:** weekly.

## Merge Policy by Bump Type

| Bump Type | Auto-merge Eligible | Review Required |
|-----------|--------------------|-----------------|
| Patch | Yes (after CI green) | No |
| Minor | No | 1 reviewer |
| Major | No | 2 reviewers + changelog review |

Major bumps require the reviewer to read the upstream changelog and note any breaking changes in the PR description.

## Security Advisories

If Dependabot or Snyk raises a **high or critical** advisory:

1. A P2 ticket is auto-created in Jira.
2. The on-call engineer must triage within **24 hours**.
3. Remediation (update or mitigating control) must be in place within **7 days** for high, **48 hours** for critical.

This is non-negotiable regardless of sprint priorities.

## Blocking Updates

If a dependency update breaks something and can't be immediately fixed:

1. Pin to the last known-good version with a comment explaining why.
2. Create a ticket to resolve the block within the next sprint.
3. Do not leave unexplained version pins — they accumulate and become impossible to clear.

## Internal Packages

For packages published internally (e.g., `@acme/platform-sdk`), follow semantic versioning strictly. Patch bumps should never contain behavior changes. Violations cause other teams' auto-merges to break unexpectedly.
