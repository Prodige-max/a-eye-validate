# Notion setup and persistence contract

Validate can run without Notion, but reuse and idempotent retry require one operator-authorized destination. Never store workspace IDs, database IDs, tokens, or per-run reports in the repository.

## Recommended structure

Create a private page titled **A-EYE Industry Research** with a database titled **Validation Runs**. One database row equals one stable Validate run; the row page contains the full report and source-level evidence table.

Recommended properties:

| Property | Type | Purpose |
|---|---|---|
| Name | Title | Human-readable scope |
| Run ID | Text | Stable idempotency key |
| Status | Select | complete, partial, blocked |
| Validated | Date | Run date |
| Industry, Geography, Buyer, Workflow | Text | Reuse search keys |
| Verdict | Select | pilot, interview first, re-scope, deprioritize |
| Confidence | Select | low, medium, high |
| Score Low, Score High | Number | Known score or uncertainty range |
| Complainants, Affected Orgs, Unknown Identity | Number | Observed demand counts |
| Offerings, Direct Fit | Number | Observed supply counts |
| Reused Evidence, Refreshed Evidence, New Evidence | Number | Evidence lifecycle |
| Top Unknown | Text | Next decision-critical gap |

Fit an existing database instead when it already has equivalent searchable fields. Do not alter an existing schema without operator authorization.

## Destination resolution

1. Use an explicit page/database URL or ID supplied for the session when present.
2. Otherwise search the authorized workspace for the exact title `A-EYE Industry Research`, then locate `Validation Runs` below it.
3. Fetch the database once and use the returned data-source URL and actual property names.
4. If several destinations match, or none can be verified, do not guess. Return the full Markdown report and state the URL/ID or permission required.

## Read and reuse

Search within the resolved destination using normalized industry, geography, buyer, and workflow. Fetch likely matches and verify evidence URLs, dates, and scope before reuse.

- Product features/pricing: refresh after 30 days.
- Other evidence: refresh after 90 days.
- Disputed or decision-critical evidence: refresh regardless of age.

Record every reused item with its original evidence ID/run ID and current run ID. A reused source that is freshly checked counts as refreshed, not both reused and refreshed.

## Idempotent write algorithm

1. Search the destination for the exact stable run ID.
2. If one row exists, fetch and update that row.
3. If no row exists, create one row with structured properties plus the complete report/evidence content.
4. If more than one row exists, stop and report the duplicate IDs; do not create another.
5. If a write result is uncertain, search the exact run ID before retrying.
6. Report success only after a successful response or verified read-back.

Never retry creation with a new run ID. Never widen writes outside the resolved destination.

## Minimum write mapping

At minimum map Name, Run ID, Status, Validated, Industry, Geography, Buyer, Workflow, Verdict, Confidence, Score Low/High, all observed demand/supply counts, evidence lifecycle counts, and Top Unknown. Store narrative, ROI scenarios, search log, coverage notes, and the source-level evidence table in the page body.

## Degraded mode

If read access is missing, research with public/supplied sources and record reuse as skipped. If write access or a destination is missing, return the complete Notion-friendly Markdown report with the stable run ID. State the exact missing capability: destination URL/ID, search/read permission, or create/update permission.
