# New Market / Jurisdiction Compliance Checklist

## Purpose
Whenever we expand into a new country or US state in a significant way (new data center, direct sales, hiring employees), legal and compliance obligations arise that vary by jurisdiction. This checklist prevents us from discovering requirements after the fact.

## Trigger Criteria
Use this playbook when ANY of the following are true:
- Signing contracts with customers domiciled in a new jurisdiction
- Storing or processing personal data of residents of a new jurisdiction
- Hiring employees or engaging contractors in a new country
- Opening a legal entity in a new jurisdiction

## Phase 1: Preliminary Assessment (Before Decision)
- [ ] Identify applicable privacy laws (GDPR, LGPD, PIPL, state consumer privacy laws, etc.)
- [ ] Identify sector-specific regulations (financial services, healthcare, education)
- [ ] Data transfer mechanism required? (EU → US: SCCs or adequacy decision)
- [ ] Local data residency requirements?
- [ ] Employment law obligations if hiring locally
- [ ] Tax and entity registration requirements (Legal/Finance scope, not Compliance)

Output: Compliance Risk Memo to be shared with leadership before go/no-go.

## Phase 2: Readiness (Pre-Launch, T-60 to T-30)
- [ ] Update data inventory and data flow diagrams to reflect new jurisdiction's data
- [ ] Update privacy policy and cookie policy if new rights apply
- [ ] Execute any required data transfer agreements (SCCs, etc.)
- [ ] Review and update sub-processor list and notify vendors
- [ ] Determine if DPA registration is required (some jurisdictions require controller registration)
- [ ] Update breach notification procedures with new jurisdiction's deadlines
  - Reference: `breach-notification-playbook.md`
- [ ] Confirm consent mechanisms are appropriate for the new jurisdiction
- [ ] Update DSR handling to cover new rights granted by local law
  - Reference: `gdpr-data-subject-request.md` (adapt as needed)

## Phase 3: Launch and Post-Launch
- [ ] Confirm all pre-launch items closed
- [ ] Monitor local regulatory developments for 90 days post-launch
- [ ] Add jurisdiction to the annual policy review scope
- [ ] Update SOC 2 and other audit documentation to reflect expanded scope

## Jurisdictions We've Already Expanded Into
See `../policies/jurisdiction-registry.md` for current list with notes on applicable obligations.

## Notes on Specific Jurisdictions

### European Union
- GDPR applies. SCCs required for data transfers to the US (using EU Commission's 2021 SCCs).
- Lead DPA designation needed if we have an EU establishment.

### Canada (PIPEDA / Quebec Law 25)
- Quebec's Law 25 has stricter requirements similar to GDPR; privacy impact assessments required for high-risk processing.

### Brazil (LGPD)
- Similar to GDPR but enforcement has been ramping up since 2023. Local DPO not yet required for our scale but monitor.

## Related
- `hipaa-baa-review.md`
- `gdpr-data-subject-request.md`
- `../policies/privacy-policy.md`
