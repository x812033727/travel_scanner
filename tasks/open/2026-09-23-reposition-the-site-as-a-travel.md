---
id: 2026-09-23-reposition-the-site-as-a-travel
title: Reposition the site as a travel and life guide for AdSense review
status: in-progress
priority: P1
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-23T16:35:59Z
created_at: 2026-09-23T16:34:36Z
completed_at:
branch: claude/confirm-failure-reason-dpoe3a
depends_on: []
scope:
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/page.test.tsx
  - apps/web/components/home-guides.tsx
  - apps/web/components/home-guides.test.tsx
  - apps/web/components/guides-navigation.test.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/components/site-footer.test.tsx
  - apps/web/app/llms.txt/route.test.ts
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-CN/metadata.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/en/navigation.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/zh-TW/navigation.json
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
---

# Reposition the site as a travel and life guide for AdSense review

## Why

AdSense rejected mokaair.com on 2026-09-23 as 缺乏價值的內容 (low value content). The
technical side is fine (ads.txt, robots, sitemap, about/contact/privacy all answer), so the
review is about what a reviewer sees:

- The site calls itself 完整旅程比價 in every `<title>`, but most indexed pages are the
  lifestyle section: about 940 zh-TW articles plus 193 in each other locale, on AI tools,
  WordPress, SEO and personal finance. A reviewer sees a flight-comparison tool that is
  mostly unrelated articles.
- The home page is the search form and destination chips: about 1,500 characters of text
  and no link into the articles that make up most of the site.

The owner chose (2026-09-23) to keep every lifestyle topic indexed and present the site as
a general travel-and-life guide instead of hiding topics with `noindex`.

## Definition of done

- [ ] The site title, description and share preview say what the site is in all five
      locales: 旅行與生活的實用指南.
- [ ] The navigation calls the lifestyle section 生活科技 rather than 生活分享.
- [ ] The home page, server-rendered and whether discovery is on or off, has a short
      original paragraph on what the site is and who runs it, then the latest travel,
      tech and money articles, each block linking to its hub.

## Steps

- [x] `metadata.json`: `title`, `description`, `ogTitle`, `ogDescription`, `lifeTitle`,
      `lifeDescription` in five locales.
- [x] `navigation.json`: `life` in five locales.
- [x] `components/home-guides.tsx`: three `getGuideList` reads (travel how-tos, the `ai`
      topic, the `finance` topic), rendered with `GuideCard`; a block with no articles is
      left out so an API failure costs only that block.
- [x] Render it after `DiscoveryHomeGate` in `app/[locale]/page.tsx`, outside the gate, so
      it is in the response in both discovery states.
- [x] Tests, `npm run check:i18n`, lint, typecheck.

## How to verify

```bash
curl -sL https://mokaair.com/zh-TW | grep -o '<title>[^<]*'
curl -sL https://mokaair.com/zh-TW | grep -c 'href="/zh-TW/life/'
```

## Notes

- 2026-09-23: code done on `claude/confirm-failure-reason-dpoe3a`; lint, i18n, typecheck and
  `test:web` (3215 tests) pass. The Definition of done boxes wait on a deploy. The
  `生活分享` label also appeared in four navigation and llms.txt tests, now in scope.

- Out of this task and left to the owner: the 關於 page body is a site page edited in the
  admin (`SiteInformationPage`), not code. It should say the site covers travel and
  tech/money, who writes, how AI assistance and fact-checking are used, and how to ask for
  corrections.
- `common.json` `guides.lifeHubTitle` (the `/life` H1, still 生活分享) is not changed here:
  `common.json` is in the scope of `2026-09-07-add-a-meal-to-a-day`, which is in review.
- Batch publication should pause while the site is under review: 940 articles in nine days
  (2026-09-14 to 09-22) is the strongest low-value signal and no code change removes it.
  Re-request review after 4-8 weeks of indexing.
- Article dates stay as published. Back-dating was considered and rejected: Google dates a
  page by its first crawl (the sitemap was first read 2026-09-21), so it would not help and
  reads as manipulation.
