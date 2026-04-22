# Internal Feature Flag SDK v1 Removal

**Status:** v1 deprecated, removal target 2025-11-01  
**Owner:** Platform  
**SDK repo:** `libs/feature-flags/`

## What's v1

The v1 SDK is the original in-house feature flag client (`libs/feature-flags/v1/`). It polls a config file from S3 every 30 seconds and caches flags in memory. It doesn't support:

- Gradual rollouts / percentage-based targeting
- User or segment targeting
- Real-time flag updates (the 30-second lag has caused problems)
- Flag evaluation analytics (we can't see which flags are actually being checked)

v2 (`libs/feature-flags/v2/`) was shipped in late 2024 and addresses all of these via a streaming connection to the flag service.

## Why Now

The S3 config file format that v1 reads is being replaced. The flag service is the new source of truth. We plan to retire the S3 polling path entirely, which means v1 becomes non-functional.

## Migration

### Install

```toml
# pyproject.toml
[tool.poetry.dependencies]
platform-feature-flags = ">=2.0.0,<3.0"
```

### Code Change

```python
# v1
from feature_flags.v1 import get_flag
enabled = get_flag("my-feature")

# v2
from feature_flags.v2 import FlagClient
client = FlagClient()  # initialized once, share the instance
enabled = client.is_enabled("my-feature", context={"user_id": user.id})
```

The `context` parameter is optional but enables targeting rules. Pass at minimum `user_id` for any user-facing flags.

## Service Tracker

| Service | Status |
|---|---|
| api-gateway | ✅ v2 |
| billing-worker | 🔄 In progress |
| notification-service | ⏳ Not started |
| data-pipeline | ✅ v2 |
| reporting-api | ⏳ Not started |

## Deadline

All services must be on v2 by **2025-10-01** to give a 30-day buffer before the S3 polling endpoint is turned off on 2025-11-01.

If your service misses this, it will fail to evaluate any flags and most likely default everything to `False`, which could silently disable features in production.

## Contact

Ping `#platform-help` with the label `feature-flags` or comment on `PLAT-3187`.

## References

- `libs/feature-flags/v2/README.md`
- `libs/feature-flags/CHANGELOG.md`
