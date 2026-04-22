# Feature Engineering Notes

This is a semi-informal working doc for the team. Decisions here should eventually graduate to `feature-store-schema.md` once they're stable.

## Active Experiments

### Sequential Session Features (in progress)

Adding a transformer-based session encoder that produces a `session_embed_v1` vector from the last 20 items in a session. Early results on the dev cohort show +1.8% NDCG@20 vs. the static `embed_v3` baseline.

Code: `src/features/session_encoder.py`  
Owner: Yuki O.  
Target schema version: v4.3

**Open questions:**
- How do we handle cold-start users with < 3 session events? Current plan: fall back to `embed_v3`.
- Session encoder inference adds ~12ms latency. Need to confirm with serving team this is acceptable.

### Price Sensitivity Signal

The `price_bucket` feature in `fs.item_features` is coarse (0–9). We're experimenting with a cross feature: `user_avg_purchase_price_bucket × item_price_bucket`. Correlation analysis in `notebooks/price_sensitivity_analysis.ipynb`.

Preliminary lift: +0.6% MRR, but noisy. Need more holdout data.

## Retired / Abandoned Features

| Feature | Why dropped |
|---|---|
| `geo_lat_lon` | Privacy concern; replaced by `country_code` + `region_code` |
| `social_graph_degree` | Social graph data too stale (updated weekly); hurt cold-start |
| `embed_v2` | Superseded by `embed_v3` in schema v4.0; old checkpoints incompatible |

## Feature Importance (from last production model)

Using permutation importance on the holdout set:
1. `embed_v3` (user embedding) — by far the most important
2. `avg_rating` — strong signal for item quality
3. `freshness_score` — important for trending items
4. `tenure_days` — helps personalization for new vs. power users
5. `category_l1` — moderate importance
6. `price_bucket` — lower importance than expected; see price sensitivity work above

## Engineering Gotchas

- `freshness_score` is computed by a separate job and can lag the main feature refresh by up to 2 hours. Don't assume it's always fresh.
- `avg_rating` is `NULL` for items with < 5 ratings — handle this explicitly in the feature pipeline (currently we fill with 3.0, the global mean).
- Embedding vectors in `embed_v3` are **not** L2-normalized at storage time. Normalize in the model, not in preprocessing.

## See Also
- `feature-store-schema.md`
- `data-cleaning-pipeline.md`
