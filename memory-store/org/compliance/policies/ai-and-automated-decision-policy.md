# AI and Automated Decision-Making Policy

**Status:** Active  
**Owner:** Privacy Office & Engineering Leadership  
**Effective:** 2024-06-01  
**Review:** Annual or upon significant model change

---

## Why This Policy

We're increasingly using machine learning models to influence or automate decisions that affect people — customers, job applicants, employees. Getting this wrong carries legal risk (GDPR Art. 22, EU AI Act, various US state laws) and, more importantly, real harm to real people. This policy sets guardrails.

## Scope

Covers any system that:
- Makes or materially influences decisions about individuals automatically (without human review)
- Uses ML or statistical models as a significant input into business decisions

Excludes: internal analytics dashboards used by humans for decision support where no automated output is acted on directly.

## Classification of Automated Decisions

| Category | Example | Required Safeguards |
|----------|---------|--------------------|
| High Impact | Credit/access decisions, employment screening | Human review required, full audit trail |
| Medium Impact | Content personalization, churn scoring | Documented model card, quarterly review |
| Low Impact | Spam filtering, internal routing | Standard logging |

## Model Governance Requirements

### Before Deployment

1. Complete a Model Risk Assessment (template: `../ai-governance/model-risk-assessment-template.md`)
2. Document the model card: training data, known limitations, intended use, out-of-scope uses
3. Bias evaluation must be conducted — minimum F1 score of 0.78 required across demographic cohorts for High Impact models
4. Privacy Office review for any model trained on personal data
5. Legal review if the decision domain is regulated (credit, employment, insurance)

### In Production

- Log inputs, outputs, and decision rationale for High Impact decisions for a minimum of **2 years**
- Monitor for distribution shift; alert if feature drift score exceeds 0.15
- Review model performance quarterly; document outcomes in `../ai-governance/model-review-log.md`

### Decommissioning

- Archive model artifacts and training data per `data-retention-schedule.md`
- Document reason for decommission and replacement in the model registry

## Human Oversight

For High Impact decisions, individuals must be able to:
- Request a human review of an automated decision that affects them
- Receive a meaningful explanation of the factors involved
- Challenge and have the decision corrected if erroneous

Product teams are responsible for building these mechanisms. If your product makes High Impact automated decisions without these features, it's not compliant.

## Prohibited Uses

- Real-time biometric categorization in public spaces
- Social scoring or systemic monitoring of personal behavior
- Emotion inference in hiring or performance evaluation
- Any use of personal data outside its declared processing purpose

## Questions

Contact the AI Governance Working Group via `#ai-governance` in Slack or email `privacy@company.internal`.
