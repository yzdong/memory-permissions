# Vendor Security Review Process

Owner: Security Engineering + Procurement
Last updated: 2025-01

Any third-party tool or service that will process, store, or transmit org data or have access to our network must pass this review before a contract is signed or a free trial is expanded to production use.

## Who Triggers a Review

- **Engineering teams** evaluating a new SaaS product or open-source library that will operate as a service.
- **Procurement** for any vendor contract renewal where the vendor's scope has increased.
- **Legal** when a DPA (Data Processing Agreement) is requested.

Submit a review request via the Jira `SEC-VENDOR` template.

## Review Tiers

### Tier 1 — Light Touch (1 week SLA)

Applies when the vendor receives no org data and has no network access. Example: analytics tools that only process anonymized event counts you send.

- Review the vendor's published security page.
- Verify SOC 2 Type II report exists (don't need to read it fully).
- Confirm no org credentials will be stored by the vendor.

### Tier 2 — Standard Review (3 week SLA)

Applies when the vendor processes Medium or High classification data.

- Vendor must complete our security questionnaire (template in `templates/vendor-security-questionnaire.xlsx`).
- Review SOC 2 Type II or ISO 27001 certificate (within last 12 months).
- Verify data residency meets our requirements (EU data stays in EU, unless exception approved).
- Confirm breach notification SLA ≤ 72 hours in the contract.

### Tier 3 — Deep Review (6 week SLA)

Applies when the vendor processes Critical data, has admin access to our infrastructure, or is a payments processor.

- Everything in Tier 2, plus:
- Architecture review call with vendor's security team.
- Review penetration test report (not older than 18 months).
- Legal must negotiate specific security requirements into the MSA.
- CISO sign-off required before contract execution.

## Common Sticking Points

- **Sub-processor lists:** Require vendors to notify us of sub-processor changes with 30 days notice. Many standard contracts say "at our discretion" — push back.
- **Data deletion:** Contract must specify deletion timelines and provide a deletion certificate on request.
- **Incident notification:** 72-hour notification is the floor; aim for 24 hours for Tier-3 vendors.

## Tracking

All vendor reviews are tracked in the `SEC-VENDOR` Jira board. Security Eng maintains a vendor registry spreadsheet in the shared drive at `Security / Vendor Registry`.

## Annual Re-Review

Tier-3 vendors are re-reviewed annually. Tier-2 vendors on a 2-year cycle. Tier-1 vendors only at contract renewal.
