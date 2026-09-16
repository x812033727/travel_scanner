---
id: 2026-09-15-summary-faq-definedterm-jsonld-web
title: 渲染摘要卡與 FAQ，JSON-LD 加 abstract／speakable／FAQPage／DefinedTerm
status: review
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:50:37Z
created_at: 2026-09-15T13:57:48Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-summary-and-faq-blocks-api
  - 2026-09-15-term-link-popover-related-grid-web
  - 2026-09-14-aio-article-citations-and-llms-txt
  - 2026-09-14-heading-anchors-for-h3
scope:
  - apps/web/lib/content-blocks.ts
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/lib/structured-data.ts
  - apps/web/lib/structured-data.test.ts
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
  - docs/seo.md
---

# 渲染摘要卡與 FAQ，JSON-LD 加 abstract／speakable／FAQPage／DefinedTerm

## Why

摘要與 FAQ 要在讀者頁面上看得到、機器也讀得到；詞條文章應以 `DefinedTerm` 標示別名與所屬詞彙表。

## Definition of done

- [x] summary 渲染為描述下方的卡（`#article-summary`），faq 為 `<details>` 段落；含新區塊的文件仍通過 `isPublishedGuide`。
- [x] JSON-LD：有摘要出 `abstract`＋`speakable`；有 faq 才出 `FAQPage`；有 term 別名出 `DefinedTerm{alternateName, inDefinedTermSet}`。
- [x] 後台可新增／編輯兩種區塊；`docs/seo.md` 記錄 Google 2023 起限制 FAQ rich result，價值在 AEO 與讀者。

## Steps

- [x] 型別與 guard；渲染器；`article.tsx` 位置。
- [x] `structured-data.guideArticle` 輸入擴充與測試。
- [x] 後台編輯器最小版。

## How to verify

```bash
cd apps/web && npx vitest run lib/structured-data.test.ts components/content-blocks.test.tsx components/guides "app/(ads-public)"
```
把文章頁 JSON-LD 貼到 validator.schema.org。

## Notes

保留 `structured-data.ts` 檔尾對 HowTo／爬來的 FAQPage 的否決紀錄並引用。

2026-09-16 落地：

- 型別在 `lib/content-blocks.ts`（`SummaryBlock`／`FaqBlock` 進 `RichContentBlock`，guard 檢查 2–5／2–10 且非空）；`lib/content-blocks.test.ts` 原本就不存在，guard 測試放 `components/content-blocks.test.tsx`。
- `splitArticleExtras()` 把兩個區塊從 body 抽出：`article.tsx` 在描述下方畫 `<SummaryCard id="article-summary">`、在資料來源前畫 `<FaqSection id="article-faq">`；`ContentBlocks` 也會畫（後台預覽用）。
- JSON-LD：`guideArticle` 多 `abstract`（句子以空白串接）＋`speakable{cssSelector:["#article-summary"]}`；`faqPage()` 與 `definedTerm()` 是獨立 graph，
  只在頁面有對應內容時進 `StructuredData` 陣列（null 會被丟掉）。檔尾對「從標題推 FAQPage」的否決保留並補註日期。
- DefinedTerm 的判定來自 API `term_set`（目錄型系列的 hub）；`alternateName` 用 `aliases` 去掉與標題相同者。
- 後台：`blockTypes` 加 summary／faq，各只能加一個（已有就不出現按鈕）；摘要用多行 textarea、FAQ 每題兩欄＋新增／移除。
