# Eval Set Rotation Schedule

## Motivation

Using a stale holdout set leads to overfitting to that specific data distribution. We've seen teams inadvertently tune hyperparameters against a fixed holdout set over multiple quarters, invalidating it as an unbiased benchmark.

## Current Rotation Policy

- **Primary holdout set**: Rotated at the start of each quarter
- **Supplemental cold-start slice**: Rotated monthly
- **Catalog coverage slice**: Rotated when catalog size changes by >15%

## Schedule (2025–2026)

| Period | Holdout Window | Date Constructed | Notes |
|--------|---------------|-----------------|-------|
| Q3 2025 | Jul 1–14 | Jun 28, 2025 | First use of new build script |
| Q4 2025 | Oct 1–14 | Sep 29, 2025 | Added stratification by device type |
| Q1 2026 | Jan 6–19 | Jan 4, 2026 | Post-holiday exclusion applied |
| Q2 2026 | Apr 1–14 | Mar 29, 2026 | TBD |

## Handoff Checklist

When rotating the holdout set:
1. Run `build_holdout.py` with the new date window
2. Run validation checks (see `holdout-set-methodology.md`)
3. Store artifacts at `gs://ml-evals/holdout/{year}-q{n}/`
4. Update `eval-harness-readme.md` to point to the new path
5. Run a single eval pass on both old and new holdout set — log the delta in this doc
6. Announce in #ml-eval

## Historical Deltas on Rotation

| Rotation | Old Precision@10 | New Precision@10 | Delta |
|----------|-----------------|-----------------|-------|
| Q3→Q4 2025 | 0.79 | 0.81 | +0.02 (new set has fewer cold items) |
| Q4→Q1 2026 | 0.81 | see `q1.md` | — |

Note: we do not restate Q1 2026 targets here — see `q1.md`.

## Risks

- Holdout sets constructed during promotional events (Black Friday etc.) are not representative; avoid those windows
- Small catalog segments (<500 interactions) have high variance — consider bootstrapped CIs when reporting on those slices
