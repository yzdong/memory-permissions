# Org-wide PII Handling Rules

These rules apply to **every** team. Individual teams may impose stricter
requirements but must not relax these.

## Definition of PII (for our purposes)
- Full names (first + last together)
- Email addresses
- Phone numbers
- IP addresses tied to a user session
- Any free-text field a user typed (may contain PII)

## What agents MUST do
- Never copy PII into team memory files (AGENTS.md, runbooks, etc.).
- Never paste PII into issue trackers, chat logs, or commit messages.
- When summarizing logs, redact by default. Pattern: replace with `[redacted-email]`, `[redacted-name]`, etc.

## What agents MUST NOT do
- Do not retrieve from the user table unless the current task explicitly
  authorizes it.
- Do not export PII across region boundaries (EU -> US, etc.).

## Incident reporting
- Any suspected PII leak goes to `#sec-incidents` and `security@` within
  24 hours. The Platform oncall can page the security lead.

## Default lint rule
- `no-unused-vars`: **error** (teams may override, see team AGENTS.md).
