# User Tower Personalization — April 2026

**Owner:** Elena Voss  
**Status:** Active

## Hypothesis

The current dual encoder ignores persistent user preferences. A dedicated user tower that encodes purchase history and long-term behavioral signals can shift item scores toward user-specific preferences without fully personalizing the retrieval index.

## Architecture Sketch

```
query_emb = query_tower(query_text)            # dim=256
user_emb  = user_tower(behavior_sequence)      # dim=256
fused_emb = alpha * query_emb + (1-alpha) * user_emb   # learned alpha

relevance = dot(fused_emb, item_emb)
```

`alpha` is a learned per-query scalar (output of a small 2-layer MLP taking query features as input).

## Data

- User behavior sequence: up to 50 most recent purchased/clicked items, truncated to 30-day window
- Users with <3 interactions fall back to α=1.0 (query-only)
- Training data: 220M (user, query, item) triples from 120-day click log

## Progress

### Done
- User tower architecture implemented: `src/encoders/user_tower.py`
- Training pipeline adapted for triplet input: `src/training/triplet_trainer.py`
- Initial run: 2 epochs on 30% data sample

### Early Offline Numbers (preliminary)

| Segment | Recall@50 (no user tower) | Recall@50 (with user tower) |
|---|---|---|
| High-activity users (>50 interactions) | 0.591 | 0.634 |
| Mid-activity (10-50) | 0.561 | 0.572 |
| Low-activity (<10) | 0.519 | 0.521 |

Strong signal for high-activity users. Low-activity gains are within noise.

### TODO
- [ ] Full training run (all data, 4 epochs)
- [ ] ANN index compatibility check — fused embedding changes per user, can't pre-build a single static index. Likely need per-user re-query or user cluster approach.
- [ ] Discuss ANN strategy with infra team (issue #2178)

## Risk

Personalization can entrench filter bubbles. We should instrument diversity metrics before shipping, per `2026-06-diversity-reranking.md` approach.
