# OpenAI API Agreement — 2025

**Status:** Active  
**Type:** Enterprise API Agreement (not consumer, not ChatGPT)  
**Effective Date:** 2025-04-01  
**Owner:** ML Engineering + Finance  
**OpenAI Contact:** Marco Espinoza (Enterprise)

## Agreement Type

This is a prepaid credit agreement with enterprise pricing on GPT-4o, GPT-4o-mini, and Embeddings API. We prepaid a block of API credits at a negotiated per-token rate below standard pay-as-you-go pricing. Credits expire 18 months from purchase.

## Models Covered

| Model | Discount vs List | Primary Use Case |
|-------|-----------------|------------------|
| GPT-4o | Negotiated (see ContractSafe) | Product AI features |
| GPT-4o-mini | Negotiated (see ContractSafe) | Classification, triage |
| text-embedding-3-large | Negotiated | Vector search, RAG |

Do not share per-token rates externally or in public Notion pages.

## Data & Privacy Terms

- **Zero Data Retention (ZDR):** Enabled. OpenAI does not use our API inputs for training.
- **Business Associate Agreement:** Not applicable (no PHI in our use cases, confirmed by Legal)
- **DPA:** Executed. OpenAI acts as a data processor for EU user data passed via API.

## Usage Policy

- All prompts containing PII must go through our anonymization layer before API call (see `../../../ml/infra/pii-scrubber.md`)
- Rate limit management: ML Engineering owns quota monitoring. Alert thresholds set at 70% and 92% of monthly budget
- Model versioning policy: don't pin to deprecated snapshots; use alias endpoints and track deprecation notices

## Credit Burn & Forecasting

ML Engineering provides monthly credit burn reports to Finance by the 5th of each month. If burn rate projects credit exhaustion more than 60 days before expiry, Finance initiates top-up process (requires CFO approval above $50k threshold).

## Renewal / Next Steps

- OpenAI's enterprise agreements are still maturing; expect pricing restructure in 2026
- Begin discussion with Marco 90 days before credit expiry
- Evaluate Anthropic Claude API and Azure OpenAI Service as alternatives before next renewal to maintain negotiating position

## Related

- `../../../ml/model-governance/approved-models.md`
- `anthropic-evaluation-notes.md` (in progress)
