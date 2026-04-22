# Holdout Set Methodology

## Purpose

This doc describes how we construct, validate, and refresh the holdout set used for offline evaluations of the recommender.

## Design Principles

1. **Temporal separation** — holdout events must be strictly later than the latest training event. We enforce a minimum 2-week gap.
2. **User-level disjoint** — users in the holdout set cannot appear in the training set for that eval run. This prevents memorization leakage.
3. **Representative distribution** — we stratify by user tenure bucket (new, <30d, 30–180d, >180d) and device type.

## Construction Process

```bash
# Run from ml-platform/scripts/
python build_holdout.py \
  --start-date 2025-11-01 \
  --end-date 2025-11-14 \
  --user-sample-rate 0.05 \
  --output gs://ml-evals/holdout/2025-q4/
```

The 5% sampling rate gives us roughly 400k user sessions, which is enough for stable metric estimates (see `recall-at-k-notes.md` for variance analysis).

## Validation Checks

Before any holdout set is used in eval:
- Confirm zero user overlap with training split
- Check item coverage — must include at least 60% of catalog items with >100 interactions in training window
- Verify event timestamp monotonicity
- Run distribution shift test (KS statistic on session length; reject if p < 0.01)

## Rotation Schedule

See `eval-set-rotation.md` for the rotation cadence. As a rule:
- Major holdout rotation: quarterly
- Supplemental slices (e.g., cold-start users, seasonal items): as-needed

## Known Issues

- Holiday periods (late Nov, late Dec) inflate short-session users. We currently exclude Dec 22 – Jan 3 from holdout construction.
- The stratification script does not yet handle multi-device users correctly — tracked at issue #5102

## Contacts

Owned by the ML eval subteam. Ping #ml-eval on Slack for questions.
