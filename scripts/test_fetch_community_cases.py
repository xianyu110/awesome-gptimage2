#!/usr/bin/env python3

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch_community_cases import (
    build_merged_payload,
    build_payload,
    merge_cases,
    normalize_image,
    parse_youmind_cases,
)


class CommunityCaseSyncTests(unittest.TestCase):
    def test_normalizes_case_and_pins_image_to_commit(self) -> None:
        payload = build_payload(
            [
                {
                    "id": 7,
                    "title": "Sample case",
                    "category": "Products & E-commerce",
                    "image": "/images/case7.jpg",
                    "prompt": "Create a product image",
                    "styles": ["Product"],
                    "scenes": ["Commerce"],
                    "sourceLabel": "Example",
                    "sourceUrl": "https://example.com/source",
                    "githubUrl": "https://example.com/case",
                }
            ],
            "abc123",
            "2026-01-01T00:00:00Z",
        )

        item = payload["cases"][0]
        self.assertEqual(item["id"], "community-7")
        self.assertEqual(item["categoryZh"], "电商与产品")
        self.assertEqual(
            item["image"],
            "https://cdn.jsdelivr.net/gh/"
            "freestylefly/awesome-gpt-image-2@abc123/data/images/case7.jpg",
        )
        self.assertEqual(payload["meta"]["count"], 1)

    def test_keeps_absolute_images(self) -> None:
        self.assertEqual(
            normalize_image("https://example.com/image.jpg", "abc123"),
            "https://example.com/image.jpg",
        )

    def test_parses_youmind_readme_case(self) -> None:
        markdown = """# Gallery
## 📋 All Prompts

### No. 1: Profile / Avatar - Sample Portrait

![Language-EN](badge)

#### 📖 Description

A polished portrait.

#### 📝 Prompt

```
Create a polished portrait
```

#### 🖼️ Generated Images

<img src="https://example.com/portrait.jpg" width="700">

#### 📌 Details

- **Author:** [Example](https://example.com/author)
- **Source:** [Twitter Post](https://example.com/post)

**[👉 Try it now →](https://youmind.com/gpt-image-2-prompts?id=42)**
"""

        cases = parse_youmind_cases(markdown)

        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0]["id"], "youmind-42")
        self.assertEqual(cases[0]["categoryZh"], "角色与一致性")
        self.assertEqual(cases[0]["sourceLabel"], "Example")
        self.assertEqual(cases[0]["prompt"], "Create a polished portrait")
        self.assertEqual(cases[0]["sourceUrl"], "https://example.com/post")

    def test_merge_cases_deduplicates_normalized_prompts(self) -> None:
        first = {
            "id": "first",
            "title": "First",
            "category": "Other",
            "image": "https://example.com/first.jpg",
            "prompt": "Create   an image",
            "caseUrl": "https://example.com/first",
        }
        duplicate = {
            **first,
            "id": "duplicate",
            "prompt": " create an IMAGE ",
        }

        self.assertEqual(
            [item["id"] for item in merge_cases([first], [duplicate])], ["first"]
        )

    def test_builds_multi_source_metadata(self) -> None:
        source = [
            {
                "id": 7,
                "title": "Primary",
                "category": "Other Use Cases",
                "image": "https://example.com/primary.jpg",
                "prompt": "Primary prompt",
                "githubUrl": "https://example.com/primary",
            }
        ]
        youmind = [
            {
                "id": "youmind-8",
                "title": "Secondary",
                "category": "Other Use Cases",
                "source": "youmind-awesome-gpt-image-2",
                "image": "https://example.com/secondary.jpg",
                "prompt": "Secondary prompt",
                "caseUrl": "https://example.com/secondary",
            }
        ]

        payload = build_merged_payload(
            source, "abc123", "2026-01-01", youmind, "def456", "2026-01-02"
        )

        self.assertEqual(payload["meta"]["count"], 2)
        self.assertEqual(len(payload["meta"]["sources"]), 2)
        self.assertEqual(payload["meta"]["duplicatePromptCount"], 0)


if __name__ == "__main__":
    unittest.main()
