# Physical Security Policy

**Owner:** Facilities & IT Security  
**Effective Date:** 2023-03-15  
**Scope:** All company offices, co-location facilities, and any space where company equipment or data is processed

---

## Intent

Digital controls matter, but a sophisticated attacker with physical access can bypass most of them. This policy establishes baseline physical security controls to protect people, equipment, and information across our facilities.

## Office Locations Covered

- HQ (primary office)
- Regional offices (see Facilities for current list)
- Colocation data center spaces managed by Infrastructure team

Home offices are covered by the BYOD and remote work guidance in `byod-policy.md`, not this policy.

## Access Control

- All office entrances require badge access. Tailgating (following someone through a door without scanning your own badge) is prohibited.
- Visitors must be registered in advance via the visitor management system and escorted by an employee at all times in non-public areas.
- Badge access logs are retained for **12 months** and reviewed monthly by Facilities.
- Lost or stolen badges must be reported to Facilities within 2 hours. Badge will be deactivated immediately.
- Access to server rooms, network closets, and infrastructure spaces is restricted to IT/Infrastructure staff and approved vendors.

## Clear Desk / Clear Screen

- Lock your screen when stepping away from your workstation. (Shortcut: `Cmd+Ctrl+Q` on macOS, `Win+L` on Windows)
- Don't leave sensitive printed documents unattended. Use the shredding bins provided.
- Whiteboards and shared screens should not display confidential information when meetings end.

## Secure Areas

Server rooms and network infrastructure closets have additional controls:

- Two-person rule for after-hours access
- CCTV coverage with 60-day footage retention
- Environmental monitoring (temperature, humidity, water detection)
- Quarterly access list review — access is revoked within 24 hours of role change

## Equipment

- Company laptops must not be left unattended in public spaces (airports, coffee shops, conference venues) even briefly.
- Locking cables should be used when working in non-secure shared spaces.
- All hardware shipped between offices must use tracked shipping with signature confirmation.
- Decommissioned hardware is returned to IT for secure wiping per `../it/hardware-disposal-procedure.md`.

## Incidents

Physical security incidents (unauthorized access, break-in, hardware theft) must be reported to Facilities and Security immediately. Do not touch or move evidence before IT Security has assessed the scene.

## Audits

Facilities conducts a quarterly physical security walk-through and reports findings to the CISO. Colocation facilities are audited annually, typically through review of the SOC 2 report from the colocation provider.

## Related Documents

- `byod-policy.md`
- `information-security-policy.md`
- `../it/hardware-disposal-procedure.md`
- `../incident-response/runbook.md`
