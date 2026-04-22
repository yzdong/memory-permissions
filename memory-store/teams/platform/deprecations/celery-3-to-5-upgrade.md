# Celery 3.x → 5.x Upgrade

**Status:** Done  
**Completed:** 2025-02-28  
**Affected services:** All Python services using async task queues

## Context

Celery 3 was the project default because it shipped with our original scaffold template in 2019. Celery 4 was skipped intentionally (it had a rough reception). We went straight to 5.x. This doc exists because a few services took shortcuts that will bite them later.

## Breaking Changes We Hit

### Task result serialization

Celery 5 defaults to JSON serialization. Some old tasks were using `pickle`, which is now disabled by default for security reasons. Services that had `CELERY_TASK_SERIALIZER = 'pickle'` needed to:
- Convert task arguments and return values to JSON-serializable types
- Explicitly set `task_serializer = 'json'` and `result_serializer = 'json'`

### `AsyncResult.get()` behavior

In Celery 3, calling `.get()` on a task that raised an exception would re-raise it in the caller. Celery 5 still does this, but the traceback format changed. A few exception-handling wrappers were checking `isinstance(e, celery.exceptions.TaskRaisedException)` which no longer exists — replace with `celery.exceptions.CeleryError`.

### Beat schedule format

The `CELERYBEAT_SCHEDULE` dict key format changed to `beat_schedule`. Both work in 5.x via a compat shim, but the shim emits a deprecation warning on startup that was flooding our logs. All beat schedules updated.

## Services That Cut Corners

`services/notification-service` still uses `task_always_eager = True` in its test config, which works but masks actual broker connectivity issues. Ticket filed: `PLAT-3302`.

## Version Pinning

All services should now have:
```toml
[tool.poetry.dependencies]
celery = ">=5.3.0,<6.0"
```

Do not pin to `5.x.x` exactly — we want to pick up patch releases.

## References

- `libs/platform-utils/tasks/base.py` — shared base task class updated for 5.x
- [Celery 5 migration guide](https://docs.celeryq.dev/en/stable/whatsnew-5.0.html)
