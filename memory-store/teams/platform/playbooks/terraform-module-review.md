# Terraform Module Review Playbook

This governs how we review and publish new shared Terraform modules to the internal registry. Modules are in `infra/terraform/modules/`.

## When is a module review needed?
- New module being published for the first time
- Breaking changes to an existing module interface (input/output variables)
- Major provider version bumps within a module
- Modules that touch IAM, networking, or secrets management — always need review regardless of change size

## Author responsibilities (before requesting review)

- [ ] Module follows the standard structure:
  ```
  modules/<name>/
    main.tf
    variables.tf
    outputs.tf
    versions.tf
    README.md
    examples/basic/
  ```
- [ ] `README.md` documents all inputs and outputs (use `terraform-docs` to generate)
- [ ] At least one example in `examples/`
- [ ] `terraform validate` passes
- [ ] `tflint` passes with the team config at `infra/.tflint.hcl`
- [ ] Unit tests added in `tests/` using Terratest or BATS

## Review criteria

### Security
- No hardcoded credentials, account IDs, or ARNs that should be parameterized
- IAM policies follow least privilege; wildcards in resource fields flagged automatically by our Checkov policy (`infra/checkov-policies/`)
- Encryption at rest enabled where applicable; explicit `false` requires a written justification in the PR description

### Interface quality
- Variable names are descriptive and consistent with existing modules
- Sensitive variables marked `sensitive = true`
- Outputs don't expose things that don't need to be exposed

### Operability
- The module shouldn't require manual state surgery for common updates
- `lifecycle` blocks justified in comments
- Tagging strategy follows `infra/tagging-policy.md`

## Review SLA
Platform engineers respond within 2 business days. Ping `#platform-review` if you're blocked.

## Publishing
After approval, bump the version in `versions.tf` (semver), tag the repo, and the CI pipeline publishes to the internal registry automatically.

```bash
git tag modules/<name>/v<major>.<minor>.<patch>
git push origin --tags
```
