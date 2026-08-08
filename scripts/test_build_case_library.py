#!/usr/bin/env python3

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_case_library import (  # noqa: E402
    README_SOURCES,
    build_payload,
    parse_prompt_library,
    prompt_hash,
    search_cases,
)


class CaseLibraryBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = build_payload()

    def test_parses_local_prompt_libraries(self) -> None:
        zh_path, zh_section = README_SOURCES["zh-CN"]
        en_path, en_section = README_SOURCES["en"]

        self.assertEqual(len(parse_prompt_library(zh_path, "zh-CN", zh_section)), 56)
        self.assertEqual(len(parse_prompt_library(en_path, "en", en_section)), 16)

    def test_builds_expected_locale_views(self) -> None:
        meta = self.payload["meta"]

        self.assertEqual(meta["totalRecords"], 772)
        self.assertEqual(meta["uniquePrompts"], 772)
        self.assertEqual(meta["duplicateRecordsRemoved"], 8)
        self.assertEqual(meta["viewCounts"], {"zh-CN": 755, "en": 692})

    def test_preserves_aliases_for_removed_duplicates(self) -> None:
        aliases = self.payload["meta"]["aliases"]

        self.assertEqual(aliases["supp-en-01"], "en-prompt-2")
        self.assertEqual(aliases["supp-appso-02"], "zh-prompt-30")

    def test_prompt_hashes_match_canonical_text(self) -> None:
        for item in self.payload["cases"]:
            self.assertEqual(item["promptHash"], prompt_hash(item["prompt"]))

    def test_search_respects_locale(self) -> None:
        results = search_cases(self.payload, "skincare", "en", 10)

        self.assertTrue(results)
        self.assertTrue(all(item["locale"] in {"und", "en"} for item in results))


if __name__ == "__main__":
    unittest.main()
