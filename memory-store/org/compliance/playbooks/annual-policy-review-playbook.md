# Annual Policy Review Playbook

## Background
All policies in `../policies/` require annual review and re-approval. This isn't just good practice — our SOC 2 auditors check for it, and several of our enterprise customer contracts require evidence of annual review. Skipping even one policy has caused audit findings in the past.

## Schedule
Policy reviews run January through March each year. Reviews started mid-year tend to slip.

| Month | Activity |
|---|---|
| January | Inventory all policies, confirm owners, open Jira epics |
| February | Owners complete reviews and submit proposed changes |
| March | Compliance consolidates, Legal reviews substantive changes, approvals obtained |
| March 31 | Target completion date; evidence packaged for SOC 2 |

## Policy Inventory
Current canonical list: `../policies/README.md`. As of last count, we have 23 active policies. If you find a policy not in that list, flag it in `#compliance-internal` — shadow policies are a liability.

## What "Review" Actually Means
A review is not just reading and saying "looks fine." Policy owners must:
1. Verify all referenced systems/tools/teams are still accurate
2. Check for regulatory changes that require updates (subscribe to IAPP alerts)
3. Confirm applicability to any new product lines or geographies launched since last review
4. Certify in writing (Jira comment with name + date is sufficient)

If no changes are needed, that's fine — document it explicitly.

## Substantive Change Process
If a policy needs material changes:
1. Draft changes in a branch of the `policies` repo (or Google Doc for non-technical owners)
2. Compliance review: 5 business days
3. Legal review if the change affects data handling, liability, or regulatory posture: additional 5 days
4. Approval sign-off from policy owner + Compliance lead
5. Publish to internal wiki and notify all employees via `#company-announcements`
6. If policy is referenced in customer contracts or DPAs: notify Legal before publishing

## Evidence Package
For each policy, auditors expect:
- Document with version number and "Last Reviewed" date updated
- Approval record (Jira ticket or email chain showing sign-off)
- Distribution record (evidence employees were notified or re-acknowledged)

Store at `//shared-drive/audits/policy-reviews/[YYYY]/`.

## Policies That Frequently Need Updates
- Data Retention Policy (product changes affect what we keep and where)
- Acceptable Use Policy (new tools adopted by eng mean new entries)
- Sub-Processor List (vendor churn is high)
- Incident Response Policy (process improvements from post-mortems)

## Related
- `soc2-audit-prep.md`
- `policy-exception-workflow.md`
- `../policies/README.md`
