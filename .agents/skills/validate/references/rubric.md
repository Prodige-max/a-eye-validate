# Validate scoring rubric

Score only from evidence in the run. Cite evidence IDs in every rationale. Each known dimension receives an integer from 0 to 5. A dimension is `unknown` when the evidence cannot distinguish its anchor; unknown contributes 0 at the total's lower endpoint and the full dimension weight at its upper endpoint.

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
| 0 | Measured/sourced downside and base cases are non-positive after implementation and running costs. |
| 1 | Positive value requires aggressive assumptions, excludes material costs, or has very poor downside. |
| 2 | Base case is positive but downside is non-positive or key baseline/cost inputs are weak. |
| 3 | Base case is positive after full costs, with plausible sensitivities and no obvious double count; baseline is partly validated. |
| 4 | Base and conservative downside are positive using buyer-fit baseline data and credible full costs; payback is acceptable to the buyer. |
| 5 | Score 4 plus buyer-validated cash realization or capacity conversion and measured pilot/analogue performance. |

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

Weights: demand 25, unmet need 25, net savings 30, feasibility 20.

```text
known dimension points = integer score * weight / 5
lower total = sum(known points) + 0 for every unknown
upper total = sum(known points) + full weight for every unknown
```

Example: demand 4 = 20, unmet need 3 = 15, net savings unknown = 0–30, feasibility 2 = 8, so total = **43–73/100**.

## Evidence confidence

Confidence is not the score.

- **High:** material claims are supported by several independent sources; evidence is recent enough for the claim; buyer, geography, and workflow closely match; and the operating/economic baseline is measured or strongly sourced. Conflicts are resolved.
- **Medium:** useful independent evidence exists, but one of independence, recency, buyer fit, or baseline quality has a material limitation. No unsupported claim is decision-critical.
- **Low:** evidence is sparse, vendor-led, stale, weakly matched, dependent on hypothetical baselines, or contains unresolved decision-critical conflict.

State which of source independence, recency, buyer fit, and baseline quality limits the rating.

## Verdict rules

The score informs but does not mechanically select the verdict.

- **Pilot:** verified buyer pain, an explicit incumbent comparison, a validated operating baseline, and a plausible integration/approval route are all present. Economics must be plausibly positive after full costs. A score range crossing material uncertainty is not enough by itself.
- **Interview first:** evidence suggests meaningful pain or attractive hypothetical economics, but buyer validation, baseline, buying process, or a critical assumption is missing. Specify the single interview/measurement that can change the decision.
- **Re-scope:** pain exists, but the buyer, workflow boundary, geography, solution shape, economics, or integration route needs narrowing or alteration. Name the proposed scope.
- **Deprioritize:** buyer-fit evidence supports low demand, low remaining need, negative economics, or an unmitigable feasibility block. Unknown is not evidence for deprioritization.

When evidence supports more than one verdict, choose the safer next commitment and explain the gating fact.
