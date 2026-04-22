# Incident: Feature Backfill Failure — 2024-10-14

**Severity:** P2  
**Duration:** ~6 hours (02:15–08:40 UTC)  
**Affected system:** `rec_data_cleaning_daily` DAG, `fs.interaction_log`  
**Reported by:** Marta S. (on-call)

---

## Timeline

| Time (UTC) | Event |
|---|---|
| 02:00 | Nightly DAG kicked off as scheduled |
| 02:15 | `mask_pii` task failed: Vault connection refused |
| 02:16 | Airflow retried 3× with 5-min backoff — all failed |
| 02:31 | Airflow marked DAG run as failed |
| 04:00 | On-call paged by Datadog alert (feature store lag > 36 h SLA breach) |
| 04:12 | Marta confirmed Vault was in sealed state after an unrelated cert rotation |
| 05:30 | Infra unsealed Vault; confirmed PII hash key accessible |
| 06:00 | Manually triggered backfill for the failed date partition |
| 08:40 | `fs.interaction_log` partition for 2024-10-14 confirmed complete |

---

## Root Cause

The Infra team rotated TLS certificates on the Vault cluster at ~01:50 UTC. The rotation caused Vault to auto-seal as a safety measure. The ML data pipeline was not informed of this maintenance window, and there was no retry logic beyond Airflow's 3-attempt default.

## Impact

- Training job scheduled for 06:00 UTC was delayed by ~3 hours while the backfill completed.
- No model was retrained on stale data — the job queued and picked up fresh data.
- No user-facing impact.

## Action Items

- [ ] Infra to add ML pipeline team to Vault maintenance notifications (**owner: Devon K., due 2024-10-21**)
- [ ] Add longer retry window to `mask_pii` task with exponential backoff up to 2 hours (**owner: Priya T., due 2024-10-28**)
- [ ] Document Vault seal recovery in `runbooks/vault-seal-recovery.md` (**owner: Marta S., due 2024-10-25**)
- [ ] Evaluate whether `mask_pii` can use a cached key for a short window during Vault outages (**owner: team, due 2024-11-08**)

## Related Docs
- `data-cleaning-pipeline.md`
- `feature-store-schema.md`
