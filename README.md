# A-EYE Validate

A-EYE Validate is an instruction-led Codex skill for evidence-bounded market validation. It researches workflow pain, observed demand, competitors, buyer economics, implementation feasibility, and reusable evidence in an authorized Notion destination.

## Install and invoke

Keep the skill at `.agents/skills/validate/SKILL.md` in the repository loaded by Codex Cloud. Invoke it with:

```text
Use Validate to research [problem] for [buyer] in [market].
```

In clients with skill mentions, select `$validate`.

The skill uses the session's hosted web search and, when authorized, its Notion connection. It requires no Windows host, Docker daemon, crawler subscription, job worker, or separate model API.

## Bounded web collector

Validate includes a robots-aware collector that converts approved public seed pages and bounded same-host links into auditable JSONL. Hosted search remains responsible for broad discovery; the collector does not bypass access controls or turn page counts into market evidence automatically.

```bash
python3 .agents/skills/validate/scripts/collect_web.py \
  --seed-file /tmp/validate-seeds.txt \
  --output /tmp/validate-corpus.jsonl
```

The default limit is 40 pages at depth one, with a per-host delay and response-size cap. Private network targets and unsafe redirects are rejected. See [web-collection.md](.agents/skills/validate/references/web-collection.md) for operating rules. Keep real corpora outside the repository.

## Notion setup

Authorize a Notion connection with search, read, and page-creation access. Supply an editable parent or database, preferably named **A-EYE Industry Research**. The recommended database fields and the idempotent save procedure are in [notion-setup.md](.agents/skills/validate/references/notion-setup.md).

Never commit credentials, workspace-specific Notion IDs, or real per-run research data. If Notion is unavailable, Validate returns a complete Markdown fallback carrying the same stable run ID.

## Buyer baseline

Public research can establish a market signal, but it cannot manufacture a buyer's operating baseline. Use [interview-baseline.md](.agents/skills/validate/references/interview-baseline.md) to measure current case volumes, handling time, referral and rework rates, losses, costs, approvals, and integration constraints before a pilot verdict.

## Checks

Python 3.10 or later is sufficient; the checks use only the standard library.

```bash
python3 .agents/skills/validate/scripts/check_fixture.py
python3 .agents/skills/validate/scripts/check_collector.py
python3 .agents/skills/validate/scripts/validate_run.py .agents/skills/validate/fixtures/valid-run.json
```

The deterministic fixtures verify deduplication, supply classification, freshness, ROI arithmetic, score ranges, degraded modes, idempotent retry behavior, HTML normalization, and collector network boundaries. `validate_run.py` checks portable run records before persistence.

## Deployment checklist

- Load the repository in a Codex Cloud task and confirm `Use Validate` resolves the skill.
- Confirm hosted web search is available, or expect partial mode with unsupported counts left unknown.
- Authorize the intended Notion destination and confirm search, read, create, and update access.
- Run both fixture checks locally or in GitHub Actions.
- Perform a live run, verify its Notion page, then repeat the same segment to confirm evidence reuse and stable retry behavior.

## Upstream reference

The staged competitor-research concept and interview gate were adapted at a high level from Ferdinando Bons's MIT-licensed [Startup Skill](https://github.com/ferdinandobons/startup-skill). See the attribution in `SKILL.md`; this repository does not copy substantial upstream text.
