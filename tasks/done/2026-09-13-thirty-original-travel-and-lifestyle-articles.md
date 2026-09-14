---
id: 2026-09-13-thirty-original-travel-and-lifestyle-articles
title: Thirty original travel and lifestyle articles batch 5
status: done
priority: P2
area: docs
owner: codex
claimed_at: 2026-09-13T22:59:47Z
created_at: 2026-09-13T22:59:27Z
completed_at: 2026-09-14T04:23:47Z
branch: codex/travel-articles-batch5
depends_on: []
scope:
  - apps/api/app/guides/content
  - apps/web/public/guides
  - docs/article-batch-5
---

# Thirty original travel and lifestyle articles batch 5

## Why

Continue the editorial collection with 30 distinct Traditional Chinese articles across travel and everyday life. Every article needs an original or licensed image, useful prose and sources, without repeating existing subjects.

## Definition of done

- [x] 15 travel how-to and 15 lifestyle packs authored with sources, tables, callouts and internal links.
- [x] 30 original AI hero illustrations and 30 original SVG diagrams are local, credited and sized for the web.
- [x] Repository baseline and live public indexes compared; no repeated title, slug, full article or hero.
- [x] All packs validate; all 30 new articles import, publish and read in disposable SQLite, with an idempotent rerun.
- [x] Complete editorial preview and image provenance are available in docs/article-batch-5.
- [x] Content reviewed and merged. Production publication remains a separate action.

## Steps

- [x] Claim scope in an isolated worktree based on origin/main, preserving the unrelated original checkout.
- [x] Research primary sources, author unique subjects, generate and inspect original images.
- [x] Check Traditional Chinese text, image size, sources, taxonomy, links and local import behavior.
- [x] Build and inspect the review preview.

## How to verify

From the repository root, run `apps/api/.venv/Scripts/python.exe docs/article-batch-5/verify_batch.py` and `npm run check:tasks`. From apps/api, run `.venv/Scripts/python.exe -m pytest tests/test_guides_content_pack.py -q`. Open docs/article-batch-5/index.html through a local static server to inspect all 30 articles; manifest.json, validation.json and live-baseline.json contain review evidence.

## Notes

2026-09-14 closeout: GitHub PR #468 is MERGED at 2026-09-14T02:20:35Z, merge commit a4ee0f50770334051c7e2618a2138617875a1b40. This closes the repository-content task and releases its broad directory claim; it does not assert that all 30 articles were published in production.

Base is e8a62c94, with 70 repository packs. Browser checks on 2026-09-14 found 41 published zh-TW how-to articles corresponding to that baseline and 40 additional AI-themed lifestyle articles. New daily-life subjects are distinct. Unpublished admin drafts were not accessed. The 30 new articles are not imported or published in production. User explicitly allowed generated images; each hero is labeled AI-generated/non-photographic. No application code, migration or existing pack changed.
