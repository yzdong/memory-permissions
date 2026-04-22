# Incident Retrospective Process

This is the program-level playbook for how we run retros, not the runbook for a specific incident. See individual incident docs in `incidents/` for specifics.

## Philosophy

Retros are blameless. If the writeup assigns fault to a person rather than a system or process, it gets sent back. We're looking for: what conditions made this possible, and how do we make recurrence harder?

## Severity Thresholds for Required Retros

| Severity | Retro Required | Timeline |
|---|---|---|
| P1 (customer-impacting, major) | Always | Within 5 business days |
| P2 (customer-impacting, minor) | Always | Within 10 business days |
| P3 (internal only, no SLO breach) | If novel | Within 2 weeks, optional |
| P4 | No | — |

## Retro Document Structure

Use the template at `templates/incident-retro-template.md`.

Required sections:
1. **Incident summary** — 2–3 sentences, non-technical audience should understand it
2. **Timeline** — UTC timestamps, what happened and who noticed
3. **Root cause(s)** — can be multiple; use "contributing factors" framing
4. **Impact** — duration, affected users/services, SLO breach details
5. **What went well** — seriously include this; it's not just fluff
6. **What went poorly** — detection time, response time, communication gaps
7. **Action items** — owner, due date, and a Jira ticket for each

## The Retro Meeting

- Scheduled within 48h of incident resolution
- Facilitator: ideally someone NOT in the incident response (less defensive)
- Attendees: everyone who was paged, plus the service team if it wasn't Platform's service
- Duration: 45–60 min for P1, 30 min for P2
- Notes taken live in the retro doc

## Action Item Tracking

Action items land in the `platform` Jira project with label `retro-action`. Platform lead reviews these weekly — they're not allowed to sit unassigned.

## Trend Review

Every quarter, Platform lead reviews all retros from the quarter:
- Recurring themes → candidate for a project, not just a ticket
- High-severity count by service → flag for that service's team
- Detection time trends → are alerts getting better or worse?

Summary goes into the quarterly platform review slide deck.
