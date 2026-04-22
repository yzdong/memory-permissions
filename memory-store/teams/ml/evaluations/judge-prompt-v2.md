# Judge Prompt v2 — Relevance Annotation for Recommender Eval

## Background

We use an LLM-based judge to label item-query relevance for eval sets where human annotation is too slow. This document describes the v2 prompt, what changed from v1, and known limitations.

## v2 Prompt

```
You are evaluating whether a recommended item is relevant to a user's current context.

User context:
- Recent interaction history (last 10 items): {interaction_history}
- Current session intent signal: {intent_signal}

Candidate item:
- Title: {item_title}
- Category: {item_category}
- Description (first 100 words): {item_description}

Task: Rate the relevance of this item to the user context on a scale of 1–5, where:
1 = Completely irrelevant
2 = Marginally related
3 = Somewhat relevant
4 = Clearly relevant
5 = Highly relevant, likely to engage

Respond with a JSON object: {"score": <int>, "rationale": "<one sentence>"}
```

## Changes from v1

| Aspect | v1 | v2 |
|--------|----|----|  
| History window | Last 5 items | Last 10 items |
| Item context | Title only | Title + category + description |
| Output format | Raw integer | JSON with rationale |
| Score anchors | Binary (0/1) | 1–5 scale |

The move to a 5-point scale was driven by feedback that binary labels were too coarse for NDCG computation — we were collapsing real signal.

## Agreement with Human Labels

We sampled 800 items from the Q4 2025 holdout set and had 3 human annotators rate them alongside the judge.

- Inter-annotator agreement (Krippendorff's α): 0.71
- Judge vs. human majority vote agreement: 0.68
- Judge tends to over-rate novelty items — known bias, tracked in issue #5211

## Usage in Eval Harness

The judge is invoked by `eval/judge_client.py`. Scores ≥ 4 are treated as "relevant" for precision/recall computation. This threshold was validated against human labels on the Q3 2025 set.

## Known Limitations

- Judge has no awareness of user demographics or geography
- Long-tail items with sparse descriptions get lower scores regardless of actual fit
- Cost per 1k judgments: ~$1.20 at current model pricing — track monthly spend in `../budget-tracker.md`

## Related

- `eval-harness-readme.md`
- `recall-at-k-notes.md`
