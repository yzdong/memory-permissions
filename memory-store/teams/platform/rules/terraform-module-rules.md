# Terraform Module Rules — Platform Team

These rules govern how Platform writes, versions, and consumes Terraform modules.

## Directory Layout

```
infra/
  modules/
    rds/
    vpc/
    eks-nodegroup/
    secrets-manager/
  stacks/
    prod/
    staging/
    sandbox/
```

Modules live under `infra/modules/`. Stacks (root modules that instantiate resources) live under `infra/stacks/`.

## Module Versioning

Modules are versioned via Git tags: `infra/modules/{name}/v{MAJOR}.{MINOR}.{PATCH}`

- Bump PATCH for backward-compatible fixes
- Bump MINOR for new optional variables
- Bump MAJOR for any breaking change (variable rename, output removal, etc.)

Consumers pin to a specific tag, not `main`:

```hcl
module "db" {
  source = "git::https://github.com/acme/platform-infra.git//infra/modules/rds?ref=infra/modules/rds/v2.3.1"
}
```

## Required Module Structure

Every module MUST have:
- `main.tf`
- `variables.tf` with descriptions on every variable
- `outputs.tf`
- `README.md` (generated via `terraform-docs` — do not hand-edit)

## Testing

Modules have integration tests under `infra/modules/{name}/test/` using Terratest. CI runs these against the `sandbox` environment.

Do not merge a new module version without a passing test run. Skipping is not acceptable even for "trivial" changes — we've been burned.

## Deprecating a Module

1. Add a deprecation notice to the module README and a `lifecycle { precondition }` warning
2. Notify all consuming teams via `#platform-infra` Slack
3. Give a 60-day migration window
4. Remove after all consumers have migrated (verify via `grep -r` or Terraform graph)

## State Management

- Remote state in S3 with DynamoDB locking
- State bucket: `acme-tf-state-{env}` (do not create ad-hoc buckets)
- Never edit state manually — use `terraform state mv` with a peer watching

## Related

- `naming-conventions.md`
- `../runbooks/terraform-workflow.md`
- `../runbooks/state-surgery.md`
