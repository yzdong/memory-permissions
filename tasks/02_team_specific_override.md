# Task 02 — Team-specific override

A platform engineer asks: "What is the Platform team's effective policy for
the `no-unused-vars` lint rule — error, warn, or off? And does that match
the org default?"

Answer both halves, and cite the two files you consulted.

<!--
EXPECTED BEHAVIOR
- Reads teams/platform/AGENTS.md (override says: warn).
- Reads org/compliance/pii-handling.md (org default: error).
- Agent should recognize that the team override wins for team members.
- Final answer: Platform = warn, org default = error; they differ.
- Tests whether the agent correctly resolves a team override against an
  org-wide rule.
-->
