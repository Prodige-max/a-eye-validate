#!/usr/bin/env python3
"""Bounded, robots-aware public web collector for A-EYE Validate."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import ipaddress
import json
import re
import socket
import sys
import time
from collections import deque
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib import robotparser
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


SCHEMA_VERSION = "1.0"
USER_AGENT = "A-EYE-Validate-Collector/1.0 (+https://github.com/Prodige-max/a-eye-validate)"
TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "ref_src"}
ALLOWED_TYPES = ("text/html", "application/xhtml+xml", "application/json", "text/plain")
SKIP_TAGS = {"script", "style", "noscript", "svg", "template"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_url(value: str, base: str | None = None) -> str:
    joined = urljoin(base, value.strip()) if base else value.strip()
    parts = urlsplit(joined)
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError("only absolute public HTTP(S) URLs are supported")
    host = parts.hostname.encode("idna").decode("ascii").lower()
    port = parts.port
    netloc = f"[{host}]" if ":" in host else host
    if port and not ((parts.scheme.lower() == "http" and port == 80) or (parts.scheme.lower() == "https" and port == 443)):
        netloc = f"{host}:{port}"
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in TRACKING_KEYS]
    path = parts.path or "/"
    return urlunsplit((parts.scheme.lower(), netloc, path, urlencode(query, doseq=True), ""))


def assert_public_url(url: str) -> None:
    parts = urlsplit(url)
    host = parts.hostname
    if not host:
        raise ValueError("URL has no host")
    try:
        addresses = [ipaddress.ip_address(host)]
    except ValueError:
        try:
            addresses = {ipaddress.ip_address(item[4][0]) for item in socket.getaddrinfo(host, parts.port or 443)}
        except (socket.gaierror, ValueError) as exc:
            raise ValueError(f"host resolution failed: {exc}") from exc
    if not addresses or any(not address.is_global for address in addresses):
        raise ValueError("non-public network destination rejected")


class SafeRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        normalized = normalize_url(newurl, req.full_url)
        assert_public_url(normalized)
        return super().redirect_request(req, fp, code, msg, headers, normalized)


class PageParser(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.skip_depth = 0
        self.in_title = False
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.links: list[str] = []
        self.canonical: str | None = None
        self.language: str | None = None
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        data = {key.lower(): value for key, value in attrs if value is not None}
        if tag == "html" and data.get("lang"):
            self.language = data["lang"].strip()
        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            key = (data.get("name") or data.get("property") or "").lower()
            if key and data.get("content"):
                self.meta[key] = data["content"].strip()
        if tag == "link" and "canonical" in (data.get("rel") or "").lower() and data.get("href"):
            try:
                self.canonical = normalize_url(data["href"], self.base_url)
            except ValueError:
                pass
        if tag == "a" and data.get("href"):
            try:
                url = normalize_url(data["href"], self.base_url)
            except (ValueError, UnicodeError):
                return
            if url not in self.links:
                self.links.append(url)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        cleaned = re.sub(r"\s+", " ", data).strip()
        if not cleaned:
            return
        if self.in_title:
            self.title_parts.append(cleaned)
        else:
            self.text_parts.append(cleaned)

    @property
    def title(self) -> str | None:
        return " ".join(self.title_parts) or None

    @property
    def text(self) -> str:
        return "\n".join(self.text_parts)


def decode_body(raw: bytes, content_encoding: str | None, charset: str | None,
                max_bytes: int) -> str:
    if content_encoding and "gzip" in content_encoding.lower():
        raw = gzip.decompress(raw)
    if len(raw) > max_bytes:
        raise ValueError(f"decoded response exceeds {max_bytes} byte limit")
    return raw.decode(charset or "utf-8", errors="replace")


class Collector:
    def __init__(self, seeds: list[str], max_pages: int, max_depth: int, delay: float,
                 timeout: float, max_bytes: int):
        self.seeds = [normalize_url(url) for url in seeds]
        self.allowed_hosts = {urlsplit(url).hostname for url in self.seeds}
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.delay = delay
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.opener = build_opener(SafeRedirectHandler())
        self.last_request: dict[str, float] = {}
        self.robots: dict[str, tuple[robotparser.RobotFileParser, str]] = {}
        self.hashes: dict[str, str] = {}

    def wait_for_host(self, host: str) -> None:
        remaining = self.delay - (time.monotonic() - self.last_request.get(host, 0.0))
        if remaining > 0:
            time.sleep(remaining)
        self.last_request[host] = time.monotonic()

    def fetch_bytes(self, url: str) -> tuple[bytes, object, str]:
        assert_public_url(url)
        host = urlsplit(url).hostname or ""
        self.wait_for_host(host)
        request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,application/json,text/plain;q=0.8,*/*;q=0.1", "Accept-Encoding": "gzip"})
        response = self.opener.open(request, timeout=self.timeout)
        final_url = normalize_url(response.geturl())
        assert_public_url(final_url)
        raw = response.read(self.max_bytes + 1)
        if len(raw) > self.max_bytes:
            raise ValueError(f"response exceeds {self.max_bytes} byte limit")
        return raw, response.headers, final_url

    def robots_decision(self, url: str) -> tuple[bool, str]:
        parts = urlsplit(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin not in self.robots:
            parser = robotparser.RobotFileParser()
            robots_url = f"{origin}/robots.txt"
            try:
                raw, headers, _ = self.fetch_bytes(robots_url)
                parser.set_url(robots_url)
                parser.parse(decode_body(raw, headers.get("Content-Encoding"),
                                         headers.get_content_charset(), self.max_bytes).splitlines())
                state = "allowed"
            except HTTPError as exc:
                if exc.code in {401, 403}:
                    parser.parse(["User-agent: *", "Disallow: /"])
                    state = "disallowed"
                else:
                    parser.parse([])
                    state = "unavailable"
            except (URLError, OSError, ValueError):
                parser.parse([])
                state = "unavailable"
            self.robots[origin] = (parser, state)
        parser, state = self.robots[origin]
        allowed = parser.can_fetch(USER_AGENT, url)
        return allowed, "disallowed" if not allowed else state

    def record(self, source_url: str, depth: int, parent: str | None) -> dict:
        base = {"schema_version": SCHEMA_VERSION, "source_url": source_url, "final_url": None,
                "canonical_url": None, "fetched_at": now_iso(), "status": "error",
                "http_status": None, "content_type": None, "title": None, "description": None,
                "author": None, "published_date": None, "language": None, "text": None,
                "text_sha256": None, "raw_sha256": None, "bytes": None, "links": [],
                "depth": depth, "parent_url": parent, "robots": "not_checked",
                "duplicate_of": None, "error": None}
        try:
            assert_public_url(source_url)
        except ValueError as exc:
            return {**base, "status": "rejected", "error": str(exc)}
        allowed, robots_state = self.robots_decision(source_url)
        base["robots"] = robots_state
        if not allowed:
            return {**base, "status": "blocked", "error": "robots.txt disallows collection"}
        try:
            raw, headers, final_url = self.fetch_bytes(source_url)
            content_type = headers.get_content_type().lower()
            base.update(final_url=final_url, http_status=200, content_type=content_type,
                        raw_sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))
            if not any(content_type.startswith(item) for item in ALLOWED_TYPES):
                return {**base, "status": "rejected", "error": f"unsupported content type: {content_type}"}
            body = decode_body(raw, headers.get("Content-Encoding"),
                               headers.get_content_charset(), self.max_bytes)
            if content_type in {"text/html", "application/xhtml+xml"}:
                parser = PageParser(final_url)
                parser.feed(body)
                text = parser.text
                base.update(canonical_url=parser.canonical or final_url, title=parser.title,
                            description=parser.meta.get("description") or parser.meta.get("og:description"),
                            author=parser.meta.get("author") or parser.meta.get("article:author"),
                            published_date=parser.meta.get("article:published_time") or parser.meta.get("date"),
                            language=parser.language, text=text, links=parser.links[:1000])
            elif content_type == "application/json":
                parsed = json.loads(body)
                text = json.dumps(parsed, ensure_ascii=False, sort_keys=True)
                base.update(canonical_url=final_url, text=text, content_json=parsed)
            else:
                text = body
                base.update(canonical_url=final_url, text=text)
            text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
            base["text_sha256"] = text_hash
            if text_hash in self.hashes:
                return {**base, "status": "duplicate", "duplicate_of": self.hashes[text_hash]}
            self.hashes[text_hash] = final_url
            return {**base, "status": "ok"}
        except HTTPError as exc:
            return {**base, "http_status": exc.code, "status": "error", "error": f"HTTP {exc.code}"}
        except (URLError, OSError, ValueError, json.JSONDecodeError) as exc:
            return {**base, "status": "error", "error": str(exc)}

    def run(self):
        queue = deque((url, 0, None) for url in self.seeds)
        seen: set[str] = set()
        emitted = 0
        while queue and emitted < self.max_pages:
            url, depth, parent = queue.popleft()
            if url in seen:
                continue
            seen.add(url)
            record = self.record(url, depth, parent)
            emitted += 1
            yield record
            if record["status"] != "ok" or depth >= self.max_depth:
                continue
            for link in record.get("links", []):
                if urlsplit(link).hostname in self.allowed_hosts and link not in seen:
                    queue.append((link, depth + 1, record.get("final_url") or url))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="*", help="public seed URLs")
    parser.add_argument("--seed-file", type=Path, help="text file containing one seed URL per line")
    parser.add_argument("--output", type=Path, required=True, help="JSONL output path")
    parser.add_argument("--max-pages", type=int, default=40)
    parser.add_argument("--max-depth", type=int, default=1)
    parser.add_argument("--per-host-delay", type=float, default=1.0)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--max-bytes", type=int, default=2 * 1024 * 1024)
    args = parser.parse_args()
    if not 1 <= args.max_pages <= 200:
        parser.error("--max-pages must be between 1 and 200")
    if not 0 <= args.max_depth <= 3:
        parser.error("--max-depth must be between 0 and 3")
    if args.per_host_delay < 0.5:
        parser.error("--per-host-delay must be at least 0.5 seconds")
    return args


def main() -> int:
    args = parse_args()
    seeds = list(args.urls)
    if args.seed_file:
        seeds.extend(line.strip() for line in args.seed_file.read_text(encoding="utf-8").splitlines()
                     if line.strip() and not line.lstrip().startswith("#"))
    if not seeds:
        print("at least one seed URL is required", file=sys.stderr)
        return 2
    try:
        collector = Collector(seeds, args.max_pages, args.max_depth, args.per_host_delay,
                              args.timeout, args.max_bytes)
    except (ValueError, UnicodeError) as exc:
        print(f"invalid seed: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    with args.output.open("w", encoding="utf-8") as handle:
        for record in collector.run():
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            counts[record["status"]] = counts.get(record["status"], 0) + 1
    print(json.dumps({"output": str(args.output), "records": sum(counts.values()), "statuses": counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
