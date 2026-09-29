---
id: 2026-09-28-batch037-pair-a-localize-stp-persona
title: Batch037 Pair A: localize STP persona research and social media planning
status: done
priority: P1
area: docs
owner: codex-batch037-pair-a
claimed_at: 2026-09-28T10:57:18Z
created_at: 2026-09-28T10:57:09Z
completed_at: 2026-09-28T13:26:49Z
branch: codex/article-localization-037-social-a
depends_on: []
scope:
  - apps/api/app/guides/content/stp-persona-research.json
  - apps/api/app/guides/content/social-media-planning.json
  - apps/web/public/guides/stp-persona-research
  - apps/web/public/guides/social-media-planning
  - docs/article-localization/batch037-pair-a-evidence.md
  - tasks/open/2026-09-28-batch037-pair-a-localize-stp-persona.md
  - tasks/done/2026-09-28-batch037-pair-a-localize-stp-persona.md
---

# Batch037 Pair A: localize STP persona research and social media planning

## Why

Both articles are published only in `zh-TW`. Readers of the other four site languages
cannot access a complete article with matching, readable artwork. This task authors the
missing locale packs and assets for review while preserving the published source.

## Definition of done

- [x] Each article has complete `zh-CN`, `en`, `ja`, and `ko` documents and localized
  hero/diagram artwork, with the original `zh-TW` document and root metadata unchanged.
- [x] The packs, browser-rendered artwork, publication-aware links, and source/asset
  integrity pass scoped validation and independent review.
- [x] A draft PR contains this exact two-article scope and evidence; release remains
  gated separately.

## Steps

- [x] Revalidate pinned repository source and obtain a fresh read-only production
  source/version snapshot.
- [x] Translate every reader-visible field and text-bearing graphic; render JPG covers.
- [x] Run structural/hash audit, scoped pack/API/web checks, and browser visual review.
- [x] Open a draft PR for review.

## How to verify

See `docs/article-localization/batch037-pair-a-evidence.md` for the SHA-pinned source,
preflight, audit, and browser receipts. Commands:

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --kind life --slug stp-persona-research --slug social-media-planning
uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py tests/test_guides_links.py tests/test_guide_rich_blocks.py -q
cd ../..
npm run check:i18n
npm run check:tasks
npm run typecheck:web
npm run test:web -- components/content-blocks.test.tsx components/guides/guide-image.test.tsx components/guides/article.test.tsx components/guides/article-page.test.tsx lib/guides.test.ts
```

The five-file web run passed four files/123 tests and timed out starting the remaining
worker under concurrent test load. `article.test.tsx` passed separately (40 tests).

## Notes

Draft PR: https://github.com/x812033727/travel_scanner/pull/911. The branch was
rebased onto `origin/main` `b00b917fa1463b84ecf1524d459176d3fc0b43c7` before
opening it; that main update only added unrelated newsletter articles. Original
starting `origin/main` was `5329ad8920300fec4fda06ded8bd006607a72d4f`.
The pinned inventory's original pack and asset hashes match that checkout. A fresh
four-lock `READ ONLY` production snapshot on 2026-09-28 confirmed both articles
active/published with `zh-TW` v4 source matching the inventory and no target locale
rows. The independent Pair B review passed document structure, source and link
preservation, and 16 SVG browser renders. Pack lint has only inherited `no_summary`
and English-length advisories. PR #911 subsequently passed all nine checks and was
merged at 2026-09-28T13:04:26Z as merge commit
`ebde813d6a7fa9cdd8282bfa2400d002c0a6add8`. This closes the authoring and
review task. No production deployment, import, or publication occurred as part of
this task; those are separate approval and release steps.
