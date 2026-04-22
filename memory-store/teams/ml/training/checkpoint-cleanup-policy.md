# Checkpoint Cleanup Policy

## Why This Matters

The NFS share at `/mnt/nfs/checkpoints/` has a 20 TB team quota. We've hit 85% utilization twice, which caused training jobs to fail mid-run when the checkpoint write couldn't complete. This policy prevents that.

## Retention Rules

| Category | Retention |
|---|---|
| Production checkpoints (under `production/`) | Indefinite (manual archival only) |
| Staging checkpoints (under `staging/`) | 30 days from creation |
| Sweep run checkpoints | 7 days after sweep completes |
| Dev / ad-hoc runs | 3 days |
| Archived production models | 90 days, then deleted |

## Automated Cleanup

The cleanup script runs daily via cron on the NFS gateway:
```
0 3 * * * /opt/ml/scripts/cleanup_old_checkpoints.sh >> /var/log/checkpoint_cleanup.log 2>&1
```

Script location: `scripts/cleanup_old_checkpoints.sh`

The script:
1. Reads checkpoint directories and their `metadata.json`.
2. Checks `created_at` timestamp and the run's category (tagged in metadata).
3. Deletes directories exceeding their retention window.
4. Reports total space freed to Datadog metric `ml.nfs.checkpoint_cleanup_gb`.

## Tagging Checkpoints

When saving a checkpoint, the `metadata.json` must include:
```json
{
  "category": "staging",
  "created_at": "2024-11-05T14:32:00Z",
  ...
}
```

Valid values for `category`: `production`, `staging`, `sweep`, `dev`.

If `category` is missing, the script defaults to treating it as `dev` (3-day retention). **Don't skip this field.**

## Manual Cleanup

If you need space urgently:
```bash
# Check current usage
du -sh /mnt/nfs/checkpoints/*/

# Dry-run the cleanup script
bash scripts/cleanup_old_checkpoints.sh --dry-run

# Delete a specific run manually (be careful)
rm -rf /mnt/nfs/checkpoints/staging/rec-v5.3.0-rc1/
```

Never delete anything under `production/` without team confirmation in `#ml-training`.

## Monitoring

- Datadog dashboard: **ML NFS Storage** → widget "Checkpoint dir usage %"
- Alert fires at 80% utilization → Slack `#ml-training`
- Alert fires at 90% utilization → PagerDuty P2

## See Also
- `model-versioning-conventions.md` — directory structure
- `gpu-cluster-access.md` — NFS quota context
