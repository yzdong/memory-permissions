# Terraform 0.12 → 1.x Upgrade

**Status:** Completed 2024-07-01  
**Owner:** Platform  
**Tracking:** PLAT-983

## Why This Took So Long

Honestly, we kept deprioritizing it. Terraform 0.12 worked fine day-to-day, and the upgrade path through 0.13 → 0.14 → 0.15 → 1.0+ felt tedious. We also had a handful of modules using HCL1-style syntax that needed rewriting. A late-2023 incident where a provider plugin failed to install because it required Terraform ≥ 0.15 forced our hand.

## Upgrade Path We Followed

HashiCorp recommends incremental upgrades. We did:

```
0.12.31 → 0.13.7 → 0.14.11 → 0.15.5 → 1.0.11 → 1.7.5
```

At each step: `terraform init -upgrade`, then `terraform plan`, then fix errors, then commit and push.

## HCL Syntax Changes

### Variable type constraints
```hcl
# Old (0.12 style, still works but deprecated)
variable "instance_count" {
  default = 2
}

# New
variable "instance_count" {
  type    = number
  default = 2
}
```

### For_each on modules
This was actually a 0.13 feature we'd been waiting for. We replaced several copy-pasted module blocks with clean `for_each` patterns.

### `terraform.workspace` references
We stopped using workspaces for environment separation (it was causing state confusion). Moved to per-environment state backends configured in `terraform/backends/`.

## State Migration

The state file format changed between 0.12 and 0.13. `terraform 0.13upgrade` handled most of it automatically, but we had to manually fix three `moved` blocks for renamed resources.

## Provider Lock Files

Starting with 0.14, `.terraform.lock.hcl` is mandatory. We committed lock files to the repo. Don't delete them — they ensure reproducible provider installs.

## Related

- `terraform/README.md`
- `runbooks/terraform-state-recovery.md`
- `../infrastructure/provider-versions.md`
