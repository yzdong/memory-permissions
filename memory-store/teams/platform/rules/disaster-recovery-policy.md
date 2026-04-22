# Disaster Recovery Policy — Platform Team

## Scope

This policy covers Platform-owned systems: the deploy pipeline, secrets infrastructure, CI runners, and shared monitoring stack. Product service DR is the responsibility of each product team — see `../../product/runbooks/dr.md`.

## Recovery Objectives

| System | RTO | RPO |
|--------|-----|-----|
| Deploy pipeline | 2 hours | 1 hour |
| Vault cluster | 30 minutes | Near-zero (raft replication) |
| CI runners | 1 hour | N/A (stateless) |
| Terraform state | 4 hours | 1 hour |
| Monitoring stack | 4 hours | 6 hours |

## Backup Strategy

- Vault: Raft snapshots every 15 minutes, stored in `acme-platform-prod-s3-backups` with 30-day retention.
- Terraform state: S3 versioning with 90-day retention.
- CI runner configs: stored as code, restore is a Terraform apply.
- Monitoring config (dashboards, alert rules): exported to `ops/monitoring-backups/` weekly.

## DR Test Schedule

DR tests are conducted every **6 months**. Results are documented in `ops/dr-tests/`. The next scheduled test is noted in the team calendar.

A DR test covers:
1. Vault restoration from snapshot
2. Deploy pipeline rebuild from scratch in a clean account
3. State recovery from S3 versioning

## Multi-Region Considerations

Current production infra is single-region (us-east-1) with cross-region backups (us-west-2). Full multi-region active/active is on the roadmap but not current state — do not promise it to other teams.

## Declaring a Disaster

A "disaster" (invoking DR procedures) is declared by the Platform Lead when RTO for a critical system is at risk. This is distinct from a normal SEV-1, which follows `incident-severity.md`.
