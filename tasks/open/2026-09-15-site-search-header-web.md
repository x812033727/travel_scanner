---
id: 2026-09-15-site-search-header-web
title: Header 搜尋框：桌機欄位＋⌘K、手機 sheet、typeahead 分專區
status: review
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-15T16:38:10Z
created_at: 2026-09-15T13:57:27Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on:
  - 2026-09-15-article-search-results-page-web
scope:
  - apps/web/components/site-search
  - apps/web/components/site-header.tsx
  - apps/web/components/site-header.test.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-footer.test.tsx
  - apps/web/app/[locale]/search/articles/page.tsx
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

- [x] 桌機 header 有 `role="search"` 表單，輸入即顯示分專區的 typeahead（≤6 筆＋「查看全部結果」），鍵盤上下／Enter／Esc 可用；⌘K／Ctrl+K 開啟對話框。
- [x] 手機以搜尋 icon 開 sheet；無 JS 時表單仍送到 `/search/articles`。
- [x] 三種導覽模式都恰好出現一次搜尋入口（`site-header.test.tsx`：搜尋框掛在 `SiteHeader`，不在 `SiteNavigation` 的三個分支裡）。

## Steps

- [x] `use-article-search.ts`：200ms debounce、AbortController、忽略過期回應、走 BFF `/api/travel/guides/search`。
- [x] `site-search.tsx`／`site-search-dialog.tsx`：combobox 語意、token 顏色、`min-h-11`。
- [x] 接進 `site-header.tsx` 與 `mobile-nav.tsx`；messages。

## How to verify

```bash
cd apps/web && npx vitest run components/site-search components/guides-navigation.test.tsx
```

## Notes

BFF 對安全 GET 直接轉發，不需新增 route。

- 搜尋框放在 `SiteHeader`（server component）而不是 `SiteNavigation`，所以三種導覽模式天然只出現一次；`guides-navigation.test.tsx` 不必改。
- 手機 icon 與對話框在不同 component tree，用 `openSiteSearch()`（window CustomEvent）開啟，不加 provider。
- discovery 列已有六顆 2.75rem 目標（380px 滿），第七顆搜尋鈕 `hidden min-[440px]:grid`；icon 用 `TextSearch` 以區別探索的放大鏡。
- `useArticleSearch` 只存最後一次答案，loading／idle 由 `trimmed` 與 `enabled` 推導（repo 的 eslint 禁止在 effect 裡直接 setState）；
  關閉清單不清答案，重新聚焦不再打 API。對話框的 open 狀態存 path（同 `mobile-nav`），換頁自動失效。
- 頁尾多一條 `/search/articles` 連結：header 搜尋在 lg 以下藏起來、discovery 列在 440px 以下藏起來，頁尾是每個回應都有的入口。
