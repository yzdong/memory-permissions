# Terraform 0.12 → 1.5 Upgrade Notes

**Status:** Complete  
**Completed:** 2024-11-01  
**Author:** Platform Infra

## We Skipped Several Major Versions — Here's What That Meant

We were running Terraform 0.12 in production until late 2024. Yes, really. The upgrade path required going through 0.13, 0.14, 0.15, 1.0, and finally 1.5. We used `terraform-upgrade-check` and tested each intermediate version in a scratch workspace.

## Major Changes Across Versions

### 0.12 → 0.13
- `required_providers` block is now required; implicit provider sources removed
- Module source addresses for registry modules now require explicit versioning

### 0.13 → 0.14
- Sensitive values in state are now redacted in plan output — this broke some CI scripts that were parsing plan text. Use `terraform show -json` instead.

### 0.14 → 0.15
- Upgraded provider protocol; any provider older than ~2 years started throwing warnings
- `terraform validate` became stricter about unused variables

### 0.15 → 1.x
- Stable: no breaking changes from 0.15
- `terraform state mv` behavior for resources with `count` and `for_each` is more predictable

### 1.0 → 1.5
- `check` blocks added (we use these for post-apply assertions now)
- `import` block added — no more `terraform import` CLI gymnastics

## State File Migration

We ran `terraform state replace-provider` to update provider source addresses in all state files. Script is at `tools/tf-state-migrate/replace-providers.sh`.

## CI Changes

Updated the Terraform version in `.github/workflows/terraform.yml`. Also added Atlantis config version bump in `atlantis.yaml`.

## What We Wish We'd Done Earlier

- Pinned provider versions from the start — would have made the upgrade path much cleaner
- Used workspaces instead of directory-per-environment — the directory pattern doesn't scale well to 40+ environments

## References

- `infra/terraform/README.md`
- `runbooks/terraform-state-ops.md`
