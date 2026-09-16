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
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/app/[locale]/life/page.test.tsx
---

# The life hub news row shows only AI news, not crypto or tech

## Why

站主 2026-09-16 要求 `/life` 開頭先列「最新新聞」（`docs/article-architecture.md` Phase 5,
`life-hub-redesign-web`）。實作是 `apps/web/app/[locale]/life/page.tsx` 的

```ts
const LIFE_NEWS_TOPIC = "ai-news";
```

**一個字串，一個子主題。** `2026-09-16-news-batch-4-0-crypto-and` 之後站上有三個新聞
子主題（`ai-news`、`tech-news`、`crypto`），但那一列永遠只會顯示 AI 新聞。
幣圈與科技新聞刊出後會直接看不到——除非讀者自己走到該主題的 hub。

這不是批次 4.0 的範圍（那張票不碰 web），但它是內容刊出前必須先落地的一步，
否則新垂直等於沒有入口。

## Definition of done

- [ ] `/life` 第一頁的「最新新聞」列同時涵蓋三個新聞子主題，最新在前。
- [ ] 「看全部」連到哪裡有明確答案（三個 hub 不能只連其中一個）——
      可能要一個新的落點，或改成連 `/life/topics/<各自>`，這是這張票要決定的事。
- [ ] 只在第一頁出現的既有規則不變（`?topic=` 或 `?cursor=` 的畫面不顯示這一列）。
- [ ] 若需要新的標題字串，五語 `messages/` 都要補，並通過 `npm run check:i18n`。

## Steps

- [ ] 決定資料取法：`getGuideList` 目前吃單一 `topic`。三個子主題要嘛三次請求後合併排序，
      要嘛 API 支援多主題查詢——先確認 `GET /guides` 的 `topic` 參數能不能收多值，
      不能的話這張票要先決定是改 API 還是在 web 合併。
- [ ] 常數從 `LIFE_NEWS_TOPIC` 改成清單，並讓「看全部」有合理去處。
- [ ] `page.test.tsx` 補上三個子主題都會出現在那一列的斷言。

## How to verify

```bash
npm run test:web && npm run check:i18n && npm run lint:web && npm run typecheck:web
```

再用 `next dev` 開 `/zh-TW/life`，確認三種新聞都出現在開頭那一列、順序是最新在前，
並確認 `?topic=ai` 的畫面仍然沒有那一列。

## Notes

- 詞彙由 `2026-09-16-news-batch-4-0-crypto-and` 的 migration `0079` 種下，
  所以這張票 `depends_on` 它：`tech-news` 與 `crypto` 在那之前不存在。
- 內容還沒寫。這張票可以先落地，列會是空的或只有 AI 新聞，
  等批次 4.1／4.2 的文章刊出後自然填滿；`ListingEmpty` 已經有空狀態。
