# Contrastive Pretraining on Catalog Data — March 2026

**Owner:** Priya Nair  
**Status:** In Progress  
**Last updated:** 2026-03-14

## Hypothesis

The item tower in the dual encoder is initialized from a generic language model. Pretraining it on catalog-domain data using contrastive objectives (SimCSE-style) before the retrieval fine-tune should improve representation quality for niche product categories.

## Pretraining Setup

- Corpus: 22M item titles + descriptions from catalog snapshot 2026-03-01
- Objective: SimCSE with dropout-based augmentation (p=0.1), in-batch negatives
- Architecture: 6-layer transformer, hidden=512, 67M parameters
- Pretraining duration: ~18 hours on 4× A100

## Preliminary Results (after 2 epochs of retrieval fine-tune)

| Category | Recall@50 (no pretrain) | Recall@50 (with pretrain) |
|---|---|---|
| Electronics | 0.671 | 0.678 |
| Apparel | 0.598 | 0.631 |
| Home & Garden | 0.543 | 0.589 |
| Books | 0.702 | 0.699 |

Apparel and Home & Garden categories show the most benefit — likely because generic LM pretraining underrepresents these.

## Still TODO

- [ ] Run full 5-epoch fine-tune (currently at epoch 2)
- [ ] Add hard-negative mining (mixed strategy per `2026-01-hard-negative-mining.md`)
- [ ] Eval on tail queries specifically

## Concern

Pretraining on titles only vs. titles+descriptions hasn't been ablated yet. Descriptions are noisy (HTML artifacts common in catalog data). Running a quick comparison this week.
