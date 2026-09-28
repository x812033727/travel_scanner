---
id: 2026-09-28-prepare-batch042-technical-roadmap-art
title: Prepare Batch042 technical SEO and learning roadmap localized art
status: in-progress
priority: P2
area: web
owner: codex-batch042-pair-b
claimed_at: 2026-09-28T15:06:09Z
created_at: 2026-09-28T15:06:00Z
completed_at:
branch: codex/article-localization-042-seo-b
depends_on: []
scope:
  - apps/web/public/guides/technical-seo-checklist
  - apps/web/public/guides/seo-learning-roadmap
  - docs/article-localization/batch042-pair-b-evidence.md
---

# Prepare Batch042 technical SEO and learning roadmap localized art

## Why

The published Traditional Chinese technical SEO and beginner roadmap guides use text-bearing cover and diagram art. Four missing language versions need their own legible art before their article packs can be reviewed or published. The article JSON files are separately claimed by the source-link correction task and must not be edited here.

## Definition of done

- [x] Each guide has a cover SVG, rendered JPG, and diagram SVG in zh-CN, en, ja, and ko; the original Traditional Chinese art is unchanged.
- [x] An external, source-bound four-language content candidate exists for each guide, with corrected source links from PR #942 and no article JSON edit in this branch.
- [x] Browser-rendered text bounds and desktop/mobile standalone article previews have reviewable receipts.
- [ ] Merge the scoped art/evidence PR; keep the article-pack installation and production release as separate guarded steps.

## Steps

- [x] Pin the read-only production and corrected source baselines.
- [x] Translate all 32 blocks and source titles in each guide; preserve URLs, dates, audience, caveats, links, credit, and dimensions.
- [x] Localize 16 SVGs, render eight 1600×900 JPG covers, and review text and image layout.
- [x] Lint staged candidate packs and render 16 standalone desktop/mobile article previews.
- [ ] Open an art/evidence PR after scoped commit and peer review; do not touch the claimed source packs.

## How to verify

`uv run python -m app.guides.pack_cli --content-dir <external lint-packs> --public-dir <this checkout>/apps/web/public lint --slug technical-seo-checklist --slug seo-learning-roadmap` returned zero errors. `node <external>/render_art.cjs` reported 16/16 SVGs with no canvas/card overflow or text overlap. `node <external>/preview_pages.cjs` passed 16/16 desktop/mobile standalone views. `npm run check:tasks` passed (existing stale/overlap warnings elsewhere on the board). See `docs/article-localization/batch042-pair-b-evidence.md` for exact receipt hashes and paths.

## Notes

The source-link fix is draft PR #942. Source pack SHA-256 after correction: `technical-seo-checklist` `a5f692c99703c5b15e683fd4543d7438c6179d46042f8336f8abaee6cdcc5e08`; `seo-learning-roadmap` `5d4d982e675e03e7cf3b9840e5ce26488bf7dbc8f54a40f75c7113fdd7635dd5`. Recheck exact bytes before a later JSON installation. External candidates and QA receipts are under `C:/Users/x8120/.codex/article-localization-release/batch042-pair-b/`; this branch changes only its two claimed art directories, this task, and its evidence file. The original sources have no summary block, and the faithful English bodies exceed the advisory 6,000-character life-guide target; the pack linter reports warnings, not errors. No production write or release occurred.
