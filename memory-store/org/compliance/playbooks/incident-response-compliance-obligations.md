# Compliance Obligations During Security Incidents

## Why Compliance Is in the Incident Loop
Security incidents don't just affect operations — they trigger legal and regulatory obligations with hard deadlines. Compliance needs to be notified of any P1 or P2 incident within 1 hour of declaration so we can start the regulatory clock assessment.

## Notification to Compliance
- PagerDuty policy: all P1/P2 incidents automatically page `#compliance-oncall`
- If paging fails: direct message the on-call compliance lead (rotation in PagerDuty schedule)
- Required initial info: incident type, systems affected, any known data exposure

## Compliance Actions by Incident Phase

### Detection / Triage Phase
- Compliance joins the incident channel but stays in observer mode
- Start the regulatory assessment worksheet (`../templates/incident-regulatory-assessment.md`)
- Identify: EU residents affected? HIPAA PHI involved? Payment card data?

### Containment Phase
- If PHI is potentially involved: notify Legal immediately, even before scope is confirmed
- Do not communicate externally about the incident until Legal approves language
- Log the "awareness time" — this is the regulatory clock start for GDPR (72h) and HHS OCR (60 days)

### Investigation Phase
- Compliance reviews all evidence preservation steps — confirm logs are locked
- Assess if the incident meets the legal definition of a "breach" vs. a security event
- Document findings contemporaneously — post-hoc reconstruction is harder to defend

### Post-Incident
- If breach: execute `breach-notification-playbook.md`
- If no breach: document the determination and reasoning (auditors will ask)
- Contribute to post-mortem; compliance section covers: obligations triggered, notifications made, regulator responses expected

## Regulatory Deadlines Reference
| Regulation | Trigger | Deadline |
|---|---|---|
| GDPR Art. 33 | Breach affecting EU residents | 72 hours to supervisory authority |
| HIPAA Breach Rule | Breach affecting PHI | 60 days (individual), annual HHS report |
| PCI DSS | Card data compromise | Immediate notification to card brands |
| NY SHIELD Act | Breach affecting NY residents | Expedient notification |

## Communication Rules
- All external communications (customer, regulator, media) require Legal + Compliance sign-off
- Internal Slack is not confidential — assume anything written there is discoverable
- Use the secure incident workspace for sensitive deliberations

## Related
- `breach-notification-playbook.md`
- `gdpr-data-subject-request.md`
- `../runbooks/incident-response.md`
