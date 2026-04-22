# Kafka Topic Management

Day-to-day topic operations that don't warrant a full runbook but that engineers need to perform occasionally.

## Listing Topics and Config

```bash
kafka-topics.sh --bootstrap-server kafka:9092 --list

# Describe a specific topic
kafka-topics.sh --bootstrap-server kafka:9092 \
  --describe --topic events.ingested
```

## Creating a New Topic

Don't create topics ad-hoc. Submit a PR to `../kafka/topic-definitions.yaml` and let the topic controller reconcile. If you need it immediately (incident context), create manually and then backfill the definition:

```bash
kafka-topics.sh --bootstrap-server kafka:9092 \
  --create \
  --topic platform.new-topic \
  --partitions 12 \
  --replication-factor 3 \
  --config retention.ms=604800000
```

Partition count decisions: see `../kafka/partition-sizing-guide.md`.

## Changing Retention

```bash
kafka-configs.sh --bootstrap-server kafka:9092 \
  --alter --entity-type topics \
  --entity-name events.ingested \
  --add-config retention.ms=172800000
```

Verify:
```bash
kafka-configs.sh --bootstrap-server kafka:9092 \
  --describe --entity-type topics \
  --entity-name events.ingested
```

## Increasing Partition Count

⚠️ Increasing partitions on a topic with keyed producers will change the key-to-partition mapping. Coordinate with all producer teams before doing this.

```bash
kafka-topics.sh --bootstrap-server kafka:9092 \
  --alter --topic events.ingested \
  --partitions 24
```

You cannot decrease partition count. If you need fewer partitions, create a new topic and migrate.

## Deleting a Topic

Topics can only be deleted if `delete.topic.enable=true` in broker config (it is). Deletion is async and may take several minutes.

```bash
kafka-topics.sh --bootstrap-server kafka:9092 \
  --delete --topic platform.deprecated-topic
```

Before deleting, confirm no active consumer groups and no producers writing to it.

## Consumer Group Management

```bash
# List groups
kafka-consumer-groups.sh --bootstrap-server kafka:9092 --list

# Delete a stale consumer group
kafka-consumer-groups.sh --bootstrap-server kafka:9092 \
  --delete --group old-worker-group-v1
```

Stale groups appear in lag monitoring and create noise. Clean them up quarterly.
