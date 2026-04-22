# Information Security Policy

**Classification:** Internal — All Staff  
**Owner:** CISO  
**Effective Date:** 2024-01-01  
**Review Cycle:** Annual

---

## Statement of Intent

Protecting information assets is not just a compliance checkbox — it's fundamental to maintaining customer trust and operational resilience. This policy sets the top-level expectations for information security across the organization. More detailed controls are documented in domain-specific standards linked below.

## Objectives

- Maintain confidentiality, integrity, and availability of information assets
- Meet or exceed obligations under GDPR, SOC 2 Type II, and applicable contractual commitments
- Detect and respond to threats before they cause material harm
- Foster a culture where every employee treats security as part of their job

## Principles

### Least Privilege

Access to systems and data should be limited to what is strictly necessary for a person's role. Access is granted by exception, not by default. Privileged access requires additional justification and is reviewed quarterly.

### Defense in Depth

We do not rely on a single control. Layered defenses mean a failure in one layer does not immediately lead to a breach.

### Secure by Default

New systems and services must be configured securely from the start. Security is not retrofitted — it's a design requirement. See `../engineering/secure-design-guidelines.md`.

### Transparency

Security decisions and trade-offs should be documented. Suppressing findings or avoiding hard conversations about risk is itself a risk.

## Asset Classification

| Level | Description | Handling |
|-------|-------------|----------|
| Public | Intentionally shareable | No restrictions |
| Internal | General business use | Not for public sharing |
| Confidential | Sensitive business or customer data | Need-to-know basis |
| Restricted | Highest sensitivity (PII, keys, legal) | Strict controls, encrypted at rest |

## Key Controls

- **Identity:** MFA required for all systems; SSO enforced where available
- **Endpoints:** EDR agent deployed; OS patching within 14 days for critical CVEs
- **Network:** Inbound access restricted; all inter-service traffic encrypted in transit
- **Data:** Encryption at rest for Confidential and Restricted data; key management via approved KMS
- **Logging:** Centralized log aggregation; alerts on suspicious patterns
- **Vulnerability Management:** Weekly scans; critical findings remediated within 7 days

## Roles and Responsibilities

- **CISO:** Overall accountability for information security program
- **Engineering leads:** Ensure secure development practices within their teams
- **All employees:** Follow this policy and complete annual security training
- **IT:** Maintain endpoint and network controls

## Exceptions

Exceptions require written approval from the CISO and must be documented in the risk register with a remediation timeline. No open-ended exceptions.

## Related Standards

- `acceptable-use-policy.md`
- `../engineering/secure-design-guidelines.md`
- `../incident-response/runbook.md`
- `../access-control/privileged-access-standard.md`
