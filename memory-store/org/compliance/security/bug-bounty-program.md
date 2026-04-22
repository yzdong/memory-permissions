# Bug Bounty Program

Status: **Active**  
Platform: HackerOne (private program)  
Program manager: @security-eng-lead  
Last policy update: 2024-11-01

## Scope

### In Scope

- `*.ourcompany.com` (excluding staging and internal subdomains listed below)
- Mobile apps (iOS, Android) — current App Store / Play Store versions
- Public APIs documented at `developer.ourcompany.com`

### Out of Scope

- `*.staging.ourcompany.com`
- `internal.ourcompany.com` and any `*.corp.*` subdomain
- Third-party services we use (report those to the vendor directly)
- Denial-of-service attacks
- Social engineering of employees
- Physical security

## Reward Tiers

| Severity | CVSS Range | Reward Range |
|---|---|---|
| Critical | 9.0 – 10.0 | $5,000 – $15,000 |
| High | 7.0 – 8.9 | $1,500 – $4,999 |
| Medium | 4.0 – 6.9 | $300 – $1,499 |
| Low | 0.1 – 3.9 | $50 – $299 |

Rewards are at our discretion. We reserve the right to award more for exceptional reports or less for reports with low reproducibility.

## Rules of Engagement

1. Don't access, modify, or delete user data that isn't yours.
2. Immediately stop and report if you stumble onto PII. See `../pii-handling.md` for context on why we take this seriously.
3. Don't perform automated scanning that generates more than 60 requests/second.
4. Don't publicly disclose until we've patched and given you clearance (90-day max embargo).
5. Only test against your own accounts unless the report involves authorization bypass, in which case create two test accounts.

## Triage SLAs

| Stage | Target |
|---|---|
| Initial response | 3 business days |
| Triage decision | 10 business days |
| Patch for Critical/High | 30 days |
| Patch for Medium | 60 days |
| Patch for Low | 90 days |

## Reporting a Finding

Use the HackerOne submission form. Include:

- Description and impact
- Step-by-step reproduction
- Proof-of-concept (screenshots, curl commands, code)
- Suggested fix (optional but appreciated)

For zero-days in underlying infrastructure, email `security@ourcompany.com` with PGP encryption (key fingerprint on our security.txt).

## Internal Handoff Process

Once a report is triaged as valid, the assigned security engineer:

1. Opens a **private** Jira ticket in `SEC` project.
2. Notifies the owning team's engineering manager.
3. Tracks patch progress against SLA.
4. Issues HackerOne reward upon patch verification.
