# GDPR Data Subject Request (DSR) Playbook

## Purpose
Step-by-step process for handling Article 15–22 requests from EU data subjects. We're legally required to respond within 30 calendar days. Failure to meet this SLA has resulted in regulator inquiries at peer companies — treat these as high-priority.

## Request Types Covered
- **Access (Art. 15):** Subject wants to know what data we hold
- **Rectification (Art. 16):** Subject wants incorrect data corrected
- **Erasure (Art. 17):** "Right to be forgotten"
- **Portability (Art. 20):** Structured machine-readable export
- **Objection / Restriction (Art. 21/18):** Limiting processing

## Intake
1. Request arrives via `privacy@company.com` or the in-product privacy portal
2. Compliance analyst logs it in the DSR tracker (Notion → Compliance → DSR Log)
3. Verify identity of requestor — see `identity-verification-sop.md` for accepted methods
4. Acknowledge receipt within **72 hours** (template in `../templates/dsr-acknowledgement.md`)

## Handling by Request Type

### Access Request
```
1. Query data inventory for subject's email / user ID
2. Pull records from: user_profiles, event_log, billing, support_tickets
3. Compile into PDF using the DSR export tool (runbooks/dsr-export.md)
4. Legal review if record set is unexpectedly large (>500 rows)
5. Deliver via encrypted email or secure portal
```

### Erasure Request
- Check if erasure is legally permissible (active contract, fraud hold, regulatory retention)
- If permissible: open engineering ticket in Jira using `GDPR-ERASURE` template
- Engineering SLA: 5 business days to complete deletion across all systems
- Compliance must verify deletion via audit log before closing ticket
- Retain erasure confirmation record for 3 years

### Portability Request
- Export must be in JSON or CSV — not PDF
- Coordinate with Data Eng; export scripts live in `//data-eng/scripts/dsr_export/`

## Escalation
- Legal counsel involvement required if: requestor is represented by attorney, request involves law enforcement hold, or subject mentions GDPR supervisory authority complaint
- DPA notification required within 72 hours of becoming aware of a related breach — see `breach-notification-playbook.md`

## Metrics
We track: intake volume, response time (target: ≤25 days average), erasure completion rate. Monthly review with Privacy Council.
