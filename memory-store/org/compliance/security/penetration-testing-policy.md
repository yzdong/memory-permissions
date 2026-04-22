# Penetration Testing Policy

Owner: Security Engineering
Last updated: 2024-12

## Purpose

This policy governs when, how, and by whom penetration tests are conducted against org systems. Unauthorized testing — even by employees — is prohibited and may result in disciplinary action.

## Types of Testing

### External Penetration Test (Annual)

- Conducted by a third-party firm approved by the CISO.
- Scope: internet-facing infrastructure and applications.
- Timing: Q4 each year, coordinated with the release freeze window.
- Output: Full report delivered to CISO and Security Eng; executive summary shared with the board.
- Findings tracked to closure in Jira under the `SEC` project.

### Internal Red Team Exercise (Bi-annual)

- Conducted by our internal security team with possible external augmentation.
- Scenario-driven; recent exercises have included assumed-breach and supply-chain scenarios.
- Rules of engagement must be signed off by Engineering VP and CISO before start.
- Purple team debrief with Blue Team within 2 weeks of exercise end.

### Developer-Requested Testing (Ad Hoc)

Teams can request a security review or limited-scope pentest for new features or services.

1. File a `SEC-REVIEW` Jira ticket with the service diagram and a list of trust boundaries.
2. Security Eng triages within 5 business days.
3. If testing is approved, a test plan is agreed before any active testing begins.
4. Testing occurs in staging unless explicitly agreed otherwise.

## Rules of Engagement

- All tests require written authorization stored in `s3://org-audit-trail/pentests/`.
- Production data must not be exfiltrated, even as proof of concept — capture metadata only.
- Any Critical finding must be verbally reported to Security Eng within 1 hour of discovery.
- Social engineering of employees is allowed only when explicitly in scope.
- Denial-of-service testing is prohibited without explicit written approval and a rollback plan.

## Vulnerability Remediation SLAs

| Severity | SLA |
|---|---|
| Critical | 7 calendar days |
| High | 30 calendar days |
| Medium | 90 calendar days |
| Low | Next quarterly cycle |

Missed SLAs require a written exception approved by the CISO.

## Vendor Selection Criteria

- Must carry minimum $5M professional liability insurance.
- References from at least two companies of comparable scale.
- Testers must sign our NDA and rules of engagement before any access is provisioned.
- Preferred vendors list maintained by Security Eng in the internal wiki.
