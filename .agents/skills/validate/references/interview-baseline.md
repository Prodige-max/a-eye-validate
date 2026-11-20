# Buyer interview and operating baseline

Use this reference when public evidence suggests a problem but the pilot gates or economics still depend on buyer data. Do not count an interview as independent evidence when the participant is selling the proposed solution.

## Target participant

Prefer the person who owns the workflow or its operating result: Head of Credit, Chief Risk Officer, Credit Operations lead, Underwriting lead, Lending Product owner, Decision Science lead, or Model Risk/Governance lead. Record role and organization only with permission.

## Evidence-first interview

Ask for a recent real case before opinions:

1. Walk through the last application that needed manual referral or exception handling.
2. Which systems, documents, data sources, and people touched it?
3. Where did it wait, get re-keyed, or return for missing information?
4. What policy or rule determined the outcome? Could the team prove the production rule matched the approved policy?
5. Who could override the result, and where was the rationale recorded?
6. What failure matters most: slow decision, wrong approval/decline, inconsistent treatment, audit evidence, fraud, or lost conversion?
7. What did the case consume in analyst/reviewer minutes and elapsed time?
8. How often does this class of case occur in a month?
9. Which current tools or vendors were tried, and what exact gap remains?
10. What integration, security, legal, procurement, model-risk, and human-review approvals would a pilot need?
11. What measurable result would justify a pilot or purchase?

Do not lead with the proposed product. Ask for artifacts such as a redacted workflow, referral reason list, policy-change ticket, decision audit, or turnaround report. Treat unshared or unverified numbers as interview-reported, not measured.

## Minimum baseline worksheet

Capture low/base/high or measured distributions where possible.

| Field | Unit | Required for | Evidence status |
|---|---|---|---|
| Monthly applications/cases | cases/month | scale and ROI | measured preferred |
| Eligible workflow share | % | ROI | measured or sampled |
| Straight-through-processing rate | % | demand and ROI | measured |
| Manual referral rate | % | demand and ROI | measured |
| Manual handling time | minutes/case | ROI | time study preferred |
| Review/exception/rework time | minutes/case | net savings | time study preferred |
| End-to-end decision time | minutes/hours/days | pain | measured distribution |
| Rework or missing-document rate | % | demand | measured |
| Override rate and reasons | % and categories | governance | measured |
| Approval and decline rates | % | outcome | measured |
| Bad rate / loss metric | buyer-defined | risk guardrail | measured |
| Loaded staffing cost | ZAR/hour | capacity value | finance-approved |
| Current software/data cost | ZAR/year | net value | contracted/invoiced |
| Expected implementation cost | ZAR | year-one value | vendor/buyer estimate |
| Expected annual running cost | ZAR/year | recurring value | vendor/buyer estimate |
| Cash-realisable saving | ZAR/year | cash payback | finance-approved |

Keep capacity value separate from cash savings. If no staff cost, vendor spend, loss, or conversion will actually change, do not present released hours as cash savings.

## Interview gate result

After each interview record:

- participant role and buyer fit;
- date and geography;
- workflow boundary;
- evidence IDs for claims and artifacts;
- measured, interview-reported, or assumed status;
- incumbent and remaining gap;
- pilot approval route;
- conflicts with public or prior evidence;
- whether the operating baseline changed the score.

Five similar interviews are not automatically five independent organizations. Deduplicate colleagues describing the same workflow and distinguish consensus from repeated internal narrative.
