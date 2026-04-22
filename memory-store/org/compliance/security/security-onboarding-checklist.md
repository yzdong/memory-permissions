# Security Onboarding Checklist

For: New engineers (all disciplines)  
Owner: Security Engineering  
Complete within your first week. Your manager will verify completion.

This isn't about compliance theater — these items correspond to real incidents we've had. Please take them seriously.

## Day 1

- [ ] Enroll in Okta MFA (hardware key or Okta Verify with biometric preferred; SMS is not accepted)
- [ ] Confirm your laptop has full-disk encryption enabled
  - macOS: `System Settings → Privacy & Security → FileVault` should show ON
  - Linux: confirm LUKS at setup time; ask `#it-ops` if unsure
- [ ] Sign the acceptable use policy (sent via DocuSign in onboarding email)
- [ ] Join `#security-announcements` Slack channel (announcements only, low noise)

## Week 1

- [ ] Complete the 25-minute security awareness training in the learning portal (link in your onboarding Jira ticket). Covers phishing, social engineering, and data classification.
- [ ] Read `../pii-handling.md` — yes actually read it, there's a quiz at the end of the training that references it.
- [ ] Set up a password manager if you don't have one. Company-approved options: 1Password (IT will provision a license), Bitwarden.
- [ ] Confirm you do not have any AWS or cloud credentials stored in plaintext anywhere (dotfiles, shell history, etc.).
  ```bash
  # Quick check for common patterns
  grep -r 'AKIA' ~/.bashrc ~/.zshrc ~/.profile 2>/dev/null
  ```

## Before Getting Production Access

Production access requires completion of the above **and**:

- [ ] Walk through `access-review-quarterly.md` with your team lead so you understand the review process.
- [ ] Understand the secrets management workflow — read `secrets-rotation-schedule.md` and know how to read from Vault.
- [ ] Know the incident response process — skim `incident-response-template.md` so you're not learning it for the first time during an incident.

## Questions?

Ask in `#security-eng`. We don't bite and there are no dumb questions about security.

## Notes for Managers

Please verify the checklist is complete before opening a prod-access Jira ticket for your report. The access provisioning ticket template will prompt you for confirmation.
