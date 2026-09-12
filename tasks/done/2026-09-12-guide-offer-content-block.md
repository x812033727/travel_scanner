---
id: 2026-09-12-guide-offer-content-block
title: Rich guide blocks — images with credits, tables, callouts, in-article partner buttons, hero and share card
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-12T17:42:16Z
created_at: 2026-09-12T05:36:19Z
completed_at: 2026-09-12T17:55:02Z
branch: claude/travel-guide-10-posts-56a1a9
depends_on:
  - 2026-09-12-affiliate-cta-guides-and-city-pages
scope:
  - apps/api/app/site_pages/schemas.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/service.py
  - apps/api/tests/test_guides.py
  - apps/web/lib/content-blocks.ts
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/card.tsx
  - apps/web/app/[locale]/guides/[kind]/[slug]/page.tsx
  - apps/web/app/[locale]/guides/[kind]/[slug]/page.test.tsx
  - apps/web/app/[locale]/life/[slug]/page.tsx
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - docs/travel-guides.md
  - docs/seo.md
  - docs/affiliate-configuration.md
---

# Rich guide blocks — images with credits, tables, callouts, in-article partner buttons, hero and share card

## Why

The article system (`/guides`, `/life`) had the publication machinery of a blog and the body
of a memo: four block types (heading, paragraph, list, link), no picture anywhere, no table
for a fare comparison, no way to place a partner button next to the paragraph that earns it,
and a share card that was the site logo for every article. Ten launch articles about airport
transfers, transit passes and itineraries need all of those, and the owner asked for the
architecture to change where it could not deliver a good blog.

Originally filed as "guide-only offer content block"; widened here because the four pieces
touch the same files and ship together. The dependency on `2026-09-09-site-experience-settings`
was dropped: that task is `blocked`, `blocked` holds no scope, and the reason it was listed
(not adding `messages/*` keys) no longer applies now that the message catalogs have moved on.

## Definition of done

- [x] An article body may carry `image` (self-hosted `/guides/<slug>/…` path, alt, size,
      caption, credit with author/licence/source), `table`, `callout` and `offer` blocks, and
      an optional raster `hero`; the legal pages' four-block union is untouched and their
      editor never meets the new blocks.
- [x] The reader sees the hero (eager, credited), a disclosure line when the body carries
      partner buttons, a table of contents from three sections, the body sliced around each
      `offer` block with the same `DestinationAffiliateOptions` island the end panel uses,
      an end panel that skips modules already placed inline, the update date when the
      article was republished, a reading time, and related travel articles.
- [x] Listing cards show the hero; the share card (`og:image`, Twitter) and the `Article`
      JSON-LD (`image`, `dateModified`) use it; without a hero the site card inherits.
- [x] The write path refuses more than three `offer` blocks, an offer without a city on a
      cross-destination article, and an offer naming a city the catalog does not know — on
      create, new translation, draft save, publish and restore, never on withdrawal.
- [x] The admin editor adds and edits every new block (tables typed as text), the hero and
      its credit, and previews partner blocks as placeholders without fetching offers.
- [x] Five-locale message keys for the reader (`common.guides.*`) and the editor
      (`admin.guides.*`), and the docs describe the rules.

## Steps

- [x] API: `safe_http_url` shared from `site_pages/schemas.py`; `GuideBlock`, `HeroImage`,
      `ImageCredit` in `guides/schemas.py`; `_validate_document` in `admin_service.py`;
      `PublicSummary.hero`; tests for round-trip, limits and malformed blocks.
- [x] Web: `RichContentBlock` + `contentImageSrc` + `licenseUrl` (`lib/content-blocks.ts`),
      renderer with figure/table/callout/heading ids/same-site links, `GuideBlock`,
      `splitGuideBlocks`, `guideHeadings`, `readingMinutes` (`lib/guides.ts`), the article,
      the page (metadata through `parent`, JSON-LD, related reading), the card, the editor.
- [x] Messages in five locales; `docs/travel-guides.md`, `docs/seo.md`,
      `docs/affiliate-configuration.md`.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_guides.py tests/test_site_pages.py tests/test_error_localization.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/content-blocks.test.tsx lib/guides.test.ts lib/guides.server.test.ts app/sitemap.test.ts components/guides/article.test.tsx "app/[locale]/guides/[kind]/[slug]/page.test.tsx" "app/[locale]/life/[slug]/page.test.tsx" components/admin-guides-panel.test.tsx
```

Then in the back office: create an article, add a hero, an image, a table, a callout and an
offer block, preview (placeholder, no `/affiliates/*` request), save, publish; open the
article: hero eager with credit, disclosure line, contents, the offer island where the block
was, the end panel without that module, `og:image` pointing at the hero.

## Notes

- New blocks live in `guides/schemas.py`, not the shared `site_pages` union:
  `admin-site-pages-panel.tsx` renders `textarea value={block.text}` for every non-list block,
  so widening the shared union would break typecheck and write `text` onto an image block.
- The offer rules are enforced in `admin_service._validate_document`, not as pydantic
  validators: the model also validates every stored revision on the public read path, and a
  destination retired from the catalog must degrade to "no button", never a 500.
- `guide_offer_*` errors are raised only from `admin_service.py`, which
  `tests/test_error_localization.py` exempts (path contains `admin`); they need no
  translations, and `content_pack.py` (next task) must not author its own `AppError`s.
- Next replaces a whole top-level metadata key, so the page reads the layout's resolved
  `openGraph` through the `parent` argument and restates `siteName`/`locale`/`alternateLocale`
  next to the hero. `localeUrl` must not be used for the image: it inserts the locale segment.
- `ContentBlocks` has no `"use client"` and stays offer-free; `article.tsx` interleaves
  renderer slices with client islands, and the admin preview renders a placeholder between
  slices. Heading ids are numbered across the whole body (`headingStart` per slice).
- `tools/check-i18n.mjs` scans comments too: a Han character in a `.tsx` comment fails CI.
- Not done here: per-article click attribution (`2026-09-12-attribute-affiliate-clicks-to-the-guide`),
  the content pack and import command, and the articles themselves (two sibling tasks).
