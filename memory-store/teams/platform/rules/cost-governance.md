# Cost Governance — Platform Team

Platform is responsible for shared infra spend. Every engineer on the team should understand how their decisions affect the bill.

## Budget Ownership

The Platform infra budget is owned by the Platform Lead. Budgets are reviewed monthly against actuals in the Finops dashboard (link in `#platform-finops`).

## Cost Tagging

All AWS resources must be tagged with `cost_center`. This is enforced by the tag audit job (`scripts/tag-audit.sh`). Resources without this tag after 72 hours will be flagged for termination review.

See `naming-conventions.md` for the full tagging schema.

## Spend Guardrails

- Any single AWS resource change expected to increase monthly cost by **> $500** requires a comment in the PR explaining the cost impact.
- Ephemeral/sandbox environments must have a TTL set via the `sandbox-ttl` tag. Default TTL is 48 hours.
- RDS instances in non-production environments must use `db.t3.medium` or smaller unless explicitly approved.

## Right-Sizing Reviews

Quarterly, Platform runs a right-sizing review using AWS Compute Optimizer. Results are posted to `ops/rightsizing-<quarter>.md`. Engineers are expected to action any "over-provisioned" recommendations within the next sprint unless there's a documented reason not to.

## Reserved Instances and Savings Plans

- The Platform Lead manages RI/SP purchasing in coordination with Finance.
- Do not purchase RIs individually — all commitments go through a central request.
- Coverage target: > 70% of steady-state compute covered by RIs or Savings Plans.

## FinOps Escalation

If you notice unusual spend (e.g., a runaway process spinning up resources), post in `#platform-finops` immediately. Do not wait for the monthly review.
