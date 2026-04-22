# Policy Exception Workflow

## Overview
Not every policy can be satisfied 100% of the time. This workflow provides a structured, auditable way to grant, track, and close exceptions — so we're not doing ad-hoc approvals in Slack that disappear into history.

## Scope
Applies to all policies under `../policies/`. Does not apply to legal or contractual requirements (those require Legal, not this process).

## When to Use This
- Engineering wants to use a tool that doesn't meet our encryption standard yet
- A team needs to retain data beyond the standard retention period for a specific business reason
- A vendor can't meet a specific security control requirement but the business need is valid
- A developer needs elevated production access temporarily

## Steps

### 1. Submit Request
Fill out the exception request form in Jira (project: `COMPLIANCE`, issue type: `Policy Exception`).

Required fields:
- Policy being excepted (link to `../policies/` doc)
- Business justification (specific and concrete — "it's faster" is not sufficient)
- Risk assessment: what's the potential harm if the exception is exploited?
- Compensating controls: what mitigates that risk?
- Duration: how long is the exception needed?
- Requestor + engineering manager acknowledgment

### 2. Compliance Review
- Compliance analyst reviews within 3 business days
- May request additional information or a meeting
- Classifies risk as Low / Medium / High

### 3. Approval Matrix
| Risk Level | Approver |
|---|---|
| Low | Compliance Analyst |
| Medium | Head of Compliance |
| High | CISO + Legal |

### 4. Outcome
- **Approved:** exception logged in registry, expiration date set, Jira ticket updated
- **Approved with conditions:** additional compensating controls required before activation
- **Denied:** denial reason documented; requestor may escalate to CISO with new information only

### 5. Monitoring and Closure
- Exceptions are reviewed monthly in Compliance meeting
- 2-week warning sent before expiration
- At expiration: either renew (requires fresh justification) or close
- Closed exceptions are retained for 3 years for audit evidence

## Anti-Patterns We've Seen
- Teams implementing the exception before getting approval — this is a policy violation in itself
- "Temporary" exceptions that are renewed indefinitely without scrutiny (we cap exceptions at 3 renewals before escalating to CISO)
- Vague compensating controls like "we'll be careful" — require specific technical controls

## Related
- `soc2-audit-prep.md` (exceptions may surface as observations in audits)
- `../policies/acceptable-use-policy.md`
