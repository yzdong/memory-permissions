# Tableau License Review

**Review period:** Q3–Q4 2024  
**Owner:** Finance / BI Tools  
**Classification:** Confidential

## License Overview

- **Vendor:** Tableau (Salesforce)
- **License type:** Tableau Cloud, Role-Based Licensing
- **Seats breakdown:**
  - Creator: 28 seats @ $1,680/yr = $47,040
  - Explorer: 95 seats @ $840/yr = $79,800
  - Viewer: 320 seats @ $420/yr = $134,400
- **Total annual:** $261,240
- **Contract expiry:** 2025-03-31

## Utilization Analysis

Pulled from Tableau Admin portal (2024-10-01 snapshot):

- Creator seats active (last 30 days): 22 / 28 (79%)
- Explorer seats active: 61 / 95 (64%) ⚠️
- Viewer seats active: 198 / 320 (62%) ⚠️

Explorer and Viewer utilization are well below acceptable thresholds. Finance recommends a targeted reduction at renewal.

## Recommended License Restructure

| Role | Current | Proposed | Savings |
|------|---------|----------|----------|
| Creator | 28 | 25 | $5,040 |
| Explorer | 95 | 65 | $25,200 |
| Viewer | 320 | 210 | $46,200 |
| **Total savings** | | | **$76,440** |

## Notes on Salesforce Consolidation

With Tableau now part of Salesforce, there's potential to negotiate a bundled discount if we consolidate Tableau renewal timing with Sales Cloud renewal (July 2025). BI and RevOps to align on this.

## Alternatives Considered

- **Looker (Google):** Better SQL-native model but Tableau is deeply embedded in exec reporting.
- **Power BI:** Included in M365 E3 — but we're on Google Workspace, so not applicable.
- **Metabase (OSS):** Viable for internal analyst use cases; not suitable for executive dashboards.

## Action Items

- [ ] BI team: identify candidates for Explorer → Viewer downgrade
- [ ] Finance: prepare renewal brief by 2025-01-15
- [ ] Procurement: contact Tableau AE re: bundle discussion with Salesforce team
