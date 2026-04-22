# Naming Conventions — Platform Team

Consistency in resource names saves time during incidents. These conventions apply to all resources Platform owns or provisions.

## General Pattern

```
{env}-{service}-{resource-type}[-{disambiguator}]
```

Examples:
- `prod-deployer-db-primary`
- `staging-secrets-kv-store`
- `dev-metrics-collector-01`

## Environments

| Short name | Meaning         |
|------------|----------------|
| `dev`      | Local / dev    |
| `staging`  | Pre-prod       |
| `prod`     | Production     |
| `sandbox`  | Experimental   |

Do not use `prd`, `stg`, or any other abbreviations. The full short names above are the standard.

## Kubernetes Resources

- Namespaces: `platform-{env}` (e.g. `platform-prod`)
- Deployments: follow general pattern
- ConfigMaps: `{service}-config[-{variant}]`
- Secrets: see `secrets-handling.md` — names follow a tighter pattern

## Terraform Modules and Resources

- Module directories: `infra/modules/{resource-type}/` (e.g. `infra/modules/rds/`)
- Resource local names: snake_case, descriptive (e.g. `primary_db_instance`, not `db1`)
- Avoid numeric suffixes unless there are genuinely multiple identical resources

## GitHub Repositories

Platform-owned repos: `platform-{purpose}` (e.g. `platform-deploy-agent`, `platform-secrets-sync`)

## Slack Channels

- Operational: `#platform-{topic}` (e.g. `#platform-oncall`, `#platform-deploys`)
- Incident bridge: `#incident-{YYYY-MM-DD}-{slug}`

## What to Avoid

- CamelCase in resource names (use kebab or snake depending on context)
- Dates in resource names (use versions or semantic tags instead)
- Personal names (use role or function)
- Abbreviations not listed in this doc

## Exceptions

External vendor resources (e.g. third-party SaaS) follow their own naming and are exempt. Document any exception in the relevant runbook.

## Related

- `secrets-handling.md`
- `../runbooks/terraform-workflow.md`
