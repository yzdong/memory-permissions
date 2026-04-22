# Database Migration Playbook

Covers schema migrations and major data migrations on production databases. This is not the place for "add an index" — this is for changes with real risk: table renames, column drops, large backfills, engine upgrades.

## Risk classification

| Change type | Risk | Required review |
|-------------|------|-----------------|
| Add column (nullable) | Low | PR review only |
| Add index (concurrent) | Low–Medium | PR + Platform sign-off |
| Backfill > 10M rows | High | Full migration plan + DBA review |
| Column/table drop | High | Full migration plan |
| Engine version upgrade | High | Vendor runbook + Platform + SRE |

## Pre-migration checklist

- [ ] Migration tested in staging with production-scale data (use anonymized snapshot from `s3://platform-db-snapshots/`)
- [ ] Estimated duration documented — run `EXPLAIN ANALYZE` or time it in staging
- [ ] Rollback procedure written and tested
- [ ] Backups verified fresh (RDS automated backup within last 24h, or trigger a manual snapshot)
- [ ] Application code is backward compatible with both old and new schema during the transition window
- [ ] Change window booked (`../oncall/change-windows.md`)

## Execution

```bash
# Always run with --dry-run first
./scripts/db/run-migration.sh --env production --dry-run --migration migrations/YYYY_NN_description.sql

# Then for real
./scripts/db/run-migration.sh --env production --migration migrations/YYYY_NN_description.sql
```

Monitor during execution:
- RDS CloudWatch: FreeStorageSpace, DatabaseConnections, WriteLatency
- Application error rate in Grafana
- Lock wait events: `SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';`

## Post-migration
- [ ] Verify row counts and spot-check data integrity
- [ ] Remove any backward-compatibility shims in application code (create ticket if not done immediately)
- [ ] Update schema docs in `docs/db-schema/`
- [ ] Log migration in `migrations/history.md` with date, who ran it, and duration

## If something goes wrong
Stop. Don't try to fix it under pressure. Roll back using the procedure you wrote before you started. Escalate to Platform lead if rollback itself looks risky.
