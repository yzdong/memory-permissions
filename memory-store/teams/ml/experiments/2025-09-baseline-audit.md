# Baseline Model Audit — September 2025

**Owner:** Marcus Webb  
**Status:** Complete  
**Purpose:** Before beginning the dual-encoder work, establish clean baseline numbers we can reference throughout the rest of 2025.

## Why This Was Needed

Our reported metrics were inconsistent across notebooks. Different eval sets, different de-dup logic, different treatment of missing labels. This audit standardizes everything.

## Canonical Eval Set

- Source: `data/eval/canonical_2025q3_held_out.parquet`
- Size: 142,000 query-item pairs
- Construction: 90-day held-out window, stratified by query frequency (head/torso/tail: 33% each), items de-duped by SKU

## Baseline Numbers (single_tower_v4)

| Metric | Head | Torso | Tail | Overall |
|---|---|---|---|---|
| Recall@10 | 0.601 | 0.538 | 0.391 | 0.510 |
| Recall@50 | 0.712 | 0.634 | 0.481 | 0.609 |
| MRR@10 | 0.411 | 0.347 | 0.264 | 0.341 |
| NDCG@10 | 0.388 | 0.322 | 0.241 | 0.317 |

## Notes on Eval Methodology

- Relevance labels: binary (click = relevant, no-click = not relevant)
- Impressions without interaction excluded — they're ambiguous
- We should consider adding explicit negative labels from the annotation pipeline later

## Action

This file is now the source of truth for "where we started." All future experiments in this directory should reference these numbers for deltas. Do not modify this file — create a new entry if methodology changes.

## Related

- Eval script: `scripts/run_eval.py --config configs/eval_canonical.yaml`
- Data pipeline: `data/pipelines/eval_set_construction.py`
