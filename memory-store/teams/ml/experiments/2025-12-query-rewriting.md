# Query Rewriting Experiment — December 2025

## Motivation
About 12% of queries hit recall@100 < 0.60. Manual inspection shows most are either misspelled, highly colloquial, or use brand-specific jargon not in training data. Rewriting queries before encoding should help.

## Hypothesis
A lightweight seq2seq rewriter (T5-small fine-tuned on query-to-canonical pairs) prepended to the retrieval pipeline will lift recall on the hard-query slice without meaningfully increasing latency.

## Setup
- Rewriter: T5-small fine-tuned on 2M (noisy_query, canonical_query) pairs
- Pairs sourced from click logs: if user rephrased a query within same session and clicked the same item, treat as positive pair
- Retrieval: dual-encoder-v2 (256-dim, hard negatives)
- Eval: `../evaluations/hard-query-dec2025.jsonl` (~180k queries flagged as difficult)

## Ablation

| Condition | Recall@100 (hard set) | Recall@100 (full set) | Added latency (p50) |
|---|---|---|---|
| No rewriting | 0.57 | 0.83 | 0 ms |
| Greedy decode | 0.66 | 0.83 | 8 ms |
| Beam search (b=4) | 0.68 | 0.83 | 22 ms |
| Top-k sampling (k=10) | 0.64 | 0.82 | 9 ms |

Greedy decode is the practical choice: 9pp gain on hard queries, only 8ms added, no degradation on easy queries.

## Failure Modes
- Rewriter sometimes over-normalizes brand names ("nike air max" → "running shoes") — loses specificity
- Queries in non-English languages get mangled. We don't train on multilingual data yet.
- About 2% of rewrites are semantically different from original — added a semantic similarity gate (cosine > 0.72) to fall back to original if rewrite drifts too far.

## Rollout Plan
1. Enable for queries with token-level edit distance heuristic > 0.3 from vocabulary center
2. Full rollout if A/B shows +2% overall CTR
3. See `runbooks/query-rewriter-deploy.md` for deployment steps

## Open Issues
- Multilingual support: punt to Q1 2026
- Rewriter model versioning: needs to be coupled to retrieval model versions, which is annoying
