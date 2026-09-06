---
id: 2026-09-06-large-text-mode
title: 大字模式：讓長輩自己把整站字放大
status: review
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T13:36:47Z
created_at: 2026-09-06T13:02:05Z
completed_at:
branch: claude/ui-ux-simplification-72afb9
depends_on: []
scope:
  - apps/web/components/text-size-switcher.tsx
  - apps/web/components/text-size-switcher.test.tsx
  - apps/web/lib/text-size.ts
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/components/site-navigation.tsx
  - apps/web/app/[locale]/layout.tsx
  - apps/web/app/globals.css
  - apps/web/messages/en/navigation.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/zh-TW/navigation.json
  - apps/web/e2e/navigation.spec.ts
---

# 大字模式：讓長輩自己把整站字放大

## Why

把全站字級下限拉到 13px（見 [[2026-09-06-readable-foundation]]）之後，還是有人需要
更大的字。手機瀏覽器的縮放會把版面一起放大到要左右捲，而且大部分長輩不知道去哪裡開；
系統層級的字級設定也不是每支手機都吃得到網頁。站上所有長度都是 rem，所以把根字級
往上調一階，是唯一一個「字、間距、按鈕一起變大，版面不會壞」的做法。

順帶處理發現的另一件事：手機標題列上有四個沒有字的圖示（外觀主題、語言、登入、選單），
其中兩個是顯示偏好。要一個看不清楚字的人先看懂「螢幕加齒輪」跟「文A」是什麼，順序反了。

## Definition of done

- [x] 標準／大／特大三段，換了之後立刻生效，重新整理與換頁都記得。
- [x] 第一次繪製前就套用，不會先畫小字再跳大。
- [x] 320px 與 390px、三段字級、五個頁面都沒有水平溢出。
- [x] 手機選單裡「文字大小」是三顆有字的大按鈕，不是圖示。
- [x] 外觀主題與語言也搬進選單，各自有一行字；標題列只留帳號與選單。

## Steps

- [x] `lib/text-size.ts`：常數與 bootstrap script。
- [x] `components/text-size-switcher.tsx`：compact（桌機標題列）與 expanded（手機選單）。
- [x] `globals.css`：`html[data-text-size]` 兩階 112.5% / 125%。
- [x] `app/[locale]/layout.tsx`：跟主題的 bootstrap 接在同一支 inline script。
- [x] `mobile-nav.tsx`：顯示偏好收進選單。
- [x] `e2e/navigation.spec.ts`：手機版的外觀／語言測試改成先開選單。

## How to verify

```bash
cd apps/web && npx playwright test e2e/navigation.spec.ts --reporter=line
cd apps/web && npx vitest run components/text-size-switcher.test.tsx components/mobile-nav.test.tsx
```

scratchpad 的 `textsize_check.mjs` 會把三段字級 × 兩個寬度 × 五個頁面的
`documentElement.scrollWidth - clientWidth` 印出來，全部是 0。

## Notes

- 用根字級而不是只放大字：Tailwind 的間距也是 rem，所以按鈕、卡片內距會一起長大，
  字不會被擠在原本的框裡。斷點是 px，所以手機在特大字下仍然是手機版面。
- 兩個地方會同時掛著這個控制項（桌機標題列與手機選單都在 DOM 裡），所以改動時
  發一個 window event 讓另一份跟上，`storage` 事件負責跨分頁。
- 沒有把偏好存到帳號（跟主題一致，只放 localStorage）。要跨裝置記住的話得動
  `/auth/me` 的 preferences，那是另一張任務。
