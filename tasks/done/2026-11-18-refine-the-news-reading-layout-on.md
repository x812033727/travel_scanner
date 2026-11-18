---
id: 2026-11-18-refine-the-news-reading-layout-on
title: Refine the news reading layout on phones and desktops
status: done
priority: P2
area: web
owner: codex-news-layout
claimed_at: 2026-11-18T10:22:46Z
created_at: 2026-11-18T10:22:24Z
completed_at: 2026-11-18T10:35:27Z
branch: codex/news-reading-layout-20261118
depends_on: []
scope:
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/components/guides/related-grid.tsx
  - apps/web/components/guides/related-grid.test.tsx
  - apps/web/components/guides/breadcrumb.tsx
  - apps/web/components/guides/breadcrumb.test.tsx
  - apps/web/components/guides/news-reading.module.css
  - apps/web/components/content-blocks.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
---

# Refine the news reading layout on phones and desktops

## Why

On a 390px phone, the article card leaves only 316px for a diagram or paragraph. Long headlines repeat in the breadcrumb and the expanded summary and contents can put more than two screens before the first paragraph. Desktop headlines share the narrower prose column, and the entire contents and trending rail sticks even when it exceeds the viewport.

## Definition of done

- [x] Standalone dated news gets a full-width headline, a readable text column and close-to-edge mobile figures.
- [x] Readers can expand the full authored summary or chapter links using the keyboard or with JavaScript disabled.
- [x] The first ranked related story is easy to identify, lower-ranked links keep their order, and the desktop contents remains reachable.

## Steps

- [x] Compare the existing and new production frontend builds with the same published article snapshots.
- [x] Verify native disclosure behavior, source text, heading targets, original-image navigation, canonical links and the default guide layout.

## How to verify

Run the article, article-page, content-blocks, breadcrumb and related-grid Vitest suites. Run web lint, typecheck, build, check:i18n and check:tasks. In Chrome, check both Dynamo and MDASH at 320, 390, 768, 1024 and 1440px, then open the additional summary points, follow a chapter link, open the figure and go Back.

## Notes

Local production comparison with the published 2026-11-17 articles: at 390px the text column widened to 358px. The Dynamo and MDASH opening paragraphs moved from 1758/1718px to 970/954px. At 1440px both opening paragraphs moved into the 900px viewport. Fifteen browser cases covered five languages and a JavaScript-disabled reader. News summary markup retains all authored text for the reader and the existing speakable selector.
