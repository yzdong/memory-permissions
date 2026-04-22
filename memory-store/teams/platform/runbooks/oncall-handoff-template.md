# On-Call Handoff Template

Use this at the start and end of every on-call shift. Fill it out in the `#platform-oncall` Slack channel.

## State at handoff

### Open incidents

List any active or recently-resolved incidents. Link to post-mortem if available.

| Incident | Status | Owner | Notes |
|---|---|---|---|
| | | | |

### Known fragile things

Anything that's in a degraded or watched state:

- _Example: Kafka partition 7 on `worker.jobs` is lagging; being monitored, expected to recover_
- _Example: Redis memory at 78%, below alert threshold but worth watching_

### Pending deploys

Any deploys queued up or in progress that the incoming engineer should know about:

- Service: ____
- Expected window: ____
- Who to contact: ____

### Snoozed alerts

List any alerts that are snoozed and why:

- Alert name: ____
- Snoozed until: ____
- Reason: ____

## Useful quick links

- Grafana: `https://grafana.internal/d/platform-service-health`
- PagerDuty escalation policy: `Platform On-Call Primary`
- Runbook index: `runbooks/README.md`
- Slack channels to monitor: `#platform-alerts`, `#platform-incidents`, `#platform-deploys`

## Shift notes

Free text for anything else the incoming engineer should know:

```
(fill in)
```

## Sign-off

- Outgoing: ____
- Incoming: ____
- Time: ____
