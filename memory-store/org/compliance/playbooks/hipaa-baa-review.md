# HIPAA Business Associate Agreement (BAA) Review Playbook

## Context
We act as a Business Associate (BA) for several covered entity customers in the healthcare space. We also have downstream sub-processors that qualify as sub-BAs. This playbook covers both: **signing BAAs as a BA** and **executing BAAs with our own sub-processors**.

## When a BAA Is Required
Any time a vendor or partner will create, receive, maintain, or transmit Protected Health Information (PHI) on our behalf — or vice versa. Common triggers:
- New enterprise customer in healthcare sector
- Onboarding a new analytics, logging, or support tool that will touch PHI environments
- Expanding scope of an existing vendor relationship into PHI-adjacent systems

If you're unsure whether PHI is involved, ask `#compliance-internal` before proceeding.

## Signing a BAA as a Business Associate (Inbound)

### Step 1: Receive and Triage
- Legal receives draft BAA from customer
- Compliance reviews against our standard acceptable provisions checklist (`../templates/baa-review-checklist.md`)
- Target review time: 5 business days

### Step 2: Redlines
Common redlines we typically request:
- Breach notification period: customers often ask for 24 hours — our standard is 72 hours (aligning to GDPR). Push back with explanation.
- Audit rights: limit to annual, written notice, reasonable scope
- Termination cure period: minimum 30 days
- Sub-BA language: must explicitly permit our listed sub-processors

### Step 3: Execution and Filing
- Executed copy stored in: `//legal/contracts/baa/inbound/[customer-name]/`
- Compliance logs in the BAA registry (Notion → Compliance → BAA Registry)
- Alert Data Eng to tag relevant customer data with `phi_in_scope: true` in the data catalog

## Executing BAAs with Sub-Processors (Outbound)

### Current Sub-BA List Requiring BAAs
See `../policies/sub-processor-list.md` for the current list. As of last review, 11 vendors require BAAs.

### Process
1. Procurement opens vendor in the security review queue
2. Compliance confirms PHI touchpoint exists
3. Use our standard BAA template unless vendor insists on their own (requires Legal approval)
4. Annual renewal review — calendar reminders set in Compliance calendar

## Annual Review
- Each BAA should be reviewed annually even if not up for renewal
- Check: Has the vendor's sub-processor list changed? Have we changed our data flows?
- Confirm our sub-processor page remains accurate

## Related
- `soc2-audit-prep.md`
- `vendor-security-questionnaire.md`
- `breach-notification-playbook.md`
