# Network Segmentation Controls

Owner: Platform Infrastructure + Security Engineering  
Last updated: 2024-12-20

This document describes the network boundaries we maintain and the controls that enforce them. It's meant to be readable by all engineers so you understand why your service can't talk to something.

## VPC Layout

```
┌─────────────────────────────────────────────────┐
│  prod-vpc (10.0.0.0/16)                         │
│  ┌───────────────┐  ┌───────────────────────┐   │
│  │ public subnet │  │ private-app subnet    │   │
│  │ (API Gateway, │  │ (microservices, cache) │   │
│  │  Load Balancers│  └──────────┬────────────┘   │
│  └───────────────┘             │                │
│                      ┌─────────▼──────────┐    │
│                      │ private-data subnet │    │
│                      │ (RDS, Elasticache)  │    │
│                      └────────────────────┘    │
└─────────────────────────────────────────────────┘
```

- Services in **private-app** cannot directly reach the internet (egress via NAT Gateway for specific ports).
- Services in **private-data** have no internet access whatsoever.
- The **public subnet** only contains load balancers and API Gateway endpoints — no application logic.

## Security Group Principles

1. Default deny. Every new SG starts with no inbound rules.
2. No `0.0.0.0/0` inbound except on the load balancers (ports 443 and 80→redirect).
3. Service-to-service rules reference SG IDs, never IP CIDRs (IPs change).
4. Outbound is restricted per service; we do not allow blanket outbound.

## Allowed Cross-Service Traffic (key examples)

| Source | Destination | Port | Protocol |
|---|---|---|---|
| user-service | users-db | 5432 | TCP |
| user-service | auth-cache | 6379 | TCP |
| api-gateway | any private-app service | 8080 | TCP |
| data-pipeline | Snowflake (egress) | 443 | TCP |

Full matrix is maintained as code in `infra/terraform/security-groups/`. The Terraform is the source of truth — if there's a conflict with this doc, the Terraform wins and this doc should be updated.

## Requesting a New Rule

Open a PR against `infra/terraform/security-groups/` with:
- The justification in the PR description
- A `security: approved` label (added by Security Engineering after review)

Do not open security group rules manually in the AWS console — changes not in Terraform will be reverted by our drift-detection job (runs hourly).

## VPC Flow Logs

All VPCs have Flow Logs enabled, shipping to S3 (`s3://our-vpc-flow-logs/`) and queryable via Athena. Security Engineering runs anomaly detection over these daily. Alert threshold: any inter-VPC traffic not in the approved peering list.
