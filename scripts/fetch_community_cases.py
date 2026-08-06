#!/usr/bin/env python3
"""Sync public GPT-Image-2 cases from the MIT-licensed reference repository."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List
from urllib import request


SOURCE_REPOSITORY = "freestylefly/awesome-gpt-image-2"
SOURCE_URL = f"https://github.com/{SOURCE_REPOSITORY}"
API_ROOT = f"https://api.github.com/repos/{SOURCE_REPOSITORY}"
SOURCE_CASES_PATH = "data/cases.json"
REQUIRED_CASE_FIELDS = {"id", "title", "category", "image", "prompt", "caseUrl"}

CATEGORY_ZH = {
    "UI & Interfaces": "UI 界面复刻",
    "Charts & Infographics": "知识科普与信息图",
    "Posters & Typography": "品牌海报设计",
    "Products & E-commerce": "电商与产品",
    "Brand & Logos": "品牌与营销",
    "Architecture & Spaces": "建筑与空间",
    "Photography & Realism": "真实摄影",
    "Illustration & Art": "艺术创作",
    "Characters & People": "角色与一致性",
    "Scenes & Storytelling": "场景与叙事",
    "History & Classical Themes": "历史与古风",
    "Documents & Publishing": "文档与出版",
    "Other Use Cases": "趣味玩法",
}


def fetch_json(url: str) -> Dict[str, Any]:
    req = request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-gptimage2-community-sync/1.0",
        },
    )
    with request.urlopen(req, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected an object from {url}")
    return payload


def fetch_source_cases() -> tuple[str, str, List[Dict[str, Any]]]:
    branch = fetch_json(f"{API_ROOT}/branches/main")
    commit = str(branch.get("commit", {}).get("sha") or "").strip()
    commit_date = str(
        branch.get("commit", {}).get("commit", {}).get("author", {}).get("date") or ""
    ).strip()
    if not commit:
        raise ValueError("The reference repository did not return a main commit")

    tree = fetch_json(f"{API_ROOT}/git/trees/{commit}?recursive=1")
    source_entry = next(
        (
            item
            for item in tree.get("tree", [])
            if isinstance(item, dict) and item.get("path") == SOURCE_CASES_PATH
        ),
        None,
    )
    blob_sha = str((source_entry or {}).get("sha") or "").strip()
    if not blob_sha:
        raise ValueError(f"Could not find {SOURCE_CASES_PATH} at {commit}")

    blob = fetch_json(f"{API_ROOT}/git/blobs/{blob_sha}")
    if blob.get("encoding") != "base64":
        raise ValueError("The reference case blob was not base64 encoded")
    raw = base64.b64decode(str(blob.get("content") or "")).decode("utf-8")
    payload = json.loads(raw)
    cases = payload.get("cases") if isinstance(payload, dict) else None
    if not isinstance(cases, list):
        raise ValueError("The reference case payload does not contain a cases array")
    return commit, commit_date, [item for item in cases if isinstance(item, dict)]


def normalize_image(image: str, commit: str) -> str:
    source = image.strip()
    if source.startswith("/images/"):
        source = f"/data{source}"
    elif source.startswith("images/"):
        source = f"/data/{source}"
    if source.startswith("/"):
        return (
            "https://cdn.jsdelivr.net/gh/"
            f"{SOURCE_REPOSITORY}@{commit}{source}"
        )
    return source


def clean_list(values: Any) -> List[str]:
    if not isinstance(values, list):
        return []
    return [str(value).strip() for value in values if str(value).strip()]


def normalize_case(item: Dict[str, Any], commit: str) -> Dict[str, Any]:
    source_id = int(item.get("id") or 0)
    if source_id <= 0:
        raise ValueError("Every reference case must have a positive numeric id")

    category = str(item.get("category") or "Other Use Cases").strip()
    prompt = str(item.get("prompt") or "").strip()
    styles = clean_list(item.get("styles"))
    scenes = clean_list(item.get("scenes"))
    source_label = str(item.get("sourceLabel") or "Community").strip()
    tags = styles + [value for value in scenes if value not in styles]
    tag_summary = ", ".join(tags[:4])

    return {
        "id": f"community-{source_id}",
        "sourceId": source_id,
        "title": str(item.get("title") or f"Case {source_id}").strip(),
        "category": category,
        "categoryZh": CATEGORY_ZH.get(category, category),
        "source": "awesome-gpt-image-2",
        "sourceLabel": source_label,
        "badge": "Community",
        "badgeZh": "社区案例",
        "image": normalize_image(str(item.get("image") or ""), commit),
        "description": (
            f"Source: {source_label}. Tags: {tag_summary}."
            if tag_summary
            else f"Source: {source_label}."
        ),
        "descriptionZh": (
            f"来源：{source_label}。标签：{tag_summary}。"
            if tag_summary
            else f"来源：{source_label}。"
        ),
        "prompt": prompt,
        "promptPreview": str(item.get("promptPreview") or prompt).strip()[:420],
        "styles": styles,
        "scenes": scenes,
        "sourceUrl": str(item.get("sourceUrl") or "").strip(),
        "caseUrl": str(item.get("githubUrl") or "").strip()
        or f"{SOURCE_URL}/blob/{commit}/docs/gallery.md#case-{source_id}",
    }


def validate_cases(cases: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = list(cases)
    if not normalized:
        raise ValueError("No community cases were generated")
    ids = set()
    for item in normalized:
        missing = sorted(REQUIRED_CASE_FIELDS.difference(item))
        if missing:
            raise ValueError(f"Case is missing required fields: {', '.join(missing)}")
        if item["id"] in ids:
            raise ValueError(f"Duplicate case id: {item['id']}")
        if not item["prompt"]:
            raise ValueError(f"Case {item['id']} has an empty prompt")
        ids.add(item["id"])
    return normalized


def build_payload(
    source_cases: Iterable[Dict[str, Any]], commit: str, commit_date: str
) -> Dict[str, Any]:
    cases = validate_cases(normalize_case(item, commit) for item in source_cases)
    return {
        "meta": {
            "sourceRepository": SOURCE_URL,
            "sourceCommit": commit,
            "sourceCommitDate": commit_date,
            "sourceLicense": "MIT",
            "count": len(cases),
        },
        "cases": cases,
    }


def validate_file(path: Path) -> int:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Community case data must be an object")
    cases = payload.get("cases")
    if not isinstance(cases, list):
        raise ValueError("Community case data must contain a cases array")
    validate_cases(cases)
    expected_count = int(payload.get("meta", {}).get("count") or 0)
    if expected_count != len(cases):
        raise ValueError(
            f"Metadata count {expected_count} does not match {len(cases)} cases"
        )
    print(f"Validated {len(cases)} community cases in {path}")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "data" / "community-cases.json",
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        return validate_file(args.output)

    commit, commit_date, source_cases = fetch_source_cases()
    payload = build_payload(source_cases, commit, commit_date)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Synced {len(payload['cases'])} community cases from {commit[:8]} "
        f"to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
