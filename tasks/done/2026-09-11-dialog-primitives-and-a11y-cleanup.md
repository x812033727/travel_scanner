---
id: 2026-09-11-dialog-primitives-and-a11y-cleanup
title: 彈層原語未統一與可及性收尾
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T19:40:23Z
created_at: 2026-09-11T03:21:17Z
completed_at: 2026-09-11T20:14:33Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/hotspot-restaurants-panel.tsx
  - apps/web/components/hotspot-restaurants-panel.test.tsx
  - apps/web/components/admin-deployments-panel.tsx
  - apps/web/components/admin-deployments-panel.test.tsx
  - apps/web/components/admin-ui.tsx
  - apps/web/components/admin-ui.test.tsx
  - apps/web/components/admin-foods-panel.tsx
  - apps/web/components/admin-food-taxonomy-panel.tsx
  - apps/web/components/admin-hotspot-guides-panel.tsx
  - apps/web/components/admin-hotspot-guides-panel.test.tsx
  - apps/web/components/admin-hotspot-theme-editor.tsx
  - apps/web/components/admin-hotspot-themes-panel.tsx
  - apps/web/components/admin-hotspot-intro-generator.tsx
  - apps/web/components/travel-card-actions.tsx
  - apps/web/components/admin-food-merchants-panel.tsx
  - apps/web/components/flight-status-search.tsx
  - apps/web/components/airline-fare-lab.tsx
  - apps/web/components/airline-fare-lab.test.tsx
  - apps/web/components/flight-status-search.test.tsx
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

- [x] 巢狀 dialog 各自有焦點陷阱，Escape 只關最上層。
- [x] 十二個 dialog 改用共用原語，或至少行為與之一致。**十一個做完，`admin-shell.tsx` 沒做**，理由見 Notes。
- [x] 三個 a11y 問題修掉。

## Steps

- [x] 先修 `hotspot-restaurants-panel.tsx`（唯一有真實巢狀的），改用 `useModalSheet` 與 `registerModalLayer`。
- [x] 其餘十一個逐一改用 `lib/modal-sheet.ts`；`admin-deployments-panel.tsx:147` 的 Escape 綁定一併換掉。
- [x] `flight-status-search.tsx:164` 補完整 tab 語意，或直接移除 `role="tablist"` 改用普通按鈕群。→ 移除，改成兩個 `aria-pressed` 切換鈕。
- [x] `airline-fare-lab.tsx:234-236` 照 `admin-tabs.tsx` 補 roving tabindex 與 `aria-controls`。
- [x] `admin-food-merchants-panel.tsx:891` 加 `role="alert"`。

## How to verify

```bash
cd apps/web && npm run lint:web && npm run test:web -- hotspot-restaurants admin
```

手動：在餐廳面板開啟巢狀的「加入行程」，按 Tab 繞一圈應該停在內層，按 Escape 只關內層。

## Notes

- 整體 a11y 底子很好，這些是例外不是通病：`role="alert"` 111 次、`role="status"` 101 次、`aria-live` 13 次，**沒有任何一個 `<img>` / `<Image>` 缺 alt**，圖示鈕基本上都有 `aria-label`。
- `route-map.tsx:392` 的 `role="img"` 問題歸 `2026-09-11-route-map-mobile-and-a11y`，不在本任務。
- `admin-deployments-panel.tsx` 與 `admin-food-merchants-panel.tsx` 也在 `2026-09-11-admin-tables-unusable-on-phone` 的 scope 裡，兩張不要同時認領。

## claim 用了 --force，理由（claude-opus-5, 2026-09-11）

`admin-food-merchants-panel.tsx` 在 `2026-09-11-food-reservation-platforms`（codex-food-reservation-platforms）的 scope 裡。claim 是 09-11 06:29，未滿 24 小時，但遠端分支 `codex/food-reservation-platforms` 已不存在，工作已合併進 main（`19a9429 feat(foods): 獨立儲存訂位平台與多平台支援 (#392)`，正是最後一次動到那個檔的 commit）。同一張任務在 `2026-09-11-admin-tables-unusable-on-phone` 也擋過一次，理由相同。

## 完成紀錄（claude-opus-5, 2026-09-11）

每一項都先寫一個會失敗的測試重現，再修，再把修正暫時還原確認測試真的會紅。

### 1. 巢狀 dialog

`hotspot-restaurants-panel.tsx` 兩層都改用 `useModalSheet`。重現的是**焦點被搶回外層**：
面板的 effect 依賴 `[onClose, tripRestaurant]`，所以打開內層「加入行程」時 effect 重跑，
`closeRef.current?.focus()` 把焦點從內層拉回外層的關閉鈕。`trapFocus` 只綁外層，而內層是
外層的最後一個子節點，所以 `querySelectorAll` 的「最後一個」正是內層的確認鈕，Tab 一按就
跳回外層開頭——內層的 Tab 陷阱形同不存在。

任務描述說「Escape 關錯層」這點**不成立**：原本的 handler 有 `if (tripRestaurant) … else …`
分支，Escape 確實只關內層。改完後這個行為由 `isTopModalLayer` 保證，測試留著當回歸防線。

`components/hotspot-restaurants-panel.test.tsx` 新增
「keeps the keyboard inside the nested add-to-trip dialog」：斷言開啟後焦點在內層、Tab 與
Shift+Tab 都在內層內環繞、Escape 只關內層且焦點回到開啟它的「加入行程」鈕、再按一次才關面板。
把內層的 `useModalSheet` 停掉後此測試轉紅，確認它咬得住。

測試裡 `opener.focus()` 是刻意的：jsdom 的 `fireEvent.click` 不像瀏覽器那樣讓按鈕取得焦點，
而「關掉內層後焦點回到哪裡」正是這條斷言要驗的東西。

### 2. 十二個 dialog

已改 11 個檔（共 13 個 dialog 層）：

| 檔 | 原本的狀況 |
| --- | --- |
| `hotspot-restaurants-panel.tsx` | 見上，兩層 |
| `admin-ui.tsx`（`AdminDetailDrawer` + `AdminConfirmDialog`） | 各自手刻且都完整，但**兩者會同時開著**——`admin-users-panel.tsx:1136/1217/1384` 從抽屜裡開出停權／刪除確認。兩個 document 層級的 handler 對同一個 Escape 各答一次，結果是確認框連同底下的會員資料一起被關掉；先卸載的那一個還會把 `body.style.overflow` 還原，讓仍被蓋住的頁面可以捲動 |
| `admin-deployments-panel.tsx` | Escape 綁在 `<form onKeyDown>`，焦點在表單外（例如點過遮罩之後）完全沒反應；沒有 Tab 陷阱也沒有捲動鎖 |
| `admin-foods-panel.tsx` | 只有 `aria-modal="true"`，沒有 Escape、沒有陷阱、沒有鎖、沒有焦點處理 |
| `admin-food-taxonomy-panel.tsx`（兩個） | 同上 |
| `admin-hotspot-theme-editor.tsx` | 同上 |
| `admin-hotspot-themes-panel.tsx` | 同上 |
| `admin-hotspot-intro-generator.tsx` | 同上 |
| `admin-hotspot-guides-panel.tsx` | 有陷阱，但抓的是 `document.querySelector("[role='dialog']")`——**文件裡第一個** dialog，不見得是自己；還原 overflow 時寫死 `""` 而不是原值；完全沒有進場焦點與焦點還原 |
| `travel-card-actions.tsx` | 幾乎是 `useModalSheet` 的手抄本，只少了分層堆疊 |

`admin-food-merchants-panel.tsx` 早已改好（上游 `19a9429` 合併進來的），任務描述寫的是舊狀態。

**`admin-shell.tsx` 沒動**：它在 `2026-09-09-site-experience-settings`
（`codex-site-experience`）的 scope 裡。那張是 `blocked`、claim 已過 24 小時（09-09 10:58），
協定上可以接手，但為了一個檔去接手整張別人的任務不對，而且它的命令面板本來就有
document 層級的 Escape、Tab 陷阱、捲動鎖與焦點還原——缺的只有分層堆疊，而 admin 的命令面板
不會疊在別的層上。另開一張後續處理。

新增 `components/admin-ui.test.tsx` 的
「keeps Escape, Tab and the scroll lock on the layer that is on top」，同時驗三件事：
Escape 只關上層、Tab 不會走進抽屜裡的按鈕、關掉下層時頁面仍保持鎖住。改之前這條在第一個
斷言就紅。

`components/admin-deployments-panel.test.tsx` 新增
「closes the confirmation with Escape from anywhere and traps Tab inside it」，改之前
在捲動鎖那條就紅。

### 3. 三個 a11y

- `flight-status-search.tsx`：選 `role="tablist"` 的相反做法。那裡沒有、也不該有 tabpanel
  （兩個模式換的是同一張表單的欄位），硬補 tab 語意等於為了滿足 role 而發明一個不存在的
  widget。改成兩個帶 `aria-pressed` 的切換鈕，如實描述它本來就是什麼。
- `airline-fare-lab.tsx`：照 `admin-tabs.tsx` 補 roving tabindex、`aria-controls`、
  Arrow/Home/End（會繞回），並補上真正的 `role="tabpanel"` 包住下方內容。
- `admin-food-merchants-panel.tsx:891`：補 `role="alert"`。

`airline-fare-lab.test.tsx` 與 `flight-status-search.test.tsx` 各新增一條，兩條都用
「把修正還原 → 轉紅 → 復原 → 轉綠」確認過。

### 改到別人測試檔的一處

`admin-hotspot-guides-panel.test.tsx:286` 原本 `fireEvent.keyDown(window, …)`。真實的 Escape
從焦點所在的元素往上冒泡，`window` 上的 listener 與 `document` 上的 listener 都會收到；只對
`window` 發事件，等於把「listener 綁在哪裡」寫進斷言裡。改成從 `document.body` 發，對兩種
綁法都成立。這不是為了讓測試變綠而放寬——它比原本更嚴格。

### 沒能做到的驗證

這三個彈層在瀏覽器裡沒能實測：admin 全部要登入、`/labs/airlines` 是四個刻意關閉的功能之一
（實際回「尚未開放」）、餐廳面板的搜尋是 POST，而本機的 production 轉接層是唯讀的。元件測試
跑的是真正的 `lib/modal-sheet.ts`（沒有 mock），`lib/modal-sheet.test.tsx` 本來就覆蓋了原語
本身，所以剩下的風險只在接線，而接線正是新測試在看的。瀏覽器那邊唯一實際量到的是
`/zh-TW/hotspots` 的「加入旅程」——但那是 `hotspot-explorer.tsx` 的彈層，本來就已經用了原語，
所以它只證明了原語在真瀏覽器裡如預期（開啟時 `overflow: hidden`、焦點進到關閉鈕、Escape
關閉並把焦點還給開啟它的按鈕），不算驗到我這次的改動。
