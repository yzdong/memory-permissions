# Lint Override Policy — Platform Team

Platform maintains a set of deliberate overrides against the org-wide linting defaults. This doc explains the rationale, the current overrides, and the process for changing them.

## Why Overrides Exist

The org defaults are written for product teams shipping user-facing features. Platform writes a lot of scaffolding, migration tooling, and infra glue code where some of those rules create more noise than signal.

Overrides are not a free pass to write sloppy code. Each one is documented here with a rationale.

## Current Overrides

### JavaScript / TypeScript (applies to `scripts/` and `tools/`)

| Rule | Org default | Platform override | Reason |
|------|------------|-------------------|--------|
| `no-unused-vars` | `error` | `warn` | Infra scripts carry stubs during active development; erroring blocks iterative work |
| `no-console` | `warn` | `off` | CLI tooling intentionally uses console for user output |
| `prefer-const` | `error` | `error` | No change — this one we agree with |

Override config: `../../.eslintrc.platform.json`

### Python (applies to `infra/scripts/`)

| Rule | Org default | Platform override | Reason |
|------|------------|-------------------|--------|
| `pylint: W0611` (unused import) | `error` | `warning` | Same rationale as no-unused-vars |
| `line-too-long` (max) | 100 | 120 | Terraform resource names push lines long |

Override config: `.pylintrc.platform`

### Terraform

| Rule | Org default | Platform override | Reason |
|------|------------|-------------------|--------|
| `terraform_required_providers` | `error` | `warn` in sandbox stack only | Sandbox is experimental |

## Adding a New Override

1. Propose in `#platform-eng` with rationale
2. Team vote (simple majority, quorum = 3 members)
3. Update this doc and the relevant config file
4. PR with 2 approvals

## Removing an Override

Same process. We should revisit overrides quarterly — they accumulate.

## Related

- `code-review-rules.md`
- `../../.eslintrc.platform.json`
