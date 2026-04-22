# Annual Access Review Playbook

## Why We Do This

Access creep is real. People change roles, leave the company, or receive emergency access that never gets revoked. This review is a SOC 2 and ISO 27001 control requirement, and it's also just good hygiene. We do it twice a year: once in Q1 (Jan–Feb) and once in Q3 (Jul–Aug).

## Scope

All systems classified as Tier 2 or above in the asset inventory:
- Production databases and data warehouses
- Cloud provider consoles (AWS, GCP)
- Code repositories (GitHub org)
- Identity provider (Okta)
- SaaS tools with access to customer data (Salesforce, Zendesk, Intercom)
- Secrets management (Vault)

## Process

### Week 1 — Pull Access Reports

```bash
# Example: pull GitHub org members and their roles
gh api /orgs/{org}/members --paginate > access-reports/github-members.json
```

- IT exports Okta user/group report
- Engineering exports DB role assignments via `scripts/db-access-report.sh`
- Cloud admin exports IAM policy bindings

### Week 2 — System Owner Review

- Assign each report to the system owner (mapped in `../assets/system-owner-registry.csv`)
- Owner marks each account: **Confirm** / **Revoke** / **Modify**
- Any account with no activity in 90+ days flagged for revocation by default
- Service accounts without documented purpose → escalate to Engineering lead

### Week 3 — Remediation

- Revocations actioned within 5 business days of owner sign-off
- Modifications documented with justification
- Exceptions logged via `policy-exception-workflow.md`

### Week 4 — Sign-Off and Evidence Collection

- System owner attestation forms signed (PDF, stored in `gs://compliance-vault/access-reviews/<year>/<half>/`)
- Compliance lead reviews for completeness
- Summary report to CISO and CPO

## Handling Departures Mid-Cycle

Off-boarding access revocation is covered by `../runbooks/offboarding.md`. Do not wait for the annual review for terminated employees — that should happen within 24 hours of termination.

## Metrics

Track and include in the summary report:
- % of accounts reviewed vs. in scope
- # of accounts revoked
- # of open exceptions
- Time to complete (target: ≤ 4 weeks)

## References

- `soc2-audit-prep.md`
- `policy-exception-workflow.md`
- `../policies/access-control-policy.md`
