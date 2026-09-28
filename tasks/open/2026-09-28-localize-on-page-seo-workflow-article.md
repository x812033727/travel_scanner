---
id: 2026-09-28-localize-on-page-seo-workflow-article
title: Localize on-page SEO workflow article
status: in-progress
priority: P2
area: docs
owner: codex-batch041-pair-b-content
claimed_at: 2026-09-28T14:29:51Z
created_at: 2026-09-28T14:29:43Z
completed_at:
branch: codex/article-localization-041-seo-b
depends_on: []
scope:
  - apps/api/app/guides/content/on-page-seo-workflow.json
---

# Localize on-page SEO workflow article

## Why

The on-page SEO guide is already published in zh-TW, but zh-CN, en, ja and ko
are absent. Add complete translations from the pinned published zh-TW v4 while
preserving the original document and publication state.

## Definition of done

- [x] Four complete locale documents retain all 32 source block types, examples,
      caveats, list/table structure, source URLs/dates and translated labels.
- [x] Root metadata and zh-TW stay parsed-identical to the pinned source.
- [x] Two related-reading labels remain translated plain-text inlines because
      the destination locales are not confirmed public.
- [ ] Independent review, focused checks and a green PR complete.
- [ ] Guarded import/publication and public browser verification receive
      separate receipts.

## Steps

- [x] Confirmed the read-only production v4 baseline and source SHA.
- [x] Installed the re-audited four-locale candidate after correcting two
      rich-paragraph block types in external staging.
- [ ] Complete peer review, tests and PR with the paired artwork.

## How to verify

Compare root metadata and zh-TW with the source pack SHA in Notes; run
`uv run python -m app.guides.pack_cli lint --slug on-page-seo-workflow` from
`apps/api`, then content-link tests, `npm run check:i18n`,
`npm run check:tasks` and `git diff --check`. Review every localized
block and asset render before PR. CI and production acceptance remain separate.

## Notes

Read-only receipt
`C:\Users\x8120\.codex\article-localization-release\batch041-seo-readonly-inventory-20260928\receipt-20260928T134834Z.json`
confirms public active article v2, zh-TW draft/published v4 matching the
repository, and four target locales absent. Original source pack SHA-256:
`2f27bcb83a1e327b29ed7584d2bbfa3208954251c72aaf0e13192f07f813b9a7`.
The corrected external combined candidate SHA-256:
`7532179b8bcc2124bfdfb6f49ce4a480fc165dd1f8516b555a1f8e81567e496e`.
It is staged in
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-b\onpage-draft`.
No deployment, import or publication occurred.
