---
id: 2026-10-05-lifestyle-articles-stop-ending-with-the
title: Lifestyle articles stop ending with the same unrelated travel posts
status: done
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-10-05T02:06:15Z
created_at: 2026-10-05T02:06:10Z
completed_at: 2026-10-05T02:30:23Z
branch: claude/project-thread-qwwuzx
depends_on: []
scope:
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/app/(ads-public)/[locale]/life/[slug]/page.test.tsx
  - docs/travel-guides.md
---

# Lifestyle articles stop ending with the same unrelated travel posts

## Why

Every lifestyle article (`/life/{slug}`: AI, tech, crypto and finance pieces included) ended
with a "最新旅遊情報攻略" block holding the three newest travel guides on the whole site and
a row of one city per country. Checked on production 2026-10-05: `tech-news-spanner-omni-ga-20260930`,
`finance-glossary-50-terms` and `ai-term-kv-cache` all closed with the same Vung Tau day
trip, Okinawa-without-a-car and Okinawa lodging-tax cards. Nothing about those cards follows
from the article, so the block read as filler under a topical "同主題延伸閱讀" list.

## Definition of done

- [x] A lifestyle article that names no destination ends with its own related reading and
      backlinks only: no travel cards, no destination chips.
- [x] A lifestyle article that names a destination still hands over to travel, but with
      travel guides about that destination and that country's cities, never the site-wide
      newest.

## Steps

- [x] Gate the handover on `destination_id` and fetch travel guides filtered by it.
- [x] Tests for both cases in `article-page.test.tsx` and the `/life/[slug]` page test.
- [x] Update "The end of a lifestyle article" in `docs/travel-guides.md`.

## How to verify

`cd apps/web && npx vitest run components/guides/article-page.test.tsx`, then after deploy
open `/zh-TW/life/ai-term-kv-cache`: the page ends at "引用本文的文章" with no
"最新旅遊情報攻略" section.

## Notes

- Tech and finance articles are `kind: "life"` and render at `/life/{slug}` through the
  same `renderGuideArticle` as `/guides/[kind]/[slug]`; the off-topic block was the
  lifestyle `travelCrosslinks` handover, not the API's `related` list, which is already
  topic-ranked (`apps/api/app/guides/links.py`, `related_articles`).
- The travel-article path (`relatedTravel`) was already destination- then topic-matched and
  is untouched.
