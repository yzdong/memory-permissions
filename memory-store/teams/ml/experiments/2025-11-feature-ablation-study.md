# Feature Ablation Study — November 2025

**Owner:** @marco  
**Goal:** Understand which input features contribute most to dual encoder quality, so we know where to invest in data quality vs. model architecture.

## Features Under Test
Item tower inputs:
- `title_tokens`: item title (tokenized, max 64 tokens)
- `category_path`: full category hierarchy (e.g. Electronics > Phones > Cases)
- `price_bucket`: log-bucketed price (20 buckets)
- `seller_embedding`: pre-trained 64-dim seller rep
- `brand_embedding`: pre-trained 32-dim brand rep
- `avg_rating_bucket`: 1–5 stars bucketed
- `review_count_bucket`: log-bucketed review count

Query tower inputs:
- `query_tokens`: raw query text
- `query_category_context`: inferred category from prior session queries
- `user_embedding`: 64-dim user rep from separate user tower

## Leave-One-Out Results (Recall@100 delta vs full model)

| Dropped feature | ΔRecall@100 |
|---|---|
| title_tokens | −0.18 |
| category_path | −0.04 |
| user_embedding | −0.03 |
| seller_embedding | −0.02 |
| brand_embedding | −0.01 |
| price_bucket | −0.005 |
| avg_rating_bucket | −0.003 |
| review_count_bucket | −0.001 |
| query_category_context | −0.009 |

## Key Takeaways
- Title is overwhelmingly important — 18pp drop without it. Any data quality issues in titles directly hurt quality.
- Category matters but less than expected — model likely infers it from title context.
- User embedding helps but only 3pp — likely because most signals are already in query text for explicit search.
- Rating and review count barely matter — the model may be ignoring them or they're collinear with popularity captured elsewhere.

## Recommendations
1. Invest in title quality (deduplication, spell-checking) before adding new features
2. Price and rating features may be worth removing to simplify the pipeline — not much signal for the complexity cost
3. User embedding: small gain but probably worth keeping; might matter more for personalized re-ranking
