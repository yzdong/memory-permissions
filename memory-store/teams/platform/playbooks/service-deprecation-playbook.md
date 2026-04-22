# Service Deprecation Playbook

When a service is being decommissioned — whether it's being replaced, merged into another service, or just shut down — this is the process. Doing this poorly causes ghost resources, orphaned alerts, and surprise bills.

## Deprecation Stages

```
Announced → Traffic Drained → Compute Stopped → Resources Deleted → Audit Complete
```

Each stage requires explicit sign-off. No skipping.

## Stage 1: Announcement (T-30 days minimum)

- Post in `#engineering-announcements` with: service name, reason, timeline, migration path (if any), and who to contact with questions
- Update the service catalog (`docs/service-catalog.md`) — mark status as `DEPRECATED`
- Add a deprecation header to the service's own README
- If the service has external callers, coordinate with them — Platform is not responsible for breaking partners silently

## Stage 2: Traffic Draining

- Move traffic gradually: 100% → 50% → 10% → 0% over at least 7 days
- Watch metrics at each step — if you see downstream errors, stop and investigate
- Remove from load balancer target group last, not first
- Keep the service running (just at 0% traffic) for 72h after full drain to confirm no hidden callers

```bash
# Check for any remaining callers in access logs
python scripts/deprecation/check-callers.py \
  --service <service-name> \
  --lookback-hours 72
```

## Stage 3: Compute Shutdown

- Scale ECS service to 0
- Do NOT delete the ECS service definition yet
- Wait 7 days — this catches weekly batch jobs that only run on certain days
- Disable CloudWatch alarms (don't delete — use for audit trail)

## Stage 4: Resource Deletion

Order matters:
1. Delete ECS service + task definitions
2. Deregister from service mesh / Consul
3. Remove from `pipeline/services.yaml` (stops CI runs)
4. Delete load balancer target group and listener rules
5. Remove security group rules pointing to the service
6. Delete RDS/ElastiCache resources (take a final snapshot first, labeled `final-<service>-<date>`)
7. Delete S3 buckets (verify empty or archive contents first)
8. Remove IAM roles and policies for the service
9. Remove Terraform resources (last — they track what we've already done)
10. Remove DNS records

## Stage 5: Audit and Cleanup

```bash
# Verify no orphaned resources tagged with the service name
python scripts/deprecation/orphan-scan.py --service-tag <service-name>
```

- Update `docs/service-catalog.md` to `DECOMMISSIONED` with date
- Archive the service repo (don't delete — code history is useful)
- Remove from Datadog dashboards and alert policies
- Write a one-paragraph deprecation summary and link it from the service's final commit

## Common Mistakes

- Deleting the IAM role before rotating credentials — check for any long-lived access keys first
- Forgetting to remove from health check endpoints — dead services in health checks cause false alerts
- Not checking CloudWatch scheduled events that invoke the service via Lambda
