# Code Review Rules — Platform Team

## Overview

Platform reviews are a bit stricter than org defaults on infra-touching PRs, and more lenient on pure tooling changes. This doc captures the team consensus as of the last retro.

## Required Approvals

- **Deploy pipeline changes**: 2 approvals, at least one from a senior platform engineer
- **Shared infra modules** (`infra/modules/`): 2 approvals
- **Runbook updates**: 1 approval, any platform team member
- **Tooling / scripts**: 1 approval, self-merge allowed after 24h if no comments

## What Counts as an Infra Change

Anything touching:
- `infra/`
- `.github/workflows/`
- `terraform/`
- `k8s/base/` or `k8s/overlays/platform/`

If you're unsure, treat it as infra and get 2 eyes on it.

## Review SLAs

| PR type         | First review within | Merge target |
|-----------------|--------------------|--------------|
| Incident fix    | 2 hours            | Same day     |
| Infra change    | 1 business day     | 3 days       |
| Tooling / docs  | 2 business days    | 1 week       |

## Linting Overrides

Platform overrides `no-unused-vars` to **warn** (org default is error). This is intentional — we keep scaffolding stubs around during active infra work. Reviewers should NOT block PRs on unused-var warnings unless they're clearly dead code.

See `../overrides/eslint-platform.json` for the full diff against org defaults.

## Blocking vs. Non-Blocking Comments

- Prefix blocking comments with `[BLOCK]`
- Prefix suggestions with `[NIT]` or `[SUGGEST]`
- Untagged comments are assumed non-blocking

## Stale PR Policy

PRs with no activity for 7 days get a bot reminder. After 14 days, platform-oncall may close with a `stale` label. Re-open is always welcome.

## Related Docs

- `branch-protection.md`
- `../runbooks/deploy.md`
