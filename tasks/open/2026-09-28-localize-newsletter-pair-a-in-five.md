---
id: 2026-09-28-localize-newsletter-pair-a-in-five
title: Localize newsletter pair A in five languages
status: review
priority: P2
area: docs
owner: codex-batch035-newsletter-pair-a
claimed_at: 2026-09-28T07:45:40Z
created_at: 2026-09-28T07:45:28Z
completed_at:
branch: codex/article-localization-035-newsletter-pair-a
depends_on: []
scope:
  - apps/api/app/guides/content/mailchimp-wordpress-newsletter.json
  - apps/api/app/guides/content/email-newsletter-planning.json
  - apps/web/public/guides/mailchimp-wordpress-newsletter
  - apps/web/public/guides/email-newsletter-planning
  - docs/article-localization/batch035-newsletter-pair-a-evidence.md
  - tasks/open/2026-09-28-localize-newsletter-pair-a-in-five.md
---

# Localize newsletter pair A in five languages

## Why

The published zh-TW versions of two newsletter guides have no zh-CN, en, ja, or ko pack documents. The source article and image assets are pinned in the Batch035 read-only inventory.

## Definition of done

- [x] Both packs contain full, reviewed five-language documents with localized source titles, alt text, and correct publication-aware links.
- [x] Each added locale has a matching text-bearing hero and diagram, with a raster hero rendered from its SVG source.
- [x] Scoped pack, image, and task checks pass; a reviewable PR records the publication state.

## Steps

- [x] Verify live source and pack SHA, branch from current origin/main, and claim this exact scope.
- [x] Author four target locales per article and 24 localized assets.
- [x] Run review and checks, then open PR.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug mailchimp-wordpress-newsletter --slug email-newsletter-planning` from `apps/api`; run scoped tests, image render QA, and `npm run check:tasks`. See the batch evidence document for checks and source hashes.

## Notes

2026-09-28 inventory: both source packs match published zh-TW v4. Their target locales are unpublished. Linked targets also have only zh-TW published, so target-language article links must remain non-clickable until corresponding locale publication.

Current source pack paths and root metadata were rechecked against `origin/main` `55e75518e147adcf54dcdda7055be1e79fef4262`; no drift. See `docs/article-localization/batch035-newsletter-pair-a-evidence.md` for validation and publication state.

Draft PR: https://github.com/x812033727/travel_scanner/pull/899. Await independent content review and CI before merge; deploy/import/publish/browser verification are separate steps.
