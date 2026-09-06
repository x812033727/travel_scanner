---
id: 2026-09-06-home-mobile-first-screen
title: 首頁手機首屏被三張說明列佔滿
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T00:53:20Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/app/[locale]/page.tsx
---

# 首頁手機首屏被三張說明列佔滿

## Why

390×844 的手機開首頁，由上而下是：header（約 68px）、eyebrow、兩行大標、三行說明文、
**三張等權重的說明列**（每筆資料標明來源／自動安排每日動線／即時與估算費用分開，約 y=350–490），
AI 規劃卡的標題到 y≈610，第一個可操作元件（核取方塊）在 y≈710。

也就是**進站第一眼看不到任何可以動手的東西**，眼睛先撞到三個灰白盒子。要「像 APP」，
首屏應該是「輸入條件 → 下一步」，說明列可以往下擺或收成一行。

這是 2026-09-05 視覺稽核的 high 級發現，當時判斷屬版面改版、動作較大，所以沒動。

## Definition of done

- [ ] 390×844 首屏（不捲動）內看得到 AI 規劃卡的第一個輸入欄位。
- [ ] 桌機版面不退步（三張說明列在桌機是有效的信任訊號，不要一起砍掉）。
- [ ] `npm run lint:web`、`typecheck:web` 通過；`e2e/navigation.spec.ts` 的
      `primary travel flow is visible` 仍過。

## Steps

- [ ] 手機把三張 benefit 列改成一行可橫捲的小 chip，或整組移到 AI 卡片下方。
- [ ] hero 的上下 padding 在手機收緊。
- [ ] 量一次：Playwright 390×844，取第一個 `input`／`select` 的 `boundingBox().y`，
      應 < 844。

## How to verify

```bash
cd apps/web && npx playwright test e2e/navigation.spec.ts --project=mobile-chromium
```

再跑一次 2026-09-05 用的截圖流程（scratchpad 的 `tour.mjs`，390×844 full-page），
肉眼比對改前改後。

## Notes

**同一份稽核在這頁還記了幾個相關但獨立的問題**，如果一起做會比較順（但不要擴大 scope，
必要時另開任務）：

- 目的地卡片把「6 個重點目的地」當標題、國名降成小 eyebrow，掃視時只讀得到一排數字。
- 桌機目的地格線參差：卡片被拉成等高但內容量差很多，最後一列只有一張孤卡。
- 手機頁尾有約 164px 空白且完全沒有 footer —— `.public-app-shell` 有
  `padding-bottom: calc(5rem + safe-area)`，`main` 又加了 `pb-20`，重複算了兩次。

**已經修掉、不要重做的**：`#trip-search` 錨點跳轉被 sticky header 蓋住（已加
`html { scroll-padding-top: 5.5rem }`）、城市晶片 32px → 44px、
「回到搜尋條件」按鈕 36px → `min-h-11`。
