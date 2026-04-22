# ML Training Team — New Engineer Onboarding

Welcome. This doc helps you get set up for contributing to the recommender training pipeline. Expect to spend 2–3 days on setup before you're ready to run your first training job.

## Step 1: Access Requests (file on day 1)

- [ ] **VPN** — IT ticket, usually same-day
- [ ] **GitHub org** — ask your manager
- [ ] **ml-training-users** IAM group — IAM portal (see `gpu-cluster-access.md`)
- [ ] **W&B team** — ask anyone on the team to add you to the `rec-training` project
- [ ] **Airflow** — request `ml-viewer` role in the internal portal
- [ ] **Data platform** — request access to `feature_store` Hive database

## Step 2: Repos to Clone

```bash
git clone git@github.com:internal/ml-models.git
git clone git@github.com:internal/ml-platform.git   # feature store definitions
git clone git@github.com:internal/airflow-dags.git   # data pipeline DAGs
```

## Step 3: Local Dev Setup

```bash
cd ml-models
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
```

> **Important:** `requirements-dev.txt` pins `numpy<2.0`. Do not upgrade it. See `training-image-build.md` for the full story.

Run the test suite to verify your setup:
```bash
pytest tests/ -m "not integration" -x
```

## Step 4: Read These Docs (in order)

1. `feature-store-schema.md` — know the data
2. `data-cleaning-pipeline.md` — know where it comes from
3. `training-config-reference.md` — understand the training loop
4. `gpu-cluster-access.md` — before submitting any jobs
5. `training-failure-modes.md` — save yourself debugging time

## Step 5: Run Your First Job

Submit a smoke-test training run on the dev cluster:
```bash
sbatch --partition=t4-16g \
       --gres=gpu:1 \
       --time=01:00:00 \
       --job-name=onboarding-smoke \
       scripts/train.sh --config configs/dev.yaml
```

Check the W&B dashboard for your run. If the loss is decreasing after 200 steps, you're good.

## Key Contacts

| Who | Role | Slack |
|---|---|---|
| Priya T. | Pipeline lead | @priya |
| Devon K. | Infra liaison | @devon |
| Marta S. | Data platform | @marta |
| Yuki O. | Features & modeling | @yuki |

## Slack Channels

- `#ml-training` — daily team discussion
- `#ml-data-eng` — data pipeline alerts and coordination
- `#infra-gpu-oncall` — cluster issues
- `#ml-serving` — coordinate with serving team on promotions
