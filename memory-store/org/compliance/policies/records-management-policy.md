# Records Management Policy

**Owner:** Legal & Compliance  
**Applies To:** All employees and contractors  
**Last Updated:** 2024-07-22

---

## Scope

A "record" is any document — email, Slack message, spreadsheet, contract, design file, code comment, or otherwise — created or received in the course of company business. This policy governs how records are created, stored, classified, and ultimately disposed of.

## Record Classification

| Class | Examples | Storage Requirement |
|---|---|---|
| Public | Marketing copy, press releases, open-source code | No special controls |
| Internal | Team wikis, project plans, internal Slack channels | Company-managed storage only |
| Confidential | Customer contracts, security assessments, HR records | Encrypted, access-controlled |
| Restricted | M&A materials, attorney-client communications, board materials | Need-to-know + DLP controls |

When in doubt, classify up. Reclassification requires manager + Legal approval.

## Storage Rules

- Company records must live in approved systems (Google Workspace, Confluence, GitHub, S3 with appropriate bucket policies).
- Personal email and consumer cloud storage (Dropbox personal, iCloud) are **not** approved for company records.
- Records must not be stored solely on a local device without a backup to an approved system.

## Retention and Disposal

Retention periods are defined in the [Data Retention Schedule](data-retention-schedule.md). When a record reaches end of life:

1. Verify no legal hold applies (check with Legal).
2. Delete from all locations, including email, Slack, and backups, per the automated pipeline where available.
3. For physical records: cross-cut shred and log in `../registers/physical-disposal-log.md`.

## Version Control and Authenticity

- Contracts and regulated documents must be stored in a system that logs modifications (Google Drive version history, SharePoint, or a DMS).
- Do not alter a finalized record without creating a new version with an edit rationale.

## Legal Holds

When Legal issues a hold, normal disposal is suspended for affected records. Employees notified of a hold must acknowledge receipt in ServiceNow within 2 business days.

## Audits

Compliance audits records management practices annually. Teams may be asked to produce records on short notice; maintaining organized, searchable storage is a business requirement, not optional hygiene.

## Related Policies

- [Data Retention Schedule](data-retention-schedule.md)
- [Privacy Policy (Internal)](privacy-policy-internal.md)
- [Acceptable Use Policy](acceptable-use-policy.md)
