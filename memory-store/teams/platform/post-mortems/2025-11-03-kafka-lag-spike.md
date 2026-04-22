# 2025-11-03 Kafka Consumer Lag Spike

## Summary

Consumer lag on the `order-events` topic grew to over 2.1 million messages over a 3-hour window, causing delayed order status updates and stale inventory reads. The spike was caused by a slow database query introduced in the same day's `worker` release.

## Timeline

| Time (UTC) | Event |
|---|---|
| 08:00 | `worker` v3.12.0 deployed |
| 08:15 | Consumer lag begins growing (baseline: ~3,000 messages) |
| 09:00 | Lag crosses 500 k; automated alert fires |
| 09:06 | On-call (Tomás) begins investigation |
| 09:35 | Slow query identified: missing index on `inventory.sku_id` |
| 09:50 | Index created concurrently on production |
| 10:18 | Consumer throughput recovers to normal (8,400 msg/s) |
| 11:07 | Lag fully drained; alert cleared |

## Root Cause

A new enrichment step in the `order-events` consumer performs a lookup against the `inventory` table by `sku_id`. The column existed but had no index — previously lookups were by primary key. At normal throughput (~8 k msg/s), each sequential scan took ~220 ms, capping effective consumer throughput at ~4.5 msg/s per partition.

The query wasn't flagged in code review because it looked reasonable, and staging load tests ran against a smaller inventory table where sequential scans were fast enough to pass.

## Impact

- 3-hour lag accumulation peaking at 2.1 M messages
- Order status webhook delays of up to 3 hours for some orders
- Inventory reservation accuracy degraded during the window (stale reads)
- No message loss; full catchup confirmed post-recovery

## Action Items

- [ ] **P0** Require `EXPLAIN ANALYZE` output for any new DB queries in consumer code — owner: Tomás, due 2025-11-10
- [ ] **P0** Load test consumers against production-scale table cardinalities in staging — owner: Leila, due 2025-11-17
- [ ] **P1** Set lag alert threshold lower: 100 k messages (currently 500 k) on `order-events` — owner: Damien, due 2025-11-06
- [ ] **P1** Add consumer throughput SLO dashboard panel — owner: Sasha, due 2025-11-13
- [ ] **P2** Document index review checklist in `runbooks/kafka-consumer-ops.md`

## References

- `../schemas/inventory-table.md` for current index coverage
- Lag graph screenshot archived in incident channel `#inc-2025-11-03`
