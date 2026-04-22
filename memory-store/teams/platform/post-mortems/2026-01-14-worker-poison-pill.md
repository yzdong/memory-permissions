# 2026-01-14 Worker Poison-Pill Message Loop

## Summary

A malformed message on the `invoice-generation` Kafka topic caused the `worker` service to crash-loop for 2 hours 41 minutes. The consumer committed offsets only on successful processing, so the same message was retried on every pod restart.

## Timeline

| Time (UTC) | Event |
|---|---|
| 07:30 | Malformed invoice event published by upstream billing service (invalid UTF-8 in `line_items` field) |
| 07:31 | `worker` consumer throws `UnicodeDecodeError`; pod crashes |
| 07:31 | Kubernetes restarts pod; same message reprocessed; pod crashes again |
| 07:31–09:52 | Crash loop: 94 pod restarts |
| 09:52 | On-call (Leila) identifies poison pill via log pattern matching |
| 09:58 | Message skipped manually by advancing consumer group offset |
| 10:12 | Worker stable; queue drained |

## Root Cause

The `invoice-generation` consumer had no dead-letter queue (DLQ) and no maximum retry count. Any message that causes an unhandled exception will be retried indefinitely. The malformed message originated from a bug in the billing service's encoding layer (separate team, separate incident).

The worker's crash-loop also prevented processing of the 12,000 messages queued behind the poison pill.

## Impact

- 2 h 41 min of `invoice-generation` consumer downtime
- ~12,000 invoice jobs delayed; all processed within 35 min of recovery
- No invoices lost; no double-sends (idempotency key checked on delivery)
- Billing team notified of encoding bug separately

## Action Items

- [ ] **P0** Implement DLQ for all `worker` Kafka consumers; route after 3 failed attempts — owner: Leila, due 2026-01-21
- [ ] **P0** Add schema validation at consumer ingress; log and DLQ malformed messages without crashing — owner: Tomás, due 2026-01-21
- [ ] **P1** Alert on DLQ depth > 0 within 5 minutes — owner: Damien, due 2026-01-24
- [ ] **P1** Cross-team: file issue with billing team to add encoding validation pre-publish
- [ ] **P2** Document DLQ ops procedure in `runbooks/kafka-consumer-ops.md`
