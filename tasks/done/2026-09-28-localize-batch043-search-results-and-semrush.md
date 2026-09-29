---
id: 2026-09-28-localize-batch043-search-results-and-semrush
title: Localize Batch043 search results and Semrush workflows
status: done
priority: P1
area: docs
owner: codex-batch043-root
claimed_at: 2026-09-28T16:55:52Z
created_at: 2026-09-28T16:17:17Z
completed_at: 2026-09-28T17:04:03Z
branch: codex/article-localization-043-search-b
depends_on: []
scope:
  - apps/api/app/guides/content/search-results-clickthrough.json
  - apps/api/app/guides/content/semrush-research-workflow.json
  - apps/web/public/guides/search-results-clickthrough
  - apps/web/public/guides/semrush-research-workflow
  - docs/article-localization/batch043-pair-b-evidence.md
---

# Localize Batch043 search results and Semrush workflows

## Why

The read-only Batch043 production inventory confirms both life articles are published in zh-TW only. The active zh-TW draft and published version 4 match repository main 57eb97b9. Add the four missing language documents and all text-bearing art without changing source content, visibility, or root metadata. This branch stages content only; production remains guarded.

## Definition of done

- [x] Both packs contain complete zh-CN, en, ja, and ko documents with the original 33-block structure and publication-aware article targets.
- [x] Each new locale uses its own editable hero and diagram SVG plus 1600x900 JPEG hero; all 24 assets render without clipping or missing glyphs.
- [x] An independent reviewer accepted the exact candidates and hash-bound evidence is ready for the draft PR.

## Steps

- [x] Compare source packs with the locked read-only production inventory and check current official Google and Semrush documentation.
- [x] Translate all document fields, images, tables, callouts, link labels, and source titles while retaining source URLs and check dates.
- [x] Validate structure, pack lint, asset bounds and render previews.
- [x] Complete independent review, capture final hashes and prepare the review PR.

## How to verify

From apps/api: `uv run python -m app.guides.pack_cli lint --kind life --slug search-results-clickthrough --slug semrush-research-workflow` and `uv run pytest tests/test_guides_content_links.py tests/test_guides_content_pack.py -q`. From repository root: `npm run check:tasks` and `git diff --check`. See `docs/article-localization/batch043-pair-b-evidence.md` for source/target hashes and visual checks.

## Notes

Read-only receipt SHA-256 `003dde60b8e1849fac50dced292c1d74515e4c6b11a90abf286a3d21953a5c07`; no production writes. The source already uses ArticleInline references, including the AI term in the CTR article; they remain keyed to the same kind/slug. Lint passed with inherited no-summary advisories and full English translations just above the optional 6,000-character guideline. Original zh-TW and root metadata compare parsed-identical to main.

Root takeover: the authoring subagent stopped at its usage limit; its completed drafts were preserved. The coordinating agent separately reviewed all eight language documents and images. Local content/link tests: 12 passed, 5 database tests skipped; five-locale desktop/mobile standalone previews: 20 passed. Production import, publication and public browser verification remain pending the isolated rehearsal and separate guarded release.
