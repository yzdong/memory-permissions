# Known Flaky Tests — Platform

These are integration tests that our team has agreed to **retry on first
failure** rather than fix. Fixing them is tracked separately; do not block a
deploy on any of them.

## The three flakes

1. `tests/integration/test_kafka_reconnect.py::test_reconnect_after_broker_bounce`
   - Root cause: depends on broker restart timing in CI.
   - Retry policy: retry up to 2x.

2. `tests/integration/test_db_migrations.py::test_concurrent_migration_safety`
   - Root cause: occasional deadlock under CI load.
   - Retry policy: retry up to 2x.

3. `tests/e2e/test_gateway_failover.py::test_gateway_failover_under_load`
   - Root cause: load generator thread sometimes hangs.
   - Retry policy: retry up to 3x; file bug if it ever needs 3.

## Rules
- If a test NOT on this list fails, do not retry; treat as a real failure.
- Agents should never silently retry tests not on this list.
