# Validate scoring rubric

Score only from evidence in the run. Cite evidence IDs in every rationale. These dimension anchors provide interpretable summaries; the exact score is calculated from the 20 weighted criteria and verification factors in `verification-scorecard.md`. A dimension is `unknown` when its outcome cannot be supported. Missing evidence earns no verified points but is not evidence of a zero outcome.

## Demand — 25 points

| Score | Anchor |
|---:|---|
| 0 | Credible, buyer-fit evidence shows the problem does not occur or is negligible in the scoped workflow. |
| 1 | Anecdotal or weakly matched pain; no repeat pattern or material workaround cost established. |
| 2 | More than one relevant signal, but identity, frequency, consequence, or buyer fit remains weak. |
| 3 | Multiple independent firsthand signals from the scoped buyer/market, with recurring workarounds or meaningful consequences. |
| 4 | Strong, recent firsthand pattern across identifiable buyers/organizations with frequency or cost supported by buyer-fit evidence. |
| 5 | Score 4 plus a validated operating baseline from the target buyer or equivalent measured dataset demonstrating material repeated pain. |

## Unmet need — 25 points

| Score | Anchor |
|---:|---|
| 0 | Current exact-fit offerings demonstrably resolve the scoped workflow for this buyer with no material remaining gap. |
| 1 | Mature direct solutions cover nearly all of the workflow; remaining pain is marginal or switching-led. |
| 2 | Direct solutions exist and cover core stages, but documented constraints leave a limited gap. |
| 3 | Solutions are partial, fragmented, service-heavy, or poorly matched; independent evidence shows pain persists. |
| 4 | No verified direct fit in the inspected sample and multiple sources support a consequential workflow gap. |
| 5 | Score 4 plus target-buyer verification that incumbents/substitutes were tried or evaluated and failed on the exact gap. |

## Net savings — 30 points

| Score | Anchor |
|---:|---|
| 0 | Measured or well-sourced base and downside year-one ROI are non-positive after implementation and running costs. |
| 1 | Positive ROI appears only in the high case, requires aggressive assumptions, excludes material costs, or has no credible realization path. |
| 2 | Base recurring value is positive, but base year-one ROI or downside ROI is non-positive, payback misses the buyer hurdle, or decision-critical inputs are weak. |
| 3 | Base year-one ROI is positive after full costs, payback is plausible, sensitivities are explicit, and the partly validated baseline has no obvious double count. |
| 4 | Base and conservative downside year-one ROI are positive using buyer-fit baseline data and credible full costs; base ROI and payback clear the buyer's documented hurdle. |
| 5 | Score 4 plus measured pilot or close-analogue performance and buyer-validated cash realization or an owned, measurable capacity-conversion plan. |

Use `year_one_roi_percent = year_one_net_economic_value / (annual_running_costs + one_time_implementation_costs) * 100`. If the buyer has no documented hurdle, report that gap rather than inventing one. Capacity-led ROI is economic ROI, not cash ROI. A hypothetical or unknown ROI basis makes Net Savings `unknown`, not 0.

## Feasibility — 20 points

| Score | Anchor |
|---:|---|
| 0 | Evidence shows a blocking legal, data, integration, approval, or safety constraint with no plausible mitigation. |
| 1 | Critical access/integration/approval assumptions are unresolved and likely difficult. |
| 2 | A plausible route exists, but one or more critical dependencies or human-review burdens remain untested. |
| 3 | Data access, integration, approvals, exceptions, and human review have credible paths; material tests remain. |
| 4 | Target environment and stakeholders validate the route, with manageable controls and known exception handling. |
| 5 | Score 4 plus successful representative technical/operational trial and owner-approved deployment path. |

## Calculation

Weights: demand 25, unmet need 25, net savings 30, feasibility 20. Use the criterion weights within those dimensions from `verification-scorecard.md`.

```text
criterion points = criterion weight * criterion rating / 5 * verification factor
verified market score = sum(criterion points)
evidence coverage = sum(criterion weight * verification factor)
```

Example: if every Demand criterion is rated 4 and verified, every Unmet Need criterion is rated 3 and verified, every Net Savings criterion is missing, and every Feasibility criterion is rated 2 and verified, the result is **43/100** with **70/100 evidence coverage**. The missing ROI is visible in coverage and criterion status; it does not create a speculative 30-point upper bound.

## Evidence confidence

Confidence is not the score.

- **High:** material claims are supported by several independent sources; evidence is recent enough for the claim; buyer, geography, and workflow closely match; and the operating/economic baseline is measured or strongly sourced. Conflicts are resolved.
- **Medium:** useful independent evidence exists, but one of independence, recency, buyer fit, or baseline quality has a material limitation. No unsupported claim is decision-critical.
- **Low:** evidence is sparse, vendor-led, stale, weakly matched, dependent on hypothetical baselines, or contains unresolved decision-critical conflict.

State which of source independence, recency, buyer fit, and baseline quality limits the rating.

## Verdict rules

The score informs but does not mechanically select the verdict.

- **Pilot:** verified buyer pain, an explicit incumbent comparison, a validated operating baseline, and a plausible integration/approval route are all present. Economics must be plausibly positive after full costs. A high score cannot substitute for a failed gate or weak evidence coverage.
- **Interview first:** evidence suggests meaningful pain or attractive hypothetical economics, but buyer validation, baseline, buying process, or a critical assumption is missing. Specify the single interview/measurement that can change the decision.
- **Re-scope:** pain exists, but the buyer, workflow boundary, geography, solution shape, economics, or integration route needs narrowing or alteration. Name the proposed scope.
- **Deprioritize:** buyer-fit evidence supports low demand, low remaining need, negative economics, or an unmitigable feasibility block. Unknown is not evidence for deprioritization.

When evidence supports more than one verdict, choose the safer next commitment and explain the gating fact.
