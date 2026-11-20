#!/usr/bin/env python3
"""Validate the portable invariants of an A-EYE Validate run record."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


RUN_ID = re.compile(r"^AEYE-[0-9]{8}-[a-z0-9-]+-[a-f0-9]{8}$")
COUNT_FIELDS = ("complainants", "affected_organizations", "unknown_identity_items", "offerings", "direct_fit")
VERDICTS = {"pilot", "interview first", "re-scope", "deprioritize"}
EVIDENCE_TYPES = {"firsthand complaint", "workaround", "buying signal", "solution", "benchmark", "secondary commentary"}
SOURCE_RELATIONSHIPS = {"independent", "incumbent/vendor", "operator-supplied", "unknown"}
RESEARCH_GROUPS = {"complaints/workarounds", "products/services", "cost/resource benchmarks",
                   "technical/operational verification"}
DIMENSION_WEIGHTS = {"demand": 25, "unmet_need": 25, "net_savings": 30, "feasibility": 20}
MARKET_TEST_STAGES = {"hypothesis", "public evidence", "buyer discovery", "baseline validated",
                      "controlled pilot", "repeatability proven"}
PILOT_GATES = {"verified_buyer_pain", "incumbent_comparison", "validated_operating_baseline",
               "plausible_integration_route"}
ROI_BASES = {"measured", "sourced", "mixed", "hypothetical", "unknown"}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def is_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate(record: dict) -> list[str]:
    errors: list[str] = []
    required = {"run_id", "status", "validated_on", "scope", "independent_research", "counts", "evidence_lifecycle",
                "dimension_scores", "roi", "score", "confidence", "market_test_stage", "pilot_gates", "verdict",
                "top_unknown", "next_step", "evidence"}
    require(required <= record.keys(), f"missing top-level fields: {sorted(required - record.keys())}", errors)
    if errors:
        return errors

    require(bool(RUN_ID.fullmatch(str(record["run_id"]))), "run_id does not match the stable AEYE format", errors)
    require(record["status"] in {"complete", "partial", "blocked"}, "invalid status", errors)
    try:
        date.fromisoformat(record["validated_on"])
    except (TypeError, ValueError):
        errors.append("validated_on must be an ISO date")

    scope = record["scope"]
    for field in ("industry", "geography", "buyer", "workflow", "currency"):
        require(isinstance(scope.get(field), str) and bool(scope[field].strip()), f"scope.{field} is required", errors)

    research = record["independent_research"]
    require(isinstance(research.get("completed"), bool), "independent_research.completed must be boolean", errors)
    groups = research.get("groups_attempted")
    require(isinstance(groups, list) and bool(groups), "independent_research.groups_attempted is required", errors)
    if isinstance(groups, list):
        require(set(groups) <= RESEARCH_GROUPS, "independent_research.groups_attempted contains an invalid group", errors)
    try:
        date.fromisoformat(research.get("fresh_search_date", ""))
    except (TypeError, ValueError):
        errors.append("independent_research.fresh_search_date must be an ISO date")
    if record["status"] == "complete":
        require(research.get("completed") is True,
                "complete runs require completed independent external research", errors)

    counts = record["counts"]
    for field in COUNT_FIELDS:
        value = counts.get(field)
        require(value is None or (isinstance(value, int) and not isinstance(value, bool) and value >= 0),
                f"counts.{field} must be a non-negative integer or null", errors)
    if counts.get("offerings") is not None and counts.get("direct_fit") is not None:
        require(counts["direct_fit"] <= counts["offerings"], "direct_fit cannot exceed offerings", errors)
    if record["status"] == "complete":
        require(all(counts.get(field) is not None for field in COUNT_FIELDS),
                "complete runs cannot have unknown observed counts", errors)

    lifecycle = record["evidence_lifecycle"]
    for field in ("reused", "refreshed", "new"):
        value = lifecycle.get(field)
        require(isinstance(value, int) and not isinstance(value, bool) and value >= 0,
                f"evidence_lifecycle.{field} must be a non-negative integer", errors)

    dimensions = record["dimension_scores"]
    require(isinstance(dimensions, dict), "dimension_scores must be an object", errors)
    if isinstance(dimensions, dict):
        require(set(dimensions) == set(DIMENSION_WEIGHTS),
                "dimension_scores must contain exactly demand, unmet_need, net_savings and feasibility", errors)
        for field in DIMENSION_WEIGHTS:
            value = dimensions.get(field)
            require(value is None or (isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 5),
                    f"dimension_scores.{field} must be an integer 0..5 or null", errors)

    roi = record["roi"]
    require(isinstance(roi, dict), "roi must be an object", errors)
    roi_fields = {"basis", "low_percent", "base_percent", "high_percent", "base_payback_months", "cash_realization"}
    if isinstance(roi, dict):
        require(set(roi) == roi_fields, "roi contains missing or unexpected fields", errors)
        require(roi.get("basis") in ROI_BASES, "roi.basis is invalid", errors)
        for field in ("low_percent", "base_percent", "high_percent"):
            value = roi.get(field)
            require(value is None or (isinstance(value, (int, float)) and not isinstance(value, bool)),
                    f"roi.{field} must be a number or null", errors)
        payback = roi.get("base_payback_months")
        require(payback is None or (isinstance(payback, (int, float)) and not isinstance(payback, bool) and payback >= 0),
                "roi.base_payback_months must be a non-negative number or null", errors)
        require(roi.get("cash_realization") is None or isinstance(roi.get("cash_realization"), bool),
                "roi.cash_realization must be boolean or null", errors)
        if isinstance(dimensions, dict) and dimensions.get("net_savings") is not None:
            require(roi.get("basis") not in {"hypothetical", "unknown"},
                    "known net_savings requires measured, sourced, or mixed ROI", errors)
            require(isinstance(roi.get("base_percent"), (int, float)) and not isinstance(roi.get("base_percent"), bool),
                    "known net_savings requires numeric roi.base_percent", errors)
        if isinstance(dimensions, dict) and isinstance(dimensions.get("net_savings"), int) and dimensions["net_savings"] >= 4:
            require(isinstance(roi.get("low_percent"), (int, float)) and roi["low_percent"] > 0,
                    "net_savings 4 or 5 requires positive downside ROI", errors)
            require(payback is not None, "net_savings 4 or 5 requires base payback", errors)

    score = record["score"]
    low, high = score.get("low"), score.get("high")
    require(isinstance(low, (int, float)) and not isinstance(low, bool) and 0 <= low <= 100, "score.low must be 0..100", errors)
    require(isinstance(high, (int, float)) and not isinstance(high, bool) and 0 <= high <= 100, "score.high must be 0..100", errors)
    if isinstance(low, (int, float)) and isinstance(high, (int, float)):
        require(low <= high, "score.low cannot exceed score.high", errors)
    if isinstance(dimensions, dict) and set(dimensions) == set(DIMENSION_WEIGHTS):
        values_are_valid = all(
            value is None or (isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= 5)
            for value in dimensions.values()
        )
        if values_are_valid:
            expected_low = sum(
                dimensions[field] * weight / 5
                for field, weight in DIMENSION_WEIGHTS.items()
                if dimensions[field] is not None
            )
            expected_high = expected_low + sum(
                weight for field, weight in DIMENSION_WEIGHTS.items() if dimensions[field] is None
            )
            require(low == expected_low, f"score.low must equal calculated lower bound {expected_low:g}/100", errors)
            require(high == expected_high, f"score.high must equal calculated upper bound {expected_high:g}/100", errors)

    require(record["confidence"] in {"low", "medium", "high"}, "invalid confidence", errors)
    require(record["market_test_stage"] in MARKET_TEST_STAGES, "invalid market_test_stage", errors)
    gates = record["pilot_gates"]
    require(isinstance(gates, dict), "pilot_gates must be an object", errors)
    if isinstance(gates, dict):
        require(set(gates) == PILOT_GATES, "pilot_gates contains missing or unexpected gates", errors)
        for gate in PILOT_GATES:
            require(isinstance(gates.get(gate), bool), f"pilot_gates.{gate} must be boolean", errors)
    require(record["verdict"] in VERDICTS, "invalid verdict", errors)
    if record["verdict"] == "pilot":
        require(isinstance(gates, dict) and set(gates) == PILOT_GATES and all(gates.values()),
                "pilot verdict requires all four pilot gates", errors)
        require(record["confidence"] != "low", "pilot verdict requires medium or high confidence", errors)
    require(bool(str(record["top_unknown"]).strip()), "top_unknown is required", errors)
    require(bool(str(record["next_step"]).strip()), "next_step is required", errors)

    evidence_ids: set[str] = set()
    for index, item in enumerate(record["evidence"]):
        prefix = f"evidence[{index}]"
        evidence_id = item.get("id")
        require(isinstance(evidence_id, str) and bool(re.fullmatch(r"E[0-9]{2,}", evidence_id)), f"{prefix}.id is invalid", errors)
        require(evidence_id not in evidence_ids, f"duplicate evidence id: {evidence_id}", errors)
        evidence_ids.add(evidence_id)
        require(is_url(item.get("url")), f"{prefix}.url must be http(s)", errors)
        require(item.get("type") in EVIDENCE_TYPES, f"{prefix}.type is invalid", errors)
        require(item.get("relationship") in SOURCE_RELATIONSHIPS, f"{prefix}.relationship is invalid", errors)
        require(item.get("lifecycle") in {"reused", "refreshed", "new"}, f"{prefix}.lifecycle is invalid", errors)
        try:
            date.fromisoformat(item.get("last_verified", ""))
        except (TypeError, ValueError):
            errors.append(f"{prefix}.last_verified must be an ISO date")

    notion_url, save_error = record.get("notion_page_url"), record.get("save_error")
    require(not notion_url or is_url(notion_url), "notion_page_url must be null or http(s)", errors)
    require(bool(notion_url) != bool(save_error), "provide exactly one of notion_page_url or save_error", errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    errors = validate(record)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"PASS run record: {record['run_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
