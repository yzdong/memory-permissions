# Change Management Rules — Platform Team

Not every infra change needs a change ticket, but the ones that do really do. This doc draws the line.

## When a Change Ticket Is Required

- Any modification to production networking (VPC, security groups, load balancers)
- Database schema migrations in production
- Cluster upgrades (EKS control plane or node groups)
- Changes to authentication or authorization infrastructure (Vault policies, IAM roles)
- Deploy pipeline changes that affect all teams
- Any change during or immediately after a freeze window

## When It's Not Required

- Application deploys within normal release process
- Terraform plan/apply with zero resource-level changes (e.g. tag updates)
- Documentation updates
- Alert tuning (threshold adjustments, not routing changes)

## Change Ticket Requirements

Every change ticket must include:

1. **Summary**: What is changing and why
2. **Blast radius**: What could break if this goes wrong
3. **Rollback plan**: Specific commands or steps, not "we'll figure it out"
4. **Test plan**: How you verified in staging
5. **Approval**: At least one platform team member who is NOT the author
6. **Scheduled window**: Proposed time, ideally low-traffic hours (see table below)

## Preferred Change Windows (Production)

| Day           | Preferred window (UTC) |
|---------------|------------------------|
| Tuesday–Thursday | 10:00–14:00         |
| Monday        | Avoid if possible      |
| Friday        | Avoid unless urgent    |
| Weekends      | Emergency only         |

## Emergency Changes

For SEV-1 mitigations, skip the ticket process but document what you did in the incident thread. Create a follow-up ticket within 24h.

## Tracking

Change tickets live in Jira under the `PLATCHANGE` project. Link any relevant PRs to the ticket.

## Related

- `incident-severity.md`
- `branch-protection.md`
- `../runbooks/deploy.md`
