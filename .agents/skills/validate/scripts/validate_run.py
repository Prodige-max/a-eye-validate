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
    required = {"run_id", "status", "validated_on", "scope", "counts", "evidence_lifecycle",
                "score", "confidence", "verdict", "top_unknown", "next_step", "evidence"}
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

    score = record["score"]
    low, high = score.get("low"), score.get("high")
    require(isinstance(low, (int, float)) and not isinstance(low, bool) and 0 <= low <= 100, "score.low must be 0..100", errors)
    require(isinstance(high, (int, float)) and not isinstance(high, bool) and 0 <= high <= 100, "score.high must be 0..100", errors)
    if isinstance(low, (int, float)) and isinstance(high, (int, float)):
        require(low <= high, "score.low cannot exceed score.high", errors)

    require(record["confidence"] in {"low", "medium", "high"}, "invalid confidence", errors)
    require(record["verdict"] in VERDICTS, "invalid verdict", errors)
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
