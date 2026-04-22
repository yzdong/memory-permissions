# Session Context Experiment — March 2026

**Owner:** @sofia  
**Status:** In progress

## Motivation
The current query encoder treats each query independently. Users often issue several queries in a session that reveal intent better understood jointly. A user who searched "trail running" then "waterproof" is clearly looking for waterproof trail shoes.

## Hypothesis
Encoding the last N queries in the session alongside the current query (via a small transformer prefix) will improve relevance on multi-query sessions without hurting single-query sessions.

## Design
```
[CLS] q_{t-2} [SEP] q_{t-1} [SEP] q_t [EOS]
                    ↓
            query tower (shared weights)
                    ↓
            session-aware query embedding
```
- Use positional IDs to indicate query order
- Mask out session context with probability 0.3 during training to simulate single-query inference

## Preliminary Results (2-week checkpoint)

| Session length | Baseline MRR@10 | +Session context MRR@10 |
|---|---|---|
| 1 query | 0.49 | 0.49 |
| 2–3 queries | 0.47 | 0.52 |
| 4+ queries | 0.44 | 0.55 |

Looks promising. No regression on single-query sessions (masking strategy works).

## Risks / Open Questions
- Session boundary definition is messy — 30-minute gap used currently, may need tuning
- Privacy: session context means we need to be more careful about what we log. Flagged for review with privacy team.
- Latency impact: prefix adds ~5ms to query encoding. Acceptable.

## What's Left
- Full eval on `../evaluations/mar2026-holdout.jsonl`
- Interact with query rewriter (from `2025-12-query-rewriting.md`) — does rewriting each query before context encoding help or hurt?
- A/B test design (draft in `../ab-tests/session-context-ab.md`)
