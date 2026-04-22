# Platform Team Member Offboarding Playbook

For when someone leaves the Platform team, whether by departure, transfer, or role change. Timing matters here — don't let this slip until the last day.

## Start this process 2 weeks before their last day

## Knowledge transfer

The departing engineer should document or hand off:
- [ ] Any services or systems they are the primary expert on — list them explicitly
- [ ] Ongoing projects that aren't finished (create handoff tickets with enough context)
- [ ] Vendor relationships they manage personally — intro their successor to the vendor contact
- [ ] Any ad-hoc scripts or tooling they maintain that aren't in the standard repo paths
- [ ] Anything they know that "everyone assumes someone else documented" — this is always something

Schedule at least two knowledge transfer sessions with their replacement/team.

## Access revocation

Coordinate with IT. Platform-specific items:
- [ ] Remove from PagerDuty rotation (end of their current shift, not mid-shift)
- [ ] Revoke Terraform Cloud team membership
- [ ] Remove from `platform-owners` IAM group
- [ ] Remove SSH public key from bastion authorized_keys
- [ ] Remove from Vault admin policy
- [ ] Remove from GitHub `platform-team` group
- [ ] Update `oncall/schedule.yaml`

For departures (not internal transfers): also remove from the platform-internal Slack channel and shared 1Password vault.

## Code & ownership
- Update `CODEOWNERS` file to reassign their files
- Check for open PRs — either close them with a note or transfer ownership
- Check for any Terraform workspaces locked under their user token

## Communication
- Post a farewell message in #platform (the person leaving should do this if they want to; don't force it)
- Notify teams that relied on the departing engineer for regular touchpoints
- Update the team roster doc at `docs/team-roster.md`

## After they're gone
- Audit all access revocations were completed within 24 hours of departure
- File an IT ticket if anything was missed
