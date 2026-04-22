# On-Call Rotation Setup Playbook

For when we add a new engineer to the on-call rotation, spin up a new rotation, or restructure coverage.

## Adding a new engineer to rotation

### Prerequisites
- Engineer has completed shadow on-call (at least 1 full week, shadowing an experienced on-caller)
- Has working PagerDuty access and mobile app configured
- Has read `runbooks/` top-level index and worked through at least 3 runbooks hands-on in staging
- Platform lead has signed off on readiness

### PagerDuty steps
1. Add user to PagerDuty team: Platform > Members > Add
2. Add to the primary escalation policy (don't skip the escalation path — it's there for a reason)
3. Insert into rotation schedule — prefer inserting at the end of the current cycle to avoid disruption
4. Test by sending a test alert and confirming they can acknowledge and resolve

### Tooling access
- Ensure `kubectl` access to production namespace (ops-access group in IAM)
- Terraform Cloud team membership
- Read access to all service dashboards in Grafana
- SSH key added for bastion access (follow `runbooks/bastion-access.md`)

## Restructuring a rotation

Common reasons: team size change, adding a secondary rotation, moving to follow-the-sun.

**Things to check before restructuring:**
- Existing on-call schedule has no gaps (verify in PagerDuty timeline view)
- Notify affected engineers at least 2 weeks in advance
- Update `oncall/schedule.yaml` in the infra repo so our tooling reflects reality

## Off-boarding from on-call

- Remove from PagerDuty schedule at the end of their current shift
- Update `oncall/schedule.yaml`
- Revoke elevated production access if they're leaving the team (coordinate with IT)
- Document any institutional knowledge they held in the relevant runbooks before they leave

## Related
- `runbooks/escalation-paths.md`
- `../oncall/change-windows.md`
