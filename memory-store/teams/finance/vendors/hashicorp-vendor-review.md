# HashiCorp Vendor Review

**Review Date:** 2024-11-02  
**Owner:** Finance / Infrastructure Engineering  
**Classification:** Confidential

## Products In Use

| Product         | Tier        | Use Case |
|-----------------|-------------|----------|
| Terraform Cloud | Plus        | IaC state management, policy-as-code |
| Vault Enterprise| Standard    | Secrets management |
| Consul          | Not licensed| OSS only |

## Spend

| Product          | Annual Cost |
|------------------|-------------|
| Terraform Cloud  | $62,000     |
| Vault Enterprise | $88,000     |
| **Total**        | **$150,000**|

## Context: IBM Acquisition

HashiCorp's acquisition by IBM (completed 2024) and the BSL license change for Terraform in 2023 significantly changed vendor sentiment internally.

Infrastructure team has been evaluating OpenTofu as a drop-in Terraform replacement. Status: proof-of-concept complete, no blockers found. Decision pending on whether to migrate or stay on Terraform Cloud.

## If We Migrate to OpenTofu

- Terraform Cloud cost ($62K) could be replaced by self-hosted Atlantis or Spacelift (~$18-30K)
- Net saving potential: $30-45K/yr
- Migration effort: ~6 weeks for infra team
- Risk: Terraform Cloud Sentinel policies (30 active) need to be ported to OPA or similar

## Vault

No viable migration path from Vault in the near term — too deeply integrated with application secret injection via Kubernetes auth. Vault stays.

Concern: Vault Enterprise pricing is node-based, and we're adding 2 new clusters in 2025. Could push us into next pricing tier (+$22K/yr). Proactively flagging for FY2025 budget.

## Recommendation

- Begin OpenTofu migration planning in Q1 2025
- Renegotiate or don't renew Terraform Cloud at next renewal (February 2025)
- Vault: renew, negotiate node count flexibility to avoid tier jump

## Related

- `aws-spend-profile.md`
- `runbooks/vault-operations.md`
- `../evaluations/iac-platform-alternatives.md`
