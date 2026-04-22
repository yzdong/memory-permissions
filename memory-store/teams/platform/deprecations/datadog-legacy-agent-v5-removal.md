# Datadog Legacy Agent v5 Removal

**Status:** Removed  
**Completed:** 2025-01-20  
**Owner:** Platform Observability

## What Happened

We had a handful of long-lived EC2 instances still running Datadog Agent v5 (the Python-based agent). The rest of the fleet had been on Agent v7 for years. These stragglers were original infrastructure nodes that predated our Ansible automation and had been manually provisioned.

Agent v5 had been silently missing several metric types and completely lacked support for the newer Datadog integrations we use. Some gaps we noticed:
- No OTLP ingest support
- Missing process-level metrics for our Python workers (needed for memory profiling)
- No support for Dynamic Instrumentation

## What We Did

1. Identified remaining v5 hosts with:
   ```bash
   ansible all -m shell -a "datadog-agent version 2>/dev/null || dd-agent info 2>/dev/null | head -1" | grep -B1 '5\.'
   ```
2. Found 7 hosts: 4 in `dc-west-2` (decommission candidates anyway), 3 in `aws-prod`
3. Upgraded the 3 AWS hosts via Ansible role `roles/datadog-agent` (already handles v7 install)
4. Decommissioned the `dc-west-2` hosts as part of the data center wind-down

## Config Differences

Agent v7 config lives at `/etc/datadog-agent/datadog.yaml`. Agent v5 config was at `/etc/dd-agent/datadog.conf`. Some integrations changed config format significantly — check `roles/datadog-agent/templates/` for the current templates.

## Gotchas

- Agent v7 runs as `dd-agent` user by default; v5 ran as root on our older hosts. Make sure log files the agent reads have appropriate permissions.
- Custom check scripts from v5 (`/etc/dd-agent/checks.d/`) need to be tested with v7 — the API changed slightly for custom check classes.

## References

- `infra/ansible/roles/datadog-agent/README.md`
- `runbooks/observability-setup.md`
