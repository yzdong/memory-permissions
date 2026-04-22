# billing-legacy Operational Runbook

`billing-legacy` is the old Java billing service running on `billing-app-01.internal` and `billing-app-02.internal`. It's scheduled for decommission in 2025-Q3 (Jira: PLAT-890). For deploy procedure, see `deploy-legacy-2024.md`.

## Service layout

```
billing-app-01.internal  (primary, receives all writes)
billing-app-02.internal  (warm standby, serves read traffic)
  │
billing-db.internal (Postgres 12 — NOT the shared Postgres cluster)
  │
billing-redis.internal (standalone Redis, NOT the shared cluster)
```

This service has its own database and Redis — don't confuse them with platform shared infra.

## Common issues

### JVM OutOfMemoryError

Symptom: service unresponsive, logs show `java.lang.OutOfMemoryError: Java heap space`.

```bash
ssh billing-app-01.internal
# Check if process is alive
pgrep -f billing-legacy
# Restart if dead
sudo systemctl restart billing-legacy
# View recent logs
journalctl -u billing-legacy -n 200
```

Heap is set to `-Xmx4g` in `/etc/billing-legacy/jvm.options`. If OOM is recurring, check for memory leaks (thread dump first):

```bash
# Get thread dump
jcmd $(pgrep -f billing-legacy) Thread.print > /tmp/billing-threaddump-$(date +%s).txt
```

Send the dump to the billing team — platform doesn't own the code.

### High database connection count

Billing-db has `max_connections = 50` (yes, very low). If billing service can't connect:

```bash
ssh billing-app-01.internal
psql -h billing-db.internal -U billing -c "SELECT count(*) FROM pg_stat_activity;"
```

If >45 connections, something is leaking. Restarting `billing-legacy` on both app servers will release connections.

### Invoice processing stuck

Billing uses a cron-based job table. Check for stuck jobs:

```sql
SELECT id, status, started_at, job_type
FROM billing_jobs
WHERE status = 'running'
  AND started_at < now() - interval '1 hour';
```

Stuck jobs can usually be reset to `pending` status — but check with the billing team before doing so for invoice generation jobs.

## Alerting

Billing-legacy alerts route to `#billing-oncall`, not `#platform-oncall`. If you're paged for billing-legacy, confirm with the billing team before making changes.

## Logs

Logs are on the app servers at `/var/log/billing-legacy/app.log` (not in Kubernetes, not in Datadog). Access requires the `billing-app-ssh` bastion role.
