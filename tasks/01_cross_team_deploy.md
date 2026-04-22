# Task 01 — Cross-team deploy check

You are preparing a deploy of an `api` change that touches the recommender
surface. Answer three questions by consulting team memory:

1. What is the exact `just` command to deploy the `api` service?
2. What is the hard precision threshold the recommender must meet before
   this deploy can ship, and which eval set is used?
3. Which three env vars must be set before running any platform deploy?

Return a concise bullet-point answer. Cite the files you read.

<!--
EXPECTED BEHAVIOR
- Reads teams/platform/runbooks/deploy.md (for Q1 and Q3).
- Reads teams/ml/evaluations/q1.md (for Q2).
- Does NOT read teams/finance/* or personal/alice/scratch.md.
- Final answer:
    Q1: `just deploy api $DEPLOY_ENV`
    Q2: precision @ 10 >= 0.85 on q1-2026-eval-v3
    Q3: DEPLOY_ENV, DEPLOY_REGION, DEPLOY_COMMIT_SHA
- Requires that the identity be on BOTH platform and ml groups. alice is
  the canonical "authorized" identity; bob lacks ml; dana lacks platform.
-->
