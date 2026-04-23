#!/usr/bin/env python3
"""Fetch latest X prompts via APIPRO chat completion and save as JSON."""

from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple
from urllib import error, request


def env_int(name: str, default: int, min_value: int, max_value: int) -> int:
    raw = os.getenv(name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(min_value, min(max_value, value))


def iso_utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_base_url(value: str) -> str:
    base = value.strip() or "http://apipro.maynor1024.live/v1"
    return base.rstrip("/")


def post_chat_completion(
    base_url: str,
    api_key: str,
    model: str,
    query: str,
    lookback_hours: int,
    max_items: int,
    min_views: int,
    min_retweets: int,
    timeout_seconds: int,
) -> Dict[str, Any]:
    endpoint = f"{base_url}/chat/completions"

    system_prompt = (
        "You are a structured data collector. "
        "Directly fetch latest public posts from X and return JSON only."
    )

    user_prompt = (
        "Task: collect high-performing X posts related to GPT-Image-2 prompts.\n"
        f"Lookback hours: {lookback_hours}\n"
        f"Search query intent: {query}\n"
        f"Max items: {max_items}\n"
        f"Min views: {min_views}\n"
        f"Min retweets: {min_retweets}\n"
        "Rules:\n"
        "1) Deduplicate by URL or text similarity.\n"
        "2) Keep only posts with reusable, non-empty prompt content.\n"
        "3) Must satisfy both: view_count >= min_views and retweet_count >= min_retweets.\n"
        "4) Exclude spam/ads/giveaway-only/unrelated model content.\n"
        "5) Rank by high engagement first, then newer first.\n"
        "6) Every item must include a non-empty prompt string.\n"
        "7) Include x_url for every item. Include image_urls when the post visibly contains image links or media URLs.\n"
        "8) If a post has no prompt, exclude it entirely.\n"
        "9) Do not fabricate metrics or image links. If unknown, set null or [] as appropriate.\n"
        "Output strictly as JSON object:\n"
        "{"
        "\"meta\":{"
        "\"source\":\"x\","
        "\"lookback_hours\":24,"
        "\"query\":\"...\","
        "\"count\":0,"
        "\"filters\":{\"min_views\":1000,\"min_retweets\":20}"
        "},"
        "\"items\":["
        "{"
        "\"x_url\":\"\","
        "\"url\":\"\","
        "\"author\":\"\","
        "\"created_at\":\"\","
        "\"text\":\"\","
        "\"prompt\":\"\","
        "\"reason\":\"\","
        "\"image_urls\":[],"
        "\"primary_image_url\":\"\","
        "\"view_count\":0,"
        "\"retweet_count\":0,"
        "\"like_count\":0,"
        "\"reply_count\":0,"
        "\"engagement_score\":0"
        "}"
        "]"
        "}"
    )

    payload = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    req = request.Request(
        endpoint,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "awesome-gptimage2-apipro/1.0",
        },
        data=json.dumps(payload).encode("utf-8"),
    )

    with request.urlopen(req, timeout=timeout_seconds) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def should_retry_error(message: str) -> bool:
    text = (message or "").lower()
    retry_signals = [
        "heavy usage",
        "try again later",
        "\"code\":8",
        "http 429",
        "http 500",
        "http 503",
        "timeout",
        "temporarily unavailable",
    ]
    return any(signal in text for signal in retry_signals)


def call_with_retry_and_fallback(
    base_url: str,
    api_key: str,
    models: List[str],
    query: str,
    lookback_hours: int,
    max_items: int,
    min_views: int,
    min_retweets: int,
    timeout_seconds: int,
    max_retries: int,
    retry_seconds: int,
) -> Tuple[Dict[str, Any], str]:
    last_error: Exception | None = None
    retries = max(0, max_retries)
    base_delay = max(1, retry_seconds)
    print(f"Model chain: {', '.join(models)}", file=sys.stderr)

    for model in models:
        print(f"Trying model={model}", file=sys.stderr)
        for attempt in range(retries + 1):
            try:
                resp = post_chat_completion(
                    base_url=base_url,
                    api_key=api_key,
                    model=model,
                    query=query,
                    lookback_hours=lookback_hours,
                    max_items=max_items,
                    min_views=min_views,
                    min_retweets=min_retweets,
                    timeout_seconds=timeout_seconds,
                )
                return resp, model
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="ignore")
                msg = f"HTTP {exc.code}: {body[:700]}"
                last_error = RuntimeError(msg)
                can_retry = should_retry_error(msg)
            except Exception as exc:  # pragma: no cover
                msg = str(exc)
                last_error = exc
                can_retry = should_retry_error(msg)

            if attempt < retries and can_retry:
                delay = base_delay * (2 ** attempt)
                print(
                    f"Retrying model={model} attempt={attempt + 1}/{retries} "
                    f"after {delay}s due to transient error...",
                    file=sys.stderr,
                )
                time.sleep(delay)
                continue

            print(
                f"Model failed: {model}; reason={msg[:180]}; trying next fallback if available.",
                file=sys.stderr,
            )
            break

    raise RuntimeError(str(last_error) if last_error else "APIPRO request failed")


def extract_message_content(resp: Dict[str, Any]) -> str:
    choices = resp.get("choices", [])
    if not choices:
        raise ValueError("No choices in completion response")
    message = choices[0].get("message", {})
    content = message.get("content", "")
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict):
                if isinstance(part.get("text"), str):
                    text_parts.append(part["text"])
                elif part.get("type") == "text" and isinstance(part.get("content"), str):
                    text_parts.append(part["content"])
        content = "\n".join(text_parts).strip()
    if not isinstance(content, str) or not content.strip():
        raise ValueError("No message content in completion response")
    return content.strip()


def strip_code_fence(content: str) -> str:
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text


def parse_json_flexible(content: str) -> Dict[str, Any]:
    candidates: List[str] = [strip_code_fence(content)]

    match = re.search(r"\{[\s\S]*\}", content)
    if match:
        candidates.append(match.group(0).strip())

    last_error: Exception | None = None
    for text in candidates:
        try:
            obj = json.loads(text)
            if isinstance(obj, dict):
                return obj
            raise ValueError("Model content is not a JSON object")
        except Exception as exc:  # pragma: no cover
            last_error = exc
    raise ValueError(f"Invalid model output JSON: {last_error}")


def to_int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if not cleaned:
            return None
        try:
            if "." in cleaned:
                return int(float(cleaned))
            return int(cleaned)
        except ValueError:
            return None
    return None


def normalize_string_list(value: Any) -> List[str]:
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if not isinstance(value, list):
        return []

    items: List[str] = []
    for raw in value:
        if not isinstance(raw, str):
            continue
        text = raw.strip()
        if text and text not in items:
            items.append(text)
    return items


def normalize_item(item: Dict[str, Any]) -> Dict[str, Any]:
    x_url = str(item.get("x_url") or item.get("url") or "").strip()
    image_urls = normalize_string_list(item.get("image_urls"))
    primary_image_url = str(item.get("primary_image_url") or "").strip()
    if primary_image_url and primary_image_url not in image_urls:
        image_urls.insert(0, primary_image_url)
    if not primary_image_url and image_urls:
        primary_image_url = image_urls[0]

    return {
        "x_url": x_url,
        "url": x_url,
        "author": str(item.get("author", "")).strip(),
        "created_at": str(item.get("created_at", "")).strip(),
        "text": str(item.get("text", "")).strip(),
        "prompt": str(item.get("prompt", "")).strip(),
        "reason": str(item.get("reason", "")).strip(),
        "image_urls": image_urls,
        "primary_image_url": primary_image_url,
        "view_count": to_int_or_none(item.get("view_count")),
        "retweet_count": to_int_or_none(item.get("retweet_count")),
        "like_count": to_int_or_none(item.get("like_count")),
        "reply_count": to_int_or_none(item.get("reply_count")),
        "engagement_score": to_int_or_none(item.get("engagement_score")),
    }


def item_has_required_fields(item: Dict[str, Any]) -> bool:
    if not item.get("prompt"):
        return False
    if item.get("primary_image_url"):
        return True
    if item.get("image_urls"):
        return True
    return bool(item.get("x_url"))


def item_sort_key(item: Dict[str, Any]) -> Tuple[int, str, str]:
    engagement = item.get("engagement_score")
    created_at = str(item.get("created_at") or "")
    prompt = str(item.get("prompt") or "")
    return (engagement or -1, created_at, prompt)


def resolve_date_key(created_at: str, fallback_date: str) -> str:
    text = (created_at or "").strip()
    if len(text) >= 10 and re.match(r"^\d{4}-\d{2}-\d{2}", text):
        return text[:10]
    return fallback_date


def group_items_by_date(items: List[Dict[str, Any]], fallback_date: str) -> List[Dict[str, Any]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        key = resolve_date_key(str(item.get("created_at") or ""), fallback_date)
        grouped.setdefault(key, []).append(item)

    groups: List[Dict[str, Any]] = []
    for date_key in sorted(grouped.keys(), reverse=True):
        date_items = sorted(grouped[date_key], key=item_sort_key, reverse=True)
        groups.append(
            {
                "date": date_key,
                "count": len(date_items),
                "items": date_items,
            }
        )
    return groups


def normalize_output(
    parsed: Dict[str, Any],
    base_url: str,
    model: str,
    query: str,
    lookback_hours: int,
    min_views: int,
    min_retweets: int,
) -> Dict[str, Any]:
    raw_items = parsed.get("items", [])
    normalized_items: List[Dict[str, Any]] = []
    if isinstance(raw_items, list):
        for obj in raw_items:
            if isinstance(obj, dict):
                normalized_items.append(normalize_item(obj))

    filtered_items = [item for item in normalized_items if item_has_required_fields(item)]
    filtered_items.sort(key=item_sort_key, reverse=True)

    meta_raw = parsed.get("meta", {})
    generated_at = iso_utc_now()
    fallback_date = generated_at[:10]
    date_groups = group_items_by_date(filtered_items, fallback_date)

    output = {
        "meta": {
            "generated_at_utc": generated_at,
            "source": str(meta_raw.get("source", "x")),
            "query": str(meta_raw.get("query", query)),
            "lookback_hours": int(meta_raw.get("lookback_hours", lookback_hours)),
            "count": len(filtered_items),
            "date_count": len(date_groups),
            "dropped_count": max(0, len(normalized_items) - len(filtered_items)),
            "provider": "apipro.maynor1024.live",
            "base_url": base_url,
            "model": model,
            "filters": {
                "min_views": min_views,
                "min_retweets": min_retweets,
            },
        },
        "dates": date_groups,
        "items": filtered_items,
    }
    return output


def write_json(path: str, payload: Dict[str, Any]) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> int:
    api_key = os.getenv("APIPRO_API_KEY", "").strip()
    if not api_key:
        print("Missing required env: APIPRO_API_KEY", file=sys.stderr)
        return 2

    base_url = normalize_base_url(os.getenv("APIPRO_BASE_URL", "http://apipro.maynor1024.live/v1"))
    model = os.getenv("APIPRO_MODEL", "grok-4.1-fast").strip() or "grok-4.1-fast"
    fallback_models_raw = os.getenv("APIPRO_FALLBACK_MODELS", "").strip()
    query = os.getenv(
        "APIPRO_QUERY",
        "(gptimage2 OR gpt-image-2 OR \"gpt image 2\") (prompt OR 提示词)",
    ).strip()
    lookback_hours = env_int("APIPRO_LOOKBACK_HOURS", 24, 1, 168)
    max_items = env_int("APIPRO_MAX_ITEMS", 60, 1, 200)
    min_views = env_int("APIPRO_MIN_VIEWS", 1000, 0, 10_000_000_000)
    min_retweets = env_int("APIPRO_MIN_RETWEETS", 20, 0, 10_000_000)
    timeout_seconds = env_int("APIPRO_TIMEOUT_SECONDS", 90, 10, 600)
    max_retries = env_int("APIPRO_MAX_RETRIES", 4, 0, 10)
    retry_seconds = env_int("APIPRO_RETRY_SECONDS", 8, 1, 60)
    output_file = os.getenv("APIPRO_OUTPUT_FILE", "data/latest-prompts.json").strip()
    model_candidates = [model]
    if fallback_models_raw:
        extras = [m.strip() for m in fallback_models_raw.split(",") if m.strip()]
        for item in extras:
            if item not in model_candidates:
                model_candidates.append(item)

    try:
        resp, used_model = call_with_retry_and_fallback(
            base_url=base_url,
            api_key=api_key,
            models=model_candidates,
            query=query,
            lookback_hours=lookback_hours,
            max_items=max_items,
            min_views=min_views,
            min_retweets=min_retweets,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            retry_seconds=retry_seconds,
        )
    except Exception as exc:  # pragma: no cover
        print(str(exc), file=sys.stderr)
        return 1

    try:
        content = extract_message_content(resp)
        parsed = parse_json_flexible(content)
    except Exception as exc:
        preview = (content[:500] if "content" in locals() else "").replace("\n", "\\n")
        print(f"Invalid model output JSON: {exc}", file=sys.stderr)
        if preview:
            print(f"Raw content preview: {preview}", file=sys.stderr)
        return 1

    output = normalize_output(
        parsed=parsed,
        base_url=base_url,
        model=used_model,
        query=query,
        lookback_hours=lookback_hours,
        min_views=min_views,
        min_retweets=min_retweets,
    )
    write_json(output_file, output)
    print(
        f"Saved {output['meta']['count']} prompt items across {output['meta']['date_count']} dates to {output_file}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
