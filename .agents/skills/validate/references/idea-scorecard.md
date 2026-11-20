# Market-tested idea scorecard

Use this scorecard for every idea so results stay comparable across markets and dates. The score measures evidence, not enthusiasm. Keep the score range, confidence, market-test stage, pilot gates, and next experiment separate; no single number replaces judgment.

## Scorecard output

Every idea receives:

1. A stable run ID and normalized scope.
2. Four dimension scores from 0 to 5 or `unknown`.
3. A weighted total or range out of 100.
4. Evidence confidence: low, medium, or high.
5. A market-test maturity stage.
6. Four pilot-gate results.
7. A verdict, top unknown, and one bounded next experiment.
8. Red flags that can override an attractive numerical score.

## Evidence checklist by dimension

The written anchors in `rubric.md` determine the integer dimension score. Use the questions below to test whether the anchor is actually supported; do not average checklist answers into false precision.

### Demand — 25 points

- **Buyer fit:** Are sources from the actual operator, decision owner, approver, industry, geography, and organization size?
- **Firsthand pattern:** How many independent identifiable buyers and organizations describe the problem themselves?
- **Frequency:** How often does it occur per day, month, case, transaction, or decision?
- **Severity:** What time, delay, loss, error, risk, revenue, customer, or compliance consequence results?
- **Workarounds:** What spreadsheets, manual reviews, services, extra headcount, or process compromises exist?
- **Buying signal:** Has a buyer budgeted, procured, trialled, requested, or switched a solution?
- **Baseline quality:** Is the pattern measured, interview-reported, externally benchmarked, assumed, or unknown?

### Unmet need — 25 points

- **Direct coverage:** Which exact workflow stages do current products and services cover?
- **Incumbent outcome:** Does independent evidence show pain remaining after adoption, not merely before purchase?
- **Substitutes:** Can ERP features, spreadsheets, services, policy changes, portals, or process redesign solve it adequately?
- **Gap materiality:** Is the remaining gap frequent and consequential or a rare edge case?
- **Access and switching:** Are cost, implementation time, procurement, data residency, integration, or vendor lock-in meaningful barriers?
- **Differentiation:** Is the idea measurably better on an important dimension rather than differently described?
- **Defensibility:** Would data, workflow embedding, distribution, approvals, switching costs, or learning effects make the advantage durable?

### Net savings — 30 points

- **Measured baseline:** Are volume, eligibility, adoption, handling time, rework, error and loaded labor cost buyer-fit?
- **Gross value:** Are capacity, loss avoidance, revenue or resource benefits calculated without double counting?
- **Full cost:** Are implementation, integration, change management, licenses, infrastructure, support, review and exception costs included?
- **Downside:** Is the conservative scenario positive after full cost?
- **Realization:** Can released capacity become cash savings, throughput, service improvement, risk reduction, or another owned outcome?
- **Payback:** Is economic payback acceptable to this buyer, and is cash payback separately supported?
- **ROI:** What are low, base, and high year-one ROI after all recurring and implementation costs, and does the base case clear a documented buyer hurdle?
- **ROI basis:** Is the result measured, sourced, mixed, hypothetical, or unknown? Hypothetical ROI cannot produce a known Net Savings score.
- **Sensitivity:** Which two inputs can reverse the decision?

Calculate year-one ROI consistently:

```text
year_one_total_benefit = annual_capacity_value + independently_verified_annual_savings
year_one_total_cost = annual_running_costs + one_time_implementation_costs
year_one_roi_percent = (year_one_total_benefit - year_one_total_cost) / year_one_total_cost * 100
```

Label capacity-led results **economic ROI**. Report **cash ROI** only when the numerator uses realizable cash inflows or cost reductions with an owner and realization plan. ROI is evaluated inside Net Savings; it does not add extra points beyond that dimension's 30-point weight.

### Feasibility — 20 points

- **Data:** Are required inputs available, lawful, sufficiently complete, timely, and attributable to the correct entity?
- **Integration:** Is there a supported read, write, idempotency, retry, read-back, and reconciliation path?
- **Accuracy and exceptions:** Are acceptance thresholds, failure modes, review load, overrides and correction paths defined?
- **Security and compliance:** Are authentication, authorization, separation, privacy, retention, audit and regulatory requirements plausible?
- **Workflow adoption:** Does a named owner have authority, incentive, time, and an operating procedure for the new workflow?
- **Delivery:** Can the team implement, operate, monitor, support, recover and update it at the target scale?
- **Approval route:** Are procurement, legal, model risk, information security and business sign-off understood?

## Market-test maturity stage

Maturity is not the score. Record the highest stage whose evidence is complete.

| Stage | Name | Required evidence |
|---:|---|---|
| 0 | Hypothesis | Problem, buyer and proposed outcome are stated but external evidence is not complete. |
| 1 | Public evidence | Independent demand, supply and benchmark research is complete with explicit gaps. |
| 2 | Buyer discovery | Target buyers supplied recent cases, current workflow, consequences, incumbent experience and buying constraints. |
| 3 | Baseline validated | Representative buyer data measures volume, time, quality, costs and the counterfactual. |
| 4 | Controlled pilot | The solution ran on representative data or workflow with predefined acceptance criteria and human controls. |
| 5 | Repeatability proven | More than one buyer or deployment reproduced value with a supportable delivery and commercial model. |

Do not advance a stage because a demo exists. Synthetic data can test mechanics but not buyer discovery, baseline validity, pilot outcomes, or repeatability.

## Pilot gates

Report each as `yes` or `no`; unknown is `no` for commitment purposes.

1. **Verified pain:** target-buyer firsthand evidence and a material repeated consequence.
2. **Incumbent comparison:** exact workflow coverage, substitutes, costs and remaining gap were evaluated.
3. **Operating baseline:** representative volume, handling, quality and cost data were validated.
4. **Integration route:** data, controls, approvals, exception handling and deployment have a plausible buyer-approved path.

All four gates and plausibly positive full-cost economics are required for a `pilot` verdict. A high score cannot waive a failed gate.

## Score interpretation

Bands describe evidence strength, not an automatic verdict.

| Total or lower bound | Interpretation | Normal commitment |
|---:|---|---|
| 0–29 | Weak or contradicted case | Deprioritize or materially re-scope. |
| 30–49 | Early signal with major uncertainty | Cheap discovery only. |
| 50–64 | Plausible opportunity | Interview, baseline or integration test. |
| 65–79 | Strong candidate | Pilot only if every gate passes. |
| 80–100 | Very strong evidence | Scale carefully; verify repeatability and operational economics. |

When a score is a range, use the lower bound for commitment decisions. Do not rank ideas by an assumed midpoint. Compare lower bound, confidence, maturity stage, failed gates, top unknown, and cost of the next test.

## Confidence rules

- **Low:** decision-critical evidence is vendor-led, supplied by the idea sponsor, weakly matched, stale, hypothetical, inaccessible, or conflicting.
- **Medium:** independent evidence is useful and current, but buyer fit, baseline quality, or source coverage has a material limitation.
- **High:** multiple independent sources and target-buyer data support the important claims; the baseline is measured and material conflicts are resolved.

Confidence can cap commitment: low-confidence ideas cannot receive `pilot`; medium confidence requires every pilot gate and a deliberately bounded pilot; high confidence does not remove operational controls.

## Red-flag overrides

Call out these facts even when the numerical score is attractive:

- A legal, safety, data-access, or approval blocker without a credible mitigation.
- Negative conservative economics after full cost.
- No material differentiation from an accessible incumbent.
- Evidence of demand comes mainly from sellers, affiliates, investors, or the idea team.
- The proposed solution creates an uncontrolled financial, credit, employment, health, legal, or security decision.
- The business case depends on counting released capacity as cash without an owner and realization plan.
- The pilot uses synthetic or unrepresentative data for a claim about buyer outcomes.
- A successful technical demo is presented as proof of adoption, willingness to pay, or repeatability.

## Selecting the next experiment

Choose one experiment that attacks the top unknown. Prefer the test with the highest decision leverage and the lowest irreversible cost. State:

- hypothesis that could be disproved;
- target buyer/sample and owner;
- evidence or data required;
- pass, fail and stop thresholds;
- time and cost boundary;
- decision that follows each outcome.

Examples include five evidence-first buyer interviews, a 30-case time study, a representative historical backtest, one read-only connector proof, a paid design-partner commitment, or a controlled pilot with pre-registered accuracy and economics.
