# S3 Path-Style Access Deprecation

**Status:** Completed 2024-12-01  
**Owner:** Platform  
**Risk:** Low (AWS deprecated path-style; virtual-hosted-style is the default now)

## What Was Path-Style Access?

Path-style S3 URLs look like: `https://s3.us-east-1.amazonaws.com/my-bucket/my-key`

Virtual-hosted-style looks like: `https://my-bucket.s3.us-east-1.amazonaws.com/my-key`

AWS stopped supporting path-style for new buckets in 2020 and has been deprecating it for existing ones. We had a handful of services still constructing path-style URLs explicitly.

## Affected Code Patterns

```python
# BAD: explicit path-style
s3_client = boto3.client('s3', config=Config(
    s3={'addressing_style': 'path'}
))

# GOOD: let boto3 default (virtual-hosted)
s3_client = boto3.client('s3')
# or explicitly:
s3_client = boto3.client('s3', config=Config(
    s3={'addressing_style': 'virtual'}
))
```

## Scan Results

Ran `grep -rn "addressing_style.*path" services/` — found 7 occurrences in 4 services:

- `services/export-service/storage.py` (2 occurrences)
- `services/archive-worker/s3_client.py` (1)
- `scripts/data/bulk-export.py` (3)
- `services/config-service/backup.py` (1)

All fixed in PR #2241.

## MinIO Caveat

Our local dev environment uses MinIO for S3 emulation. MinIO still requires path-style access. Handle this with an environment check:

```python
if os.getenv('S3_USE_PATH_STYLE', 'false').lower() == 'true':
    s3_config = Config(s3={'addressing_style': 'path'})
else:
    s3_config = Config(s3={'addressing_style': 'virtual'})
```

Set `S3_USE_PATH_STYLE=true` in `.env.local` for dev. Do not set this in any deployed environment.

## Related

- `runbooks/s3-access-troubleshooting.md`
- `../infrastructure/object-storage-policy.md`
