#!/usr/bin/env python3
"""Build, validate, inspect, and search the unified prompt case library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "data" / "case-library.json"
COMMUNITY_PATH = ROOT / "data" / "community-cases.json"
CURATED_PATHS = {
    "zh-CN": ROOT / "data" / "curated-cases.zh.json",
    "en": ROOT / "data" / "curated-cases.en.json",
}
README_SOURCES = {
    "zh-CN": (ROOT / "README.md", "提示词合集"),
    "en": (ROOT / "en" / "README.md", "Prompt Library"),
}
SCHEMA_VERSION = "1.0.0"

CATEGORY_KEYS = {
    "UI 界面复刻": "ui-interfaces",
    "知识科普与信息图": "charts-infographics",
    "品牌海报设计": "posters-typography",
    "电商与产品": "products-ecommerce",
    "品牌与营销": "brand-marketing",
    "建筑与空间": "architecture-spaces",
    "真实摄影": "photography-realism",
    "艺术创作": "illustration-art",
    "角色与一致性": "characters-people",
    "场景与叙事": "scenes-storytelling",
    "历史与古风": "history-classical",
    "文档与出版": "documents-publishing",
    "趣味玩法": "other-use-cases",
    "图片编辑与参考": "image-editing-reference",
    "创意字体": "creative-typography",
    "补充案例提示词": "supplemental-prompts",
}


def read_json(path: Path) -> Dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected an object in {path}")
    return payload


def normalize_prompt(prompt: str) -> str:
    return " ".join(prompt.lower().split())


def prompt_hash(prompt: str) -> str:
    return hashlib.sha256(normalize_prompt(prompt).encode("utf-8")).hexdigest()


def slugify(value: str) -> str:
    known = CATEGORY_KEYS.get(value)
    if known:
        return known
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if slug:
        return slug
    digest = hashlib.sha1(value.encode("utf-8")).hexdigest()[:10]
    return f"category-{digest}"


def normalize_category_name(value: str, locale: str) -> str:
    source = re.sub(r"\s+", " ", value).strip()
    if locale == "zh-CN":
        normalized = re.sub(r"^[\d一二三四五六七八九十百千]+[、.．\-\s]*", "", source)
    else:
        normalized = re.sub(r"^\d+(?:\.\d+)?\s*", "", source)
    return normalized.strip() or ("未分类" if locale == "zh-CN" else "Uncategorized")


def parse_prompt_library(path: Path, locale: str, section_name: str) -> List[Dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_section = False
    category = "未分类" if locale == "zh-CN" else "Uncategorized"
    current: Optional[Dict[str, Any]] = None
    cases: List[Dict[str, Any]] = []

    def finish() -> None:
        nonlocal current
        if not current:
            return
        body_lines = current["lines"]
        body = "\n".join(body_lines).strip()
        image_match = re.search(r"!\[[^\]]*\]\((https?://[^)\s]+)\)", body)
        code_match = re.search(r"```(?:[\w-]+)?\n([\s\S]*?)```", body)
        description = ""
        for raw_line in body_lines:
            text = raw_line.strip()
            if not text or text.startswith(("![", "```", "|")):
                continue
            description = re.sub(r"^[-*]\s*", "", text)
            break
        fallback = "暂无提示词内容" if locale == "zh-CN" else "No prompt text available yet"
        prompt = (code_match.group(1) if code_match else "").strip() or description or fallback
        number = len(cases) + 1
        cases.append(
            {
                "id": f"{'zh' if locale == 'zh-CN' else 'en'}-prompt-{number}",
                "title": current["title"],
                "category": current["category"],
                "source": "主教程" if locale == "zh-CN" else "English Guide",
                "badge": "教程" if locale == "zh-CN" else "Guide",
                "image": image_match.group(1) if image_match else "",
                "description": description or ("暂无说明" if locale == "zh-CN" else "No description"),
                "promptText": prompt,
            }
        )
        current = None

    for line in lines:
        if re.match(rf"^##\s+{re.escape(section_name)}\s*$", line):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            finish()
            break
        if not in_section:
            continue
        category_match = re.match(r"^###\s+(.+)", line)
        if category_match:
            finish()
            category = normalize_category_name(category_match.group(1), locale)
            continue
        title_match = re.match(r"^####\s+(.+)", line)
        if title_match:
            finish()
            current = {
                "title": title_match.group(1).strip(),
                "category": category,
                "lines": [],
            }
            continue
        if current:
            current["lines"].append(line)

    finish()
    if not cases:
        raise ValueError(f"No prompt cases parsed from {path}")
    return cases


def normalize_local_case(item: Dict[str, Any], locale: str) -> Dict[str, Any]:
    prompt = str(item.get("promptText") or "").strip()
    category = str(item.get("category") or "").strip()
    if not prompt or not category:
        raise ValueError(f"Local case {item.get('id')} is missing prompt or category")
    return {
        "id": str(item.get("id") or "").strip(),
        "locale": locale,
        "title": str(item.get("title") or "").strip(),
        "category": {"key": slugify(category), "labels": {locale: category}},
        "source": {
            "key": "local",
            "kind": "local",
            "label": str(item.get("source") or "Local guide").strip(),
        },
        "badge": {locale: str(item.get("badge") or "Curated").strip()},
        "image": {"url": str(item.get("image") or "").strip()},
        "summary": {locale: str(item.get("description") or "").strip()},
        "prompt": prompt,
        "promptHash": prompt_hash(prompt),
        "tags": [],
    }


def community_source_metadata(payload: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    sources = payload.get("meta", {}).get("sources", [])
    result: Dict[str, Dict[str, str]] = {}
    for source in sources:
        repository = str(source.get("sourceRepository") or "")
        key = (
            "youmind-awesome-gpt-image-2"
            if "YouMind-OpenLab" in repository
            else "awesome-gpt-image-2"
        )
        result[key] = {
            "repository": repository,
            "license": str(source.get("sourceLicense") or ""),
        }
    return result


def normalize_community_case(
    item: Dict[str, Any], source_meta: Dict[str, Dict[str, str]]
) -> Dict[str, Any]:
    prompt = str(item.get("prompt") or "").strip()
    source_key = str(item.get("source") or "community").strip()
    category_en = str(item.get("category") or "Other Use Cases").strip()
    category_zh = str(item.get("categoryZh") or category_en).strip()
    metadata = source_meta.get(source_key, {})
    source: Dict[str, Any] = {
        "key": source_key,
        "kind": "community",
        "label": str(item.get("sourceLabel") or source_key).strip(),
    }
    optional_source = {
        "repository": metadata.get("repository"),
        "license": metadata.get("license"),
        "originalUrl": str(item.get("sourceUrl") or "").strip(),
        "caseUrl": str(item.get("caseUrl") or "").strip(),
    }
    source.update({key: value for key, value in optional_source.items() if value})
    tags = list(
        dict.fromkeys(
            str(value).strip()
            for value in list(item.get("styles") or []) + list(item.get("scenes") or [])
            if str(value).strip()
        )
    )
    return {
        "id": str(item.get("id") or "").strip(),
        "locale": "und",
        "title": str(item.get("title") or "").strip(),
        "category": {
            "key": slugify(category_en),
            "labels": {"en": category_en, "zh-CN": category_zh},
        },
        "source": source,
        "badge": {
            "en": str(item.get("badge") or "Community").strip(),
            "zh-CN": str(item.get("badgeZh") or "社区案例").strip(),
        },
        "image": {"url": str(item.get("image") or "").strip()},
        "summary": {
            "en": str(item.get("description") or "").strip(),
            "zh-CN": str(item.get("descriptionZh") or item.get("description") or "").strip(),
        },
        "prompt": prompt,
        "promptHash": prompt_hash(prompt),
        "tags": tags,
    }


def deduplicate_cases(cases: Iterable[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], Dict[str, str]]:
    unique: List[Dict[str, Any]] = []
    aliases: Dict[str, str] = {}
    seen: Dict[tuple[str, str], str] = {}
    for item in cases:
        key = (item["locale"], item["promptHash"])
        existing_id = seen.get(key)
        if existing_id:
            aliases[item["id"]] = existing_id
            continue
        seen[key] = item["id"]
        unique.append(item)
    return unique, aliases


def build_payload() -> Dict[str, Any]:
    local_cases: List[Dict[str, Any]] = []
    for locale, (readme_path, section_name) in README_SOURCES.items():
        parsed = parse_prompt_library(readme_path, locale, section_name)
        curated_payload = read_json(CURATED_PATHS[locale])
        curated = curated_payload.get("cases")
        if not isinstance(curated, list):
            raise ValueError(f"Curated cases are missing in {CURATED_PATHS[locale]}")
        expected = int(curated_payload.get("count") or 0)
        if expected != len(curated):
            raise ValueError(f"Curated case count is stale in {CURATED_PATHS[locale]}")
        local_cases.extend(normalize_local_case(item, locale) for item in parsed + curated)

    community_payload = read_json(COMMUNITY_PATH)
    raw_community = community_payload.get("cases")
    if not isinstance(raw_community, list):
        raise ValueError("Community case data does not contain a cases array")
    source_meta = community_source_metadata(community_payload)
    community_cases = [
        normalize_community_case(item, source_meta) for item in raw_community
    ]
    cases, aliases = deduplicate_cases(local_cases + community_cases)
    locale_counts = Counter(item["locale"] for item in cases)
    source_counts = Counter(item["source"]["key"] for item in cases)
    payload = {
        "schemaVersion": SCHEMA_VERSION,
        "meta": {
            "totalRecords": len(cases),
            "uniquePrompts": len({item["promptHash"] for item in cases}),
            "duplicateRecordsRemoved": len(aliases),
            "aliases": dict(sorted(aliases.items())),
            "localeCounts": dict(sorted(locale_counts.items())),
            "viewCounts": {
                "zh-CN": locale_counts["und"] + locale_counts["zh-CN"],
                "en": locale_counts["und"] + locale_counts["en"],
            },
            "sourceCounts": dict(sorted(source_counts.items())),
            "generatedFrom": [
                "README.md",
                "en/README.md",
                "data/curated-cases.zh.json",
                "data/curated-cases.en.json",
                "data/community-cases.json",
            ],
        },
        "cases": cases,
    }
    validate_payload(payload)
    return payload


def validate_payload(payload: Dict[str, Any]) -> None:
    if payload.get("schemaVersion") != SCHEMA_VERSION:
        raise ValueError(f"Unsupported schema version: {payload.get('schemaVersion')}")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Case library must contain a non-empty cases array")
    ids = set()
    for item in cases:
        case_id = str(item.get("id") or "")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", case_id):
            raise ValueError(f"Invalid case id: {case_id}")
        if case_id in ids:
            raise ValueError(f"Duplicate case id: {case_id}")
        ids.add(case_id)
        if item.get("locale") not in {"und", "zh-CN", "en"}:
            raise ValueError(f"Invalid locale for {case_id}")
        if not item.get("title") or not isinstance(item.get("image"), dict):
            raise ValueError(f"Media or title is incomplete for {case_id}")
        if not isinstance(item.get("summary"), dict) or not isinstance(item.get("badge"), dict):
            raise ValueError(f"Localized display fields are incomplete for {case_id}")
        if not isinstance(item.get("tags"), list) or len(item["tags"]) != len(set(item["tags"])):
            raise ValueError(f"Tags are invalid for {case_id}")
        prompt = str(item.get("prompt") or "")
        if not prompt or item.get("promptHash") != prompt_hash(prompt):
            raise ValueError(f"Invalid prompt fingerprint for {case_id}")
        category = item.get("category") or {}
        source = item.get("source") or {}
        if not category.get("key") or not category.get("labels"):
            raise ValueError(f"Invalid category for {case_id}")
        if source.get("kind") not in {"local", "community"} or not source.get("key"):
            raise ValueError(f"Invalid source for {case_id}")
        if source.get("kind") == "community" and (
            not source.get("repository") or not source.get("license")
        ):
            raise ValueError(f"Community attribution is incomplete for {case_id}")

    meta = payload.get("meta") or {}
    if meta.get("totalRecords") != len(cases):
        raise ValueError("Metadata totalRecords does not match cases")
    if meta.get("uniquePrompts") != len({item["promptHash"] for item in cases}):
        raise ValueError("Metadata uniquePrompts is stale")
    aliases = meta.get("aliases")
    if not isinstance(aliases, dict):
        raise ValueError("Metadata aliases is invalid")
    for alias, canonical_id in aliases.items():
        if alias in ids or canonical_id not in ids:
            raise ValueError(f"Invalid case alias: {alias}")
    if meta.get("duplicateRecordsRemoved") != len(aliases):
        raise ValueError("Metadata duplicateRecordsRemoved is stale")
    locale_counts = Counter(item["locale"] for item in cases)
    if meta.get("localeCounts") != dict(sorted(locale_counts.items())):
        raise ValueError("Metadata localeCounts is stale")
    expected_views = {
        "zh-CN": locale_counts["und"] + locale_counts["zh-CN"],
        "en": locale_counts["und"] + locale_counts["en"],
    }
    if meta.get("viewCounts") != expected_views:
        raise ValueError("Metadata viewCounts is stale")


def serialize(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def search_cases(
    payload: Dict[str, Any], query: str, locale: Optional[str], limit: int
) -> List[Dict[str, Any]]:
    terms = normalize_prompt(query).split()
    results = []
    for item in payload["cases"]:
        if locale and item["locale"] not in {"und", locale}:
            continue
        source = item["source"]
        haystack = " ".join(
            [
                item["title"],
                item["prompt"],
                " ".join(item["category"]["labels"].values()),
                " ".join(item["summary"].values()),
                source["label"],
                " ".join(item["tags"]),
            ]
        )
        normalized = normalize_prompt(haystack)
        if all(term in normalized for term in terms):
            results.append(item)
        if len(results) >= limit:
            break
    return results


def print_stats(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload["meta"], ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("build")
    subparsers.add_parser("check")
    subparsers.add_parser("stats")
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--locale", choices=["zh-CN", "en"])
    search_parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    command = args.command or "build"

    if command == "build":
        payload = build_payload()
        OUTPUT_PATH.write_text(serialize(payload), encoding="utf-8")
        print(f"Built {payload['meta']['totalRecords']} cases at {OUTPUT_PATH}")
        return 0

    existing = read_json(OUTPUT_PATH)
    validate_payload(existing)
    if command == "check":
        expected = serialize(build_payload())
        if OUTPUT_PATH.read_text(encoding="utf-8") != expected:
            raise ValueError("case-library.json is stale; run the build command")
        print(f"Validated {existing['meta']['totalRecords']} cases in {OUTPUT_PATH}")
        return 0
    if command == "stats":
        print_stats(existing)
        return 0
    if command == "search":
        if args.limit <= 0:
            parser.error("--limit must be positive")
        results = search_cases(existing, args.query, args.locale, args.limit)
        print(json.dumps({"count": len(results), "cases": results}, ensure_ascii=False, indent=2))
        return 0
    parser.error(f"Unknown command: {command}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1)
