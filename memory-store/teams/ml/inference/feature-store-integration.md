# Feature Store Integration in Inference

We pull user and item features from Redis during online inference. This doc
explains the setup and common issues.

## What Features We Fetch

At request time we have the `item_id` and `user_id`. From Redis we fetch:

- `user:{user_id}:profile` — user preference vector (256-dim float32, stored as bytes)
- `item:{item_id}:meta` — item metadata (category, freshness score, engagement rate)
- `user:{user_id}:history_hash` — compact representation of recent interactions

These are concatenated with the tokenizer output before passing to the ranker.

## Redis Key Schema

```
user:{user_id}:profile      → bytes (256 * 4 bytes, little-endian float32)
item:{item_id}:meta         → JSON string
user:{user_id}:history_hash → bytes (64 bytes)
```

TTL on user features: 1 hour. Item meta: 24 hours.

Feature population is handled by the Data team's pipeline. See
`../../data/feature-pipeline/redis-write.md` for their SLA (they target < 5min
freshness for user features).

## Cache Miss Behavior

If a key is missing we **do not fail the request**. Instead:
- Missing user profile → zero vector (model handles this gracefully; tested).
- Missing item meta → hardcoded defaults in `configs/inference-service/feature-defaults.yaml`.
- Missing history hash → empty bytes.

Cache miss rate is monitored. Alert fires if miss rate exceeds 5% over a 10-min
window — that typically means the feature pipeline is behind.

## Performance

We pipeline the three Redis GETs in a single `mget` call. Typical round-trip
is 1–2ms on the same AZ. We've seen it spike to 15ms during Redis failover;
the 3ms budget in the latency plan (`inference-service-architecture.md`) has
enough headroom for normal jitter but not a full failover.

## Planned: Feature Store Migration

We're evaluating moving from raw Redis to a proper feature store (Feast or
Tecton). Decision doc in `../planning/feature-store-migration.md`.
No timeline yet — depends on Platform's infra roadmap.
