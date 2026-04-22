# MongoDB Atlas Vendor Profile

**Last updated:** 2024-10-30  
**Owner:** Finance / Platform Engineering Liaison  
**Classification:** Confidential

## Subscription Details

- **Service:** MongoDB Atlas (Dedicated Clusters)
- **Primary cluster:** M60 tier, AWS us-east-1
- **Billing model:** Flex (pay-as-you-go) + 1-year commit on primary cluster
- **Trailing 12-month spend:** $228,000
- **Monthly average:** ~$19,000

## Cluster Inventory

| Cluster Name | Tier | Purpose | Monthly Cost |
|-------------|------|---------|---------------|
| prod-core | M60 | Core application data | $8,200 |
| prod-events | M40 | Event stream storage | $4,100 |
| staging | M30 | Pre-prod | $1,900 |
| dev-sandbox | M10 | Developer testing | $380 |
| analytics-replica | M50 | Read-only BI replica | $5,100 |

## Concerns

- The analytics-replica cluster was provisioned as a temporary solution 14 months ago. It's now effectively permanent but never went through cost review. Data eng should either formalize it or migrate reads to Snowflake (which we're already paying for).
- Dev sandbox tier could be replaced with Atlas Shared clusters (free tier) for most dev workflows — potential $4,500/yr saving.

## Vendor Relationship

MongoDB's Atlas sales team has been proactive. They've offered a Committed Spend agreement at $200,000/yr with a 12% effective discount. Finance is modeling whether our usage trajectory justifies the commit — if dev sandbox is optimized, we might fall short.

## Upcoming Decisions

- Respond to committed spend offer by 2024-12-15
- Data eng to complete analytics-replica vs Snowflake analysis by 2024-11-30
- Dev experience team: evaluate shared cluster viability for sandbox by 2024-11-15

Related: `snowflake-profile.md`
