# Incident Response Template

> Copy this file into `incidents/YYYY-MM-DD-<slug>.md` when opening a new incident.
> Do not edit the template itself.

## Incident Metadata

| Field | Value |
|---|---|
| Incident ID | IR-XXXX |
| Severity | P1 / P2 / P3 |
| Declared At | YYYY-MM-DDTHH:MM:SSZ |
| Incident Commander | @handle |
| Comms Lead | @handle |
| Scribe | @handle |

## Summary

_One paragraph. What happened, what was affected, current status._

## Timeline

- `HH:MM` — First alert fired (link to alert)
- `HH:MM` — Incident declared
- `HH:MM` — On-call engineer paged
- `HH:MM` — Root cause hypothesis formed
- `HH:MM` — Mitigation applied
- `HH:MM` — Incident resolved

## Impact

- **Services affected**: list service names
- **User impact**: describe blast radius
- **Data exposure**: yes/no — if yes, loop in `#security-incidents` immediately

## Root Cause

_Fill in after the incident. Link to any relevant PRs or commits._

## Mitigation Steps Taken

1. Step one
2. Step two

## Action Items

| Action | Owner | Due Date | Ticket |
|---|---|---|---|
| Post-mortem written | @ic | +5 business days | |
| Monitoring gap closed | @oncall | +2 weeks | |

## Related Docs

- Post-mortem process: `runbooks/post-mortem.md`
- Escalation contacts: `../escalation-contacts.md`
- PII exposure rules: `../pii-handling.md`
