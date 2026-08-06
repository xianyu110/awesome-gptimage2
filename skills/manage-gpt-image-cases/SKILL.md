---
name: manage-gpt-image-cases
description: Build, validate, search, export, and maintain structured GPT image prompt case libraries with stable IDs, localized categories, prompt fingerprints, source attribution, and license metadata. Use when Codex needs to import prompt/image examples, deduplicate cases, query reusable prompts, update a case-library JSON pipeline, or audit provenance and schema compliance.
---

# Manage GPT Image Cases

Use one generated case library as the contract shared by sites, agents, and data jobs. Preserve stable IDs and provenance while keeping source-specific parsing outside consumers.

## Start Here

1. Locate the canonical JSON file and its build script. Prefer `data/case-library.json` and `scripts/build_case_library.py` when present.
2. Run validation before reading or editing data:

```bash
python3 <skill-dir>/scripts/case_library.py validate --data <repo>/data/case-library.json
```

3. Read [references/case-schema.md](references/case-schema.md) before adding a source, changing fields, or writing an adapter.
4. Treat generated JSON as read-only. Edit source documents, curated inputs, or source adapters, then rebuild.

## Query Cases

Search title, prompt, category, summary, source, and tags:

```bash
python3 <skill-dir>/scripts/case_library.py search \
  --data <repo>/data/case-library.json \
  --query "product image" \
  --locale en \
  --limit 10
```

Narrow by category key or source key when the request is specific:

```bash
python3 <skill-dir>/scripts/case_library.py search \
  --data <repo>/data/case-library.json \
  --category products-ecommerce \
  --source awesome-gpt-image-2
```

Use `stats` to inspect locale, source, and view counts. Use `export --format jsonl` to produce machine-friendly subsets on stdout.

## Maintain The Library

For repositories with the bundled pipeline:

```bash
python3 scripts/build_case_library.py build
python3 scripts/build_case_library.py check
python3 <skill-dir>/scripts/case_library.py validate --data data/case-library.json
```

When importing a new source:

1. Confirm a redistribution license and keep the repository, license, original URL, and upstream case URL.
2. Pin remote assets or source revisions when the upstream format allows it.
3. Normalize records into the canonical schema. Do not expose source-specific fields to site code.
4. Compute `promptHash` from lowercase, whitespace-normalized prompt text.
5. Deduplicate within a locale. Keep the first stable ID and map discarded IDs through `meta.aliases`.
6. Rebuild deterministically and require `check` to produce no diff.
7. Update tests and workflow inputs whenever a source contract changes.

## Quality Gates

Require all of the following before delivery:

- Unique canonical IDs and valid alias targets.
- Prompt hashes matching the normalized prompt text.
- Complete repository and license metadata for community records.
- Root counts matching the actual records and locale views.
- No hand edits to generated output.
- Site/runtime verification when consumers change.
- No secrets, credential-bearing URLs, or unlicensed private media.

If an upstream source becomes incomplete, below its expected minimum, or loses its license, fail the sync instead of shrinking or silently replacing the library.
