# Change Management — Platform Team

## What Counts as a Change

Any modification to production infra or the deploy pipeline is a change, including:
- Terraform applies to production
- Configuration changes to shared services (Vault, CI runners, monitoring)
- Network or firewall rule modifications
- IAM policy modifications

Code deploys to product services are managed by the deploy pipeline, not this process.

## Change Categories

### Standard Changes
Well-understood, low-risk changes with documented runbooks. Examples: cert rotation, updating a runner AMI. Can proceed during business hours with one reviewer.

### Non-Standard Changes
Anything not in the standard change library. Requires:
- PR with plan/description
- Two reviewers, one being a Platform Lead
- Change window coordination (no non-standard changes on Fridays)

### Emergency Changes
Required to resolve an active SEV-1 or SEV-2. Can bypass normal gates but must be documented retroactively within 24 hours in `ops/emergency-changes.md`.

## Change Communication

Post to `#platform-changes` before starting any non-standard change:

```
**Change:** <brief description>
**Start time:** <ISO timestamp>
**Expected duration:** <estimate>
**Rollback plan:** <one sentence or 'see <runbook>'>
**Impact:** <what teams/services might be affected>
```

## Post-Change Verification

- Monitor dashboards for 30 minutes after any non-standard change.
- Confirm with affected teams that their services are healthy.
- Update the change ticket with the outcome.

## Change Freeze

Same windows as deploy pipeline policy. See `deploy-pipeline-policy.md`.
