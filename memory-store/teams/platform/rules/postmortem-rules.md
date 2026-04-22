# Postmortem Rules — Platform Team

Postmortems are how we get smarter. They are blameless by policy and required by process.

## When a Postmortem Is Required

- All SEV-1 incidents
- All SEV-2 incidents that took longer than 1 hour to resolve
- Any SEV-2 that recurs within 30 days
- Any incident where a mitigation step caused a secondary incident

SEV-3 incidents get a lightweight retro note in the weekly sync — not a full postmortem.

## Timeline

| Step | Deadline |
|------|----------|
| Draft started | Within 24h of incident close |
| Draft circulated for comment | Within 48h |
| Final doc published | Within 5 business days |
| Action items assigned | Same day as publish |

## Template

Use `../templates/postmortem-template.md`. Required sections:

1. **Summary** (2–3 sentences, readable by anyone)
2. **Timeline** (UTC timestamps, what happened, what we did)
3. **Root cause** (the thing we could fix, not the person who made a mistake)
4. **Contributing factors**
5. **What went well** (seriously, include this)
6. **Action items** (owner + due date for each)

## Blameless Policy

Postmortems name systems, configurations, and processes — not people. If a reviewer finds personal blame language in a draft, they should flag it for revision, not just note it.

This is a no-exceptions policy. Escalate to the platform lead if there's pushback.

## Action Item Tracking

Action items go into Jira under `PLATPM` with the incident ID in the title. They are reviewed in every weekly platform sync until closed.

An action item with no progress for 3 weeks gets escalated to the platform lead.

## Publishing

Publish the final postmortem to `../postmortems/{YYYY-MM-DD}-{slug}.md` and post a link in `#platform-oncall` and `#incidents`.

## Related

- `incident-severity.md`
- `on-call-rotation.md`
- `../templates/postmortem-template.md`
