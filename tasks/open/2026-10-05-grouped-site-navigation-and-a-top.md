---
id: 2026-10-05-grouped-site-navigation-and-a-top
title: Grouped site navigation and a top-level AI hub at /ai
status: review
priority: P1
area: web
owner: claude-opus-5-5
claimed_at: 2026-10-05T02:52:31Z
created_at: 2026-10-05T02:52:26Z
completed_at:
branch: claude/determined-clarke-1laipc
depends_on: []
scope:
  - apps/web/lib/nav-links.ts
  - apps/web/lib/guides.ts
  - apps/web/components/site-navigation.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/site-footer.tsx
  - apps/web/components/nav-menu.tsx
  - apps/web/components/guides-navigation.test.tsx
  - apps/web/components/guides/topic-hub-page.tsx
  - apps/web/components/guides/ai-hub-rails.tsx
  - apps/web/components/guides/ai-hub-rails.test.tsx
  - apps/web/app/[locale]/ai
  - apps/web/app/[locale]/life/topics/[topic]
  - apps/web/e2e/site-navigation.spec.ts
  - apps/web/components/guides/topic-hub-page.test.tsx
  - apps/web/components/guides/topic-chips.test.tsx
  - apps/web/components/guides/topic-tiles.test.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/app/[locale]/life/page.test.tsx
  - apps/web/app/[locale]/search/articles/page.test.tsx
  - apps/web/app/llms.txt/route.test.ts
  - apps/web/app/sitemaps/sitemap.test.ts
  - apps/web/messages/en/navigation.json
  - apps/web/messages/en/common.json
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-CN/metadata.json
  - apps/web/messages/zh-TW/navigation.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-TW/metadata.json
---

# Grouped site navigation and a top-level AI hub at /ai

## Why

The owner found the front end cluttered and hard to search, and pointed at
maplefeather.com/page/ai-applications as the model: a short top menu with grouped
sub-sections, and one AI hub laid out by what the reader needs. Our header had three modes
with up to nine flat links, the phone sheet and bottom bar each showed a different set, and
the AI section (about 640 articles, the site's largest) sat two levels down at
`/life/topics/ai` under "生活科技".

## Definition of done

- [x] One grouped list (`navGroups` in `lib/nav-links.ts`) drives the desktop header, the
      phone menu sheet and an AI column in the footer: 旅遊情報攻略, AI 應用, 生活科技,
      旅行工具 (plain header only) and 影片.
- [x] Desktop groups open on hover or from their chevron button; Escape and an outside click
      close them; the links are always in the document for crawlers.
- [x] `/ai` is the AI family's hub, with its own title and description and need-based rails
      (方案與費用, 助手實測, 工作效率, 創作, 寫程式, AI 賺錢 when it exists, latest news);
      `guideTopicHref("life", "ai")` returns `/ai`, so canonical, sitemap, llms.txt and
      breadcrumbs follow; `/life/topics/ai` answers 308 to `/ai`, keeping its query.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
# e2e (desktop + phone): header groups, phone sheet without horizontal overflow, the 308
npx playwright test e2e/site-navigation.spec.ts
```

## Notes

- `primaryNavLinks` stays: the community panels render it as a flat "travel tools" grid.
- The rails are sub-topics, so their names and leads come from the API vocabulary in every
  language and an empty sub-topic simply drops out. `ai-income` is listed ahead of time; it
  appears once `2026-10-05-life-ai-income-investing-batch` adds the sub-topic and publishes.
- An earlier draft opened the panel on `:focus-within`, so Escape could not close it while
  focus stayed on the chevron. The panel now opens on hover or `data-open` only, and Escape
  also holds the hover off until the pointer leaves the group.
- Local e2e on 2026-10-05: the new spec passes on both projects. Of the neighbouring specs,
  `claude-code-series.spec.ts:16` needs a production build (`next start`), and
  `navigation.spec.ts:246` fails on a planner date heading (`11月11日週三`). Neither touches
  the header.
