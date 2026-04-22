# Weekly Training Notes — Nov 2024

Informal notes from the team's weekly training sync. Not authoritative — check actual experiment logs in MLflow.

---

## Week of Nov 4

- Kicked off first v4 baseline run. Loss curve looks healthy; no NaN issues.
- `data_cleaning_pipeline` missed its SLA on Nov 5 (Dataproc preemption). Run started 90 min late. Training data for that day was clean per integrity check.
- Reminder: **do not start training jobs before 07:00 UTC** — the dataset export isn't guaranteed done until then.

---

## Week of Nov 11

- Sweep results (80 trials): best config is `lr=3.2e-4, batch=1024, dropout=0.15, emb_dim=64`. NDCG@10 of 0.401 on the validation split — 1.8% above current prod baseline.
- @priya noted that `avg_dwell_seconds` has a long tail of values >3600s that we're not filtering. Added a cap at 900s in the cleaning pipeline. Reprocessing Nov data.
- numpy pin held firm — someone on the infra team tried upgrading to 2.1 "just to see" and broke the faiss import. See `numpy-migration-plan.md`.

---

## Week of Nov 18

- Full training run with best sweep config completed in 31 hours on 8×A100. Final val NDCG@10: 0.3991 (slightly lower than sweep, which is expected — sweep overfits to the val split somewhat).
- Recall@50: 0.736 ✓ (exceeds 0.72 threshold)
- Canary deployment started in staging. Watching error rates.
- Opened ML-318: offline evaluation script breaks on models with custom tokenizers.

---

## Week of Nov 25

- Canary results clean after 24h. Promoting `recommender_v4_20241118_c7a2f0` to Production stage in MLflow.
- Post-mortem from Nov 5 Dataproc outage filed with Platform team.
- @tommy starting feature work on `search_query_embedding` — privacy review expected to conclude by Dec 15.
- Reminder: GPU cluster will be at reduced capacity Dec 24–Jan 1 due to infra maintenance. Plan large runs accordingly.

---

## Action Items (carried into Dec)

- [ ] Fix ML-318 (tokenizer eval bug) — @chen-ml
- [ ] Finalize dwell_seconds cap value and add to cleaning config — @priya
- [ ] Phase 2 of numpy migration — @chen-ml + Platform
- [ ] Schedule fairness slice review for v4 model — @all
