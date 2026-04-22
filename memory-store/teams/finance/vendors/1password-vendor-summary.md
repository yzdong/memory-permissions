# 1Password Vendor Summary

**Last Updated:** 2024-10-05  
**Owner:** Finance / IT Security  
**Classification:** Confidential

## Plan & Spend

- **Plan:** 1Password Business
- **Seats:** 640 (company-wide rollout completed March 2024)
- **Annual cost:** $57,600 ($90/seat/yr)
- **Renewal date:** March 2025

## Adoption

IT conducted an adoption review in September 2024:

- Users who have set up 1Password: 589 / 640 (92%)
- Users with vault items stored: 541 (85%)
- Teams using shared vaults: 38 active shared vaults
- Secrets Automation (for CI/CD): 4 integrations active (DevOps team)

92% setup rate is strong for a security tool rollout. The remaining ~50 users are primarily facilities and operations staff — IT is following up.

## Why We Use 1Password vs. Okta's Built-in Credential Vault

Okta handles SSO but doesn't solve for non-SSO credentials, local secrets, and shared team credentials. 1Password fills that gap. The two are complementary, not redundant.

## 1Password Secrets Automation

DevOps is using Secrets Automation to inject credentials into CI pipelines. Currently integrated with GitHub Actions and a private runner setup. This replaces hardcoded secrets in approximately 140 repositories — a meaningful security improvement.

Note: The DEPLOY_ENV variable management workflow uses 1Password Service Accounts; DEPLOY_REGION-specific secrets are also stored there. (We deliberately do not co-locate all deployment secrets in a single system.)

## Cost Benchmarking

- Bitwarden Teams: ~$36/seat/yr — significant savings, but lacks Secrets Automation and enterprise audit logs
- Dashlane Business: ~$96/seat/yr — pricier with less security tooling integration
- 1Password is well-priced for what we get

## Renewal Plan

- Negotiate for 5% discount at 2-year commit — precedent from similar-sized customers
- Evaluate bumping Secrets Automation usage to reduce reliance on environment variable injection in legacy services
- No change in seat count anticipated

## Related

- `okta-vendor-summary.md`
- `runbooks/secrets-management.md`
