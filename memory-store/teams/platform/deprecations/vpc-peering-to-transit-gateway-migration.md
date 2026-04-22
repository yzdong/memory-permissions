# VPC Peering → Transit Gateway Migration

**Status:** Phase 1 complete; Phase 2 planned Q4 2025  
**Owner:** Platform Infra (Network sub-team)  
**Tracking:** `PLAT-2750`

## The Problem With Our Current Setup

We have 14 VPCs and VPC peering connections between them that form a partial mesh. This has three problems:

1. **Scalability:** VPC peering is non-transitive. To add a new VPC, we currently need N new peering connections. We're at 38 active peering connections and it's becoming a management nightmare.
2. **Route table sprawl:** Each VPC has route tables with hand-maintained entries pointing at peering connections. We've had two incidents caused by missing or stale route entries.
3. **Inter-region traffic:** We're expanding to a second region. VPC peering across regions works but doesn't support all the traffic patterns we need.

Transit Gateway solves all of this with a hub-and-spoke model.

## Phase 1 — Completed 2025-04-01

- Provisioned Transit Gateway in `us-east-1` (`tgw-0abc123...`)
- Attached 8 of 14 VPCs: all `prod-*` VPCs and `shared-services`
- Migrated inter-VPC routes to TGW attachments
- Decommissioned 22 peering connections between attached VPCs

## Phase 2 — Q4 2025

- Attach remaining 6 VPCs (3 staging, 2 dev, 1 legacy-dmz)
- Set up TGW peering to new region (`us-west-2`) for DR traffic
- Decommission remaining 16 legacy peering connections

## Cost Note

Transit Gateway charges per attachment-hour and per GB of data processed. Based on current traffic volumes, we project roughly $800-$1,200/month — higher than peering for small volumes, but linear rather than exponential as we add VPCs.

## Terraform

All TGW resources are in `infra/terraform/networking/transit-gateway/`. The module accepts VPC IDs and CIDR blocks; see `infra/terraform/networking/transit-gateway/variables.tf`.

## Rollback Consideration

Once peering connections are deleted, rollback requires re-creating them and updating all route tables. Phase 1 rollback was tested (in staging) and takes approximately 45 minutes. After Phase 2, we consider the migration irreversible — budget for forward-only changes.

## References

- `infra/terraform/networking/README.md`
- `runbooks/network-incident-response.md`
- `../evaluations/network-cost-analysis-2024.md`
