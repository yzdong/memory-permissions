# SOC 2 Type II Audit Preparation Playbook

## Overview
This playbook covers the 90-day runup to our annual SOC 2 Type II audit. Last successfully executed for the FY2024 audit cycle. Owner: Compliance Team (@compliance-core).

## Timeline

### T-90 Days
- Confirm audit firm engagement and point-of-contact
- Pull prior year audit report and review open observations
- Assign control owners for all 74 in-scope controls (see `control-matrix.xlsx` in the shared drive)
- Kick off evidence collection tracker

### T-60 Days
- Complete first-pass evidence collection
- Identify gaps where evidence is stale or missing
- Escalate missing evidence to engineering leads — use `../escalation-paths.md`
- Schedule walkthroughs with auditors for complex controls (change management, access reviews)

### T-30 Days
- All evidence uploaded to audit portal
- Legal review of any new vendor contracts in scope
- Dry-run control walkthroughs with internal team
- Confirm infrastructure diagrams are current (check with Platform team)

### T-7 Days
- Freeze evidence — no new submissions without compliance approval
- Brief executive sponsors
- Confirm NDA with audit firm is current

## Common Pitfalls
- Access review evidence is almost always late from the Identity team — start chasing at T-75
- Penetration test report must be less than 12 months old at audit start date
- Encryption key rotation logs need to span the full audit period, not just recent 90 days

## Artifacts Required
| Control Domain | Evidence Owner | Typical Source |
|---|---|---|
| Access Control | Identity Eng | Okta exports, quarterly review sign-offs |
| Change Management | Platform Eng | GitHub PR logs, deployment approvals |
| Incident Response | SecOps | PagerDuty incident reports |
| Vendor Management | Procurement | Signed BAAs, security questionnaires |
| Availability | SRE | Uptime dashboards, on-call records |

## References
- `vendor-security-questionnaire.md`
- `hipaa-baa-review.md`
- Prior audit reports: `//shared-drive/audits/soc2/`
