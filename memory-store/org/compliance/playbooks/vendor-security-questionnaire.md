# Vendor Security Questionnaire Process

## Why This Exists
We receive ~40 security questionnaires per year from enterprise customers doing vendor due diligence. Historically these took 2–3 weeks to complete and blocked deals. This playbook cuts that to 5 business days for standard questionnaires.

## Roles
- **Compliance Analyst:** owns the response process and coordinates internally
- **Security Engineering:** provides technical answers (architecture, encryption, logging)
- **Legal:** reviews any answers touching liability, SLAs, or indemnification language
- **Sales/CS:** customer-facing communication only — they do not draft answers

## Process

### Step 1: Classify the Questionnaire
| Type | Criteria | Target Turnaround |
|---|---|---|
| Standard | <50 questions, common frameworks (SIG Lite, CAIQ) | 3 business days |
| Full | 50–200 questions | 5 business days |
| Custom | >200 questions or novel legal asks | 10 business days + legal review |

### Step 2: Check the Response Library
- Library lives in Notion → Security → Vendor Q&A Library
- Search by keyword before drafting from scratch
- Library covers ~78% of commonly asked questions
- If a new answer is crafted, **add it to the library** after approval

### Step 3: Draft and Review
```
compliance-analyst     → drafts using library + new content
security-engineering   → reviews technical accuracy (required for any infra question)
legal                  → reviews if customer requests modifications to standard language
compliance-analyst     → final proofread, submit
```

### Step 4: Submission
- Preferred: customer's portal
- If email only: encrypt the document (see `../runbooks/secure-file-transfer.md`)
- Log submission date and customer name in the tracker

## Sensitive Disclosures
Never disclose without Legal sign-off:
- Specific cloud regions for data residency unless already public
- Names of sub-processors not listed on our public sub-processor page
- Details of any open audit findings
- Pending litigation

## Ongoing Maintenance
- Quarterly: compliance analyst reviews top 20 library entries for accuracy
- After each SOC 2 audit: update any audit-related answers
- Ping `#compliance-internal` when the library is updated so Sales knows

## Related Docs
- `soc2-audit-prep.md`
- `hipaa-baa-review.md`
- `../policies/sub-processor-list.md`
