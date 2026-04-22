# Cross-Lingual Retrieval Experiment — January 2026

**Owner:** Soo-Jin Park  
**Status:** Scoped, Not Started

## Motivation

Our catalog has items with titles in 8 languages, but the query encoder was trained on English-only data. International users querying in Spanish, Portuguese, or Japanese get substantially worse recall. The localization team flagged this as a P1 for H1 2026.

## Proposed Approaches

### Option A — Multilingual LM Backbone

Replace the query encoder backbone with mBERT or XLM-R. Retrain from scratch.

- Pro: handles code-switching and mixed-language queries
- Con: ~2× inference latency, non-trivial retraining cost

### Option B — Translate-then-Retrieve

Run a lightweight MT model on non-English queries before encoding.

- Pro: no change to the core model
- Con: MT latency (~15 ms), failure modes for product-specific terminology

### Option C — Language-Aware Fine-tune

Keep English backbone, add language embeddings + fine-tune on parallel query data.

- Pro: smaller model footprint
- Con: limited by English backbone's multilingual capacity

## Preliminary Data

We have ~2.1M Spanish query–click pairs and ~800K Portuguese pairs. Japanese coverage is thin (~120K pairs) — may need augmentation.

## Blocked On

- Annotation team capacity to produce multilingual eval set (estimated Q1 2026)
- Infrastructure support for MT model deployment (in discussions with serving team)

## Owner will revisit

Planning to kick off Option B shadow test in February once infra is confirmed. See `../proposals/cross-lingual-h1-2026.md` for the full project proposal.
