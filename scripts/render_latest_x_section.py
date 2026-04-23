#!/usr/bin/env python3
"""Render the latest X prompt summary into README.md from data/latest-prompts.json."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

START_MARKER = "<!-- latest-x-prompts:start -->"
END_MARKER = "<!-- latest-x-prompts:end -->"
DEFAULT_MAX_ITEMS = 12


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    return data


def normalize_groups(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw_groups = payload.get("dates", [])
    if isinstance(raw_groups, list):
        return [group for group in raw_groups if isinstance(group, dict)]

    raw_items = payload.get("items", [])
    if not isinstance(raw_items, list):
        return []

    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        created_at = str(item.get("created_at") or "")
        date_key = created_at[:10] if len(created_at) >= 10 else "unknown"
        grouped.setdefault(date_key, []).append(item)

    return [
        {"date": date_key, "count": len(items), "items": items}
        for date_key, items in sorted(grouped.items(), reverse=True)
    ]


def format_links(item: Dict[str, Any]) -> str:
    links: List[str] = []
    x_url = str(item.get("x_url") or item.get("url") or "").strip()
    if x_url:
        links.append(f"[X 原帖]({x_url})")

    image_urls = item.get("image_urls") if isinstance(item.get("image_urls"), list) else []
    for idx, url in enumerate(image_urls[:3], start=1):
        if isinstance(url, str) and url.strip():
            links.append(f"[图片 {idx}]({url.strip()})")

    return " · ".join(links) if links else "无可用链接"


def render_item(item: Dict[str, Any], index: int) -> List[str]:
    author = str(item.get("author") or "未知作者").strip()
    created_at = str(item.get("created_at") or "").strip()
    prompt = str(item.get("prompt") or "").strip()
    reason = str(item.get("reason") or "").strip()
    lines = [f"#### {index}. @{author}"]
    meta_bits = [bit for bit in [created_at, format_links(item)] if bit]
    if meta_bits:
        lines.append(f"- {' | '.join(meta_bits)}")
    if reason:
        lines.append(f"- 备注：{reason}")
    lines.extend([
        "```text",
        prompt,
        "```",
        "",
    ])
    return lines


def render_section(payload: Dict[str, Any], max_items: int) -> str:
    meta = payload.get("meta", {}) if isinstance(payload.get("meta"), dict) else {}
    groups = normalize_groups(payload)
    generated_at = str(meta.get("generated_at_utc") or "").strip() or "--"
    model = str(meta.get("model") or "--").strip()
    total_count = int(meta.get("count") or 0)
    date_count = int(meta.get("date_count") or len(groups))

    lines = [
        "## 最新 X Prompt",
        "",
        "> 这个区块由 GitHub Action 根据 `data/latest-prompts.json` 自动生成，只展示带提示词的 X 帖子摘要。",
        "",
        f"- 更新时间：`{generated_at}`",
        f"- 模型：`{model}`",
        f"- 条目数：`{total_count}` · 日期分组：`{date_count}`",
        "- 原始数据：[`data/latest-prompts.json`](data/latest-prompts.json)",
        "",
    ]

    remaining = max(0, max_items)
    if not groups or remaining == 0:
        lines.append("_暂无数据_")
        return "\n".join(lines).strip() + "\n"

    for group in groups:
        if remaining <= 0:
            break
        date_key = str(group.get("date") or "unknown")
        items = group.get("items") if isinstance(group.get("items"), list) else []
        items = [item for item in items if isinstance(item, dict) and str(item.get("prompt") or "").strip()]
        if not items:
            continue

        lines.append(f"### {date_key}")
        lines.append("")
        for item in items[:remaining]:
            lines.extend(render_item(item, len([line for line in lines if line.startswith('#### ')]) + 1))
            remaining -= 1
            if remaining <= 0:
                break

    return "\n".join(lines).strip() + "\n"


def replace_between_markers(content: str, replacement: str) -> str:
    start = content.find(START_MARKER)
    end = content.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        raise ValueError("README markers for latest X prompts are missing")
    before = content[: start + len(START_MARKER)]
    after = content[end:]
    return before + "\n\n" + replacement.strip() + "\n\n" + after


def main() -> int:
    base_dir = Path(__file__).resolve().parents[1]
    json_path = Path(os.getenv("LATEST_X_JSON", base_dir / "data/latest-prompts.json"))
    readme_path = Path(os.getenv("LATEST_X_README", base_dir / "README.md"))
    max_items = int(os.getenv("LATEST_X_README_MAX_ITEMS", str(DEFAULT_MAX_ITEMS)))

    payload = load_json(json_path)
    rendered = render_section(payload, max_items=max_items)
    original = readme_path.read_text(encoding="utf-8")
    updated = replace_between_markers(original, rendered)
    readme_path.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
