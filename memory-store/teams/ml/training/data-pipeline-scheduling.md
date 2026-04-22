# Data Pipeline Scheduling

## Overview

All ML data pipelines are orchestrated in Airflow. The DAG definitions live in `airflow/dags/` in the `data-platform` repo (not this repo). This doc describes the schedules and dependencies relevant to ML training.

## Pipeline Dependency Graph

```
event_ingestion_dag (hourly)
    └─> data_cleaning_pipeline (daily, 02:00 UTC)
            └─> feature_materialization_dag (daily, 04:00 UTC)
                    └─> training_dataset_export_dag (daily, 06:00 UTC)
```

Training jobs should not start before 07:00 UTC to ensure the dataset export is complete.

## SLAs

| DAG | Expected completion | SLA breach page |
|-----|--------------------|-----------------|
| `event_ingestion_dag` | Within 30min of hour | #data-platform-alerts |
| `data_cleaning_pipeline` | By 03:30 UTC | #ml-data-alerts |
| `feature_materialization_dag` | By 05:30 UTC | #ml-data-alerts |
| `training_dataset_export_dag` | By 07:00 UTC | #ml-data-alerts |

## What to Do When a Pipeline Is Late

1. Check Airflow logs for the failed task: `https://airflow.internal/tree?dag_id=data_cleaning_pipeline`
2. If it's a Dataproc issue, see `runbooks/dataproc-triage.md`
3. If the cleaning DAG failed and you need training data urgently, you can run the cleaning job manually:
   ```bash
   gcloud dataproc jobs submit pyspark \
     gs://ml-scripts/cleaning/run_cleaning.py \
     --cluster=ml-dataproc-batch \
     -- --date=$(date -u +%Y-%m-%d --date=yesterday)
   ```
4. Notify `#ml-oncall` before starting a training job on potentially stale data

## Backfilling

To backfill a date range:

```bash
airflow dags backfill data_cleaning_pipeline \
  --start-date 2024-11-01 \
  --end-date 2024-11-15
```

Backfills are expensive — coordinate with Platform before running more than 7 days.

## Monitoring Dashboard

`https://grafana.internal/d/ml-data-pipelines` — shows lag, row counts, and data quality signals per run.

## See Also

- `data-cleaning-pipeline.md`
- `feature-store-schema.md`
