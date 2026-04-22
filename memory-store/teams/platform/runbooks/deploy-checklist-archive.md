# Deploy Checklist Archive

> This file archives retired deploy checklists. These are kept for audit and post-mortem reference. For the current checklist, see `deploy.md` (the canonical deploy runbook in this directory).

---

## Checklist v3 (Used: 2024-03-01 to 2024-08-31)

This checklist was in use during the monolith-to-services migration period.

### Pre-Deploy
- [ ] Announce in #deploys with expected services and SHAs
- [ ] Confirm DB migration backward compatibility reviewed
- [ ] Verify staging deploy passed within last 4 hours
- [ ] Check active incidents — no P0/P1 open
- [ ] Confirm cache warm-up script is ready if needed (`scripts/cache-warmup.sh`)

### During Deploy
- [ ] Monitor error rate per service (thresholds: api < 1%, gateway < 0.5%, worker < 2%)
- [ ] Watch Kafka lag during worker deploy
- [ ] Spot-check three synthetic transactions post-deploy

### Post-Deploy
- [ ] 15-minute observation period before closing deploy ticket
- [ ] Update deploy log in `../deploys/log.csv`
- [ ] Close staging environment freeze

---

## Checklist v2 (Used: 2023-07-15 to 2024-02-28)

Pre-migration, single-artifact deploys only.

### Pre-Deploy
- [ ] Maintenance window scheduled and announced
- [ ] Rollback plan documented in deploy ticket
- [ ] DBA signed off on any schema changes
- [ ] Load balancer health checks verified manually

### During Deploy
- [ ] Watch application logs on `mono-api-prod-01` (primary canary)
- [ ] Confirm `/healthz` returns 200 before marking complete

### Post-Deploy
- [ ] Send all-clear in #platform channel
- [ ] Archive deploy artifact SHA in Confluence (pre-2024 process)

---

## Notes on Checklist Evolution

The shift from v2 to v3 happened when we moved to Kubernetes rolling deploys. The shift from v3 to the current process happened when we introduced the `just` CLI and automated most of the manual verification steps. Key lessons from the v2/v3 era:
- Manual load balancer health checks caused two incidents when engineers forgot to re-enable them post-deploy.
- The 15-minute observation window was added after the 2024-04-12 incident (`../incidents/2024-04-12-api-regression.md`).
