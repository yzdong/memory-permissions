# Online vs. Batch Inference — When to Use Which

This comes up every time someone wants to add a new model to our stack.
Here's the framework we use internally.

## The Core Question

> Does the user (or downstream system) need the score *right now*, or can it
> be pre-computed and looked up?

If the inputs aren't known until request time, you need online inference.
If you can enumerate inputs ahead of time, batch is almost always better.

## Characteristics

| Dimension | Online | Batch |
|---|---|---|
| Latency requirement | <100ms p99 | Minutes to hours OK |
| Input space | Unknown at request time | Enumerable ahead of time |
| Freshness | Real-time | Staleness acceptable (hours/day) |
| Throughput | Bursty | Predictable, high sustained |
| Cost | Expensive (reserved GPU) | Cheaper (spot, off-peak) |
| Failure impact | User-visible | Delayed score refresh |

## Current Model Placement

| Model | Mode | Reason |
|---|---|---|
| Ranker | Online | Query-dependent; can't precompute |
| Embedder | Online | Document embeddings computed at index time, but query embedding is online |
| Doc embedder | Batch (nightly) | Corpus is known; embeddings cached in vector store |
| Content classifier | Batch (hourly) | Classification needed before content goes live; 1hr staleness OK |

## Hybrid Patterns

Some models can be partially batched:
- Precompute embeddings for the known item catalog offline.
- At query time, only compute the query embedding online, then do ANN lookup.
- This is what we do for the retrieval path. See `retrieval-architecture.md`.

## Adding a New Model

Before you add online serving capacity, check:
1. Can inputs be precomputed? If >80% of queries hit cached items, consider batch.
2. What's the latency SLA? If >500ms is acceptable, batch + async response may work.
3. What's the cold-start story? Batch jobs can reload models at each run; online
   replicas need to stay warm.

Talk to @platform-team before adding a new online endpoint — they need to update
their routing config.
