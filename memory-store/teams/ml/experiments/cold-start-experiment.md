# Cold Start Experiment

**Status:** Ongoing  
**Owner:** @sofia, @dani  
**Related:** `2025-11-hard-negative-mining.md`, `../data/cold-start-items.md`

## Problem Statement
New items (<48h in catalog) have no interaction history. The current item tower produces near-random embeddings for them because it relies heavily on co-click context. CTR on new items is 0.41× that of comparable established items.

## Hypothesis
If we train a separate "cold start" item encoder that uses only content features (title, category, price bucket, seller embedding), and blend its output with the main tower using a learned gate, cold-start CTR improves without degrading warm-item quality.

## Experiments Run So Far

### v0 — Content-only fallback (no blending)
- Just swapped cold items to a content encoder at inference time
- Cold CTR: +18% relative vs baseline
- Warm CTR: no change (gated by item age)
- Problem: hard cutoff at 48h creates a cliff in recommendations

### v1 — Learned gate on age signal
```python
# gate = sigmoid(w * log(1 + age_hours) + b)
# embedding = gate * warm_tower + (1 - gate) * cold_tower
```
- Cold CTR: +23% relative
- Warm CTR: −0.4% relative (statistically significant, worrying)
- The gate leaks: some warm items get partial cold embeddings.

### v2 — Hard gate with soft transition window
- Age < 24h: 100% cold tower
- 24–72h: linear interpolation
- > 72h: 100% warm tower
- Warm CTR: −0.1% (within noise)
- Cold CTR: +21% relative

## Current Status
v2 is in shadow mode on 5% of traffic. A/B results expected by end of month. Preliminary numbers look good.

## Next Steps
- Add image embedding as an additional cold-start feature (waiting on vision team API)
- Evaluate cold-start recall@100 separately from overall recall — currently hard to isolate in the eval pipeline
- Write up findings for `../reports/cold-start-q4.md` once A/B concludes
