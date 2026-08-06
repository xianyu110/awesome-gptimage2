#!/usr/bin/env python3

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fetch_community_cases import build_payload, normalize_image


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


if __name__ == "__main__":
    unittest.main()
