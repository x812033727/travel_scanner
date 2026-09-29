---
id: 2026-09-28-localize-batch043-google-ranking-and-trends
title: Localize Batch043 Google ranking and Trends guides
status: done
priority: P2
area: api
owner: codex-batch043-root
claimed_at: 2026-09-28T17:03:00Z
created_at: 2026-09-28T16:14:34Z
completed_at: 2026-09-28T17:14:11Z
branch: codex/article-localization-043-search-a
depends_on: []
scope:
  - apps/api/app/guides/content/google-ranking-history.json
  - apps/api/app/guides/content/google-trends-research.json
  - apps/web/public/guides/google-ranking-history
  - apps/web/public/guides/google-trends-research
  - docs/article-localization/batch043-pair-a-evidence.md
---

# Localize Batch043 Google ranking and Trends guides

## Why

Both published life articles have only zh-TW documents. Add four full translations and localized text-bearing images while preserving the exact source documents and root metadata.

## Definition of done

- [x] Eight complete locale documents preserve all 33 blocks and original source links/check dates.
- [x] All 24 localized assets render correctly and the coordinator has reviewed language, source parity, numbers and image text.
- [x] Local pack and content/link tests pass; stricter inherited editorial intake failures are separately recorded.
- [x] Hash-bound evidence and five-language desktop/mobile standalone previews are ready for the draft PR.

## Steps

- [x] Verify the pinned read-only production source receipt and repository baseline.
- [x] Translate the full documents and adapt SVG masters plus JPEG covers.
- [x] Independently review all eight documents; correct zh-CN terminology and re-render.
- [x] Record exact hashes, test outcomes, source editorial findings and separate release requirements.

## How to verify

Run the two-slug `pack_cli lint --kind life`, `pytest tests/test_guides_content_links.py tests/test_guides_content_pack.py -q`, `npm run check:tasks` and `git diff --check`. Evidence is in `docs/article-localization/batch043-pair-a-evidence.md`.

## Notes

The authoring subagent stopped at quota. Root took over the claimed scope, independently reviewed its drafts and applied the explicit zh-CN terminology correction list. Source/root metadata remain parsed-identical to main. Local tests: 12 passed / 5 database tests skipped. Strict source intake still reports inherited missing summary and duplicate self-reference findings, tracked by the separate editorial ticket in PR #951. No production write, import or publication occurred; release awaits the isolated rehearsal and later live validation.
