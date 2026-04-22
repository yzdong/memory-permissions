# Platform Team — Agent Guide

This file gives LLM agents the context they need to act on behalf of the
Platform team. Load this file at the start of any Platform task.

## Who we are
The Platform team owns the deploy pipeline, shared infra (Postgres, Redis,
Kafka), and the internal CLI (`just`). We support all product teams.

## Key files in our team memory
- `runbooks/deploy.md` — canonical deploy sequence for our three services.
- `known-flaky-tests.md` — tests we have agreed to auto-retry rather than fix.

## Overrides we maintain (vs. org defaults)
- Lint rule `no-unused-vars`: **warn** (org default is error). We intentionally
  keep some scaffolding variables in early-stage services.
- Pre-commit hook `license-header`: **disabled** for this team; headers are
  injected at build time.
- Python version floor: **3.11** (org says 3.10).

## House style
- Always reference services by their short name: `api`, `worker`, `gateway`.
- Any change to `runbooks/deploy.md` requires a second approver from the team.
