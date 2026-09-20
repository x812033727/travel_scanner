---
id: 2026-09-20-article-localization-verified-site-links
title: Localize verified same-site guide links in article translation jobs
status: in-progress
priority: P1
area: tools
owner: codex-batch006-link-tool
claimed_at: 2026-09-20T12:35:56Z
created_at: 2026-09-20T12:35:27Z
completed_at:
branch: codex/batch006-localize-site-links
depends_on: []
scope:
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
  - tools/article-localization/README.md
---

# Localize verified same-site guide links in article translation jobs

## Why

Batch006 has three published zh-TW LinkBlock URLs in four translated jobs each.
The pipeline treated URL fields as immutable, so its 12 target-language staged
documents linked back to zh-TW even though the target-language destination pages
are public. An unverified or unpublished same-site destination must not become
a clickable public link in a translated article.

## Definition of done

- [x] The three verified public routes are written with the staged document's
  locale in all four target languages; all 15 destination URLs were checked for
  HTTP 200, no redirect, matching HTML `lang` and canonical.
- [x] Unknown same-site routes, unavailable target locales and noncanonical URL
  variants stop materialization before document or asset output. External links,
  source URLs and source check dates remain unchanged.
- [x] Focused tests, lint, format and task checks pass; no content pack or asset
  is changed by this tooling PR.
- [ ] Parent review and PR merge/release decision.

## Steps

- [x] Inspect route evidence, Batch006 source jobs, article schemas and existing
  publication assembler; close the completed overlapping AI-credit task.
- [x] Add a narrow verified-route mapping at pipeline materialization and tests
  for all five locales, external/source preservation and refusal paths.
- [ ] Open an independent PR without merging, deploying or publishing.

## How to verify

`apps/api/.venv/Scripts/python.exe tools/article-localization/test_pipeline.py`
(using an existing API venv), `ruff check tools/article-localization/pipeline.py
tools/article-localization/test_pipeline.py`, `ruff format --check` on the same
two files, `git diff --check`, and `npm run check:tasks`. Also exercise the
helper against the 12 external Batch006 source jobs without writing to them.

## Notes

The reviewed routes are `/guides/howto`, `/destinations/hanoi`, and
`/destinations/singapore`. The read-only route verification JSON is SHA-256
`84dd8fcdd5102b61b314873a56096f91c5c9673c796b9cb1f8e495796d5a135f`.
Its 15 rows all have status 200, no redirect, matching `html_lang` and canonical.
Only URL values of LinkBlock and rich-paragraph link nodes are rewritten; the
translation field allowlist still excludes URLs. Publication assembly applies
its separate article-link checks, and release must recheck current route status.
The Hanoi zh-TW source sentence is under a separate editorial HOLD.
