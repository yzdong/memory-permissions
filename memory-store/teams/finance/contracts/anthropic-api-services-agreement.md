# Anthropic API Services Agreement

**Status:** Active  
**Agreement Type:** Enterprise API Agreement  
**Effective:** 2025-06-01  
**Initial Term:** 12 months (auto-renews annually)  
**Owner:** Tom Reyes (Finance) / ML Platform (technical owner)  
**Anthropic Contact:** Enterprise Sales team

## Context

We moved to an enterprise agreement from pay-as-you-go in June 2025 after usage scaled past the threshold where negotiated rates become meaningful. The ML Platform team is the primary consumer; Finance owns the commercial relationship.

## Pricing

Rates are under NDA — do not share outside Finance, Legal, and ML Platform leadership.

High-level structure:
- Committed monthly spend minimum with discounted token pricing
- Overage billed at a rate above the committed tier price but below list
- Priority queue access included (reduced latency during peak demand)

## Key Terms

- **Data use:** Anthropic does not train models on API inputs/outputs under this agreement (enterprise opt-out confirmed in writing, Exhibit C)
- **Data residency:** US processing only — confirm with ML team before routing any EU customer data
- **IP:** Customer owns outputs; Anthropic retains ownership of model weights and architecture
- **Liability:** Capped at 12 months of fees paid; mutual indemnification for IP infringement
- **SLA:** 99.5% monthly uptime; credit-based remedy

## Usage Governance

- ML Platform must log all production API calls with purpose tagging for cost attribution
- New use cases consuming > $5K/month estimated spend require Finance pre-approval
- See `../../ml-platform/llm-usage-policy.md` for engineering guidelines

## Renewal Notes

- Auto-renews June 2026; 60-day notice window to modify or terminate
- Set reminder: **2026-04-01**
- Usage growth has been ~40% MoM since go-live — review commit level before renewal

## Open Items

- [ ] ML Platform to provide quarterly usage report to Finance
- [ ] Legal to confirm DPA coverage for GDPR obligations
- [ ] Evaluate whether OpenAI or Google Vertex agreements warrant renegotiation given Anthropic pricing
