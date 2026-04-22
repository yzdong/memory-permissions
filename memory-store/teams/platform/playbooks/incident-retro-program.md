# Incident Retrospective Program Playbook

This describes how Platform facilitates the post-incident review (PIR) process for platform-owned incidents, and how we make sure action items actually get done.

## Scope
This playbook covers Sev1 and Sev2 incidents where Platform's infrastructure was a contributing factor. Service teams run their own PIRs for application-layer issues.

## Timeline expectations

| Severity | Draft PIR due | PIR published |
|----------|---------------|---------------|
| Sev1     | 48 hours      | 5 business days |
| Sev2     | 5 business days | 10 business days |

These are tight on purpose. Memory fades fast.

## PIR structure

Use the template at `templates/pir-template.md`. Sections:
1. **Summary** — one paragraph, written for someone who wasn't on-call
2. **Timeline** — timestamped, factual, no blame framing
3. **Contributing factors** — use the 5-whys approach; stop when you hit organizational or systemic causes
4. **Impact** — duration, affected services, user impact (error counts, not just percentages)
5. **What went well** — this section is mandatory, not optional
6. **Action items** — each item has an owner and a due date

## Facilitating the review meeting
- Keep it to 45 minutes
- The facilitator is not the incident commander — get a different person
- No blame, no "you should have" — redirect if it goes there
- Focus on system design, not individual decisions

## Action item tracking

Action items go into the Platform Jira board under the PIR epic. We review open PIR actions in the weekly Platform sync.

Items that slip past their due date get escalated to the Platform lead. If an item is genuinely lower priority than other work, say so and re-date it — don't leave it silently stale.

## Trend analysis

Every quarter, review all PIRs from the prior quarter (`docs/pirs/`) and look for patterns:
- Repeated contributing factors → systemic issue, needs a project
- Action items that keep getting re-opened → original fix was wrong or insufficient

Publish a quarterly trends summary in `docs/platform-reliability-trends-YYYY-QN.md`.
