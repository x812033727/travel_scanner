---
id: 2026-09-16-stop-showing-article-counts-and-lesson
title: Stop showing article counts and lesson numbers; series move into topics
status: in-progress
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-16T06:13:26Z
created_at: 2026-09-16T06:05:00Z
completed_at:
branch: claude/hub-counts-and-series-topics
depends_on: []
scope:
  - apps/web/components/guides
  - apps/web/components/gemini-series
  - apps/web/components/codex-learning
  - apps/web/app/[locale]/life
  - apps/web/app/[locale]/guides
  - apps/web/app/[locale]/search/articles
  - apps/web/app/llms.txt
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guide-series-copy.ts
  - apps/web/lib/codex-learning/copy.ts
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/e2e/gemini-series.spec.ts
  - apps/web/e2e/claude-code-series.spec.ts
  - docs/article-architecture.md
  - docs/seo.md
---

# Stop showing article counts and lesson numbers; series move into topics

## Why

#531 上線當天站主看過正式站後提出三件事：

1. 生活分享首頁的「系列與教學中心」不該在首頁，應該出現在各個主題裡面。
2. 所有篇數都不要顯示：首頁「639 篇文章／9 個主題」、主題卡「352 篇」、系列卡
   「50 篇完整教學…」、主題頁「85 篇文章」。**理由是數字會一直增加，顯示出來就一直是錯的。**
3. 不要寫「第幾篇」：文章頁的「第 1／50 篇」與總目錄的 `01`、`02`。同一個理由。

站主另外確認：邊界數字全部拿掉（「還有 3 個子主題」、搜尋結果數、`llms.txt` 裡的數字），
課程編號兩種格式都拿掉，首頁的系列區塊完全移除。

## Definition of done

- [x] 兩個首頁（`/life`、`/guides`）沒有統計列、主題卡沒有篇數、沒有「系列與教學中心」區塊。
- [x] 主題頁出現該主題的系列卡；父主題頁（`ai`）列出底下所有子主題的系列。
- [x] 讀者看得到的地方沒有任何目錄大小或課程序號。
- [x] 排序、上一篇／下一篇、主題頁 `noindex`、hreflang、sitemap、搜尋分頁全部不受影響。
- [x] 三個 `aria-live` 篩選回饋仍然會講話，只是不講數字。

## Steps

- [x] 首頁：`HubHero` 拿掉 `stats`，移除 `SeriesRow` 與 `sectionArticleCount()`。
- [x] `topic-hub-page.tsx`：`reads()` 加 `getSeriesIndex`，在工具列前插入該主題的 `SeriesRow`。
- [x] 顯示層拿掉篇數：`topic-tiles`、`topic-chips`、`listing-toolbar`、`topic-hub-page`、
      `guides/[kind]/page`、`series-row`、`destination-groups`、`search/articles/page`、`llms.txt/route`。
- [x] 顯示層拿掉序號：`gemini-series/navigation`、`gemini-series/directory`、`guides/series-hub`、
      `guides/series-navigation`、`codex-learning/hub`（含寫死六課的「01–06」單元範圍）。
- [x] 五語系 `common.json` 刪鍵與改寫，`guide-series-copy.ts` 的 `results` 一起改。
- [x] 測試與兩個 e2e。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

逐頁看：`/zh-TW/life`、`/zh-TW/guides`（沒有統計列與系列區塊）、`/zh-TW/life/topics/ai`
（三張系列卡、沒有篇數）、`/zh-TW/life/topics/ai-chat`（只有 Gemini）、`/zh-TW/life/gemini-guide`
（目錄沒有 `01`）、`/zh-TW/life/gemini-beginner-guide`（沒有「第 1／50 篇」，但上下篇仍正確）、
`/llms.txt`（沒有數字，仍挑到篇數最多的語系）。

## Notes

**數字留在資料裡，只拿掉畫面。** 每一個要拿掉的數字，它的欄位同時是邏輯來源：

- `TopicOption.count` / `.counts`：空主題不顯示、主題頁 `noindex`、hreflang（`topicLocales`）、sitemap 子項
- `SeriesEntry.number` / `Lesson.number`：排序、上下篇、學習路線、指令錨點；
  `apps/web/lib/guide-series.ts:35` 的 runtime guard 硬性要求它存在，拿掉會讓整個系列驗證失敗
- `GuideSearchResult.total`：搜尋分頁
- `DestinationFacet.count`：濾掉沒有文章的城市
- `SitemapSummary.counts`：sitemap index 子檔、hub 是否為空

所以 **API 契約一行都不要改**，`apps/api/tests/test_guides.py` 與 `test_guide_series.py` 的 count 斷言不用動。
`sectionArticleCount()` 會變成死碼可以刪，但 `guideSitemapSummary()` 不能刪（sitemap 還在用）。

系列→主題不需要新資料：`series_registry.json` 五個系列都已經有 `topic`，
`SeriesSummary.topic` 早就在 wire 上（`schemas.py:836`）也已經在 `guide-series.ts:44` 驗證，
只是從來沒有頁面讀它。五個 topic（`claude-code`、`codex`、`ai-chat`、`ai-terms`、`ai-search`）
的 parent 全是 `ai`（`taxonomy.py:96-110`），所以父主題頁會是主要入口。

內容包裡寫死的數字（標題「81 個概念」「10 篇看懂差在哪」、描述「五十篇教學」，以及 73 個包正文的
「第 N 篇」）不在這張票裡 —— `apps/api/app/guides/content` 正被
`2026-09-15-content-summary-howto-and-life` 佔著，另開 `2026-09-16-content-packs-counts-in-hub-titles`。

做完後補記：

- 三個 `role="status" aria-live` 的篩選回饋整段內容原本就是數字。直接刪掉會讓讀螢幕的人
  完全收不到「篩選生效了」，所以改成 `sr-only` 加一句不含數字的字串：`geminiSeries.count`
  改名 `filtered`、`guide-series-copy.ts` 的 `results` 改名 `filtered`、
  `codex-learning/copy.ts` 位置陣列補第 36 格。看得見的數字沒了，回饋還在。
- `ChipRow` 的 `moreLabel` 仍是 `(count) => string`，因為美食與熱點也用同一個元件、
  而且它們的數字不在這次範圍內。這裡只傳一個忽略參數的函式。
- `claude-code-series.spec.ts` 原本用「第 61 篇練習材料」當連結名稱找元素。那句話是內容、
  正要被上面那張票改掉，所以先改成用 `href` 定位，免得內容一改這個 e2e 就紅。
- **本機 `node_modules` 是 vitest 4.1.11，lockfile 鎖的是 5.0.0。** 版本不對時
  `components/mobile-nav.test.tsx` 會紅（`it.each` 兩個案例共用同一個 `vi.fn()`，
  vitest 4 不會自動清），在乾淨的 `main` 上也一樣紅，CI 則是綠的。跑測試前先確認
  `node -p "require('./node_modules/vitest/package.json').version"`。
