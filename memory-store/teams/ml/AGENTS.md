# ML Team — Agent Guide

Context for LLM agents acting on behalf of the ML team.

## Who we are
ML team owns the recommender model, the eval harness, and the offline
training pipeline. We do not own any user-facing services.

## Key files in our team memory
- `evaluations/q1.md` — Q1 eval thresholds and the current eval set definition.

## Overrides we maintain (vs. org defaults)
- Python version floor: **3.11** (matches Platform).
- We pin `numpy<2.0` because our training image hasn't migrated yet.

## Cross-team coordination
- Before Platform deploys an API change touching the recommender surface,
  they must confirm our precision threshold is met. See `evaluations/q1.md`.

## House style
- Report metrics to 3 decimal places.
- Never include raw user IDs in commits, even in test fixtures.
