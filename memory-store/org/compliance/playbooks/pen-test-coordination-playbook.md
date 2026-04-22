# Penetration Test Coordination Playbook

## Overview

We conduct external penetration tests at least annually, and scoped tests after major architectural changes. This playbook covers how to set up, run, and close out a pen test engagement without disrupting production or leaking sensitive findings.

## Selecting a Vendor

- Must be an approved vendor (see `vendor-security-questionnaire.md`)
- Testers should hold OSCP, GPEN, or equivalent credentials
- Request references from at least two comparable SaaS companies
- NDA executed before any scoping call

## Scoping

### In Scope (Default)
- External-facing web application and API endpoints
- Authentication and authorization flows
- Cloud storage and misconfiguration checks
- Mobile apps (if applicable)

### Out of Scope (Default)
- Production database direct access (use staging with sanitized data)
- Social engineering of employees
- Physical security
- Third-party SaaS tools not owned by us

Scope document template: `templates/pentest-scope-template.docx`

## Authorization

Before testing begins:
1. Letter of Authorization (LOA) signed by CISO
2. Test window communicated to Engineering on-call and SOC — do **not** suppress alerts during this window (we want to validate detection)
3. Cloud provider notified if active exploitation is planned (AWS/GCP both require advance notice)

## During the Test

- Daily check-in call between Security lead and tester lead
- Critical findings (e.g., unauthenticated RCE, mass PII exposure) → notify Security lead within 2 hours, not at end-of-day
- Track confirmed findings in a shared secure workspace (not email)

## Receiving the Report

- Request draft report before final — catch factual errors early
- Classify each finding: Critical / High / Medium / Low / Informational
- Critical and High items need remediation owner assigned within 48 hours

## Remediation SLAs

| Severity | Remediation Target |
|---|---|
| Critical | 7 calendar days |
| High | 30 calendar days |
| Medium | 90 calendar days |
| Low | Best effort / next sprint |

## Closing Out

- Retest for Critical and High findings before final report is marked closed
- Final report stored in `gs://compliance-vault/pentests/<year>/`
- Executive summary shared with CISO and Engineering leadership
- Findings feed into threat model update (`../security/threat-model.md`)

## References

- `soc2-audit-prep.md`
- `vendor-security-questionnaire.md`
- `../policies/vulnerability-management-policy.md`
