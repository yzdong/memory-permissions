# Bring Your Own Device (BYOD) Policy

**Effective Date:** 2023-09-01  
**Owner:** IT Security  
**Applies To:** All employees and contractors who access corporate resources from personal devices

---

## Why This Policy Exists

Personal devices are increasingly used to access corporate email, Slack, and internal tools. Without clear guardrails, this creates a patchwork of unmanaged endpoints that security can't monitor or remediate. This policy tries to balance flexibility with a baseline of protection that keeps us collectively safe.

## Eligibility

BYOD is permitted for:
- Full-time and part-time employees in roles approved by their manager and IT
- Contractors whose agreements explicitly allow BYOD (most don't — check your MSA)

BYOD is **not** permitted for roles that regularly handle:
- Payment card data (PCI DSS environments)
- Health records (HIPAA-covered data)
- Classified customer contractual data above Tier 2 sensitivity

If you're unsure about your role's tier, ask your manager or open a ticket with IT Security.

## Required Device Configuration

Before accessing corporate resources, personal devices must meet all of the following:

- [ ] OS on a supported version (no more than two major versions behind current release)
- [ ] Full-disk encryption enabled (FileVault on macOS, BitLocker or equivalent on Windows)
- [ ] Screen lock set to 5 minutes or less
- [ ] MDM enrollment via Jamf or Intune (IT will walk you through this)
- [ ] Company-approved endpoint security agent installed
- [ ] No jailbreak or root access

## What IT Can and Cannot Do

**IT can:**
- Enforce configuration profiles and policies via MDM
- Remotely wipe the corporate data container on the device
- View compliance status (OS version, encryption state, etc.)

**IT cannot:**
- Access personal photos, messages, or files outside managed apps
- Perform a full device wipe without employee consent, except where legally required

## Departure Procedures

On your last day (or earlier if access is revoked):
1. Corporate data container is wiped remotely by IT
2. MDM profile is removed
3. You retain your personal data

## Incident Response

If your personal device is lost or stolen, report it to `security@company.internal` **immediately**. IT will initiate a remote wipe of corporate data within 4 hours of confirmed loss.

## Violations

Failure to maintain device compliance may result in revocation of BYOD access and return to a company-issued device if available, or restricted access to corporate systems.

## Related Documents

- `acceptable-use-policy.md`
- `../it/mdm-enrollment-guide.md`
- `../incident-response/lost-device-runbook.md`
