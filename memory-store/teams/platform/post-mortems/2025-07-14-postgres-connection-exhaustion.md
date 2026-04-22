# 2025-07-14 Postgres Connection Exhaustion

## Summary

Between 14:22 and 15:47 UTC, the `api` service began rejecting requests with `FATAL: remaining connection slots are reserved for non-replication superuser connections`. PgBouncer was misconfigured after a routine infra change, causing it to bypass pool limits and exhaust the 200-connection ceiling on the primary Postgres instance.

## Timeline

| Time (UTC) | Event |
|---|---|
| 13:55 | Platform engineer merges PgBouncer config update to reduce idle timeouts |
| 14:22 | `api` error rate crosses 5%; on-call paged |
| 14:31 | Initial hypothesis: slow query backlog; DBA begins investigation |
| 14:48 | Connection count confirmed at 199/200 on primary |
| 15:02 | PgBouncer config identified as root cause; rollback initiated |
| 15:19 | Rollback deployed; connection count drops to ~45 |
| 15:47 | Error rate returns to baseline; incident closed |

## Root Cause

The PgBouncer config change set `pool_mode = session` instead of `pool_mode = transaction` for the `api` pool. Session mode holds connections open for the life of a client session rather than returning them to the pool between queries. Under normal traffic, this caused the effective connection count to grow linearly with active API workers.

Relevant config diff is preserved at `infra/pgbouncer/2025-07-14-bad-config.diff`.

## Impact

- ~82 minutes of elevated error rates on `api` (peak 34% 5xx)
- `worker` service unaffected (uses a separate PgBouncer pool)
- Approximately 14,000 failed requests during the window
- No data loss or corruption

## Action Items

- [ ] **Platform** Add integration test that validates PgBouncer pool mode is `transaction` for all service pools before merge — owner: @dana, due 2025-07-28
- [ ] **Platform** Add Datadog alert when active Postgres connections exceed 150 (was 190, too late) — owner: @ryo, due 2025-07-21
- [ ] **Platform** Document PgBouncer config change process in `runbooks/pgbouncer-config.md` — owner: @dana, due 2025-08-01
- [ ] **DBA** Review whether 200 connection limit is still appropriate given current fleet size — owner: @priya, due 2025-07-31
