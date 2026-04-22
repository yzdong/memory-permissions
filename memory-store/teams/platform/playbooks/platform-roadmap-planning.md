# Platform Roadmap Planning Playbook

How we build and maintain the Platform team roadmap. This isn't about sprint planning — it's about the bigger picture: what are we building over the next 6–12 months and why.

## Cadence
- Full roadmap refresh: every 6 months (aligned to H1/H2 planning)
- Lightweight quarterly check-in: mid-quarter, adjust priorities based on what's changed
- Ad-hoc amendments: any time a major incident, new requirement, or leadership directive warrants it

## Inputs to roadmap planning

### 1. Reliability data
Pull from the incident retro program (`incident-retro-program.md`). What themes keep coming up? Those are candidates for platform investments.

### 2. Service team requests
- Quarterly survey sent to all engineering teams — link to the template in `templates/platform-feedback-survey.md`
- Backlog of requests in the Platform Jira project (filter: label = `team-request`)
- Direct feedback from Platform syncs

### 3. Tech debt inventory
- Maintained in `docs/tech-debt-register.md`
- Prioritize items that are blockers for reliability or security

### 4. Strategic direction
- Company-level engineering priorities from the CTO's quarterly letter
- Any regulatory or compliance requirements on the horizon (coordinate with Legal)

## Prioritization framework

We use a simple scoring model. Score each initiative on:
- **Impact** (1–5): How much does this improve reliability, velocity, or cost?
- **Urgency** (1–5): Time-sensitive? Blocking other teams?
- **Effort** (1–5, inverted): 5 = small effort, 1 = very large

Score = Impact × Urgency × Effort. Rank and use judgment — don't let the numbers make the decision for you.

## Output format

Roadmap lives in `docs/platform-roadmap.md`. Structure:
- **Now** (current quarter): committed work with owners
- **Next** (following quarter): planned but not committed
- **Later** (6+ months): directional, expected to shift

Each item should have: one-line description, owner, rough size (S/M/L/XL), and a link to the detailed doc or ticket.

## Communication
- Present the roadmap at the quarterly all-hands engineering review
- Send a brief written summary to #platform-announcements after each planning cycle
- Keep `docs/platform-roadmap.md` current — if it's stale, people stop trusting it
