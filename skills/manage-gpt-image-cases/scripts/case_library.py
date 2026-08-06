#!/usr/bin/env python3
"""Validate, inspect, search, and export a structured prompt case library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


SUPPORTED_SCHEMA = "1.0.0"
SUPPORTED_LOCALES = {"und", "zh-CN", "en"}


def read_payload(path: Path) -> Dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Case library root must be an object")
    return payload


def normalized_prompt(value: str) -> str:
    return " ".join(value.lower().split())


def fingerprint(value: str) -> str:
    return hashlib.sha256(normalized_prompt(value).encode("utf-8")).hexdigest()


def validate(payload: Dict[str, Any]) -> Dict[str, int]:
    if payload.get("schemaVersion") != SUPPORTED_SCHEMA:
        raise ValueError(f"Unsupported schema version: {payload.get('schemaVersion')}")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Case library must contain records")

    ids = set()
    for item in cases:
        case_id = str(item.get("id") or "")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", case_id):
            raise ValueError(f"Invalid case id: {case_id}")
        if case_id in ids:
            raise ValueError(f"Duplicate case id: {case_id}")
        ids.add(case_id)
        if item.get("locale") not in SUPPORTED_LOCALES:
            raise ValueError(f"Invalid locale for {case_id}")
        if not item.get("title") or not isinstance(item.get("image"), dict):
            raise ValueError(f"Media or title is incomplete for {case_id}")
        if not isinstance(item.get("summary"), dict) or not isinstance(item.get("badge"), dict):
            raise ValueError(f"Localized display fields are incomplete for {case_id}")
        if not isinstance(item.get("tags"), list) or len(item["tags"]) != len(set(item["tags"])):
            raise ValueError(f"Tags are invalid for {case_id}")
        prompt = str(item.get("prompt") or "")
        if not prompt or item.get("promptHash") != fingerprint(prompt):
            raise ValueError(f"Prompt fingerprint mismatch for {case_id}")
        category = item.get("category") or {}
        if not category.get("key") or not category.get("labels"):
            raise ValueError(f"Category is incomplete for {case_id}")
        source = item.get("source") or {}
        if source.get("kind") not in {"local", "community"}:
            raise ValueError(f"Source kind is invalid for {case_id}")
        if not source.get("key") or not source.get("label"):
            raise ValueError(f"Source is incomplete for {case_id}")
        if source.get("kind") == "community" and (
            not source.get("repository") or not source.get("license")
        ):
            raise ValueError(f"Community attribution is incomplete for {case_id}")

    meta = payload.get("meta") or {}
    if meta.get("totalRecords") != len(cases):
        raise ValueError("meta.totalRecords is stale")
    if meta.get("uniquePrompts") != len({item["promptHash"] for item in cases}):
        raise ValueError("meta.uniquePrompts is stale")
    locale_counts = Counter(item["locale"] for item in cases)
    if meta.get("localeCounts") != dict(sorted(locale_counts.items())):
        raise ValueError("meta.localeCounts is stale")
    source_counts = Counter(item["source"]["key"] for item in cases)
    if meta.get("sourceCounts") != dict(sorted(source_counts.items())):
        raise ValueError("meta.sourceCounts is stale")
    expected_views = {
        "zh-CN": locale_counts["und"] + locale_counts["zh-CN"],
        "en": locale_counts["und"] + locale_counts["en"],
    }
    if meta.get("viewCounts") != expected_views:
        raise ValueError("meta.viewCounts is stale")
    aliases = meta.get("aliases")
    if not isinstance(aliases, dict):
        raise ValueError("meta.aliases must be an object")
    for alias, canonical_id in aliases.items():
        if alias in ids or canonical_id not in ids:
            raise ValueError(f"Invalid alias: {alias}")
    if meta.get("duplicateRecordsRemoved") != len(aliases):
        raise ValueError("meta.duplicateRecordsRemoved is stale")
    return {"records": len(cases), "aliases": len(aliases)}


def localized(values: Any, locale: Optional[str]) -> str:
    if not isinstance(values, dict):
        return ""
    for key in [locale, "en", "zh-CN"]:
        if key and values.get(key):
            return str(values[key])
    return str(next(iter(values.values()), ""))


def select_cases(
    cases: Iterable[Dict[str, Any]],
    query: str,
    locale: Optional[str],
    category: Optional[str],
    source: Optional[str],
) -> List[Dict[str, Any]]:
    terms = normalized_prompt(query).split()
    selected = []
    for item in cases:
        if locale and item["locale"] not in {"und", locale}:
            continue
        if category and item["category"]["key"] != category:
            continue
        if source and item["source"]["key"] != source:
            continue
        haystack = " ".join(
            [
                item["title"],
                item["prompt"],
                " ".join(item["category"]["labels"].values()),
                " ".join(item["summary"].values()),
                item["source"]["label"],
                " ".join(item["tags"]),
            ]
        )
        normalized = normalized_prompt(haystack)
        if terms and not all(term in normalized for term in terms):
            continue
        selected.append(item)
    return selected


def add_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--query", default="")
    parser.add_argument("--locale", choices=["zh-CN", "en"])
    parser.add_argument("--category")
    parser.add_argument("--source")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ["validate", "stats"]:
        child = subparsers.add_parser(name)
        child.add_argument("--data", type=Path, required=True)
    search = subparsers.add_parser("search")
    search.add_argument("--data", type=Path, required=True)
    add_filters(search)
    search.add_argument("--limit", type=int, default=10)
    export = subparsers.add_parser("export")
    export.add_argument("--data", type=Path, required=True)
    add_filters(export)
    export.add_argument("--format", choices=["json", "jsonl"], default="json")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    payload = read_payload(args.data)
    result = validate(payload)
    if args.command == "validate":
        print(f"Valid case library: {result['records']} records, {result['aliases']} aliases")
        return 0
    if args.command == "stats":
        print(json.dumps(payload["meta"], ensure_ascii=False, indent=2))
        return 0

    selected = select_cases(
        payload["cases"], args.query, args.locale, args.category, args.source
    )
    if args.command == "search":
        if args.limit <= 0:
            parser.error("--limit must be positive")
        cases = selected[: args.limit]
        summaries = [
            {
                "id": item["id"],
                "locale": item["locale"],
                "title": item["title"],
                "category": localized(item["category"]["labels"], args.locale),
                "source": item["source"]["key"],
                "prompt": item["prompt"],
                "image": item["image"]["url"],
                "originalUrl": item["source"].get("originalUrl", ""),
                "caseUrl": item["source"].get("caseUrl", ""),
            }
            for item in cases
        ]
        print(json.dumps({"count": len(selected), "cases": summaries}, ensure_ascii=False, indent=2))
        return 0
    if args.format == "jsonl":
        for item in selected:
            print(json.dumps(item, ensure_ascii=False))
    else:
        print(json.dumps({"count": len(selected), "cases": selected}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
