---
id: 2026-09-16-the-life-hub-news-row-shows
title: The life hub news row shows only AI news, not crypto or tech
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-17T02:28:41Z
created_at: 2026-09-16T11:36:40Z
completed_at: 2026-09-17T02:42:21Z
branch: claude/brave-hopper-8ezxba
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

- [x] `NEWS_TOPICS` 納入 `tech-news` 與 `crypto`，
      兩個主題頁因此自動變成 `sort=news` 的一行一則清單（`isNewsTopic` 已經接好）。
- [x] `/life` 首頁那一列涵蓋三個新聞子主題，仍然依 `news_date` 由新到舊、仍然只取前 20 條。
- [x] 「看全部」的去處已決定，見下。
- [x] 測試涵蓋：三個主題的文章都會出現在首頁那一列，且排序是跨主題的 `news_date`。

## Steps

- [x] 確認了：`GET /guides` 的 `topic` **只收單值**
      （`apps/api/app/guides/router.py:68` `topic: str | None = Query(default=None, max_length=64)`），
      所以這張票是**純 web**：首頁打三次再合併。沒有動 API。
- [x] `NEWS_TOPICS` 加兩個 slug。
- [x] `/life` 首頁改成三個主題各讀一次、合併後排序。
- [x] **不需要新字串**，五語 `messages/` 沒有動（理由見下）。`check:i18n` 仍然通過。

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

## 決定：「看全部」連去哪裡

一列混合三個垂直的新聞，單一個「看全部」就沒有正確的去處——
API 的 `topic` 只收單值，站上也沒有「全部新聞」這個清單頁。

做法是**列出實際有內容的那幾個主題**，各自連到自己的主題頁，
標籤直接用該主題在該語言的 `label`，取自這一頁本來就會讀的主題詞彙
（`getGuideTopics(locale, "life")`）。因此**不需要新增任何 i18n 字串**。

這個做法有一個刻意的性質：**只有一個垂直有內容時，它就退化成今天的樣子**——
一個連結、文字仍然是「看全部」。所以幣圈與科技還沒刊出之前，畫面完全沒有變化。

## 實作要點

- `newsOrder`（`apps/web/lib/guides.ts`）是合併用的比較函式，刻意複製 API 自己的
  news keyset：`news_date` → `published_at` → `slug`，都是遞減（slug 遞增）。
  它必須跟 `apps/api/app/guides/service.py` 的 `_encode_news_cursor` 保持同步，
  註解裡寫明了這件事。
- **三次讀取各要滿額 20 筆**，不是各 7 筆。幣圈與科技從零開始，
  而某個垂直的密集一週不應該因為分配名額就把其他垂直的新聞擠掉。
- **依 slug 去重**：一個內容包可能同時掛 `crypto` 與 `ai-news`，
  那它會在兩次讀取裡各出現一次，但首頁只能有一列。
- `page.test.tsx` 原本那條「listing 只讀一次」的測試會被新的兩次讀取打到。
  它的過濾條件原本寫死 `!== "ai-news"`，改成用 `NEWS_TOPICS` 過濾——
  以後再加第四個新聞主題也不會再壞。

## 已知限制

首頁那一列取三個主題**各自最新的 20 筆**再合併取前 20。
如果某個垂直一次刊出超過 20 則、而且日期都比其他垂直新，
理論上會蓋掉其他垂直——但那正是「依新聞日期排序」本來就該有的結果，不是缺陷。
真正的限制是**不做分頁**：這一列本來就只在沒有 `?topic=` 與 `?cursor=` 的首頁出現。
