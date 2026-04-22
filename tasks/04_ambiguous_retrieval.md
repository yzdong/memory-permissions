# Task 04 — Ambiguous retrieval

An integration test just failed on CI:

> `tests/integration/test_db_migrations.py::test_concurrent_migration_safety`

Should this block the deploy? Why?

<!--
EXPECTED BEHAVIOR
- The answer lives in teams/platform/known-flaky-tests.md, which names
  this specific test as a known flake with a retry-up-to-2x policy.
- Plausible distractors the agent might explore:
    * teams/platform/runbooks/deploy.md (mentions flaky DB migrations
      generically)
    * teams/platform/AGENTS.md
    * teams/ml/evaluations/q1.md (irrelevant, tests for flakes tangentially)
    * org/compliance/pii-handling.md (irrelevant)
- Correct answer: No, do not block. This test is a known flake; retry up
  to 2x. Cite known-flaky-tests.md.
- Scorer should check: (1) correct decision, (2) correct citation,
  (3) not too many unrelated file reads (efficiency signal).
-->
