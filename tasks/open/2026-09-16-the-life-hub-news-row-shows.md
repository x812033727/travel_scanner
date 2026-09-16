---
id: 2026-09-16-the-life-hub-news-row-shows
title: The life hub news row shows only AI news, not crypto or tech
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-16T11:36:40Z
completed_at:
branch:
depends_on:
  - 2026-09-16-news-batch-4-0-crypto-and
scope:
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
---

# The life hub news row shows only AI news, not crypto or tech

## Why

站主 2026-09-16 要求 `/life` 開頭先列「最新新聞」。PR #537 把它做成
依 `news_date` 排序的 `NewsList`（首頁前 20 條），並留了擴充點：

```ts
// apps/web/lib/guides.ts
export const LIFE_NEWS_TOPIC = "ai-news";
export const NEWS_TOPICS: readonly string[] = [LIFE_NEWS_TOPIC];
```

`NEWS_TOPICS` 的註解自己寫明：「Add a topic here when it starts carrying dated
news packs with `news_date`」。

`2026-09-16-news-batch-4-0-crypto-and`（PR #536）加了 `tech-news` 與 `crypto`
兩個新聞子主題。**內容一刊出，這兩個垂直就會是「帶 `news_date` 的新聞包」，
但不會出現在首頁那一列，它們的主題頁也還是卡片而不是新聞清單。**

## Definition of done

- [ ] `NEWS_TOPICS` 納入 `tech-news` 與 `crypto`，
      兩個主題頁因此自動變成 `sort=news` 的一行一則清單（`isNewsTopic` 已經接好）。
- [ ] `/life` 首頁那一列涵蓋三個新聞子主題，仍然依 `news_date` 由新到舊、仍然只取前 20 條。
- [ ] 「看全部」有合理去處——現在連 `guideTopicHref("life", LIFE_NEWS_TOPIC)`，
      三個主題之後要決定連哪裡。**這是這張票要決定的事**，不是實作細節。
- [ ] 測試涵蓋：三個主題的文章都會出現在首頁那一列，且排序是跨主題的 `news_date`。

## Steps

- [ ] 先確認 `GET /guides` 的 `topic` 參數能不能收多值。
      收不到的話，首頁那一列要嘛打三次再合併排序，要嘛改 API——
      **先確認再動手**，這決定這張票是純 web 還是要跨到 api。
- [ ] `NEWS_TOPICS` 加兩個 slug。
- [ ] `/life` 首頁的取法改成涵蓋三個主題。
- [ ] 若需要新的標題或「看全部」字串，五語 `messages/` 都要補，並過 `npm run check:i18n`。

## How to verify

```bash
npm run test:web && npm run check:i18n && npm run lint:web && npm run typecheck:web
```

再用 `next dev` 開 `/zh-TW/life`，確認三種新聞都在開頭那一列、
順序是跨主題依 `news_date`，並確認 `?topic=ai` 的畫面仍然沒有那一列。

## Notes

- **`depends_on` 是內容票，不是 #536。** 詞彙已經在 #536 裡了，
  但 `NEWS_TOPICS` 加了空主題只會得到兩個空清單頁。
  **等 4.1／4.2 有文章刊出再做**，或做了之後接受短期的空狀態（`ListingEmpty` 已經有）。
- #537 已經把 `isNewsTopic` 接到 `topic-hub-page.tsx` 的預設排序與渲染，
  所以主題頁那半邊**不用改程式**，加進 `NEWS_TOPICS` 就會生效。
- 原本這張票寫的是「`LIFE_NEWS_TOPIC` 寫死在 `life/page.tsx`」——
  #537 之後常數搬到 `lib/guides.ts` 並多了 `NEWS_TOPICS` 這個擴充點，
  scope 與做法都已依此更新。
