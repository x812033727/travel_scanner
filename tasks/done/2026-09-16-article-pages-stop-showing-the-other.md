---
id: 2026-09-16-article-pages-stop-showing-the-other
title: Article pages stop showing the other-language list
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-16T13:49:39Z
created_at: 2026-09-16T13:48:48Z
completed_at: 2026-09-16T15:25:24Z
branch: claude/jolly-dirac-yg32tb
depends_on: []
scope:
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
  - apps/web/app/(ads-public)/[locale]/life/[slug]/page.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
---

# Article pages stop showing the other-language list

## Why

Every published article ended with an "其他語言版本" section listing the same article in the
other languages it is published in. The site owner does not want it shown: the header's
language switcher already moves a reader between languages on the same path, and the
translations are declared to search engines in the head, so the list under the article only
repeated what the page already says and pushed the end of the article further down.

Hiding the section is not the same as dropping hreflang. `guideArticleMetadata` still builds
`alternates.languages` from `published_locales` (plus `x-default` when English exists), so
crawlers keep every translation; only the reader-facing list goes.

## Definition of done

- [x] A published article ends at its sources — no language heading, no per-language link.
- [x] The head still declares every published locale (`alternates.languages`, `x-default`).
- [x] The "not translated yet" screen keeps its language links: that screen exists to hand the
      reader a language that does have the article.
- [x] No dead copy left behind: `guides.otherLanguages` is gone from all five catalogs and the
      label is gone from `GuideArticleLabels`.

## Steps

- [x] `article.tsx`: drop the `others` list, the section, and the now-unused `localeLabels`,
      `Locale` and `guideHref` imports.
- [x] `article-page.tsx`: stop passing the label.
- [x] `messages/<locale>/common.json`: remove `guides.otherLanguages` in all five.
- [x] Tests: the two page tests that asserted the visible links now assert the head declares
      them and the body lists none; `article.test.tsx` gains the same guard.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

Then open any article published in more than one language (for example
`/zh-TW/life/ai-news-siri-ai-ios-27-20260914`): the page ends with 來源, and
`view-source` still shows `<link rel="alternate" hreflang="…">` for each published locale.

## Notes

- Merged as #538 (squash, `9d1257d7`). Locally green before the push — full web suite
  (288 files, 3110 tests), `lint:web`, `check:i18n`, `typecheck:web`, `test:tools` — and every
  CI job green on the merge head, `web` included.
- `docs/travel-guides.md` still lists "other languages" as the last thing an article draws,
  in "What a travel article looks like" (line 734 when this was written, 766 after #536 grew
  the file — the section name is the stable reference). That file is held by
  `2026-09-16-news-date-field-and-news-list`, so the one-line correction is filed separately
  as `2026-09-16-travel-guides-doc-article-ending`.
- The unavailable/untranslated screen in `article-page.tsx` keeps its own list of published
  locales; it is the only place a reader is offered another language by link.
