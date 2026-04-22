# Terraform Governance — Platform Team

## State Management

All Terraform state lives in S3 with DynamoDB locking. Do not use local state for anything shared.

```hcl
terraform {
  backend "s3" {
    bucket         = "acme-platform-prod-tf-state"
    key            = "<module-path>/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "acme-platform-tf-locks"
    encrypt        = true
  }
}
```

The state bucket has versioning and point-in-time recovery enabled. Do not delete state versions without going through `runbooks/state-recovery.md`.

## Module Versioning

- Internal modules are pinned by git tag: `ref=v1.4.2`.
- Never use `ref=main` for modules consumed by production roots.
- Provider versions must be pinned with `~>` for minor/patch flexibility, never unpinned.

## Plan/Apply Workflow

1. PRs include a `terraform plan` output (CI generates this automatically via Atlantis).
2. Reviewers must verify the plan scope before approving.
3. `terraform apply` runs in CI only — no manual applies in production.
4. Applies are logged to `ops/apply-log.md` automatically by Atlantis.

## Drift Detection

A scheduled job runs `terraform plan` against all production root modules every 6 hours. If drift is detected, a ticket is auto-created and the on-call engineer is notified.

Suppressing drift detection for a module requires a comment in the Jira ticket and Lead approval.

## Sensitive Variables

Never declare `sensitive = false` on a variable that could hold a credential, key, or token. When in doubt, mark it sensitive. This prevents values from appearing in plan output and CI logs.

See `secrets-handling.md` for how sensitive variables should be sourced.
