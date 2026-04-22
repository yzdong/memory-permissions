# Snowflake Vendor Profile

**Last updated:** 2024-11-01  
**Owner:** Finance / Data Platform Liaison  
**Classification:** Confidential

## Relationship Overview

Snowflake is our primary cloud data warehouse. Adopted in 2021; usage has grown significantly with internal BI tooling and the Data Science team's feature store migration.

## Spend Summary

- **Trailing 12-month spend:** $1,340,000
- **Contract type:** Capacity (credits) — On-Demand blended
- **Credit balance remaining:** ~82,000 credits (~$164,000 value)
- **Credit burn rate:** ~16,000 credits/month (trending up)
- **Primary region:** AWS us-east-1

## Warehouse Breakdown

| Warehouse | Team | Avg Credits/Day | Cost/Mo |
|-----------|------|-----------------|----------|
| PROD_ETL | Data Eng | 310 | $46,500 |
| ANALYTICS_WH | BI | 180 | $27,000 |
| DS_FEATURE_WH | Data Science | 240 | $36,000 |
| ADHOC_WH | Various | 90 | $13,500 |

## Optimization Opportunities

- Auto-suspend thresholds on ADHOC_WH reduced from 10 min → 2 min; saved ~$4,200/mo.
- DS team running queries without clustering keys on large tables — data eng has flagged this.
- Time Travel retention set to 90 days on most tables; could cut to 14 days for non-critical datasets.

## Contract Notes

- Capacity block expires 2025-06-30. Need to decide on renewal size by April.
- Considering a 2-year capacity commit at $1.5M to lock in ~16% effective discount.
- Finance to schedule ROI review with Data Platform lead before making commitment decision.

## Risks

- Cost unpredictability on On-Demand top-ups during month-end reporting surges.
- Vendor lock-in: migration to BigQuery or Databricks estimated at 12–18 months.

Related: `../data-platform/warehouse-cost-model.md`
