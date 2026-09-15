---
id: 2026-09-15-site-search-header-web
title: Header 搜尋框：桌機欄位＋⌘K、手機 sheet、typeahead 分專區
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-15T13:57:27Z
completed_at:
branch:
depends_on:
  - 2026-09-15-article-search-results-page-web
scope:
  - apps/web/components/site-search
  - apps/web/components/site-header.tsx
  - apps/web/components/site-header.test.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/components/guides-navigation.test.tsx
  - apps/web/messages/en/navigation.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/zh-TW/navigation.json
  - apps/web/messages/zh-CN/navigation.json
---

# Header 搜尋框：桌機欄位＋⌘K、手機 sheet、typeahead 分專區

## Why

header 沒有任何搜尋入口；讀者要找文章只能翻列表。

## Definition of done

- [ ] 桌機 header 有 `role="search"` 表單，輸入即顯示分專區的 typeahead（≤6 筆＋「查看全部結果」），鍵盤上下／Enter／Esc 可用；⌘K／Ctrl+K 開啟對話框。
- [ ] 手機以搜尋 icon 開 sheet；無 JS 時表單仍送到 `/search/articles`。
- [ ] 三種導覽模式都恰好出現一次搜尋入口（`guides-navigation.test.tsx`）。

## Steps

- [ ] `use-article-search.ts`：200ms debounce、AbortController、忽略過期回應、走 BFF `/api/travel/guides/search`。
- [ ] `site-search.tsx`／`site-search-dialog.tsx`：combobox 語意、token 顏色、`min-h-11`。
- [ ] 接進 `site-header.tsx` 與 `mobile-nav.tsx`；messages。

## How to verify

```bash
cd apps/web && npx vitest run components/site-search components/guides-navigation.test.tsx
```

## Notes

BFF 對安全 GET 直接轉發，不需新增 route。
