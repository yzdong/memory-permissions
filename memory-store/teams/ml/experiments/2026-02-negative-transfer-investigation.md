# Negative Transfer Investigation — February 2026

**Owner:** @lena  
**Trigger:** Unexpected quality drop in fashion vertical after January multilingual training run

## What Happened
After shipping cross-lingual Strategy B (`2026-01-cross-lingual-embeddings.md`), overall metrics looked fine, but fashion vertical saw a −5pp drop in Recall@100 during week-over-week monitoring. No other vertical was affected.

## Investigation

### Hypothesis 1: Multilingual fashion data is low quality
Checked fashion item titles in Spanish/Portuguese training set. Found ~18% of fashion items had garbled machine-translated titles (translator apparently struggled with fashion brand names and sizing notation).

### Hypothesis 2: Shared trunk learned to prioritize localization features at cost of fashion-specific semantics
Probed the shared trunk layers with a linear classifier on fashion vs. non-fashion. Pre-multilingual fine-tuning: 89% accuracy. Post-fine-tuning: 87% accuracy. Small but real degradation.

### Hypothesis 3: Fashion-specific hard negatives got diluted
We used a global hard negative mining strategy. After adding multilingual data, fashion in-language negatives became a smaller fraction. Fashion negatives are more nuanced (color, fit, silhouette) — dilution could explain the drop.

## Evidence
Hypothesis 1 and 3 both have supporting evidence. Hypothesis 2 is likely a secondary factor.

## Fixes Applied
1. Filtered garbled fashion titles from multilingual training set (reduced fashion items from 4.1M to 3.4M but cleaner)
2. Added a fashion-specific hard negative pool to the sampling strategy (15% of negatives must be from fashion when the query is fashion)
3. Increased fashion data sampling rate by 1.5×

## Result After Fixes
Fashion Recall@100 recovered to 0.84 (pre-incident was 0.83, so actually slightly ahead). Closed incident.

## Process Lesson
Vertical-level monitoring should be a first-class alerting metric, not something we check manually after the fact. Filed ticket to add per-vertical breakdowns to the eval dashboard.
