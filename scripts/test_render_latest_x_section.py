#!/usr/bin/env python3

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_latest_x_section import (  # noqa: E402
    END_MARKER,
    START_MARKER,
    normalize_groups,
    render_section,
    replace_between_markers,
)


class LatestXSectionTests(unittest.TestCase):
    def test_normalizes_flat_items_by_date(self) -> None:
        groups = normalize_groups(
            {
                "items": [
                    {"created_at": "2026-04-29T10:00:00Z", "prompt": "A"},
                    {"created_at": "2026-04-28T10:00:00Z", "prompt": "B"},
                    {"created_at": "2026-04-29T11:00:00Z", "prompt": "C"},
                ]
            }
        )

        self.assertEqual([group["date"] for group in groups], ["2026-04-29", "2026-04-28"])
        self.assertEqual(groups[0]["count"], 2)

    def test_render_section_uses_metadata_and_item_limit(self) -> None:
        payload = {
            "meta": {
                "generated_at_utc": "2026-04-29T16:54:01Z",
                "model": "grok-4.1",
                "count": 3,
                "date_count": 1,
            },
            "dates": [
                {
                    "date": "2026-04-29",
                    "items": [
                        {"author": "One", "prompt": "Prompt one"},
                        {"author": "Two", "prompt": "Prompt two"},
                        {"author": "Three", "prompt": "Prompt three"},
                    ],
                }
            ],
        }

        output = render_section(payload, max_items=2)

        self.assertIn("条目数：`3`", output)
        self.assertIn("#### 1. @One", output)
        self.assertIn("#### 2. @Two", output)
        self.assertNotIn("@Three", output)

    def test_replaces_only_marked_section(self) -> None:
        content = f"before\n{START_MARKER}\nold\n{END_MARKER}\nafter\n"

        updated = replace_between_markers(content, "new section\n")

        self.assertEqual(
            updated,
            f"before\n{START_MARKER}\n\nnew section\n\n{END_MARKER}\nafter\n",
        )


if __name__ == "__main__":
    unittest.main()
