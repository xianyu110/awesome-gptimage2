# Case Library Schema

## Contents

- Root contract
- Case contract
- Locale views
- Source adapter contract
- Compatibility and aliases
- Quality checks

## Root Contract

`schemaVersion` identifies the contract. Reject unsupported versions rather than guessing field meanings.

`meta` contains derived values:

| Field | Meaning |
| --- | --- |
| `totalRecords` | Canonical records after locale-aware deduplication |
| `uniquePrompts` | Distinct normalized prompt fingerprints |
| `duplicateRecordsRemoved` | Input records removed during the build |
| `aliases` | Removed ID to canonical ID mapping |
| `localeCounts` | Records stored for `und`, `zh-CN`, and `en` |
| `viewCounts` | Records visible in each localized consumer |
| `sourceCounts` | Canonical records grouped by source key |
| `generatedFrom` | Repository-relative inputs used by the build |

`cases` is the ordered canonical record array. Preserve deterministic ordering so generated diffs remain reviewable.

## Case Contract

| Field | Rules |
| --- | --- |
| `id` | Stable lowercase identifier; never recycle it for different content |
| `locale` | `und` for shared community records, otherwise `zh-CN` or `en` |
| `title` | Display title in the record locale or upstream language |
| `category.key` | Stable machine key used by filters and exports |
| `category.labels` | Localized display labels keyed by locale |
| `source.key` | Stable grouping key such as `local` or an upstream adapter key |
| `source.kind` | `local` or `community` |
| `source.label` | Author, publication, or guide label shown to users |
| `source.repository` | Required for community records |
| `source.license` | Required redistribution license for community records |
| `source.originalUrl` | Original creator post when available |
| `source.caseUrl` | Upstream case or gallery page when available |
| `badge` | Localized badge labels |
| `image.url` | Public preview URL; may be empty for text-only local records |
| `summary` | Localized short descriptions |
| `prompt` | Full reusable prompt, never a truncated preview |
| `promptHash` | SHA-256 of lowercase whitespace-normalized prompt text |
| `tags` | Deduplicated style, scene, or topical tags |

The authoritative JSON Schema is `schema/case-library.schema.json` in compatible repositories.

## Locale Views

A localized consumer includes records where `case.locale` is `und` or matches the requested locale. It localizes labels by trying the requested locale, then `en`, then `zh-CN`, then the first available value.

Do not duplicate shared community records for each language. This keeps one prompt, image, and attribution record authoritative.

## Source Adapter Contract

An adapter must:

1. Resolve a stable upstream revision when supported.
2. Enforce a conservative minimum record count so format drift cannot erase the library.
3. Return complete prompt, image, title, source, and case URLs.
4. Record the upstream repository and license in root source metadata.
5. Preserve author attribution without claiming upstream endorsement.
6. Fail on malformed required fields instead of manufacturing content.

Keep adapter parsing separate from canonical normalization. Consumers must never know the upstream README or API shape.

## Compatibility And Aliases

When duplicate records already have public IDs, retain the first canonical record and add each removed ID to `meta.aliases`. Consumers should resolve aliases before opening deep links or reading favorites.

Do not use aliases to hide unrelated ID changes. An alias is valid only when the prompt fingerprint and locale match the canonical record.

## Quality Checks

- Validate generated output after every build.
- Compare a fresh in-memory build with the committed file in check mode.
- Confirm root counts, source counts, locale counts, and view counts.
- Require community license and repository fields.
- Test at least one search and one localized view.
- Keep the build deterministic: omit current timestamps unless they come from a pinned source revision.
