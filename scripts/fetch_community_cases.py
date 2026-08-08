#!/usr/bin/env python3
"""Sync public GPT-Image-2 cases from the MIT-licensed reference repository."""

from __future__ import annotations

import argparse
import base64
import json
import os
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
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "awesome-gptimage2-community-sync/1.0",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(
        url,
        headers=headers,
    )
    with request.urlopen(req, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected an object from {url}")
    return payload


def fetch_repository_blob_sha(repository: str, path: str, commit: str) -> str:
    api_root = f"https://api.github.com/repos/{repository}"
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
    return blob_sha


def fetch_repository_file(repository: str, path: str) -> Tuple[str, str, str, str]:
    api_root = f"https://api.github.com/repos/{repository}"
    branch = fetch_json(f"{api_root}/branches/main")
    commit = str(branch.get("commit", {}).get("sha") or "").strip()
    commit_date = str(
        branch.get("commit", {}).get("commit", {}).get("author", {}).get("date") or ""
    ).strip()
    if not commit:
        raise ValueError(f"{repository} did not return a main commit")

    blob_sha = fetch_repository_blob_sha(repository, path, commit)
    blob = fetch_json(f"{api_root}/git/blobs/{blob_sha}")
    if blob.get("encoding") != "base64":
        raise ValueError(f"The {repository}/{path} blob was not base64 encoded")
    raw = base64.b64decode(str(blob.get("content") or "")).decode("utf-8")
    return commit, commit_date, blob_sha, raw


def fetch_source_cases() -> tuple[str, str, str, List[Dict[str, Any]]]:
    commit, commit_date, blob_sha, raw = fetch_repository_file(
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
    return commit, commit_date, blob_sha, normalized


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


def fetch_youmind_cases() -> tuple[str, str, str, List[Dict[str, Any]]]:
    commit, commit_date, blob_sha, markdown = fetch_repository_file(
        YOUMIND_REPOSITORY, YOUMIND_README_PATH
    )
    cases = parse_youmind_cases(markdown)
    if len(cases) < MIN_YOUMIND_CASES:
        raise ValueError(
            f"YouMind case count dropped below {MIN_YOUMIND_CASES}: {len(cases)}"
        )
    return commit, commit_date, blob_sha, cases


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
    source_cases: Iterable[Dict[str, Any]],
    commit: str,
    commit_date: str,
    blob_sha: str,
) -> Dict[str, Any]:
    cases = validate_cases(normalize_case(item, commit) for item in source_cases)
    return {
        "meta": {
            "sourceRepository": SOURCE_URL,
            "sourceCommit": commit,
            "sourceCommitDate": commit_date,
            "sourceBlobSha": blob_sha,
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


def merge_source_history(
    current_cases: Iterable[Dict[str, Any]],
    existing_cases: Iterable[Dict[str, Any]],
    source_key: str,
) -> List[Dict[str, Any]]:
    current = validate_cases(current_cases)
    current_by_id = {str(item["id"]): item for item in current}
    merged: List[Dict[str, Any]] = list(current)
    seen_ids = set(current_by_id)

    for existing in existing_cases:
        if existing.get("source") != source_key:
            continue
        case_id = str(existing.get("id") or "")
        if not case_id or case_id in seen_ids:
            continue
        merged.append(existing)
        seen_ids.add(case_id)

    return validate_cases(merged)


def build_merged_payload(
    source_cases: Iterable[Dict[str, Any]],
    source_commit: str,
    source_commit_date: str,
    source_blob_sha: str,
    youmind_cases: Iterable[Dict[str, Any]],
    youmind_commit: str,
    youmind_commit_date: str,
    youmind_blob_sha: str,
    existing_cases: Iterable[Dict[str, Any]] = (),
) -> Dict[str, Any]:
    history = list(existing_cases)
    current_primary_cases = [
        normalize_case(item, source_commit) for item in source_cases
    ]
    current_secondary_cases = list(youmind_cases)
    primary_cases = merge_source_history(
        current_primary_cases, history, "awesome-gpt-image-2"
    )
    secondary_cases = merge_source_history(
        current_secondary_cases, history, "youmind-awesome-gpt-image-2"
    )
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
                    "sourceBlobSha": source_blob_sha,
                    "sourceLicense": "MIT",
                    "currentAvailableCount": len(current_primary_cases),
                    "availableCount": len(primary_cases),
                    "historicalCount": len(primary_cases)
                    - len(current_primary_cases),
                    "includedCount": primary_included,
                },
                {
                    "sourceRepository": YOUMIND_URL,
                    "sourceCommit": youmind_commit,
                    "sourceCommitDate": youmind_commit_date,
                    "sourceBlobSha": youmind_blob_sha,
                    "sourceLicense": "CC-BY-4.0",
                    "currentAvailableCount": len(current_secondary_cases),
                    "availableCount": len(secondary_cases),
                    "historicalCount": len(secondary_cases)
                    - len(current_secondary_cases),
                    "includedCount": youmind_included,
                },
            ],
        },
        "cases": cases,
    }


def source_key_for_repository(repository_url: str) -> str:
    if repository_url == SOURCE_URL:
        return "awesome-gpt-image-2"
    if repository_url == YOUMIND_URL:
        return "youmind-awesome-gpt-image-2"
    raise ValueError(f"Unsupported community source: {repository_url}")


def accumulate_existing_payload(
    current_payload: Dict[str, Any], history_cases: Iterable[Dict[str, Any]]
) -> Dict[str, Any]:
    current_cases = validate_cases(current_payload.get("cases") or [])
    source_metadata = current_payload.get("meta", {}).get("sources")
    if not isinstance(source_metadata, list) or not source_metadata:
        raise ValueError("Current payload has no source metadata")

    available_history = current_cases + list(history_cases)
    source_groups: Dict[str, List[Dict[str, Any]]] = {}
    updated_sources: List[Dict[str, Any]] = []

    for source in source_metadata:
        if not isinstance(source, dict):
            raise ValueError("Every community source must be an object")
        source_key = source_key_for_repository(
            str(source.get("sourceRepository") or "")
        )
        source_cases = [
            item for item in current_cases if item.get("source") == source_key
        ]
        current_available_count = int(
            source.get("currentAvailableCount")
            or source.get("availableCount")
            or len(source_cases)
        )
        current_included_count = int(
            source.get("includedCount") or len(source_cases)
        )
        current_window = source_cases[:current_included_count]
        accumulated = merge_source_history(
            current_window, available_history, source_key
        )
        historical_count = len(accumulated) - len(current_window)
        source_groups[source_key] = accumulated
        updated_sources.append(
            {
                **source,
                "currentAvailableCount": current_available_count,
                "availableCount": current_available_count + historical_count,
                "historicalCount": historical_count,
            }
        )

    ordered_groups = [
        source_groups[source_key_for_repository(source["sourceRepository"])]
        for source in updated_sources
    ]
    cases = merge_cases(*ordered_groups)
    for source in updated_sources:
        source_key = source_key_for_repository(source["sourceRepository"])
        source["includedCount"] = sum(
            item.get("source") == source_key for item in cases
        )

    return {
        "meta": {
            **current_payload.get("meta", {}),
            "count": len(cases),
            "duplicatePromptCount": sum(
                int(source["availableCount"]) for source in updated_sources
            )
            - len(cases),
            "sources": updated_sources,
        },
        "cases": cases,
    }


def load_existing_payload(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Existing community case data must be an object")
    return payload


def find_source_metadata(
    payload: Dict[str, Any], repository_url: str
) -> Dict[str, Any]:
    sources = payload.get("meta", {}).get("sources", [])
    if not isinstance(sources, list):
        return {}
    return next(
        (
            source
            for source in sources
            if isinstance(source, dict)
            and source.get("sourceRepository") == repository_url
        ),
        {},
    )


def ensure_case_count_not_decreased(
    source_label: str, fetched_count: int, existing_source: Dict[str, Any]
) -> None:
    previous_count = int(
        existing_source.get("currentAvailableCount")
        or existing_source.get("availableCount")
        or 0
    )
    if previous_count and fetched_count < previous_count:
        raise ValueError(
            f"{source_label} case count decreased from {previous_count} "
            f"to {fetched_count}; refusing to shrink the library"
        )


def choose_source_revision(
    existing_source: Dict[str, Any],
    fetched_commit: str,
    fetched_commit_date: str,
    fetched_blob_sha: str,
    previous_blob_sha: str = "",
) -> Tuple[str, str]:
    existing_commit = str(existing_source.get("sourceCommit") or "").strip()
    existing_commit_date = str(
        existing_source.get("sourceCommitDate") or ""
    ).strip()
    existing_blob_sha = str(
        existing_source.get("sourceBlobSha") or previous_blob_sha
    ).strip()
    if (
        existing_commit
        and existing_commit_date
        and (
            existing_commit == fetched_commit
            or (existing_blob_sha and existing_blob_sha == fetched_blob_sha)
        )
    ):
        return existing_commit, existing_commit_date
    return fetched_commit, fetched_commit_date


def resolve_previous_blob_sha(
    repository: str,
    path: str,
    existing_source: Dict[str, Any],
    fetched_commit: str,
    fetched_blob_sha: str,
) -> str:
    stored_blob_sha = str(existing_source.get("sourceBlobSha") or "").strip()
    if stored_blob_sha:
        return stored_blob_sha
    existing_commit = str(existing_source.get("sourceCommit") or "").strip()
    if not existing_commit:
        return ""
    if existing_commit == fetched_commit:
        return fetched_blob_sha
    return fetch_repository_blob_sha(repository, path, existing_commit)


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
    required_source_text_fields = {
        "sourceRepository",
        "sourceCommit",
        "sourceCommitDate",
        "sourceBlobSha",
        "sourceLicense",
    }
    required_source_count_fields = {
        "currentAvailableCount",
        "availableCount",
        "historicalCount",
        "includedCount",
    }
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("Every community source must be an object")
        missing_source_fields = sorted(
            field
            for field in required_source_text_fields
            if not source.get(field)
        )
        missing_source_fields.extend(
            sorted(
                field
                for field in required_source_count_fields
                if field not in source
            )
        )
        if missing_source_fields:
            raise ValueError(
                "Community source is missing required metadata: "
                + ", ".join(missing_source_fields)
            )
        current_count = int(source.get("currentAvailableCount") or 0)
        historical_count = int(source.get("historicalCount") or 0)
        source_available_count = int(source.get("availableCount") or 0)
        source_included_count = int(source.get("includedCount") or 0)
        if current_count + historical_count != source_available_count:
            raise ValueError("Source historical counts do not match availability")
        if source_included_count > source_available_count:
            raise ValueError("Source included count exceeds availability")
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
    parser.add_argument(
        "--history-from",
        action="append",
        type=Path,
        default=[],
        help="Merge cases from an older community-cases.json snapshot",
    )
    parser.add_argument(
        "--history-only",
        action="store_true",
        help="Merge snapshots without fetching current upstream data",
    )
    args = parser.parse_args()

    if args.check:
        return validate_file(args.output)

    existing_payload = load_existing_payload(args.output)
    existing_cases = list(existing_payload.get("cases") or [])
    for history_path in args.history_from:
        history_payload = load_existing_payload(history_path)
        history_cases = history_payload.get("cases")
        if not isinstance(history_cases, list):
            raise ValueError(f"History payload has no cases array: {history_path}")
        existing_cases.extend(history_cases)
    existing_source = find_source_metadata(existing_payload, SOURCE_URL)
    existing_youmind = find_source_metadata(existing_payload, YOUMIND_URL)

    if args.history_only:
        if not existing_payload:
            raise ValueError("--history-only requires an existing output payload")
        payload = accumulate_existing_payload(existing_payload, existing_cases)
        args.output.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Accumulated {len(payload['cases'])} community cases in {args.output}")
        return 0

    commit, commit_date, source_blob_sha, source_cases = fetch_source_cases()
    youmind_commit, youmind_commit_date, youmind_blob_sha, youmind_cases = (
        fetch_youmind_cases()
    )
    ensure_case_count_not_decreased(
        SOURCE_REPOSITORY, len(source_cases), existing_source
    )
    ensure_case_count_not_decreased(
        YOUMIND_REPOSITORY, len(youmind_cases), existing_youmind
    )

    previous_source_blob_sha = resolve_previous_blob_sha(
        SOURCE_REPOSITORY,
        SOURCE_CASES_PATH,
        existing_source,
        commit,
        source_blob_sha,
    )
    previous_youmind_blob_sha = resolve_previous_blob_sha(
        YOUMIND_REPOSITORY,
        YOUMIND_README_PATH,
        existing_youmind,
        youmind_commit,
        youmind_blob_sha,
    )
    source_revision, source_revision_date = choose_source_revision(
        existing_source,
        commit,
        commit_date,
        source_blob_sha,
        previous_source_blob_sha,
    )
    youmind_revision, youmind_revision_date = choose_source_revision(
        existing_youmind,
        youmind_commit,
        youmind_commit_date,
        youmind_blob_sha,
        previous_youmind_blob_sha,
    )
    payload = build_merged_payload(
        source_cases,
        source_revision,
        source_revision_date,
        source_blob_sha,
        youmind_cases,
        youmind_revision,
        youmind_revision_date,
        youmind_blob_sha,
        existing_cases,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Synced {len(payload['cases'])} community cases from "
        f"{source_revision[:8]} and {youmind_revision[:8]} to {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
