# Feature Store Schema — Recommender Model

## Overview

This document describes the canonical feature schema consumed by the recommender training pipeline. The authoritative source is the `feature_store` Hive database on the internal data platform.

## Primary Feature Tables

### `fs.user_embeddings`
| Column | Type | Description |
|---|---|---|
| `user_id` | STRING | Hashed user identifier |
| `embed_v3` | ARRAY<FLOAT> | 128-dim embedding, refreshed nightly |
| `country_code` | STRING | ISO 3166-1 alpha-2 |
| `tenure_days` | INT | Days since first active session |
| `last_active_ts` | TIMESTAMP | UTC |

### `fs.item_features`
| Column | Type | Description |
|---|---|---|
| `item_id` | STRING | Catalog item identifier |
| `category_l1` | STRING | Top-level taxonomy |
| `price_bucket` | INT | 0–9 logarithmic bucket |
| `avg_rating` | FLOAT | 30-day rolling average |
| `freshness_score` | FLOAT | Recency signal [0,1] |

### `fs.interaction_log`
Partitioned by `event_date`. Retention: 180 days.
- `user_id`, `item_id`, `event_type` (click/purchase/skip), `session_id`, `rank_position`

## Schema Versioning

- Schema changes require a PR to `ml-platform/feature-store-defs` **and** a migration note here.
- Breaking changes must be announced in `#ml-data-eng` at least 5 business days before cutover.
- Current schema version: `v4.2` (promoted 2024-11-03)

## Feature Freshness SLAs

| Feature group | Refresh cadence | Max acceptable lag |
|---|---|---|
| user_embeddings | 24 h | 36 h |
| item_features | 6 h | 12 h |
| interaction_log | 1 h | 3 h |

## Notes

- Do not read directly from `fs.interaction_log_raw` — it contains PII before masking.
- See `../data-cleaning-pipeline.md` for how raw logs are preprocessed before landing here.
- `embed_v3` replaced `embed_v2` in schema v4.0; old checkpoints trained on v2 embeddings are incompatible.
