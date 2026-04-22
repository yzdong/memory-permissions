# Quarterly Access Review Playbook

## Purpose
Access reviews are a core SOC 2 control and a recurring pain point. This doc is the canonical guide for running them. If you're an access review owner reading this for the first time — start with the checklist at the bottom.

## Cadence
- Quarterly for production systems and privileged access
- Semi-annual for internal tools and SaaS apps
- Annual for read-only / low-privilege roles

## Scope of Systems
All systems in the access review scope are listed in `../control-matrix.xlsx`. Key systems as of last update:
- AWS IAM (production accounts)
- GitHub organization (all repos)
- Snowflake (data warehouse)
- Salesforce
- Okta groups feeding downstream apps

## Roles and Responsibilities
| Role | Responsibility |
|---|---|
| System Owner | Reviews and certifies access for their system |
| People Ops | Provides up-to-date employee/contractor roster |
| Compliance | Coordinates, tracks completion, escalates |
| IT/Identity Eng | Pulls access reports, executes revocations |

## Process

### Week 1: Setup
- Compliance sends kickoff email with due dates and instructions
- Identity Eng pulls access snapshots for all in-scope systems
- Reports delivered to system owners as CSV or directly in the review tool (currently AccessOwl)

### Week 2–3: Review
- System owners mark each account: `Approved`, `Revoke`, `Modify`, `No Longer Employed`
- `No Longer Employed` should have already been handled by offboarding — flag these to People Ops immediately
- Completion target: 90% by end of week 3

### Week 4: Remediation
- Identity Eng executes all revocations and modifications
- Compliance verifies completion via follow-up access snapshot
- Any exceptions documented using `policy-exception-workflow.md`

## Common Issues
- Shared/service accounts with no clear owner — assign an owner before review starts
- Contractors who roll off mid-cycle; People Ops roster must be updated within 24h of departure
- System owners rubber-stamping everything — compliance spot-checks 10% of `Approved` certifications

## Evidence Package for SOC 2
The auditors want to see:
1. Initial access snapshot
2. Review completion records (who certified what, when)
3. Revocation confirmation (ticket + screenshot of access removed)
4. Summary sign-off from system owner

Store all artifacts in `//shared-drive/audits/access-reviews/[YYYY-QN]/`.

## Checklist for New Access Review Owners
- [ ] Confirm you're listed as owner in `../control-matrix.xlsx`
- [ ] Verify you can access the review tool
- [ ] Know your system's user list source of truth
- [ ] Block time in week 2-3 — this takes 2–4 hours for most systems
- [ ] Know who to ping for revocations (usually `#identity-eng`)
