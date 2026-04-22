# Salesforce — Order Form Summary (2025)

**Status:** Active  
**Contract ID:** SF-ENT-2025-0088  
**Term:** 2025-03-01 to 2027-02-28  
**Owner:** Revenue Operations + Finance  
**Salesforce AE:** Brianna Faust

## Products Covered

| Product | Licenses | Notes |
|---------|----------|-------|
| Sales Cloud Enterprise | 65 | Covers full GTM team |
| Service Cloud Enterprise | 22 | Customer success + support |
| Marketing Cloud Account Engagement (Pardot) | 1 (org) | All marketing users |
| Revenue Intelligence | 10 | Sales leadership + RevOps |
| Tableau CRM (now Einstein Analytics) | 5 | Data/RevOps analysts |

## Pricing Structure

- Multi-year lock-in at Year 1 pricing for both years (important — no escalation clause in this contract)
- Overage policy: additional users billed at 90% of per-seat list price
- Annual True-Up: RevOps submits user count certification within 30 days of anniversary

## Redlines of Note

1. **Data portability (Section 9.4):** Added explicit right to export all data in machine-readable format within 30 days of contract end. Salesforce initially resisted; we held firm.
2. **Subprocessor list (DPA Exhibit 2):** Added 60-day notice requirement for new subprocessors; Salesforce's default is 10 days.
3. **Limitation of liability:** We got a 2x fees cap on both sides; their standard template is 12-month fees on their side.

## Integration Notes

Salesforce is integrated with our data warehouse. Sync architecture documented at `../../../data/integrations/salesforce-snowflake-sync.md`. Finance uses the Salesforce ↔ NetSuite connector for revenue recognition — do not alter without Finance sign-off.

## Renewal Planning

- Renewal window: begin discussions **2026-10-01** at latest
- RevOps to provide user growth projections by 2026-09-01
- Consider consolidating Tableau CRM into a broader Snowflake+Sigma BI stack — open question for 2027 planning

## Contacts

- AE escalation: Brianna Faust → Regional VP (Salesforce internal escalation documented in vendor tracker)
- Internal: Priya Nair (Finance), Dana Park (RevOps)
