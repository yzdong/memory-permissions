# Celery 3.x Deprecation and Upgrade to Celery 5

**Status:** Completed 2024-08-01  
**Owner:** Platform  
**Affected Services:** `ingestion-worker`, `notification-service`, `report-exporter`

## Why Celery 3 Had to Die

Celery 3.1.x hasn't had a release since 2017. We were accumulating CVEs (two moderate-severity ones in the message serialization layer in 2023) and couldn't use any modern task routing features.

Celery 5 dropped Python 2 support and revamped the configuration namespace. The upgrade is not trivial.

## Configuration Namespace Changes

This is the biggest pain point. Every config key changed prefix.

```python
# Celery 3 style
CELERYBROKER_URL = 'redis://redis.internal:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis.internal:6379/1'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

# Celery 5 style
app.conf.broker_url = 'redis://redis.internal:6379/0'
app.conf.result_backend = 'redis://redis.internal:6379/1'
app.conf.task_serializer = 'json'
app.conf.accept_content = ['json']
```

Celery provides a migration utility: `celery upgrade settings <your-settings-file>`. It catches most but not all cases — review the diff manually.

## Task API Changes

- `task.apply_async(countdown=60)` still works
- `task.subtask()` is removed — use `task.signature()` or the `s()` shorthand
- `@task` decorator still works, but prefer `@shared_task` for reusability

## Worker Startup Change

```bash
# Old (Celery 3)
python -m celery worker -A myapp -l info

# New (Celery 5)
celery -A myapp worker -l INFO
```

Update your `supervisord.conf` and container `CMD` accordingly.

## Rollout Strategy

We deployed with the old and new worker running in parallel briefly (different queue names) to drain in-flight tasks before cutting over. Do not restart workers mid-task on high-volume queues without this.

## Related

- `runbooks/celery-worker-scaling.md`
- `services/ingestion-worker/README.md`
