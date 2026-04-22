# Cross-Lingual Embedding Experiment — January 2026

**Owner:** @lena  
**Status:** Completed, results mixed

## Background
We expanded catalog to 6 new locales in Q4 2025. The English-trained dual encoder is unsurprisingly bad for Spanish, Portuguese, and Turkish queries. Recall@100 on those locales is 0.51–0.58 vs 0.83 for English.

## Approach
Two strategies evaluated in parallel:

### Strategy A: mDEBERTa-based shared encoder
- Fine-tune multilingual DeBERTa on translated training pairs
- Single encoder for all languages
- Risk: English quality degradation due to multilingual interference

### Strategy B: Language-specific heads on top of shared trunk
- Shared transformer backbone (first 8 layers)
- Per-language projection heads (last 4 layers)
- Allows targeted fine-tuning per locale

## Results

| Locale | Baseline Recall@100 | Strategy A | Strategy B |
|---|---|---|---|
| English | 0.83 | 0.80 | 0.83 |
| Spanish | 0.55 | 0.76 | 0.78 |
| Portuguese | 0.52 | 0.74 | 0.77 |
| Turkish | 0.51 | 0.69 | 0.73 |

Strategy B dominates but at the cost of more parameters and more complex deployment.

## Concerns
- Strategy A causes −3pp English regression — unacceptable without further investigation
- Strategy B: 4 language heads × 2 towers = 8 extra projection matrices. Model size goes from 110M to 128M params. Acceptable.
- Turkish recall still trails. Likely data issue — only 400k Turkish training pairs vs 2M for Spanish.

## Decision
Proceed with Strategy B for Spanish and Portuguese (largest user bases). Turkish remains English fallback until data volume improves.

## Next Steps
- Collect more Turkish training pairs through translation of top English pairs (assigned @jan)
- Strategy B ships to staging by Jan 31
- Revisit multilingual interference analysis with probing classifiers
