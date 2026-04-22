# Tail Item Boosting Experiment — January 2026

**Owner:** @dani, @jan  
**Follows from:** `2025-09-popularity-bias-audit.md`

## Goal
Improve Recall@100 for bottom-30% popularity items (D7–D10) without degrading D1–D3.

## Approaches Tested

### Approach 1: Popularity-inverse sampling weight
- Weight each training example by `1 / (log(1 + item_popularity) + 1)`
- Simple, no architecture change

### Approach 2: Mixup augmentation for tail items
- Randomly interpolate between a tail item embedding and a semantically similar head item embedding during training
- Gives tail items more gradient signal via smooth blending

### Approach 3: Separate tail tower with knowledge distillation
- Train a separate item tower for tail items
- Use head-item tower as teacher
- Complex to maintain but theoretically strong

## Results (D7–D10 Recall@100 / D1–D3 Recall@100)

| Approach | D7-D10 Recall@100 | D1-D3 Recall@100 | Net |
|---|---|---|---|
| Baseline | 0.63 | 0.88 | — |
| Approach 1 | 0.71 | 0.86 | +8pp tail, −2pp head |
| Approach 2 | 0.74 | 0.87 | +11pp tail, −1pp head |
| Approach 3 | 0.77 | 0.88 | +14pp tail, 0pp head |

## Decision
Approach 3 is best but expensive to maintain. Shipping Approach 2 as a near-term improvement; Approach 3 parked for a future quarter.

## Notes
- Mixup requires computing semantic similarity between tail and head items — done offline weekly using a frozen embedding snapshot
- Mixup ratio α=0.2 worked best (tried 0.1, 0.2, 0.5; 0.5 hurt head quality)
- Index changes: no changes needed for approaches 1 and 2

## Follow-Up
- Should check if cold-start experiment (`cold-start-experiment.md`) and tail boosting interact — they both modify item representation for sparse items
