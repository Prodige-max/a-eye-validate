#!/usr/bin/env python3
"""Deterministic, offline checks for the bounded web collector."""

from __future__ import annotations

import importlib.util
import ipaddress
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "collect_web.py"
FIXTURE = ROOT / "fixtures" / "web-page.html"


def load_module():
    spec = importlib.util.spec_from_file_location("collect_web", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def main() -> None:
    module = load_module()
    normalized = module.normalize_url("HTTPS://Example.ORG/research?a=1&utm_source=x#frag")
    assert normalized == "https://example.org/research?a=1"

    parser = module.PageParser("https://example.org/start")
    parser.feed(FIXTURE.read_text(encoding="utf-8"))
    assert parser.title == "Credit review workflow"
    assert parser.meta["description"] == "A fixture about manual credit review."
    assert parser.meta["author"] == "Fixture Analyst"
    assert parser.meta["article:published_time"] == "2026-10-01"
    assert parser.canonical == "https://example.org/research/credit-review"
    assert parser.language == "en-ZA"
    assert "Manual review remains slow" in parser.text
    assert "embedded instruction" not in parser.text
    assert parser.links == ["https://example.org/research/next"]

    assert not ipaddress.ip_address("127.0.0.1").is_global
    try:
        module.assert_public_url("http://127.0.0.1/private")
    except ValueError as exc:
        assert "non-public" in str(exc)
    else:
        raise AssertionError("private destination was not rejected")

    try:
        module.normalize_url("file:///etc/passwd")
    except ValueError:
        pass
    else:
        raise AssertionError("non-HTTP URL was not rejected")

    print("PASS collector: URL normalization and tracking removal")
    print("PASS collector: HTML metadata, visible text, canonical URL and links")
    print("PASS collector safety: scripts ignored; private and non-HTTP destinations rejected")


if __name__ == "__main__":
    main()
