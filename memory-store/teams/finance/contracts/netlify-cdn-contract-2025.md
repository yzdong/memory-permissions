# Netlify — CDN & Hosting Contract (2025)

**Status:** Under Review — likely migrating off platform  
**Current Term:** 2025-01-01 to 2025-12-31  
**Owner:** Platform Engineering + Finance  
**Decision Deadline:** 2025-11-01  

## Current Usage

Netlify hosts our marketing site and documentation portal. Monthly traffic varies seasonally. Build minutes and bandwidth are within tier limits for most months, with spikes during product launches.

## Why We're Reconsidering

Platform Engineering raised concerns in Q3 2025:
- Build times have increased with the docs site rewrite (monorepo approach doesn't cache well on Netlify's build infra)
- Support response SLAs have slipped — two incidents where P1 tickets took >6 hours for first response
- Pricing for enterprise features (IP allowlisting, SSO, audit logs) is bundled into a tier that's more expensive than comparable options

## Alternatives Evaluated

| Option | Pros | Cons |
|--------|------|------|
| Vercel Enterprise | Better Next.js support, faster builds | Higher cost at current scale |
| Cloudflare Pages | Excellent CDN, good pricing | Less mature CI/CD integration |
| AWS Amplify + CloudFront | Already on AWS EDP, could get discount | Higher eng overhead to maintain |
| Self-hosted on existing k8s | Maximum control | Significant infra eng time cost |

Platform Engineering preference: Cloudflare Pages. Finance preference: AWS Amplify (leverages existing EDP commitment). Decision to be made jointly by VP Engineering and CFO.

## Contract Termination Notes

Netlify contract has 60-day written termination notice requirement. If we decide to migrate:
- Notice must be sent by **2025-11-01** to avoid auto-renewal
- Data export: static site files are in GitHub, no migration risk
- DNS cutover plan: coordinate with infra team (`../../../infra/runbooks/dns-migration.md`)

## Action Items

- [ ] Platform Eng to complete Cloudflare Pages POC by 2025-10-15
- [ ] Finance to model AWS Amplify cost under EDP discount scenario
- [ ] Decision meeting: 2025-10-22 with VP Eng + CFO
- [ ] Send termination notice if migrating: 2025-11-01
