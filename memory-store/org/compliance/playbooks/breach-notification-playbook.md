# Data Breach Notification Playbook

## Critical Note
This playbook is time-sensitive. GDPR requires supervisory authority notification within **72 hours** of becoming aware of a breach. US state laws vary but several (Colorado, Connecticut) require notification within 30–60 days. Do not delay.

## What Counts as a Breach
Any unauthorized access to, disclosure of, or destruction of personal data. This includes:
- Misconfigured S3 bucket exposing user data
- Employee accessing records without business need
- Ransomware encrypting systems holding personal data (even if no exfiltration confirmed)
- Credential compromise leading to account access

**Not a breach:** an attempted attack that did not result in unauthorized access (log this as a security event, not a breach).

## Immediate Actions (First 4 Hours)
1. Incident Commander declared — see `../runbooks/incident-commander.md`
2. Contain the exposure: revoke credentials, restrict access, isolate systems as needed
3. Do NOT delete logs — preserve all evidence
4. Loop in: CISO, Legal, Compliance, PR (for anything above P3 severity)
5. Open a confidential Slack channel: `#breach-[YYYY-MM-DD]`

## Assessment (Hours 4–24)
- Determine scope: how many individuals affected, what data categories
- Data categories matter for regulatory threshold:
  - Health data → HIPAA and state law triggers
  - Payment card data → PCI DSS notification requirements
  - EU residents → GDPR 72-hour clock running
- Document findings in the Breach Assessment Template (`../templates/breach-assessment.md`)

## Notification Decision Tree
```
Affects EU residents?
  YES → Notify supervisory authority within 72h (likely required)
       → Notify affected individuals if high risk to rights/freedoms
  NO  → Check US state law obligations by state of residence of affected users
       → Check contractual notification obligations (customer contracts, BAAs)
```

## Regulatory Notification Contacts
| Jurisdiction | Authority | Contact |
|---|---|---|
| EU/EEA (primary) | Lead DPA (Ireland, ICO, etc.) | See Legal's DPA contact list |
| California | CA AG (if >500 CA residents) | oag.ca.gov |
| New York | NY AG | ag.ny.gov |
| HIPAA | HHS OCR | hhs.gov/ocr |

## Post-Incident
- 5-day post-mortem with Compliance, Security, and Engineering
- Update threat model and control matrix
- If GDPR notification was made: track regulator response, respond within deadlines
- Annual review of this playbook after any activation

## Related
- `gdpr-data-subject-request.md`
- `../runbooks/incident-response.md`
- `../policies/data-retention-policy.md`
