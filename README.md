# A-EYE Validate

A repository skill for evidence-bounded market validation in Codex Cloud.

Validate researches workflow pain, competitors, buyer economics, feasibility, and reusable Notion evidence. It includes deterministic fixture checks for demand/supply counting, evidence freshness, ROI, score ranges, degraded modes, and idempotent Notion retries.

## Use

Invoke with:

```text
Use Validate to research [problem] for [buyer] in [market].
```

## Verify

```bash
python3 .agents/skills/validate/scripts/check_fixture.py
```

The live workflow requires hosted web search and an authorized Notion parent or database for A-EYE Industry Research.
