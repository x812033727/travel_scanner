---
id: 2026-09-28-localize-wordpress-plugin-translation-and-social
title: Localize WordPress plugin translation and social embeds guides
status: in-progress
priority: P2
area: docs
owner: codex-batch034-two-guides
claimed_at: 2026-09-28T03:42:49Z
created_at: 2026-09-28T03:42:43Z
completed_at:
branch: codex/batch034-two-unblocked-guides
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-plugin-theme-translation.json
  - apps/api/app/guides/content/wordpress-social-embeds.json
  - apps/web/public/guides/wordpress-plugin-theme-translation
  - apps/web/public/guides/wordpress-social-embeds
---

# Localize WordPress plugin translation and social embeds guides

## Why

The two published WordPress guides only have zh-TW content. Readers in en, ja,
ko, and zh-CN need complete text and localized diagrams before those locales
can be released. The separate Batch034 source-link fixes for two other guides
remain under review and are outside this task.

## Definition of done

- [x] Both packs contain complete en, ja, ko, zh-CN documents while their
  existing zh-TW documents and pack metadata remain unchanged.
- [x] Each new document preserves source URLs and check dates, block structure,
  ArticleInline targets, rights credits, and 1600×900 image dimensions.
- [x] Each new locale has a matching hero SVG, raster JPG, and diagram SVG;
  rendered text has no missing glyphs, overlap, or overflow.
- [ ] Draft PR is reviewed and merged. Import and publication are separate
  guarded release steps and are not part of this content PR.

## Steps

- [x] Verify origin/main source and the published zh-TW v4 documents before
  translation. Neither selected pack conflicted with the live source.
- [x] Translate all four target locales, including titles, descriptions,
  paragraphs, lists, tables, callouts, image text/alt/captions, link text, and
  source titles.
- [x] Render and inspect localized visuals and run structural/content checks.
- [x] Run scoped lint, relevant API tests, and task validation.
- [ ] Open draft PR; retain the task in review until merge.

## How to verify

- `cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --slug wordpress-plugin-theme-translation`
- `cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --slug wordpress-social-embeds`
- `cd apps/api && uv run pytest -q tests/test_guides_content_pack.py tests/test_guides_content_links.py tests/test_guide_rich_blocks.py`
- `npm run check:tasks` and `git diff --check`
- Compare zh-TW and pack metadata with `origin/main`, plus locale block types,
  source URL/check-date pairs, ArticleInline slugs, and referenced image paths.

## Notes

- Source GuideDocument hashes checked against published v4: plugin/theme
  `1b0cd4a99c4f2991a7fb58dc2a2130795c8c9acd91c8853a33d7f452c79b2baa`;
  social embeds `e5505097397a27f85088d9210ca3ffdeada633ecac59741bbcd098fece4e66bb`.
- Social embeds uses 32 blocks and five sources per locale. Plugin/theme uses
  31 blocks and five sources per locale. Each pack has two ArticleInline links.
- At preparation time, multilingual-site and map-form-embeds target articles
  were only published in zh-TW. Website-backup and themes-plugins-install had
  five published locales. ArticleInline keeps the correct target slug; the
  front end must render an unpublished target locale as plain text.
- Lint passed on both packs. Existing `no_summary` warnings remain; complete
  English translations exceed the life-guide length guideline (6,678 and
  6,251 characters), without dropping source content.
- Related API tests: 23 passed, 7 skipped. `npm run check:tasks` passed with
  warnings from unrelated longstanding task claims. No import, production
  write, or publication has occurred.
