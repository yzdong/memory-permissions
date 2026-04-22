# Internal Privacy Policy

**Note:** This is the internal-facing document describing how we handle personal data. The public-facing privacy notice is maintained by Legal at `../legal/public-privacy-notice.md`.

**Owner:** Privacy Office  
**Effective:** 2023-11-01

---

## Scope

This policy governs how we collect, use, store, share, and delete personal data — covering:

- Customer personal data (end users of our products)
- Employee personal data
- Prospective customer data collected through sales and marketing
- Data collected from third-party sources

## Lawful Basis for Processing

We must have a lawful basis before processing personal data. The most common bases we rely on:

| Basis | When We Use It |
|-------|---------------|
| Contract | Processing necessary to deliver our product to a paying customer |
| Legitimate Interest | Analytics, fraud prevention, internal research (documented in LIA) |
| Consent | Marketing emails, cookies beyond strictly necessary |
| Legal Obligation | Tax records, responding to lawful orders |

If you're starting a new data processing activity, work with the Privacy Office to document the lawful basis **before** going live.

## Data Minimization

Collect only what you need. If a product feature can work without storing personal data, it should. Talk to the Privacy Office before adding new personal data fields to a product or analytics pipeline.

## Cross-Border Transfers

Transferring personal data from the EU/EEA to countries without an adequacy decision requires a valid transfer mechanism:

- Standard Contractual Clauses (SCCs) — our default
- Binding Corporate Rules (BCRs) — not yet implemented
- Adequacy decision for the destination country

Do not enable data replication to new geographic regions without confirming the transfer mechanism is in place.

## Individual Rights

Data subjects have rights under GDPR and other applicable laws. When a request comes in:

1. Log it in the DSR tracker within 24 hours
2. Verify identity before fulfilling
3. Respond within 30 days (GDPR deadline); escalate if you can't meet it
4. Coordinate with Engineering if data deletion requires code-level intervention

See `../privacy/dsr-handling-procedures.md` for the full workflow.

## Retention and Deletion

Follow the schedule in `data-retention-schedule.md`. Do not retain personal data beyond the defined period without a documented legal hold or regulatory justification.

## Breach Notification

If a personal data breach occurs:

- Notify the Privacy Office within 1 hour of discovery
- Regulatory notification may be required within 72 hours (GDPR)
- See `../incident-response/data-breach-runbook.md`

## Training

All employees who handle personal data must complete privacy training annually. Completion is tracked in the LMS. Non-completion blocks system access renewal.
