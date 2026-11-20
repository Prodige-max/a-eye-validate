#!/usr/bin/env python3
"""Deterministic acceptance checks for the Validate synthetic fixture."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import date
from pathlib import Path

from validate_run import validate as validate_run_record


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "acceptance.json"
VALID_RUN = ROOT / "fixtures" / "valid-run.json"
SKILL = ROOT / "SKILL.md"
REPORT_TEMPLATE = ROOT / "references" / "report-template.md"
REQUIRED_REFERENCES = (
    ROOT / "references" / "interview-baseline.md",
    ROOT / "references" / "idea-scorecard.md",
    ROOT / "references" / "notion-setup.md",
    ROOT / "references" / "run-record.schema.json",
    ROOT / "references" / "web-collection.md",
    ROOT / "references" / "web-record.schema.json",
)


def load_fixture() -> dict:
    with FIXTURE.open(encoding="utf-8") as handle:
        return json.load(handle)


def observed_counts(rows: list[dict]) -> dict[str, int]:
    accepted = [row for row in rows if row.get("accessible") and not row.get("duplicate_of")]
    firsthand = [row for row in accepted if row["type"] == "firsthand complaint"]
    people = {row["author"] for row in firsthand if row.get("author")}
    organizations = {row["organization"] for row in firsthand if row.get("organization")}
    unknown_identity = sum(not row.get("author") and not row.get("organization") for row in firsthand)
    offerings = {row["offering"] for row in accepted if row["type"] == "solution"}
    direct = {row["offering"] for row in accepted if row["type"] == "solution" and row["fit"] == "direct"}
    return {"complainants": len(people), "organizations": len(organizations),
            "unknown_identity": unknown_identity, "offerings": len(offerings), "direct_fit": len(direct)}


def stale_feature_ids(data: dict) -> list[str]:
    as_of = date.fromisoformat(data["run"]["as_of"])
    limit = data["run"]["feature_refresh_days"]
    return [row["id"] for row in data["evidence"]
            if row.get("claim_kind") == "product feature"
            and (as_of - date.fromisoformat(row["last_verified"])).days > limit]


def roi(inputs: dict) -> dict[str, float]:
    hours = (inputs["monthly_case_volume"] * 12 * inputs["eligible_share"]
             * inputs["adoption_share"] * inputs["net_minutes_saved"] / 60)
    capacity = hours * inputs["loaded_hourly_cost_zar"]
    recurring = capacity + inputs["independently_verified_annual_savings_zar"] - inputs["annual_running_cost_zar"]
    year_one = recurring - inputs["one_time_implementation_cost_zar"]
    payback = inputs["one_time_implementation_cost_zar"] / (recurring / 12) if recurring > 0 else None
    year_one_cost = inputs["annual_running_cost_zar"] + inputs["one_time_implementation_cost_zar"]
    year_one_roi_percent = year_one / year_one_cost * 100 if year_one_cost > 0 else None
    return {"annual_hours": hours, "capacity_zar": capacity, "recurring_zar": recurring,
            "year_one_zar": year_one, "payback_months": payback,
            "year_one_roi_percent": year_one_roi_percent}


def score_range(scores: dict) -> tuple[float, float]:
    weights = {"demand": 25, "unmet_need": 25, "net_savings": 30, "feasibility": 20}
    lower = sum(scores[key] * weight / 5 for key, weight in weights.items() if scores[key] is not None)
    upper = lower + sum(weight for key, weight in weights.items() if scores[key] is None)
    return lower, upper


def main() -> None:
    data = load_fixture()
    skill_text = SKILL.read_text(encoding="utf-8")
    report_text = REPORT_TEMPLATE.read_text(encoding="utf-8")
    assert skill_text.startswith("---\nname: validate\n")
    for phrase in ("market validation", "workflow gaps", "competitors", "buyer savings", "Notion evidence"):
        assert phrase in skill_text.split("---", 2)[1]
    assert all(path.is_file() for path in REQUIRED_REFERENCES)
    assert "## Capability preflight" in skill_text
    assert "## Independent research requirement" in skill_text
    assert "Every Validate run must perform fresh independent external research" in skill_text
    assert "Independent external research not completed" in skill_text
    assert "scripts/validate_run.py" in skill_text
    assert "references/idea-scorecard.md" in skill_text
    assert "## Portable run record" in report_text
    assert "### Scoring diagnostics" in report_text
    assert "## Supplied-claim verification" in report_text
    assert "**Independent research:** completed | partial" in report_text
    assert observed_counts(data["evidence"]) == {
        "complainants": 2, "organizations": 2, "unknown_identity": 1, "offerings": 2, "direct_fit": 1}
    assert stale_feature_ids(data) == ["E6"]
    assert any(not row.get("accessible") for row in data["evidence"]), "coverage note fixture missing"
    roi_result = roi(data["roi"])
    assert roi_result | {"year_one_roi_percent": 0} == {
        "annual_hours": 600.0, "capacity_zar": 180000.0, "recurring_zar": 120000.0,
        "year_one_zar": 40000.0, "payback_months": 8.0, "year_one_roi_percent": 0}
    assert abs(roi_result["year_one_roi_percent"] - 28.5714285714) < 1e-9
    assert score_range(data["scores"]) == (43.0, 73.0)
    run_record = json.loads(VALID_RUN.read_text(encoding="utf-8"))
    assert validate_run_record(run_record) == []
    wrong_score = deepcopy(run_record)
    wrong_score["score"]["high"] = 72
    assert any("calculated upper bound 73/100" in error for error in validate_run_record(wrong_score))
    premature_pilot = deepcopy(run_record)
    premature_pilot["verdict"] = "pilot"
    assert any("all four pilot gates" in error for error in validate_run_record(premature_pilot))
    hypothetical_roi = deepcopy(run_record)
    hypothetical_roi["dimension_scores"]["net_savings"] = 3
    hypothetical_roi["score"] = {"low": 61, "high": 61}
    assert any("known net_savings requires measured, sourced, or mixed ROI" in error
               for error in validate_run_record(hypothetical_roi))
    degraded = data["degraded"]
    assert degraded["web_search_available"] is False and degraded["unsupported_counts"] == "unknown"
    assert degraded["notion_write_available"] is False and degraded["fallback_complete"] is True
    for section in ("## Decision summary", "## Search log and coverage", "## Observed demand",
                    "## Supply and remaining pain", "## Business case", "## Score",
                    "## Supplied-claim verification", "## Source-level evidence", "## Persistence"):
        assert section in report_text, f"Markdown fallback missing {section}"
    retry = degraded["save_retry"]
    assert retry["original_run_id"] == retry["retry_run_id"]
    assert retry["existing_page_found"] is True and retry["action"] == "update"
    print("PASS skill fixture: demand/supply deduplication and coverage")
    print("PASS freshness: E6 refresh required; E7 current")
    print("PASS ROI: 600 h; R180,000 capacity; R40,000 year one; 28.57%; 8 months")
    print("PASS score: 43-73/100")
    print("PASS score enforcement: arithmetic, ROI evidence and pilot gates")
    print("PASS degraded modes: unknown counts, Markdown fallback, idempotent retry")


if __name__ == "__main__":
    main()
