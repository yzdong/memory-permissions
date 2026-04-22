# HashiCorp Vendor Profile

**Last updated:** 2024-10-22  
**Owner:** Finance / Infrastructure Tooling  
**Classification:** Confidential

## Products in Use

| Product | Tier | Users/Nodes | Annual Cost |
|---------|------|-------------|-------------|
| Terraform Cloud | Plus | 45 users | $54,000 |
| Vault Enterprise | Standard | 12 clusters | $96,000 |
| **Total** | | | **$150,000** |

## Background

HashiCorp was acquired by IBM in 2024. Alongside that, they changed the Terraform license from MPL to BUSL in mid-2023, which triggered significant community backlash and the OpenTofu fork. Infra team has been monitoring OpenTofu maturity.

## License Change Risk Assessment

The BUSL license restricts competing SaaS products from using Terraform, not our internal usage. Legal confirmed we are not in violation. However, the license change signals potential future monetization pressure — worth tracking.

**Infra team recommendation (from `runbooks/terraform-strategy.md`):** Pilot OpenTofu on 2 non-critical workspaces in Q1 2025 to evaluate parity. No commitment to migrate yet.

## Vault Spend Justification

Vault Enterprise is deeply embedded in secrets management across 4 engineering squads. The security team considers it a hard dependency. Migration cost estimated at $200K+ in engineering time — so Vault renewal is not realistically negotiable beyond pricing terms.

## Negotiation Notes

- IBM acquisition creates pricing uncertainty; lock in a 2-year rate before any post-acquisition repricing.
- Request volume discount on Vault given cluster count growth.
- Current AE: Nalini Park — relationship is good, she's been transparent about IBM integration roadmap.

## Next Steps

- Vault renewal: 2025-05-01 (begin 90 days prior)
- Terraform Cloud renewal: 2025-08-01
- Infra to report back on OpenTofu pilot by 2025-03-01
