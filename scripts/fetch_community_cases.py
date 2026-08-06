#!/usr/bin/env python3
"""Sync public GPT-Image-2 cases from the MIT-licensed reference repository."""

from __future__ import annotations

import argparse
import base64
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple
from urllib import request


SOURCE_REPOSITORY = "freestylefly/awesome-gpt-image-2"
SOURCE_URL = f"https://github.com/{SOURCE_REPOSITORY}"
SOURCE_CASES_PATH = "data/cases.json"
YOUMIND_REPOSITORY = "YouMind-OpenLab/awesome-gpt-image-2"
YOUMIND_URL = f"https://github.com/{YOUMIND_REPOSITORY}"
YOUMIND_README_PATH = "README.md"
MIN_SOURCE_CASES = 400
MIN_YOUMIND_CASES = 100
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

YOUMIND_CATEGORY_MAP = {
    "Profile / Avatar": "Characters & People",
    "Social Media Post": "Documents & Publishing",
    "Infographic / Edu Visual": "Charts & Infographics",
    "YouTube Thumbnail": "Posters & Typography",
    "Comic / Storyboard": "Scenes & Storytelling",
    "Product Marketing": "Products & E-commerce",
    "E-commerce Main Image": "Products & E-commerce",
    "Game Asset": "Illustration & Art",
    "Poster / Flyer": "Posters & Typography",
    "App / Web Design": "UI & Interfaces",
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


def fetch_repository_file(repository: str, path: str) -> Tuple[str, str, str]:
    api_root = f"https://api.github.com/repos/{repository}"
    branch = fetch_json(f"{api_root}/branches/main")
    commit = str(branch.get("commit", {}).get("sha") or "").strip()
    commit_date = str(
        branch.get("commit", {}).get("commit", {}).get("author", {}).get("date") or ""
    ).strip()
    if not commit:
        raise ValueError(f"{repository} did not return a main commit")

    tree = fetch_json(f"{api_root}/git/trees/{commit}?recursive=1")
    source_entry = next(
        (
            item
            for item in tree.get("tree", [])
            if isinstance(item, dict) and item.get("path") == path
        ),
        None,
    )
    blob_sha = str((source_entry or {}).get("sha") or "").strip()
    if not blob_sha:
        raise ValueError(f"Could not find {path} in {repository} at {commit}")

    blob = fetch_json(f"{api_root}/git/blobs/{blob_sha}")
    if blob.get("encoding") != "base64":
        raise ValueError(f"The {repository}/{path} blob was not base64 encoded")
    raw = base64.b64decode(str(blob.get("content") or "")).decode("utf-8")
    return commit, commit_date, raw


def fetch_source_cases() -> tuple[str, str, List[Dict[str, Any]]]:
    commit, commit_date, raw = fetch_repository_file(
        SOURCE_REPOSITORY, SOURCE_CASES_PATH
    )
    payload = json.loads(raw)
    cases = payload.get("cases") if isinstance(payload, dict) else None
    if not isinstance(cases, list):
        raise ValueError("The reference case payload does not contain a cases array")
    normalized = [item for item in cases if isinstance(item, dict)]
    if len(normalized) < MIN_SOURCE_CASES:
        raise ValueError(
            f"Reference case count dropped below {MIN_SOURCE_CASES}: {len(normalized)}"
        )
    return commit, commit_date, normalized


def markdown_section(body: str, heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\s*\n+(.*?)(?=^#### |\Z)",
        body,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def parse_markdown_link(body: str, label: str) -> Tuple[str, str]:
    match = re.search(
        rf"^- \*\*{re.escape(label)}:\*\* "
        r"(?:\[([^\]]+)\]\(([^)]+)\)|(.+))$",
        body,
        flags=re.MULTILINE,
    )
    if not match:
        return "", ""
    return (match.group(1) or match.group(3) or "").strip(), (
        match.group(2) or ""
    ).strip()


def parse_youmind_cases(markdown: str) -> List[Dict[str, Any]]:
    marker = "## 📋 All Prompts"
    if marker not in markdown:
        raise ValueError("YouMind README does not contain the All Prompts section")
    gallery = markdown.split(marker, 1)[1]
    headings = list(
        re.finditer(r"^### No\. (\d+): (.+)$", gallery, flags=re.MULTILINE)
    )
    cases: List[Dict[str, Any]] = []

    for index, heading in enumerate(headings):
        body_start = heading.end()
        body_end = (
            headings[index + 1].start()
            if index + 1 < len(headings)
            else len(gallery)
        )
        body = gallery[body_start:body_end]
        title = heading.group(2).strip()
        prompt_block = markdown_section(body, "#### 📝 Prompt")
        prompt_match = re.search(
            r"^```[^\n]*\n(.*?)\n```", prompt_block, flags=re.MULTILINE | re.DOTALL
        )
        image_match = re.search(r'<img\s+src="([^"]+)"', body)
        case_match = re.search(
            r"\*\*\[👉 Try it now →\]\((https://youmind\.com/[^)]+[?&]id=(\d+))\)\*\*",
            body,
        )
        if not prompt_match or not image_match or not case_match:
            continue

        raw_category = next(
            (name for name in YOUMIND_CATEGORY_MAP if title.startswith(f"{name} - ")),
            "Other Use Cases",
        )
        category = YOUMIND_CATEGORY_MAP.get(raw_category, raw_category)
        author, author_url = parse_markdown_link(body, "Author")
        _, original_url = parse_markdown_link(body, "Source")
        language_match = re.search(r"!\[Language-([^\]]+)\]", body)
        description = markdown_section(body, "#### 📖 Description")
        prompt = prompt_match.group(1).strip()
        case_id = int(case_match.group(2))
        language = language_match.group(1).strip() if language_match else ""

        cases.append(
            {
                "id": f"youmind-{case_id}",
                "sourceId": case_id,
                "title": title,
                "category": category,
                "categoryZh": CATEGORY_ZH.get(category, category),
                "source": "youmind-awesome-gpt-image-2",
                "sourceLabel": author or "YouMind Community",
                "badge": "YouMind",
                "badgeZh": "YouMind 案例",
                "image": image_match.group(1).strip(),
                "description": description or f"Source: {author or 'YouMind Community'}.",
                "descriptionZh": (
                    f"来源：{author or 'YouMind 社区'}。"
                    + (f"语言：{language}。" if language else "")
                ),
                "prompt": prompt,
                "promptPreview": prompt[:420],
                "styles": [],
                "scenes": [raw_category] if raw_category != "Other Use Cases" else [],
                "languages": [language] if language else [],
                "sourceUrl": original_url or author_url,
                "caseUrl": case_match.group(1),
            }
        )

    if not cases:
        raise ValueError("No YouMind community cases could be parsed")
    return cases


def fetch_youmind_cases() -> tuple[str, str, List[Dict[str, Any]]]:
    commit, commit_date, markdown = fetch_repository_file(
        YOUMIND_REPOSITORY, YOUMIND_README_PATH
    )
    cases = parse_youmind_cases(markdown)
    if len(cases) < MIN_YOUMIND_CASES:
        raise ValueError(
            f"YouMind case count dropped below {MIN_YOUMIND_CASES}: {len(cases)}"
        )
    return commit, commit_date, cases


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


def prompt_key(prompt: str) -> str:
    return " ".join(prompt.lower().split())


def merge_cases(*case_groups: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged: List[Dict[str, Any]] = []
    seen_prompts = set()
    for group in case_groups:
        for item in group:
            key = prompt_key(str(item.get("prompt") or ""))
            if not key or key in seen_prompts:
                continue
            seen_prompts.add(key)
            merged.append(item)
    return validate_cases(merged)


def build_merged_payload(
    source_cases: Iterable[Dict[str, Any]],
    source_commit: str,
    source_commit_date: str,
    youmind_cases: Iterable[Dict[str, Any]],
    youmind_commit: str,
    youmind_commit_date: str,
) -> Dict[str, Any]:
    primary_cases = [normalize_case(item, source_commit) for item in source_cases]
    secondary_cases = list(youmind_cases)
    cases = merge_cases(primary_cases, secondary_cases)
    primary_included = sum(item["source"] == "awesome-gpt-image-2" for item in cases)
    youmind_included = sum(
        item["source"] == "youmind-awesome-gpt-image-2" for item in cases
    )
    return {
        "meta": {
            "count": len(cases),
            "duplicatePromptCount": (
                len(primary_cases) + len(secondary_cases) - len(cases)
            ),
            "sources": [
                {
                    "sourceRepository": SOURCE_URL,
                    "sourceCommit": source_commit,
                    "sourceCommitDate": source_commit_date,
                    "sourceLicense": "MIT",
                    "availableCount": len(primary_cases),
                    "includedCount": primary_included,
                },
                {
                    "sourceRepository": YOUMIND_URL,
                    "sourceCommit": youmind_commit,
                    "sourceCommitDate": youmind_commit_date,
                    "sourceLicense": "CC-BY-4.0",
                    "availableCount": len(secondary_cases),
                    "includedCount": youmind_included,
                },
            ],
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
    sources = payload.get("meta", {}).get("sources")
    if not isinstance(sources, list) or len(sources) < 2:
        raise ValueError("Community case metadata must contain both sources")
    included_count = sum(int(source.get("includedCount") or 0) for source in sources)
    available_count = sum(int(source.get("availableCount") or 0) for source in sources)
    duplicate_count = int(payload.get("meta", {}).get("duplicatePromptCount") or 0)
    if included_count != len(cases):
        raise ValueError("Source included counts do not match the case count")
    if available_count - len(cases) != duplicate_count:
        raise ValueError("Duplicate prompt metadata does not match source counts")
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
    youmind_commit, youmind_commit_date, youmind_cases = fetch_youmind_cases()
    payload = build_merged_payload(
        source_cases,
        commit,
        commit_date,
        youmind_cases,
        youmind_commit,
        youmind_commit_date,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Synced {len(payload['cases'])} community cases from "
        f"{commit[:8]} and {youmind_commit[:8]} to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
