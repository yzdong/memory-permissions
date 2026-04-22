# Session Context Fusion — May 2026

**Owner:** Elena Voss  
**Status:** In Progress  
**Last updated:** 2026-05-09

## Hypothesis

The current query encoder ignores in-session context (items clicked or browsed before the current query). Prepending a summary of the session to the query representation should help for queries like "more like this" or short follow-up searches.

## Architecture

Two variants under test:

**Variant A — Concatenation:**  
Concatenate a mean-pooled session embedding (last 5 items, dim=256) with the query embedding before projection.

**Variant B — Cross-attention:**  
Add a 2-layer cross-attention block where query attends to session item embeddings.

## Early Numbers (epoch 2 of 4)

| Model | Recall@50 (with session context) | Recall@50 (no session context) |
|---|---|---|
| Baseline (no fusion) | 0.561 | 0.561 |
| Variant A (concat) | 0.579 | 0.558 |
| Variant B (cross-attn) | 0.591 | 0.553 |

Variant B is stronger when session context is available but regresses slightly without it. Variant A is more robust.

## Concern

Nearly 30% of queries arrive with no prior session events (new sessions, direct link). Variant B's regression for no-context cases is worrying. Will try:
- Masking session with dropout (p=0.3) during training to force robustness
- Fallback: use zero-vector for empty session (already implicit in concat)

## Next Update

Full 4-epoch results expected by 2026-05-16. Will share in #ml-experiments Slack.

## Related

- `2025-12-query-rewriting.md` — overlapping inference graph, need to coordinate pipeline order
- `src/encoders/session_fusion.py` for implementation
