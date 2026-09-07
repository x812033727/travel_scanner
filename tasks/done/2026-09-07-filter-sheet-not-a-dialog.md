---
id: 2026-09-07-filter-sheet-not-a-dialog
title: 手機篩選面板看起來是對話框，但沒有 dialog role、不移動 focus、Escape 不關、Tab 走得出去
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T01:09:46Z
created_at: 2026-09-07T01:09:05Z
completed_at: 2026-09-07T01:09:49Z
branch: claude/filter-sheet-dialog
depends_on: []
scope:
  - apps/web/lib/modal-sheet.ts
  - apps/web/lib/modal-sheet.test.tsx
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/food-browser.tsx
---

# 手機篩選面板看起來是對話框，但沒有 dialog role、不移動 focus、Escape 不關、Tab 走得出去

## Why

`/hotspots` 的手機篩選面板在畫面上是一個蓋著暗色遮罩的底部 sheet，但它只是
`<form aria-label>`：

```
role: null                 // 沒有 role="dialog"，也沒有 aria-modal
開啟後 focus: 還在觸發它的那顆按鈕上
Escape: 面板不關
Tab:    進得去，但沒有邊界，會走出去到遮罩底下的頁面
```

`/foods` 的面板是同一套結構（同一個 `.mobile-filter-sheet` class），同樣四項都缺。
全站只有這兩個地方用那個 class。

站內已經有做對的例子可以照抄：`mobile-nav` 的選單有 `role="dialog"` + `aria-modal`、
開啟時 focus 移到關閉鍵、Escape 關閉、關閉後 focus 回到觸發鍵（#275 有測試守著）。
**但它也沒有 Tab 陷阱**，所以那個 `aria-modal="true"` 是一個頁面沒有兌現的宣告。

## Definition of done

- [x] 兩個面板在開啟時是 `role="dialog"` + `aria-modal`，關閉時不是。
- [x] 開啟時 focus 進到面板，關閉時回到原本的地方。
- [x] Escape 關閉。
- [x] Tab 與 Shift+Tab 在面板內循環，不會走到遮罩底下。
- [x] 每個行為都有測試，而且測試證明過會失敗。

## Steps

- [x] 共用 hook `apps/web/lib/modal-sheet.ts`，兩個面板都用它。
- [x] `role`／`aria-modal` 只在開啟時掛上去（見下）。
- [x] 九個測試，逐項破壞驗證。

## How to verify

```bash
npm run lint:web && npm run typecheck:web
cd apps/web && npx vitest run modal-sheet hotspot-explorer food-browser
```

手機寬度開 `/zh-TW/hotspots` → 按「搜尋條件」→ 焦點應在關閉鍵上 → Escape 應關閉且焦點回到
觸發鍵 → 重開後一直按 Tab 應該在面板內繞圈。

## Notes（做的時候發現的三件事）

**1. `role="dialog"` 不能無條件掛。** 同一個 `<form>` 在 ≥768px 是常駐的篩選列、在手機才變
sheet。永遠標成 dialog 等於對螢幕閱讀器謊稱桌機的篩選列是強制回應的對話框。所以 role 與
`aria-modal` 只在 `filtersOpen` 為真時才加。

**2. 用 `offsetParent` 判斷可見性會讓測試變成空跑。** jsdom 不做版面計算，每個元素的
`offsetParent` 都是 `null`，可聚焦清單於是永遠是空的——Tab 陷阱看起來有測試，實際上測試
在跑一個空迴圈。改用 `hidden` 屬性、`aria-hidden` 祖先與 `getComputedStyle` 的
`display`／`visibility`，兩邊都成立。這是我這輪第二次遇到「測試通過但什麼都沒驗到」。

**3. 稽核報告裡「Tab walks focus underneath the dark scrim」這句不成立。** Tab 是進得去
面板的，走不出去才是問題。實際成立的是上面 Why 段列的四項。

**沒有一起改 `mobile-nav`。** 它現在的行為與這個 hook 相同，只差 Tab 陷阱，而它有 #275 的
測試守著、又正被另一個 session 的 `claude/ux-*` 分支碰。把它換成這個 hook 是好事，但要等
那條線靜下來，另開票比較安全。
