# AI Tools Acceptable Use Policy

**Owner:** Legal & Security  
**Status:** Active  
**Effective Date:** 2024-04-01  
**Review Cycle:** 6 months (landscape moves fast)

---

## Motivation

AI tools are increasingly embedded in how we work. This policy doesn't prohibit their use — it sets guardrails to protect customer data, intellectual property, and our legal standing.

## Approved vs. Unapproved Tools

Approved tools are listed in `../catalogs/approved-software.md`. Using a tool not on the list, even for a one-off experiment, requires a quick security intake. Submit at `https://intake.security.company.internal`.

**The most common mistake:** pasting code from a private repo or customer support tickets into a public LLM web UI. This is a data classification violation.

## What You May NOT Put into Unapproved AI Services

- Customer PII or any data classified CONFIDENTIAL or RESTRICTED
- Proprietary source code from private repositories
- Internal financial data, forecasts, or M&A materials
- Employee personal information
- Legal strategy documents or attorney-client communications

## What's Generally Fine

- Generic coding questions that don't include proprietary context
- Drafting public-facing content (subject to human review)
- Summarizing publicly available information
- Personal productivity tasks on approved tools

## Output Review Requirements

- AI-generated code must be reviewed the same way any human-authored code is — security review, test coverage, code review.
- AI-generated external communications must be reviewed by the author before sending. Do not forward raw AI output to customers.
- Model accuracy is not guaranteed. Verify factual claims independently.

## Autonomous Agents and Automated Pipelines

Using AI agents that can take actions (write files, call APIs, submit forms) in production environments requires Security sign-off. Submit an RFC and tag `#security-review` in your PR.

## Violations

Incidents involving AI misuse are treated as data incidents under the [Information Security Policy](information-security-policy.md). Report to `security@company.internal`.

## Related Policies

- [Acceptable Use Policy](acceptable-use-policy.md)
- [Privacy Policy (Internal)](privacy-policy-internal.md)
- [Code of Conduct](code-of-conduct.md)
