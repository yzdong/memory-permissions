# New Service Onboarding Playbook

This covers what Platform does when a team wants to ship a net-new service. The service team owns their code; we own the infra scaffolding and the deploy pipeline plumbing.

## Prerequisites (service team's responsibility)
- [ ] Architecture review approved (link in ticket)
- [ ] Service name agreed and doesn't conflict (`./scripts/check-name-collision.sh <name>`)
- [ ] SLO targets defined — we need these before we configure alerting

## Platform checklist

### Infra provisioning
- [ ] Create namespace in Kubernetes: `kubectl create namespace <service>`
- [ ] Add namespace to `infra/k8s/namespaces.tf` and open PR
- [ ] Provision service account with least-privilege IAM role
- [ ] Set resource quotas (default template at `templates/resource-quota.yaml`)

### Deploy pipeline
- [ ] Create pipeline config in `.ci/pipelines/<service>.yml` using the standard template
- [ ] Wire up staging and production promotion gates
- [ ] Add the service to `deploy-groups.yaml` under the correct tier (critical / standard / batch)
- [ ] Confirm canary analysis is enabled — **do not skip this for Tier 1 services**

### Observability
- [ ] Grafana dashboard provisioned from `dashboards/service-template.json`
- [ ] PagerDuty service created and escalation policy attached
- [ ] Log sink configured (structured JSON expected; warn the team if they're not doing this)
- [ ] Add to synthetic monitoring if the service has public endpoints

### Secrets
- [ ] Vault path created: `secret/platform/<env>/<service>/`
- [ ] Rotation schedule set (90-day default, 30-day for anything touching payment data)

### Runbook
The service team must create their own runbook in their repo. Point them at `docs/runbook-template.md`.

## Handoff
Once all boxes are checked, close the onboarding ticket and post a summary in #deployments. Tag the service team's on-call so they know they're live.
