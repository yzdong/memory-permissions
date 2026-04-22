# Q1 Eval Process Notes

This is a working doc capturing process decisions and open questions for Q1 2026 evaluations. It is **not** the canonical thresholds document — see `q1.md` for the actual targets.

## Changes to Eval Process This Quarter

### Daily Eval Cadence
We moved from every-3-days to daily eval runs. This required:
- Optimizing the harness to run in <30 min on the full holdout set (was ~90 min)
- Key change: switched from full re-embedding to cached item embeddings with delta updates
- Validated that cached embeddings don't meaningfully change metric values (<0.001 difference in practice)

### New Reporting Dashboard
The BigQuery data now feeds a Looker dashboard at `go/ml-eval-dashboard`. Replaces the manual weekly Sheets doc. The dashboard shows:
- Rolling 30-day metric trends with confidence bands
- Alert history
- Per-segment breakdowns (new users, cold items, mobile vs. desktop)

### Judge Prompt Upgraded
We're running judge-prompt-v2 this quarter (see `judge-prompt-v2.md`). First two weeks of Q1 we ran both v1 and v2 in parallel for calibration. v2 ratings correlated better with human labels (0.68 vs. 0.61 agreement).

## Open Questions

1. **Tail-item weighting** — should we weight tail items more heavily in aggregate metrics? Currently unweighted. The ranking team is doing this for their evals and it changes their numbers noticeably.

2. **Multi-objective metrics** — product wants a single scalar score. Composite score like `0.4*P@10 + 0.4*R@50 + 0.2*(1 - latency_penalty)` has been proposed. Needs more discussion before we adopt.

3. **Counterfactual eval** — the online shadow logging work is partially done. If it lands by Feb, we can start closing the offline-online gap analysis loop.

## Process Reminders

- Holdout set for Q1 is the Jan 6–19 window; do not use the Q4 set
- Before shipping any model change, a clean eval run must pass — no eyeballing
- Any threshold waiver must be documented in Linear with the justification

## Related Docs

- `q1.md` — the actual Q1 targets (do not restate here)
- `eval-set-rotation.md`
- `regression-tracking.md`
