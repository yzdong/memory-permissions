# 2026-04-02 Worker Silent Data Loss — Webhook Events

## Summary

For approximately 6 hours on 2026-04-02, the `worker` service silently dropped webhook delivery events instead of retrying them. A try/except block swallowed `ConnectionTimeout` exceptions and acknowledged Kafka messages as processed. Roughly 28,000 webhook deliveries were not attempted.

## Timeline

| Time (UTC) | Event |
|---|---|
| 00:00 | Worker v2.19.0 deployed — includes new HTTP client library upgrade |
| 00:00–06:14 | Webhook delivery failures silently dropped; no alert |
| 06:14 | Customer reports webhook endpoint never received expected events |
| 06:31 | Support ticket escalated to Platform on-call |
| 07:02 | Code investigation finds swallowed exception in `worker/src/handlers/webhook.py` |
| 07:18 | Hotfix deployed; worker begins routing `ConnectionTimeout` to DLQ |
| 07:45 | DLQ replay initiated for affected window |
| 11:30 | Replay complete; affected customers notified |

## Root Cause

The new HTTP client library raises `httpx.ConnectTimeout` instead of `requests.exceptions.Timeout`. The exception handler caught the old exception type only. `ConnectTimeout` fell through to a bare `except Exception` block that logged a warning and committed the Kafka offset — effectively discarding the message.

PR #4901 introduced the library swap without updating exception handling. The PR had tests but they mocked the HTTP client and didn't raise the new exception type.

## Impact

- ~28,000 webhook deliveries silently lost during 6-hour window
- Successful replay of ~24,600 (remainder were for deleted endpoints)
- Three enterprise customers affected; compensatory SLA credits issued
- This is classified as a **P0** data loss incident

## Action Items

- [ ] Audit all exception handlers in `worker` for library-specific exception types — owner: @farah, due 2026-04-09
- [ ] Add integration test that actually raises `ConnectTimeout` without mocking — owner: @farah, due 2026-04-09
- [ ] Add DLQ depth alert: any DLQ with 0 messages processed for 15 minutes during business hours should alert — owner: @ryo, due 2026-04-16
- [ ] Require exception-handling review in PR template for library upgrades — owner: @marco, due 2026-04-16
- [ ] Incident review with affected enterprise customers scheduled for 2026-04-07
- [ ] Full post-mortem review with CTO; see `../../../incidents/p0-review-2026-04.md`
