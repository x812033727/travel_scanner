---
id: 2026-09-06-admin-shell-resilience
title: 後台外殼：錯誤頁在地化、面板不要整頁炸掉、手機選單擋內容
status: review
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T13:29:26Z
created_at: 2026-09-06T13:02:12Z
completed_at:
branch: claude/ui-ux-simplification-72afb9
depends_on: []
scope:
  - apps/web/app/[locale]/error.tsx
  - apps/web/app/[locale]/admin/error.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/messages/en/errors.json
  - apps/web/messages/ja/errors.json
  - apps/web/messages/ko/errors.json
  - apps/web/messages/zh-CN/errors.json
  - apps/web/messages/zh-TW/errors.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 後台外殼：錯誤頁在地化、面板不要整頁炸掉、手機選單擋內容

## Why

2026-09-06 在本機用假資料把十個後台頁跑過一遍（`page.route("**/api/travel/**")` 餵
資料，桌機 1440×900 與手機 390×844），出現三件事：

1. **一個面板讀到沒預期的欄位，整頁就變成 Next.js 內建的英文錯誤畫面。** 站上有
   五種語言，這頁只有 “This page couldn’t load / Reload to try again, or go back”，
   而且是整個 `app/` 底下都沒有 `error.tsx` 的結果。`/admin/settings`、
   `/admin/system-settings`、`/admin/layout-settings`、`/admin/hotspots` 四頁都
   複製得出來。
2. **手機的後台選單按鈕浮在畫面中間。** 它寫死 `bottom: calc(5.6rem + safe-area)`
   讓開給底部導覽列，但 `AppBottomNav` 在 `/admin` 底下是 `return null`，所以那
   5.6rem 底下什麼都沒有。而且它只有一個漢堡圖示，沒有字，卻是手機上唯一進得去
   十個後台區塊的入口。
3. 側邊欄的搜尋框與空狀態寫死繁中，英日韓後台讀者看到的是「搜尋後台功能」。

## Definition of done

- [x] 任一後台頁的 render 例外只換掉內容區，側邊欄還在，文案跟著站台語系走。
- [x] 公開頁也有同一套在地化錯誤畫面（兩顆大按鈕：重新載入、回首頁）。
- [x] 手機後台選單按鈕貼齊畫面底部，並且帶著文字標籤。
- [x] 側邊欄搜尋框與「沒有符合的功能」跟著語系走。

## Steps

- [x] 新增 `app/[locale]/error.tsx` 與 `app/[locale]/admin/error.tsx`。
- [x] `messages/*/errors.json` 補上八個鍵（含 `{digest}` 參照碼）。
- [x] `admin-nav.tsx`：按鈕位置與標籤、三個寫死字串改走 `admin.navigation.*`。

## How to verify

在本機 `next dev` 上開 `/zh-TW/admin/hotspots`，用 `page.route` 把
`/api/travel/**` 全部回成 `{"items": [], "total": 0}`（`overview` 缺欄位），面板會
丟例外；畫面應該只有內容區換成「這個後台頁面載入失敗」，側邊欄仍在，`/ja/...`
顯示日文。scratchpad 的 `probe4.mjs` 就是這個情境。

## Notes

- **刻意沒做**：後台頁面同時掛著公開站的主導覽（熱門景點／城市美食／我的旅程／
  價格通知／航班動態／航空票價／方案＝七個連結）和後台側邊欄的十個連結，一個畫面
  十七個導覽項目。要收掉得替後台做一個精簡版 header，牽動 `site-header.tsx` 與
  `site-navigation.tsx`，跟「大字模式」那張任務會撞檔，留給後續。
- **另一個發現**：`/admin/settings` 的載入失敗分支會把原始的 JS 例外訊息
  （`Cannot read properties of undefined (reading 'map')`）直接印給管理者看，下面
  再接一句 `loadErrorHint`「請先在主機設定 ADMIN_EMAILS…」——那句只有在 401／403
  的時候才成立，其他錯誤時會把人帶錯方向。已另開任務。
- `messages/*/admin.json` 與 open 的
  `2026-09-06-admin-panels-i18n-remaining` 有重疊；這裡只在 `navigation` 物件開頭
  加三個鍵，沒有動其他區塊。
