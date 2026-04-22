# MySQL → PostgreSQL Migration

**Status:** Phase 2 of 3 in progress  
**Owner:** Platform (DBA sub-team)  
**Slack channel:** `#db-migration`  
**Completion target:** 2025-12-01

## Why

MySQL was the default when this stack was built. We've accumulated a lot of PostgreSQL-specific tooling (pgvector, logical replication, pg_partman) that we can't use while MySQL is still in the picture. The dual-DB situation also means two sets of on-call runbooks, two backup strategies, and two cost centers.

This migration consolidates onto PostgreSQL, which the data team already runs exclusively.

## Current State

- **MySQL clusters:** 3 remaining (`prod-mysql-billing`, `prod-mysql-auth`, `prod-mysql-legacy`)
- **Already migrated:** `prod-mysql-events`, `prod-mysql-reporting` (completed Q4 2024)
- **PostgreSQL target cluster:** `prod-pg-main` (Aurora PostgreSQL 15.4)

## Phase Summary

### Phase 1 — Completed Q4 2024
Migrated events and reporting databases. Low risk: read-heavy, well-understood schema.

### Phase 2 — In Progress (target: 2025-09-01)
Migrating `prod-mysql-billing`. Billing is the most write-heavy and has the most FK complexity.

Approach:
1. Schema conversion via `pgloader` with manual review of generated DDL
2. Dual-write period: app writes to both MySQL and Postgres for 4 weeks
3. Read traffic shifted to Postgres at 10% → 50% → 100% via feature flag
4. MySQL deprecated, connections drained, instance terminated

### Phase 3 — Planned Q4 2025
Migrate `prod-mysql-auth` and `prod-mysql-legacy`. Auth has more complexity due to the LDAP session tables (which may be dropped as part of `legacy-auth-shim-removal.md`).

## SQL Compatibility Notes

- MySQL's `TINYINT(1)` → Postgres `BOOLEAN` — pgloader handles this but verify app ORM mappings
- `AUTO_INCREMENT` → `SERIAL` or `GENERATED ALWAYS AS IDENTITY`
- `ON UPDATE CURRENT_TIMESTAMP` doesn't exist in Postgres — replace with a trigger
- Backtick quoting → double-quote quoting; SQLAlchemy handles this transparently if you're not using raw SQL

## Rollback Plan

During dual-write, rollback is: flip feature flag to 0% Postgres reads, disable Postgres writes in app config, verify MySQL is consistent. After MySQL is decommissioned, rollback is a restore from the final snapshot (retained for 30 days).

## Related

- `runbooks/postgres-failover.md`
- `infra/terraform/aurora/README.md`
- `tools/pgloader-configs/billing-migration.conf`
