# On-Call Rotation — Platform Team

## Schedule

Rotation is weekly, Monday 09:00 → Monday 09:00 (local to the primary's timezone, which must be communicated in the handoff message).

Current rotation order (update when personnel change):

1. Priya
2. Dae-jung
3. Margaux
4. Tobias
5. Lena

Rotation is managed in PagerDuty under the `platform-primary` escalation policy.

## Responsibilities During On-Call Week

- **Acknowledge** pages within 5 minutes (hard limit)
- **Triage** within 15 minutes — even if just "looking into it" in the incident channel
- **Escalate** to secondary if you haven't made progress in 30 minutes on a SEV-1
- Own the postmortem draft for any SEV-1 or SEV-2 that fires on your watch
- Review and merge any pending infra PRs at least once per day

## Handoff Protocol

On Sunday evening, the outgoing on-call drops a handoff note in `#platform-oncall` with:

```
Handoff — [DATE]
Open incidents: <list or "none">
Watching: <anything that's been noisy but hasn't paged>
Notes: <anything the next person should know>
```

## Escalation Path

```
Primary on-call
  → Secondary on-call (same rotation, next in list)
    → Platform lead (Margaux)
      → Engineering Director (Soren)
```

## Compensation

Follow HR policy doc `../../hr/oncall-comp.md`. TL;DR: weekday pages after 21:00 local count as after-hours; weekend pages have a flat bonus regardless of time.

## Shadow Rotations

New team members shadow for two full rotations before going primary. Coordinate with the platform lead to schedule.

## Related

- `incident-severity.md`
- `../runbooks/escalation.md`
