# Data Cleaning Pipeline

## Purpose

Raw interaction events come off the Kafka topic `rec.user_events.v2` and go through several cleaning stages before landing in the feature store. This document covers what each stage does and where the code lives.

## Pipeline DAG (Airflow)

DAG name: `rec_data_cleaning_daily`  
DAG file: `airflow/dags/rec_data_cleaning_daily.py`  
Schedule: `0 2 * * *` (02:00 UTC)

```
raw_event_ingest
    └── deduplicate_sessions
            └── mask_pii
                    └── filter_bots
                            └── compute_interaction_labels
                                    └── write_to_feature_store
```

## Stage Details

### 1. `deduplicate_sessions`
- Drops duplicate `(user_id, item_id, session_id)` tuples within a 30-minute window.
- ~2–4% of raw events are duplicates, mostly from mobile retry logic.

### 2. `mask_pii`
- Replaces raw user IDs with HMAC-SHA256 hashed versions using the rotating key in Vault at `secret/ml/pii-hash-key`.
- **Never** log or store the pre-hash user ID downstream.

### 3. `filter_bots`
- Applies the bot detection model from `models/bot_classifier_v2` (threshold: 0.72 confidence).
- Also hard-filters known bot IP ranges from the `sec.known_bot_cidrs` table.
- Drops ~8% of events on average; spikes to ~15% during sale events.

### 4. `compute_interaction_labels`
- Maps raw event types to training labels:
  - `purchase` → positive (weight 3.0)
  - `click` + dwell > 30s → positive (weight 1.0)
  - `skip` or click + dwell < 5s → negative (weight 1.0)
  - Everything else → excluded

### 5. `write_to_feature_store`
- Writes to `fs.interaction_log` partitioned by `event_date`.
- Triggers a metadata update so downstream consumers see fresh data.

## Data Quality Checks

Each stage emits metrics to Datadog under `rec.pipeline.cleaning.*`. Alert thresholds:
- Bot filter drop rate > 20% → PagerDuty P2
- Positive label rate < 3% → Slack alert to `#ml-data-eng`

## Re-running a Backfill

```bash
airflow dags backfill rec_data_cleaning_daily \
  --start-date 2024-10-01 \
  --end-date 2024-10-07
```
Note: backfills can conflict with the nightly run if they overlap. Pause the DAG first.

## Related Docs
- `feature-store-schema.md` — downstream schema
- `../evaluations/offline-eval-guide.md` — how cleaned data feeds offline eval
