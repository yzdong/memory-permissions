# Vendor Evaluation Playbook

For evaluating new infrastructure vendors, SaaS tooling, or managed services. Security and Finance need to be looped in early — don't wait until you've already decided.

## Trigger criteria
Start a formal evaluation when:
- Estimated annual spend would exceed $20k
- The vendor would have access to production data or our VPC
- We're replacing an existing vendor (comparative eval required)

## Phase 1: Requirements

Write a short requirements doc (`templates/vendor-requirements.md`). Include:
- Functional must-haves vs. nice-to-haves
- Non-functional: availability SLA, data residency, compliance certifications needed
- Rough usage projections for pricing estimates
- Integration requirements (API, Terraform provider, Kubernetes operator, etc.)

Get sign-off from the Platform lead and the primary stakeholder team before moving forward.

## Phase 2: Shortlist

Research candidates. Typical shortlist is 2–4 vendors. For each:
- [ ] Public documentation quality check
- [ ] Community / support reputation (check forums, Slack communities, GitHub issues)
- [ ] Reference check — do we know anyone using them at our scale?
- [ ] Pricing model clarity — usage-based vs. seat-based, egress costs, etc.

## Phase 3: POC

- Time-box POCs to 2 weeks max per vendor
- Use the staging environment; never eval with production traffic unless unavoidable
- Define success criteria **before** you start the POC, not after
- Track findings in `evaluations/vendor-poc-notes.md`

Typical criteria we weight:
| Criterion             | Weight |
|-----------------------|--------|
| Reliability / SLA     | 30%    |
| Ops burden            | 25%    |
| Cost at projected scale | 20%  |
| Security posture      | 15%    |
| Migration effort      | 10%    |

## Phase 4: Decision

- Present shortlisted vendors and POC results in a Platform team review
- Security completes vendor questionnaire review
- Legal reviews DPA / data processing agreement
- Finance approves budget commitment
- Decision recorded in `decisions/YYYY-MM-<vendor>.md`

## Phase 5: Onboarding
- Vendor added to vendor register (Finance owns this)
- Credentials stored in Vault; no shared personal accounts
- Runbook created for any operational tasks (restarts, config changes, incident escalation)
