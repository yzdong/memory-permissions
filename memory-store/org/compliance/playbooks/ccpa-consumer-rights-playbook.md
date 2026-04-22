# CCPA / CPRA Consumer Rights Playbook

## Who This Covers

California residents exercising rights under the California Consumer Privacy Act (as amended by CPRA). Scope: any consumer whose personal information we have collected, sold, or shared in the preceding 12 months.

## Rights We Must Honor

- **Know** — categories and specific pieces of PI collected
- **Delete** — with exceptions for legitimate retention needs
- **Correct** — inaccurate personal information
- **Opt-out of sale/sharing** — via the "Do Not Sell or Share" link (must be functional at all times)
- **Limit use of sensitive PI** — toggle in consent management platform
- **Non-discrimination** — cannot deny service for exercising rights

## Intake Channels

1. In-product privacy portal (preferred)
2. Toll-free number (staffed during business hours; VM triaged same day)
3. Email to `privacy@company.io`

All channels funnel into Jira project `PRIV`. Tag CCPA-specific tickets with label `ccpa`.

## Verification

For "Know" and "Delete" requests:
- Authenticated users: match account email + verify session or confirm via secondary email link
- Unauthenticated: must provide 2 data points we can match (e.g., email + zip + last order date)
- Authorized agents: require signed permission + copy of consumer's government ID

Do not over-collect verification data — use only what is reasonably necessary.

## Response Timeline

| Request Type | Initial Acknowledgment | Substantive Response |
|---|---|---|
| Know / Delete / Correct | 10 business days | 45 calendar days (extendable 45 more) |
| Opt-out of sale/sharing | Immediate (automated) | Confirm within 15 business days |

## Opt-Out Infrastructure

- Global Privacy Control (GPC) signals must be honored automatically — confirm with Engineering quarterly
- The "Do Not Sell or Share" link in the footer must point to `https://company.io/privacy/opt-out`
- Check link functionality is part of the weekly smoke test suite in `../qa/privacy-checks.md`

## Metrics and Reporting

Compliance tracks monthly:
- Volume by request type
- On-time response rate (target: ≥ 97%)
- Denial rate and reasons

Report surface: `../reporting/privacy-metrics-dashboard.md`

## References

- `gdpr-data-subject-request.md`
- `../policies/data-retention-policy.md`
- `breach-notification-playbook.md`
