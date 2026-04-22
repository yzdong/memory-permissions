# Kafka 0.10 Sunset

**Status:** Sunset complete — consumers migrated, brokers decommissioned  
**Completed:** 2025-03-14  
**Authored by:** Platform Infra

## Why We're Documenting a Completed Sunset

Several runbooks and service configs still reference the old broker URLs. This document is the canonical record of what happened and what was changed, so teams stop asking in #platform-help.

## What Was Kafka 0.10

We ran a 3-node Kafka 0.10.2 cluster on bare metal in `dc-west-2`. It was the original event bus, predating our move to managed MSK. By 2024 it hosted roughly 18 legacy topics, half of which had zero active consumers.

## Migration Summary

- **Active topics migrated:** 9 topics moved to MSK (us-east-1 cluster `prod-msk-main`)
- **Dead topics archived:** 9 topics snapshotted to S3 at `s3://platform-kafka-archive/0.10-snapshot/`
- **Consumers updated:** 6 services repointed; see `services/billing-worker`, `services/event-router`, `services/audit-logger`
- **Brokers decommissioned:** All three bare-metal hosts returned to infra pool on 2025-03-14

## Config Changes

Old broker string (do not use):
```
kafka.brokers=kafka-01.dc-west-2.internal:9092,kafka-02.dc-west-2.internal:9092,kafka-03.dc-west-2.internal:9092
```

New MSK endpoint (use this):
```
kafka.brokers=b-1.prod-msk-main.abc123.c3.kafka.us-east-1.amazonaws.com:9092
```

## Lingering References

Search your service configs for `kafka-0[12].dc-west-2` — if you find any, they will silently fail to connect. File a ticket against platform or ping `#platform-help`.

## Lessons Learned

- Should have enforced a broker URL config abstraction earlier; hardcoded broker strings in app configs caused 80% of the migration toil
- Dead topic audit should happen quarterly, not when we're forced to migrate
- MSK IAM auth is worth the setup pain; SASL/PLAIN on the old cluster was a headache

## Related

- `runbooks/msk-consumer-setup.md`
- `../evaluations/kafka-migration-postmortem.md`
