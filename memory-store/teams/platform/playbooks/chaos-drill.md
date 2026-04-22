# Chaos Engineering Drill Playbook

We run chaos drills quarterly. The goal is to validate that our systems degrade gracefully and that our on-call process actually works — not just to break things for fun.

## Scheduling
- Drills are scheduled during business hours (10am–3pm local) with at least 1 week notice to #platform and the affected service teams
- Never run drills during a freeze window (see `../oncall/change-windows.md`)
- Always have a designated safety officer who is not the one running experiments

## Preparation

### 1. Define the hypothesis
Write it down before you start. Example: _"If the payments-cache pod is evicted, the checkout service will serve from the database fallback with < 500ms latency increase and no failed transactions."_

### 2. Define the blast radius
- Which services / namespaces are in scope?
- What's the rollback plan if things go worse than expected?
- What steady-state metrics are we monitoring?

### 3. Notify
- Post in #incidents-drills: date, time, scope, hypothesis, who to contact
- Brief the on-call engineer — they should be watching dashboards during the drill

## Tooling
We use [Chaos Toolkit](https://chaostoolkit.org/) with the Kubernetes extension. Experiment definitions live in `chaos/experiments/`.

```bash
chaos run chaos/experiments/<experiment>.json --var-file chaos/vars/staging.yaml
```

Always run against staging first, then production only if staging results are clean.

## During the drill
- The safety officer monitors Grafana dashboard: `dashboards/chaos-drill-overview.json`
- Abort immediately if error rate exceeds 5% or latency p99 doubles
- Keep a running Slack thread with timestamped observations

## After the drill

### Debrief
- Schedule a 30-min retro within 48 hours
- Did the hypothesis hold? If not, why?
- What surprised us?

### Action items
- File tickets for any resilience gaps found
- Update experiment definitions if they need tuning
- Publish a brief summary in `chaos/reports/YYYY-QN.md`

## Anti-patterns
- Running experiments without a written hypothesis — this is exploration, not a drill
- Skipping staging and going straight to production
- Forgetting to notify the on-call engineer and watching them scramble
