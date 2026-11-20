# Verified Market Score

Use this system to produce one comparable score out of 100 without disguising missing evidence as market potential. The score measures the opportunity verified today. A missing criterion earns zero verified points but remains labelled `unknown`; it is not evidence that the market outcome itself is zero.

## Calculation

Each criterion has a fixed weight, a performance rating, and a verification grade.

```text
criterion points = criterion weight * performance rating / 5 * verification factor
verified market score = sum of all criterion points
evidence coverage = sum of criterion weight * verification factor
```

Round criterion points and the final score to two decimals. The weights total 100. Use `unknown` for a performance rating that cannot be supported and assign zero points. Do not create a best-case endpoint or substitute an assumed midpoint.

## Verification grades

| Grade | Factor | Minimum standard |
|---|---:|---|
| Verified | 1.00 | Representative target-buyer measurement, controlled pilot, signed operating record, or equivalent primary dataset. |
| Strong | 0.90 | Multiple independent, current, buyer-fit sources with consistent findings and no unresolved material conflict. |
| Moderate | 0.70 | Independent evidence exists but is indirect, weakly matched by geography/segment, aggregated, or missing one decision-critical baseline element. |
| Weak | 0.40 | Single source, pseudonymous sample, vendor-led evidence, weak buyer fit, or a material unresolved conflict. |
| Assumed | 0.20 | Explicit hypothesis or scenario input supplied for sensitivity analysis, not observed market evidence. |
| Missing | 0.00 | No usable evidence. Performance must be `unknown`. |

Vendor documentation may strongly verify its own feature or price but cannot verify buyer pain, achieved savings, superiority, or willingness to pay. Grade those claims separately.

## Criteria and weights

### Demand — 25 points

| ID | Criterion | Weight | Rating focus |
|---|---|---:|---|
| buyer_pain | Buyer-fit pain | 7 | Direct evidence from the scoped operator, buyer, industry, geography, and organization size. |
| frequency_severity | Frequency and severity | 7 | Measured recurrence and consequences in time, delay, loss, risk, revenue, customer, or compliance terms. |
| workaround_cost | Workaround burden | 5 | Current labor, spreadsheets, services, rework, extra headcount, or process compromise. |
| buying_signal | Buying intent | 6 | Budget, procurement, paid trial, switch, design-partner commitment, or credible willingness to pay. |

### Unmet need — 25 points

| ID | Criterion | Weight | Rating focus |
|---|---|---:|---|
| incumbent_gap | Remaining incumbent gap | 8 | Pain demonstrated after available solutions or substitutes are considered. |
| substitute_adequacy | Substitute inadequacy | 6 | ERP, spreadsheet, service, policy, portal, or process alternatives fail materially. |
| differentiation | Material differentiation | 6 | The idea is measurably better on an outcome the buyer values. |
| switching_access | Access and switching | 5 | Procurement, implementation, price, data, residency, integration, or lock-in create a reachable opening. |

### Net savings and ROI — 30 points

| ID | Criterion | Weight | Rating focus |
|---|---|---:|---|
| baseline_quality | Operating baseline | 5 | Buyer-fit volume, eligibility, handling, rework, quality, and cost inputs. |
| base_roi | Base year-one ROI | 8 | Positive full-cost ROI using measured or strongly sourced inputs. |
| downside_roi | Downside resilience | 6 | Conservative year-one ROI remains positive without optimistic adoption or savings. |
| payback | Payback and hurdle | 4 | Payback clears the buyer's documented threshold. |
| value_realization | Value realization | 4 | Cash savings or an owned, measurable plan for capacity, throughput, risk, or service value. |
| full_cost_sensitivity | Full cost and sensitivity | 3 | Implementation, integration, operation, support, review, exceptions, and reversal sensitivities are included. |

### Feasibility — 20 points

| ID | Criterion | Weight | Rating focus |
|---|---|---:|---|
| data_access | Data access | 4 | Required data is lawful, complete, timely, attributable, and available. |
| integration | Integration route | 4 | Supported read/write, authentication, idempotency, retry, read-back, and reconciliation. |
| accuracy_review | Accuracy and review | 4 | Acceptance thresholds, exceptions, overrides, correction, and human-review load. |
| security_compliance | Security and compliance | 3 | Privacy, authorization, separation, retention, audit, regulatory, and model-risk controls. |
| workflow_adoption | Workflow adoption | 3 | Named owner, authority, incentive, training, operating procedure, and change path. |
| delivery_support | Delivery and support | 2 | Implementation, monitoring, recovery, maintenance, support, and target-scale operation. |

## Rating anchors

| Rating | Meaning |
|---:|---|
| 0 | Suitable evidence directly contradicts the criterion or demonstrates no material value. |
| 1 | Very weak outcome; material blockers or disadvantages dominate. |
| 2 | Limited outcome; some signal exists but gaps or substitutes materially constrain it. |
| 3 | Credible outcome; useful value is supported but important validation remains. |
| 4 | Strong outcome; buyer-fit evidence supports material value with manageable limitations. |
| 5 | Exceptional outcome; representative measurement or repeated results establish the claim. |

Never use 0 merely because evidence is missing. Use `unknown` with verification grade `missing`.

## Evidence coverage and reliability

| Coverage | Reliability | Commitment limit |
|---:|---|---|
| 0–39 | Fragile | Discovery only. |
| 40–59 | Developing | Interviews or measurements; do not pilot. |
| 60–79 | Decision-useful | Bounded test if gates pass. |
| 80–100 | Investment-grade | Pilot or scale decision may be considered subject to gates and red flags. |

A high market score with low coverage is not a strong opportunity. Always display `score / 100` beside `coverage / 100`.

## Ranking ideas

Rank only ideas scored under the same rubric version and comparable scope. Sort by:

1. verified market score;
2. evidence coverage;
3. all mandatory pilot gates passed;
4. downside ROI points;
5. market-test maturity;
6. lower cost and time of the next falsification test.

Show the top criterion driving the rank and the top missing criterion that could change it. Do not rank an assumed scenario above a lower-scoring idea backed by representative buyer evidence without flagging the evidence-grade difference.

## Calibration questions before research

Start every new market test with two or three concise questions. Do not repeat facts already supplied; confirm them and ask the highest-impact missing detail.

1. **Buyer and scope:** Who operates, buys, and approves this workflow; in which industry, geography, and organization-size segment?
2. **Current baseline:** What happens today, approximately how many cases occur, how much time/cost/risk is involved, and what software or workaround is already used?
3. **Candidate and commitment:** What solution is proposed, what outcome should improve, and what price, integration, or pilot constraint matters?

If the operator cannot answer, continue with explicit assumptions, mark affected criteria assumed or missing, and reduce evidence coverage automatically.
