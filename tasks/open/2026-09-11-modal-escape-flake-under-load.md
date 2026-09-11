---
id: 2026-09-11-modal-escape-flake-under-load
title: 整套測試在負載下，有守門的 Escape 偶爾不生效
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-11T21:23:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/modal-sheet.ts
  - apps/web/lib/modal-sheet.test.tsx
  - apps/web/components/travel-card-actions.test.tsx
  - apps/web/vitest.config.ts
---

# 整套測試在負載下，有守門的 Escape 偶爾不生效

## Why

同一份程式碼連跑三次整套 `npm run test:web`：第二、三次全綠（230 檔 / 2348 測試），
**第一次紅一條**：

```
components/travel-card-actions.test.tsx
  × resumes trip selection without committing and keeps keyboard focus inside the sheet
  AssertionError: expected <section role="dialog" aria-label="選擇旅程" …> to be null
```

失敗在 `travel-card-actions.test.tsx:64`——按了 Escape 之後彈層應該關掉，實際上還在。
單獨跑那個檔案永遠會過。

這和 `trip-editor.test.tsx:292` 那條（「disables arrange and adjustment navigation until
itinerary generation finishes」，在 CI 紅過兩次）是**同一個形狀**：有守門的關閉／Escape，
在整套跑的負載下行為和單獨跑不一樣。但兩者落在不同的元件、不同的原語：
一個是 `PlannerOverlay`，一個是 `useModalSheet`。

所以這不是某一個元件的守門寫壞了。要找的是兩個原語共用的時序假設，或者 jsdom 裡
事件與 effect 的時序本身。

## 已經排除的（別重走）

1. **跨檔模組汙染**。`vitest.config.ts` 的 `isolate` 是預設的 true，每個測試檔有自己的
   模組登錄，`lib/modal-sheet.ts` 與 `planner-overlay.tsx` 的 module-level `layers`
   不會跨檔累積。
2. **同檔殘留層**。在 `trip-editor.test.tsx` 裝過探針，每個案例開始前檢查
   `document.body.style.position` 與殘留的 `.planner-overlay`：70 個案例，零洩漏。
3. **`onCloseRef` 寫在 passive effect 裡會落後 DOM 一個 render**。寫了探針元件，同時用
   `useEffect` 與 `useLayoutEffect` 寫同一個值，在 `flushSync` commit 之後立刻讀：
   兩個 ref 都已經是新值。React 會在 `flushSync` 前後把待處理的 passive effect 沖掉。
4. **那個 commit 本身**。用 `git worktree` 從 `17cd7b2`（CI 紅的那個）開乾淨的一份跑整套：
   227 檔 / 2299 測試全過。
5. **前一層層數不對導致 `isTopModalLayer` 為否**。留在 `layers` 裡的舊項目排在前面，
   新的 sheet 仍然是最後一個，`isTopModalLayer` 還是 true——寫過測試確認。

## 還沒查的方向

- `useModalSheet` 的 Escape 有兩個提前返回：`isTopModalLayer(sheet)` 為否，以及
  `document.querySelectorAll("dialog[open]")` 裡有不屬於自己的原生 dialog。
  第二個在整套跑的環境下有沒有可能被別的東西滿足？
- `vitest.config.ts` 的 `testTimeout` 在 Linux 只有 5 秒，而
  `trip-editor.test.tsx` 一個檔就要跑 27 秒 / 70 個案例。負載高時個別案例會不會擦到邊，
  以某種不是逾時訊息的方式表現出來？
- jsdom 的 `fireEvent` 在 `act` 裡 dispatch；負載下 React 的 scheduler 走到不同的 lane，
  會不會讓「DOM 已更新但 handler 還是舊的」這件事**在 `flushSync` 以外的路徑**成立？
  （第 3 點只證明了 `flushSync` 這條路走不通。）

## 一個要一起考慮的事實

`travel-card-actions.tsx` 是 2026-09-11 的
`2026-09-11-dialog-primitives-and-a11y-cleanup` 才改成用 `useModalSheet` 的。在那之前它
自己手刻的 keydown handler **沒有** `isTopModalLayer` 檢查。所以這個檔案很可能是那次改動
帶出來的新暴露面，而不是本來就會紅。

不建議改回去——那個原語是對的，現在有十一個彈層靠它。但如果查到最後發現
`isTopModalLayer` 在某些時序下會錯誤地為 false，那就是原語要修的地方。

## Definition of done

- [ ] 能穩定重現（例如在 CPU 有競爭時重跑，或找出觸發條件）。
- [ ] 找到真正的成因，不是再一個沒有證據的假設。
- [ ] 修好之後，連續三次整套 `npm run test:web` 都綠。
- [ ] **不可以**用放寬斷言、加 `waitFor`、或 skip 來讓它變綠。

## How to verify

```bash
cd apps/web && for i in 1 2 3; do npx vitest run --silent; done
```

同時讓機器有事做（例如另一個 build）比較容易重現。

## Notes

- 完整的調查過程在 `tasks/done/2026-09-11-trip-editor-close-guard-order-dependence.md`。
- `trip-editor.test.tsx:292` 那條斷言已經加上失敗時的現場狀態輸出（DOM 裡有幾個 dialog、
  元素是否還連著、是否被 `aria-hidden`／`inert` 蓋住、幾層 overlay、body 的 position）。
  下次它紅的時候，先看那段輸出。`travel-card-actions.test.tsx:64` 還沒有同等的輸出，
  值得補上。
