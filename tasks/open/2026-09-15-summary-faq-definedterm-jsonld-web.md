---
id: 2026-09-15-summary-faq-definedterm-jsonld-web
title: 渲染摘要卡與 FAQ，JSON-LD 加 abstract／speakable／FAQPage／DefinedTerm
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:48Z
completed_at:
branch:
depends_on:
  - 2026-09-15-summary-and-faq-blocks-api
  - 2026-09-15-term-link-popover-related-grid-web
  - 2026-09-14-aio-article-citations-and-llms-txt
  - 2026-09-14-heading-anchors-for-h3
scope:
  - apps/web/lib/content-blocks.ts
  - apps/web/lib/content-blocks.test.ts
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
  - docs/seo.md
---

# 渲染摘要卡與 FAQ，JSON-LD 加 abstract／speakable／FAQPage／DefinedTerm

## Why

摘要與 FAQ 要在讀者頁面上看得到、機器也讀得到；詞條文章應以 `DefinedTerm` 標示別名與所屬詞彙表。

## Definition of done

- [ ] summary 渲染為描述下方的卡（`#article-summary`），faq 為 `<details>` 段落；含新區塊的文件仍通過 `isPublishedGuide`。
- [ ] JSON-LD：有摘要出 `abstract`＋`speakable`；有 faq 才出 `FAQPage`；有 term 別名出 `DefinedTerm{alternateName, inDefinedTermSet}`。
- [ ] 後台可新增／編輯兩種區塊；`docs/seo.md` 記錄 Google 2023 起限制 FAQ rich result，價值在 AEO 與讀者。

## Steps

- [ ] 型別與 guard；渲染器；`article.tsx` 位置。
- [ ] `structured-data.guideArticle` 輸入擴充與測試。
- [ ] 後台編輯器最小版。

## How to verify

```bash
cd apps/web && npx vitest run lib/structured-data.test.ts components/content-blocks.test.tsx components/guides "app/(ads-public)"
```
把文章頁 JSON-LD 貼到 validator.schema.org。

## Notes

保留 `structured-data.ts` 檔尾對 HowTo／爬來的 FAQPage 的否決紀錄並引用。
