# Linting and Style Rules — Platform Team

This document captures Platform's linting configuration choices and the rationale behind deviations from org defaults.

## ESLint Overrides

Config file: `.eslintrc.platform.json` (repo root)

```json
{
  "extends": "../../.eslintrc.org.json",
  "rules": {
    "no-unused-vars": "warn",
    "no-console": "warn",
    "complexity": ["warn", 15]
  }
}
```

**Why `no-unused-vars` is warn, not error:**
Deploy orchestration code often has variables declared for debugging purposes that get stripped in production builds. Treating them as errors caused too many false-positive CI failures. We accept warn and do periodic cleanups.

**Why `complexity` threshold is 15:**
Pipeline orchestration functions are inherently complex. Splitting them further often makes them harder to follow, not easier. This is a judgment call the team revisited in Q3 and stood by.

## Python (for infra scripts)

We use `ruff` for linting and `black` for formatting. Config in `pyproject.toml`.

- Line length: 100 (not the ruff default of 88 — pipeline scripts have long argument chains).
- Ignored rules: `E501` for generated files only (marked with `# noqa: E501` inline).

## Shell Scripts

`shellcheck` runs on all `.sh` files in CI. No exceptions. If shellcheck flags something and you believe it's a false positive, use an inline disable comment with an explanation:

```bash
# shellcheck disable=SC2086 # word splitting is intentional here for arg expansion
```

## Terraform

`terraform fmt` and `tflint` both run in CI. `tflint` uses the AWS ruleset. Warnings are allowed; errors block merge.

## Pre-Commit Hooks

All Platform engineers should run `pre-commit install` after cloning any Platform repo. The hook config (`.pre-commit-config.yaml`) runs linting and secret scanning before each commit. If it's slowing you down, profile which hook is the culprit before disabling anything.
