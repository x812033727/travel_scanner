---
id: 2026-09-11-dialog-primitives-and-a11y-cleanup
title: 彈層原語未統一與可及性收尾
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T03:21:17Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/hotspot-restaurants-panel.tsx
  - apps/web/components/admin-deployments-panel.tsx
  - apps/web/components/admin-food-merchants-panel.tsx
---

# 彈層原語未統一與可及性收尾

## Why

repo 裡有兩個寫得很好的彈層原語，但十二個 dialog 沒有用它們，各自手刻或乾脆不做。

標準做法（應作為範本）：

- `lib/modal-sheet.ts:51-127` 的 `useModalSheet`——分層捲動鎖（`:9-19`）、真正的 Tab 陷阱（`:88-106`）、Escape（`:82-86`）、焦點還原並檢查開啟者是否還在 DOM（`:123`），且會讓路給原生 `<dialog open>`（`:81`）。
- `planner-overlay.tsx:37-70` 的 `PlannerOverlay`——position-fixed 的 body 鎖（同時解決 iOS 橡皮筋）、捲軸寬度補償（`:50-53`）、精確捲動還原（`:66-68`）、對非作用層下 `inert`（`:28-35`）。

問題：

1. **巢狀 dialog 的 Escape 關錯層、Tab 走得出去。** `hotspot-restaurants-panel.tsx:244-249` 只有一個 document 層級的 Escape handler，`trapFocus`（`:256-264`）只綁在外層的 `dialogRef`（`:355`），`:385` 的「加入行程」內層 dialog 沒有自己的陷阱——Tab 會走進背後的餐廳列表。同檔 `:242-243` 還直接改 `document.body.style.overflow`（`:253` 還原）而不是用 `registerModalLayer`，若哪天巢狀在 `PlannerOverlay` 底下，解鎖順序會競態。
2. **十二個 dialog 沒引入原語。** `admin-ui.tsx`、`admin-shell.tsx`、`admin-deployments-panel.tsx`、`admin-foods-panel.tsx`、`admin-food-merchants-panel.tsx`、`admin-food-taxonomy-panel.tsx`、`admin-hotspot-guides-panel.tsx`、`admin-hotspot-theme-editor.tsx`、`admin-hotspot-themes-panel.tsx`、`admin-hotspot-intro-generator.tsx`、`hotspot-restaurants-panel.tsx`、`travel-card-actions.tsx`。其中 `admin-deployments-panel.tsx:147` 把 Escape 綁在 `<form>` 的 `onKeyDown` 上，焦點不在表單裡時按 Escape 沒反應。
3. **三個 a11y 收尾。** `flight-status-search.tsx:164` 有 `role="tablist"` 卻放兩個普通 `<button>`，沒有 `role="tab"`、沒有 `aria-selected`、沒有 `aria-controls`、沒有 tabpanel。`airline-fare-lab.tsx:234-236` 有 `role="tab"` 但沒有 roving tabindex 也沒有 `aria-controls`（正確做法見 `admin-tabs.tsx:112-143`，含 Arrow/Home/End 與手機用的 `<select>` 鏡像）。`admin-food-merchants-panel.tsx:891` 是全 repo 唯一沒有 `role="alert"` 的錯誤訊息，對螢幕閱讀器完全無聲。

## Definition of done

- [ ] 巢狀 dialog 各自有焦點陷阱，Escape 只關最上層。
- [ ] 十二個 dialog 改用共用原語，或至少行為與之一致。
- [ ] 三個 a11y 問題修掉。

## Steps

- [ ] 先修 `hotspot-restaurants-panel.tsx`（唯一有真實巢狀的），改用 `useModalSheet` 與 `registerModalLayer`。
- [ ] 其餘十一個逐一改用 `lib/modal-sheet.ts`；`admin-deployments-panel.tsx:147` 的 Escape 綁定一併換掉。
- [ ] `flight-status-search.tsx:164` 補完整 tab 語意，或直接移除 `role="tablist"` 改用普通按鈕群。
- [ ] `airline-fare-lab.tsx:234-236` 照 `admin-tabs.tsx` 補 roving tabindex 與 `aria-controls`。
- [ ] `admin-food-merchants-panel.tsx:891` 加 `role="alert"`。

## How to verify

```bash
cd apps/web && npm run lint:web && npm run test:web -- hotspot-restaurants admin
```

手動：在餐廳面板開啟巢狀的「加入行程」，按 Tab 繞一圈應該停在內層，按 Escape 只關內層。

## Notes

- 整體 a11y 底子很好，這些是例外不是通病：`role="alert"` 111 次、`role="status"` 101 次、`aria-live` 13 次，**沒有任何一個 `<img>` / `<Image>` 缺 alt**，圖示鈕基本上都有 `aria-label`。
- `route-map.tsx:392` 的 `role="img"` 問題歸 `2026-09-11-route-map-mobile-and-a11y`，不在本任務。
- `admin-deployments-panel.tsx` 與 `admin-food-merchants-panel.tsx` 也在 `2026-09-11-admin-tables-unusable-on-phone` 的 scope 裡，兩張不要同時認領。
