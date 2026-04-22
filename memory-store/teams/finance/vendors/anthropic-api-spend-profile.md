# Anthropic API Spend Profile

**Last updated:** 2024-11-10  
**Owner:** Finance / AI Tooling  
**Classification:** Confidential

## Overview

Anthropics' Claude API was onboarded in Q1 2024 following an internal evaluation. Usage is growing quickly as product teams integrate LLM capabilities into customer-facing features and internal tooling.

## Spend Summary

| Month | Input Tokens (M) | Output Tokens (M) | Cost |
|-------|-----------------|-------------------|------|
| Aug-2024 | 4,210 | 1,830 | $38,400 |
| Sep-2024 | 5,680 | 2,410 | $51,200 |
| Oct-2024 | 7,900 | 3,350 | $71,500 |

Month-over-month growth in October was 40% — driven by the product team's new document summarization feature launch.

## Model Usage Breakdown (Oct 2024)

| Model | % of Spend | Primary Use Case |
|-------|-----------|------------------|
| claude-3-5-sonnet | 61% | Customer features, summarization |
| claude-3-haiku | 33% | Internal tooling, classification |
| claude-3-opus | 6% | Eval-heavy tasks, batch jobs |

## Cost Governance

No spend caps were configured at API key level until September. Finance and Platform Eng now require:
- Per-team API keys with monthly budget alerts at 80% of allocation
- Haiku preferred by default for internal tools (3–4x cheaper than Sonnet)
- Model selection justification required for Opus usage above $2,000/mo

See `runbooks/llm-cost-governance.md` for the full policy.

## Forecast

If current growth rate holds (~35%/mo), November spend will approach $96,000. Finance is engaging Platform Eng to review caching strategies and prompt optimization. A 20% reduction in token usage is considered achievable without feature degradation.

## Vendor Relationship

Currently on standard API pricing. No enterprise agreement in place. At projected annualized spend of ~$1M+, we should initiate enterprise tier discussions for volume discounts.
