# SAML SSO Runbook

Owner: IT/Ops + Security Engineering  
IdP: Okta  
Last tested: 2024-12-10

## Overview

All internal applications must use Okta as the identity provider via SAML 2.0. Direct username/password auth is only permitted for legacy services on an approved exception list (see `access-exceptions.md`). New services: do not roll your own auth — come talk to us first.

## Adding a New Application

### 1. Request an Okta app registration

Open a ticket in the `IT` Jira project with:
- Application name and owner team
- ACS URL (Assertion Consumer Service)
- Entity ID (SP entity ID)
- Requested attribute mappings (email, groups, etc.)

IT/Ops will provision the app within 2 business days.

### 2. Configure your service provider

Okta will provide:
- IdP SSO URL
- IdP entity ID
- X.509 signing certificate

Store the certificate in Vault at `secret/sso/<app-name>/idp-cert`. Do **not** commit it to the repo.

```python
# Example: loading IdP cert from Vault in Python
import hvac
client = hvac.Client(url=os.environ["VAULT_ADDR"])
cert = client.secrets.kv.v2.read_secret_version(
    path=f"sso/{APP_NAME}/idp-cert"
)["data"]["data"]["cert"]
```

### 3. Test the integration

- Use a test Okta account with no real permissions.
- Verify SAML response attributes are correct.
- Confirm logout (SLO) propagates if your app supports it.

### 4. Enable MFA enforcement

All production app integrations must have an Okta sign-on policy requiring MFA. Confirm the policy is attached before going live.

## Certificate Rotation

Okta signing certificates expire every 5 years, but we rotate them every 2 years. Schedule:

| Step | When |
|---|---|
| Add new cert alongside old (dual-cert mode) | T-30 days |
| Switch SPs to new cert | T-7 days |
| Remove old cert from Okta | T+0 |

See `secrets-rotation-schedule.md` for the master rotation calendar.

## Troubleshooting

### "Invalid SAML response" errors

1. Check that system clocks are synced (NTP) — SAML assertions have a short validity window (typically 5 minutes).
2. Verify the ACS URL matches exactly what's registered in Okta (trailing slash matters).
3. Decode the SAML response: `echo '<base64>' | base64 -d | xmllint --format -`

### User not assigned to app

User's Okta group must be assigned to the application. IT/Ops can add group assignments; individual exceptions need manager approval.

## Contacts

- Okta admin console: `https://ourcompany.okta.com/admin`
- IT/Ops on-call: `#it-ops-oncall` Slack channel
- Security question: `#security-eng`
