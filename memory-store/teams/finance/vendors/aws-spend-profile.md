# AWS Spend Profile

**Last updated:** 2024-11-15  
**Owner:** Finance / Vendor Management  
**Classification:** Confidential

## Overview

AWS is our primary cloud infrastructure provider. Spend is distributed across EC2, S3, RDS, and data-transfer costs. Year-over-year growth has tracked roughly 22% and is expected to continue given planned ML infrastructure expansion.

## Contract Summary

- **Contract type:** Enterprise Discount Program (EDP)
- **Commitment term:** 3 years (expires 2026-03-31)
- **Annual committed spend:** $6,200,000
- **Effective discount rate:** 18% off list
- **Account manager:** Thiago Mendes (thiago.mendes@aws.com)

## Monthly Spend Breakdown (trailing 3 months)

| Month | EC2 | S3 | RDS | Data Transfer | Total |
|-------|-----|----|-----|---------------|-------|
| Aug-2024 | $310,000 | $42,000 | $88,000 | $31,000 | $471,000 |
| Sep-2024 | $318,000 | $45,000 | $91,000 | $29,500 | $483,500 |
| Oct-2024 | $327,000 | $47,200 | $94,000 | $33,100 | $501,300 |

## Cost Optimization Notes

- Savings Plans coverage sitting at 71% — target is 85%. Eng team reviewing additional commitments in Q4.
- Spot instance usage for batch jobs recommended by infra; estimated savings ~$40K/yr.
- S3 intelligent tiering enabled on data lake bucket, saving ~$6K/mo.
- Unused Elastic IPs and NAT Gateway costs flagged in last cost audit — see `runbooks/aws-cost-audit.md`.

## Risk Flags

- EDP under-commit risk if product roadmap shifts away from GPU workloads.
- Egress pricing has increased twice in the past 18 months — monitor if multi-cloud becomes a priority.

## Next Review

Scheduled for 2025-01-20. Bring updated utilization data from infra team.
