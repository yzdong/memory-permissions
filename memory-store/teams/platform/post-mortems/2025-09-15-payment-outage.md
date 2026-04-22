# 2025-09-15 Payment Processing Outage

## Summary

The payment charge endpoint was unavailable for 47 minutes due to a deadlocked database migration that held a lock on the `orders` table. Charges failed with 500 errors; no double-charges or data corruption occurred.

## Timeline

| Time (UTC) | Event |
|---|---|
| 11:01 | `api` deploy initiated for v2.24.0; migration starts automatically |
| 11:02 | Migration acquires `ACCESS EXCLUSIVE` lock on `orders` |
| 11:03 | Incoming charge requests begin queueing behind lock |
| 11:08 | Connection pool saturates; 503s begin returning to clients |
| 11:14 | PagerDuty fires; Sasha picks up |
| 11:20 | Lock identified via `pg_stat_activity`; migration process found stuck |
| 11:31 | Decision to terminate migration process and roll back deploy |
| 11:48 | Rollback complete; lock released; payment endpoint healthy |

## Root Cause

The migration added an index `CONCURRENTLY` but wrapped it inside an explicit transaction, which is invalid in Postgres — `CREATE INDEX CONCURRENTLY` cannot run inside a transaction block. Postgres silently fell back to a non-concurrent build, acquiring a full table lock. With the `orders` table at ~210 M rows, the lock was held for the entire index build duration.

The migration was tested on a staging dataset of ~400 k rows where the lock duration was sub-second and not noticed.

## Impact

- 47-minute window with ~100% failure rate on `/v1/payments/charge`
- Estimated 3,200 failed payment attempts (all retriable; no revenue lost per payment team)
- No data inconsistency; migration was rolled back cleanly

## Action Items

- [ ] **P0** Add CI lint rule: disallow `CREATE INDEX CONCURRENTLY` inside transaction blocks — owner: Sasha, due 2025-09-19
- [ ] **P0** Migrations must be tested against a dataset ≥ 50 M rows in staging before promotion — owner: Priya, due 2025-09-26
- [ ] **P1** Implement lock-timeout guard (`SET lock_timeout = '3s'`) on all migration connections — owner: Damien, due 2025-10-03
- [ ] **P1** Add pre-deploy migration dry-run step to pipeline — see `runbooks/deploy.md` for pipeline hook docs
- [ ] **P2** Write ADR for long-running migration strategy (shadow tables, pt-online-schema-change, etc.)

## References

- Postgres docs on `CREATE INDEX CONCURRENTLY` limitations
- `../schemas/orders-index-history.md`
