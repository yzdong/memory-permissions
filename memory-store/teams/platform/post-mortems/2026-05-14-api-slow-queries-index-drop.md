# 2026-05-14 API Degradation — Accidental Index Drop

## Summary

A developer accidentally dropped a critical index on `orders.user_id` during a migration cleanup. The `api` service's order-listing endpoints degraded from P99 < 80ms to P99 > 12 seconds within minutes. The index was recreated concurrently within 40 minutes, but the recreation itself took 22 minutes on the large table.

## Timeline

- **10:05** — Developer runs `DROP INDEX orders_user_id_idx` in production psql session, believing it to be a duplicate of a newer partial index
- **10:06** — Order listing latency spikes; P99 crosses 2s
- **10:08** — Latency alert fires
- **10:12** — On-call traces slow queries to sequential scans on `orders`
- **10:17** — Missing index identified via `EXPLAIN ANALYZE`
- **10:19** — `CREATE INDEX CONCURRENTLY` initiated
- **10:41** — Index creation complete; query plans revert to index scans
- **10:44** — P99 latency back to < 90ms

## Root Cause

The developer was cleaning up legacy indexes listed in `db/migrations/legacy-index-notes.md`. The document was out of date and listed `orders_user_id_idx` as superseded by `orders_user_id_status_idx` (a partial index). However, `orders_user_id_idx` was still used by 4 query patterns that the partial index didn't cover.

No process exists to validate that an index is truly unused before dropping it.

## Impact

- 36 minutes of severely degraded order listing (P99 12s+)
- Approximately 19,000 slow or timed-out requests
- No data loss
- `worker` unaffected (uses different query patterns)

## Action Items

- [ ] Require `pg_stat_user_indexes.idx_scan` review before any index drop in production — add to `runbooks/schema-migrations.md` — owner: @priya, due 2026-05-21
- [ ] Mark `db/migrations/legacy-index-notes.md` as archived; migrate to automated index usage tracking — owner: @priya, due 2026-06-01
- [ ] Add psql audit logging for DDL statements in production — owner: @dana, due 2026-05-28
- [ ] Investigate read replica query-plan divergence that masked the issue in staging — owner: @priya, due 2026-06-01
