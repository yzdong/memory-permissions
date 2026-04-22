# Terraform State Migration Playbook

For when we need to move resources between Terraform state files, refactor module references, or migrate from one backend to another. This is high-risk and has caused outages elsewhere. We treat it accordingly.

## Before you touch state

**Lock the workspace before doing anything.** In Terraform Cloud:
```bash
terraform workspace select <workspace>
# Lock via API or UI — do not rely on state locking alone during manual surgery
```

Make a manual state backup:
```bash
terraform state pull > backups/$(date +%Y%m%d-%H%M%S)-<workspace>.tfstate
```
Store this backup in `s3://platform-tf-backups/manual/` — the S3 bucket is versioned and has object lock.

## Moving resources within the same state

```bash
terraform state mv 'module.old_path.resource_type.name' 'module.new_path.resource_type.name'
```

- Run `terraform plan` after every batch of moves — expected output is no changes
- Move resources in small batches (5–10 at a time), not all at once
- If plan shows unexpected changes, stop and investigate before continuing

## Moving resources between state files

This requires coordinating the source and destination workspaces.

```bash
# Export from source
terraform state mv -state-out=./temp.tfstate 'resource_type.name' 'resource_type.name'

# Import into destination
terraform state push ./temp.tfstate  # careful — review the tfstate file first
```

Actually, prefer `terraform import` for cross-state moves when the resource supports it. It's safer than pushing partial state files.

## Backend migration

To migrate from local backend to Terraform Cloud (or between cloud backends):
1. Update `backend {}` block in `main.tf`
2. Run `terraform init -migrate-state`
3. Verify the remote state is correct before removing the local state file
4. Update CI pipeline to use new backend credentials

## Post-migration verification

- `terraform plan` should show zero changes
- Confirm all resource IDs match what's actually deployed (spot-check in AWS Console or equivalent)
- Remove any backup files from local disk — they may contain secrets
- Document the migration in `infra/state-migration-log.md` with date, what moved, and who did it

## Related runbooks
- `runbooks/terraform-apply.md`
- `runbooks/terraform-cloud-workspace.md`
