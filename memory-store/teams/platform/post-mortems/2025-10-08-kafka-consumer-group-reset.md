# 2025-10-08 Kafka Consumer Group Offset Reset

## Summary

A miscommunication between Platform and the Data Engineering team led to a consumer group offset being reset to earliest on the `user-events` topic. The `worker` service reprocessed ~6 hours of historical events, triggering duplicate notifications and incorrect analytics counts.

## Timeline

- **10:30** — Data Engineering requests help diagnosing consumer lag on `user-events`
- **10:47** — Platform engineer resets offsets to `earliest` on what was believed to be a staging consumer group
- **10:49** — `worker` begins reprocessing; notification volume spikes 40x
- **10:52** — Users start reporting duplicate emails and push notifications
- **10:55** — Platform on-call identifies the consumer group as production
- **11:01** — Consumer group paused; offset fast-forwarded to latest
- **11:14** — Reprocessing stops; notification queue drains
- **11:40** — Duplicate notification suppression confirmed working for remaining queued items

## Root Cause

The consumer group naming convention in staging mirrors production with only a `-staging` suffix. The engineer ran `kafka-consumer-groups.sh --reset-offsets` against `user-events-processor` (production) instead of `user-events-processor-staging`. There is no confirmation step or environment tag in the CLI output to disambiguate.

## Impact

- ~18,000 users received duplicate notifications (email and/or push)
- Analytics dashboards overcounted events for a 6-hour window; corrected by Data Engineering the following day
- No data loss; no financial impact
- Customer trust impact: support ticket volume up 3x for ~4 hours

## Action Items

- [ ] Enforce naming convention: production consumer groups must include `-prod-` infix — owner: @farah, due 2025-10-20
- [ ] Wrap `kafka-consumer-groups.sh` reset in a platform CLI subcommand that requires explicit `--env production` flag and shows a diff before applying — owner: @ryo, due 2025-11-01
- [ ] Add idempotency checks to notification dispatch in `worker` — owner: Notifications team, due 2025-11-15
- [ ] Document offset reset procedure in `runbooks/kafka-operations.md`
- [ ] Retrospective with Data Engineering on cross-team Kafka access patterns
