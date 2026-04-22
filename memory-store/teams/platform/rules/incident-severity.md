# Incident Severity Levels — Platform Team

Platform owns the pipeline and shared infra, so our severity definitions are tuned to reflect infrastructure blast radius, not just user-facing impact.

---

## SEV-1 — Critical

**Page immediately. All hands if needed.**

Examples:
- Deploy pipeline fully down (no deploys possible for any team)
- Production database unreachable for >5 minutes
- Secret store (Vault) unavailable
- Cluster-level networking failure affecting multiple services

Response:
- Acknowledge within 5 min
- Incident commander role assigned within 10 min
- Status page update within 15 min
- Postmortem required within 48h

---

## SEV-2 — High

**Page primary on-call. Secondary on standby.**

Examples:
- Single-service deploy broken (blocking one team's releases)
- Metrics / alerting pipeline degraded
- Non-secret config store flapping
- Canary analysis producing bad data

Response:
- Acknowledge within 10 min
- Status update in `#incidents` within 20 min
- Postmortem required if >1h to resolve or if recurrence within 7 days

---

## SEV-3 — Medium

**Notify on-call via Slack. No page.**

Examples:
- Deployment slower than usual (but succeeding)
- Non-critical dashboard broken
- Alert firing that's known-flaky (tracked in `runbooks/flaky-alerts.md`)

Response:
- Acknowledge within 2 hours during business hours
- Ticket created and triaged same day

---

## SEV-4 — Low / Informational

Log it in the backlog. No urgency.

---

## Severity Escalation

When in doubt, escalate up. It's cheaper to declare a false SEV-1 than to under-respond to a real one.

Any team member can raise severity; only the incident commander can lower it.

## Related Docs

- `on-call-rotation.md`
- `../runbooks/incident-response.md`
- `../postmortems/`
