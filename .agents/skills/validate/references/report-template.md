# Validate report template

Use Markdown that pastes cleanly into Notion. Do not omit sections; use `unknown` and explain why.

```markdown
# A-EYE Validate — <problem> for <buyer>

**Run ID:** <stable ID>  
**Status:** complete | partial  
**Validated on:** <ISO date>  
**Scope:** <industry> · <geography> · <buyer> · <workflow>  
**Evidence window:** <start> to <end>; older background labeled  
**Candidate solution:** <supplied description or not supplied>  
**Currency:** <currency>
**Independent research:** completed | partial — <fresh searches and limiting capability>

## Calibration questions

| Question | Operator answer | Assumption if unanswered | Criteria affected |
|---|---|---|---|
| <buyer/scope question> | ... | ... | ... |
| <workflow/baseline question> | ... | ... | ... |
| <candidate/commitment question, when material> | ... | ... | ... |

## Decision summary

- Observed sample: <complainants or unknown> identifiable firsthand complainants; <organizations or unknown> identifiable affected organizations; <unknown-identity items or unknown> relevant unknown-identity firsthand items
- Supply sample: <offerings or unknown> verified offerings; <direct or unknown> direct fit
- Evidence lifecycle: <reused> reused; <refreshed> refreshed; <new> new
- Verified Market Score: <N/100>
- Evidence Coverage: <N/100 — fragile/developing/decision-useful/investment-grade>
- Confidence: <low/medium/high> — <limiting factors>
- Market-test stage: <hypothesis/public evidence/buyer discovery/baseline validated/controlled pilot/repeatability proven>
- Verdict: <pilot/interview first/re-scope/deprioritize>
- Top unknown: <one decision-critical unknown>
- Next step: <one bounded action>

## Scope and assumptions

<definitions, inclusions, exclusions, assumptions, and default date-window disclosure>

## Supplied-claim verification

| Supplied claim | Supplied source | Independent source IDs | Result | Notes |
|---|---|---|---|---|
| ... | ... | ... | corroborated/contradicted/unverified | ... |

## Prior evidence and freshness

<Notion destination searched, matched runs, freshness decisions, or exact reason reuse was skipped>

## Search log and coverage

| Group | Query | Date window | URLs inspected | Accepted | Notes/gaps |
|---|---|---|---:|---:|---|
| Complaints/workarounds | ... | ... | ... | ... | ... |
| Products/services | ... | ... | ... | ... | ... |
| Cost/resource benchmarks | ... | ... | ... | ... | ... |

Inaccessible/rejected sources: <URL, reason, date>.  
Coverage gaps: <buyer/geography/workflow/source gap>.

## Observed demand

<Counts, deduplication notes, dates and links. Keep complaints, workarounds, and buying signals distinct. Explicitly say this is an inspected-search sample, not population demand.>

## Supply and remaining pain

| Offering | Fit | Target buyer | Workflow coverage | Constraints / remaining pain | Evidence IDs |
|---|---|---|---|---|---|
| ... | direct/partial/workaround/custom/unknown | ... | ... | ... | ... |

## Business case

| Input | Low | Base | High | Unit/currency | Status | Evidence ID / assumption |
|---|---:|---:|---:|---|---|---|
| Monthly case volume | ... | ... | ... | cases/month | measured/sourced/assumed | ... |
| Eligible share | ... | ... | ... | % | ... | ... |
| Adoption share | ... | ... | ... | % | ... | ... |
| Net minutes saved | ... | ... | ... | minutes/handled case | ... | net of review/exceptions/rework |
| Loaded staffing cost | ... | ... | ... | currency/hour | ... | ... |
| Independently verified savings | ... | ... | ... | currency/year | ... | ... |
| Annual running costs | ... | ... | ... | currency/year | ... | ... |
| One-time implementation | ... | ... | ... | currency | ... | ... |

| Output | Low | Base | High |
|---|---:|---:|---:|
| Annual hours recovered | ... | ... | ... |
| Annual capacity value | ... | ... | ... |
| Annual recurring net economic value | ... | ... | ... |
| Year-one net economic value | ... | ... | ... |
| Economic payback | ... | ... | ... |
| Year-one economic ROI | ...% | ...% | ...% |
| Year-one cash ROI | unknown/...% | unknown/...% | unknown/...% |

Cash savings: <separate supported amount or unknown>.  
ROI basis: <measured/sourced/mixed/hypothetical/unknown>; buyer hurdle: <documented threshold or unknown>.  
Major sensitivities: <inputs>.  
Buyer data needed: <measurements needed to validate assumptions>.

## Verified score

| Criterion | Dimension | Weight | Rating | Verification | Factor | Verified points | Evidence IDs | Rationale |
|---|---|---:|---:|---|---:|---:|---|---|
| Buyer-fit pain | Demand | 7 | .../unknown | verified/strong/moderate/weak/assumed/missing | ... | ... | ... | ... |
| Frequency and severity | Demand | 7 | .../unknown | ... | ... | ... | ... | ... |
| Workaround burden | Demand | 5 | .../unknown | ... | ... | ... | ... | ... |
| Buying intent | Demand | 6 | .../unknown | ... | ... | ... | ... | ... |
| Remaining incumbent gap | Unmet need | 8 | .../unknown | ... | ... | ... | ... | ... |
| Substitute inadequacy | Unmet need | 6 | .../unknown | ... | ... | ... | ... | ... |
| Material differentiation | Unmet need | 6 | .../unknown | ... | ... | ... | ... | ... |
| Access and switching | Unmet need | 5 | .../unknown | ... | ... | ... | ... | ... |
| Operating baseline | Net savings | 5 | .../unknown | ... | ... | ... | ... | ... |
| Base year-one ROI | Net savings | 8 | .../unknown | ... | ... | ... | ... | ... |
| Downside resilience | Net savings | 6 | .../unknown | ... | ... | ... | ... | ... |
| Payback and hurdle | Net savings | 4 | .../unknown | ... | ... | ... | ... | ... |
| Value realization | Net savings | 4 | .../unknown | ... | ... | ... | ... | ... |
| Full cost and sensitivity | Net savings | 3 | .../unknown | ... | ... | ... | ... | ... |
| Data access | Feasibility | 4 | .../unknown | ... | ... | ... | ... | ... |
| Integration route | Feasibility | 4 | .../unknown | ... | ... | ... | ... | ... |
| Accuracy and review | Feasibility | 4 | .../unknown | ... | ... | ... | ... | ... |
| Security and compliance | Feasibility | 3 | .../unknown | ... | ... | ... | ... | ... |
| Workflow adoption | Feasibility | 3 | .../unknown | ... | ... | ... | ... | ... |
| Delivery and support | Feasibility | 2 | .../unknown | ... | ... | ... | ... | ... |

| Dimension | Weight | Verified points | Summary anchor | Key limitation |
|---|---:|---:|---:|---|
| Demand | 25 | ... | .../5 or unknown | ... |
| Unmet need | 25 | ... | .../5 or unknown | ... |
| Net savings (includes ROI) | 30 | ... | .../5 or unknown | ... |
| Feasibility | 20 | ... | .../5 or unknown | ... |

**Verified Market Score:** <N>/100  
**Evidence Coverage:** <N>/100 — <reliability and commitment limit>  
**Confidence:** <rating and rationale>  
**Pilot gates:** pain <yes/no>; incumbent comparison <yes/no>; validated baseline <yes/no>; integration route <yes/no>.

### Scoring diagnostics

| Dimension | Confirmed criteria | Missing or conflicting criteria | Red flags |
|---|---|---|---|
| Demand | buyer fit, firsthand pattern, frequency, severity, workarounds, buying signal, baseline quality | ... | ... |
| Unmet need | direct coverage, incumbent outcome, substitutes, gap materiality, access/switching, differentiation, defensibility | ... | ... |
| Net savings | baseline, gross value, full cost, downside, realization, low/base/high ROI, ROI basis, buyer hurdle, payback, sensitivity | ... | ... |
| Feasibility | data, integration, accuracy/exceptions, security/compliance, adoption, delivery, approval route | ... | ... |

**Market-test stage:** <stage and why the next stage is not yet complete>.  
**Override:** <none, or the red-flag fact that limits commitment>.  
**Next experiment:** <falsifiable hypothesis; sample/owner; required evidence; pass/fail/stop thresholds; time/cost boundary; resulting decision>.

## Source-level evidence

| Evidence ID | Canonical URL | Title | Published | Last verified | Source type | Relationship | Evidence type | Claim/excerpt | Observable author | Observable organization | Industry | Buyer | Geography | Workflow | Run ID | Lifecycle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | unknown if unavailable | ... | ... | independent/incumbent-vendor/operator-supplied/unknown | firsthand complaint/workaround/solution/benchmark/secondary commentary | concise paraphrase | unknown if unavailable | unknown if unavailable | ... | ... | ... | ... | ... | reused/refreshed/new |

## Persistence

Notion page: <verified URL, or exact error and destination/permission required>.
```

## Portable run record

For automation or deferred persistence, also produce a JSON record matching `run-record.schema.json`. Validate it with `scripts/validate_run.py` when the repository runtime is available. Keep real run records out of version control unless the operator explicitly asks to add a sanitized fixture.

## Synthetic acceptance fixture

The machine-readable fixture is `fixtures/acceptance.json`; `scripts/check_fixture.py` verifies it. It contains two identifiable firsthand complainants at two companies; one repeat post; one relevant unknown-identity item; one syndicated secondary article; one direct and one partial competitor; a product-feature claim 31 days old; and one inaccessible source retained only as a coverage gap.

Expected results: 2 distinct complainants, 2 affected identifiable organizations, 1 unknown-identity firsthand item, 2 verified offerings, 1 direct fit, and the 31-day feature claim marked for refresh.

The fixture's base ROI inputs are 10,000 cases/month, 20% eligible, 50% adoption, 3 net minutes saved, R300/hour, R60,000/year running cost, and R80,000 one-time cost. Expected outputs are 600 hours/year, R180,000 annual capacity value, R120,000 annual recurring net economic value, R40,000 year-one net economic value, 28.57% year-one economic ROI, and 8 months economic payback. If all criteria within the four dimensions are respectively rated 4, 3, unknown, and 2 with verified evidence for every known rating, the result is 43/100 with 70/100 evidence coverage.

Degraded expectations: unavailable web search makes unsupported counts `unknown`; unavailable Notion write yields a complete Markdown fallback; retrying an uncertain save preserves the original run ID and updates the page found by that ID.
