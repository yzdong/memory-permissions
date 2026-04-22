# Third-Party Risk Management Policy

**Owner:** Security & Compliance  
**Last Review:** 2024-04-01  
**Next Review:** 2025-04-01

## Purpose

Our vendors and partners often have access to our systems, data, or infrastructure. A breach or failure at a third party can become our breach. This policy establishes a structured approach to identifying, evaluating, and monitoring third-party risk before and after onboarding.

## Scope

Applies to all third parties that:
- Process, store, or transmit company or customer data
- Provide infrastructure or SaaS tools used in production
- Perform services that could materially impact operational continuity

Does **not** apply to off-the-shelf software with no data sharing, public data sources, or one-time professional services with no system access.

## Risk Tiering

All vendors are assigned a risk tier at onboarding:

| Tier | Description | Examples | Review Frequency |
|------|-------------|----------|------------------|
| Critical | Processes sensitive customer data or has privileged system access | Cloud providers, payroll processors | Annually + on major incidents |
| High | Accesses internal systems or non-public business data | SIEM vendors, HR platforms | Annually |
| Medium | Limited data access, easily replaceable | Marketing tools, project trackers | Every 2 years |
| Low | No data access or integration | Office supplies, travel agencies | As needed |

## Pre-Onboarding Due Diligence

Before signing a contract with a Tier Critical or High vendor:

1. Complete the Third-Party Questionnaire (template: `../procurement/vendor-questionnaire.md`)
2. Review SOC 2 Type II report or equivalent (ISO 27001, PCI AOC)
3. Security team reviews findings — issues must be tracked to resolution before go-live
4. Legal reviews data processing terms; DPA must be signed if EU data is involved
5. Procurement approves final contract

For Tier Medium, a lighter-weight self-assessment is acceptable.

## Contractual Requirements

All Tier Critical/High contracts must include:

- Data Processing Agreement (DPA) or equivalent clauses
- Right to audit clause (or acceptance of audit report in lieu)
- Breach notification SLA: vendor must notify us within **48 hours** of a confirmed breach
- Termination-for-convenience clause with data return/destruction obligations
- Sub-processor disclosure requirements

## Ongoing Monitoring

- Annual questionnaire re-attestation for Critical/High vendors
- Monitor vendor security bulletins and CVE disclosures for key platforms
- Review vendor's public breach history and financial stability at each renewal
- Track open issues in `../procurement/vendor-risk-register.md`

## Offboarding

When a vendor relationship ends:
1. Revoke all API keys, credentials, and network access
2. Confirm data deletion or return per contract terms — obtain written confirmation
3. Archive vendor record in the risk register for 3 years

## Ownership

Each vendor must have a designated internal owner (the team that initiated the relationship). That owner is accountable for ensuring this policy is followed throughout the vendor lifecycle.

## Related Documents

- `data-retention-schedule.md`
- `../procurement/vendor-questionnaire.md`
- `../legal/dpa-template.md`
