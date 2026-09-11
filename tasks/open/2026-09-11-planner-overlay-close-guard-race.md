---
id: 2026-09-11-planner-overlay-close-guard-race
title: 安排編輯器的關閉鈕在儲存在途時被靜默吞掉
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T10:24:18Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
  - apps/web/components/planner-overlay.tsx
  - apps/web/lib/modal-sheet.ts
  - apps/web/components/planner-overlay.test.tsx
---
# 安排編輯器的關閉鈕在儲存在途時被靜默吞掉

## Why

行程規劃器裡打開一個安排的編輯器後按「關閉」，有時候**什麼都不會發生**——沒有錯誤、沒有回饋、
彈層留在原地。使用者只剩 Escape 或點背景可以脫身。

這顆按鈕背後有**三道各自會靜默失敗的閘門**。點擊先經過 `PlannerOverlay.closeOverlay`
（`planner-overlay.tsx:119`），再到 `closeEditor()`（`trip-editor.tsx:991`）
→ `requestExit(clearEditor)`（`trip-editor.tsx:964`）：

```ts
function requestExit(run: () => void) {
  if (draftSavingRef.current || panelWriteBusyRef.current || action?.startsWith("update-")) return false;
  const editorDirty = Boolean(draftItem && JSON.stringify(draftItem) !== JSON.stringify(editingBaseRef.current));
  if (editorDirty || preferencesDirty || tripNoteDirty || dayNoteDirty || departureDirty || settingsDirty) {
    setPendingExit({ run }); return false;
  }
  run(); return true;
}
```

| | 條件 | 結果 |
| --- | --- | --- |
| 閘門 1 | 有寫入在途 | `return false` — 什麼都沒發生，零回饋 |
| 閘門 2 | 任何一處 dirty | 開啟確認彈層，編輯器留著不關 |
| 閘門 3 | `isTopModalLayer(panel)` 為否 | `onClose` 根本不會被呼叫 |

**閘門 1 是最可能的成因。** `openEditor()`（`trip-editor.tsx:993`）本身是 `async`，
開頭就 `await flushChanges(false)`；另有一個 1 秒 debounce 的自動儲存（`trip-editor.tsx:784`）。
只要點擊落在寫入在途的窗口，`panelWriteBusyRef.current` 或 `action?.startsWith("update-")`
為真，點擊就被吞掉。

這已經讓 CI 紅過兩次：`trip-editor.test.tsx` 連續「開啟編輯器 → 關閉 → 再開 → 關閉」，
第二次關閉逾時。`999dbc5`（2026-09-11）試著在點擊後補 `waitFor`，**無法生效**——
被吞掉的點擊從未排入任何狀態更新，等再久都不會關。等待只能解決「已觸發、尚未渲染完」。

該測試全程沒有輸入任何東西進編輯器，所以 `draftItem` 與 `editingBaseRef.current` 深度相等，
**閘門 2 在這個情境不成立**。

## Definition of done

- [ ] 儲存在途時按下關閉，使用者一定看得到結果：要嘛關閉，要嘛明確顯示為何還不能關。
- [ ] 三道閘門都不再有「按了完全沒反應」的路徑。
- [ ] 有一支回歸測試：自動儲存在途時按關閉，斷言編輯器仍會關閉（修好前應失敗）。
- [ ] `trip-editor.test.tsx` 不必再靠 `waitFor` 掩蓋這個行為。

## Steps

- [ ] 先確認假設：在 `requestExit` 暫時記錄是哪一道閘門返回 false，在 CPU 競爭下重跑
      `trip-editor.test.tsx`。這只是診斷，不進版。
- [ ] 閘門 1 改為**排隊而非丟棄**：保留 `run`，等在途寫入解決後執行；或把關閉鈕設為
      disabled 並顯示儲存中，讓原因可見。
- [ ] 閘門 3 同理：`isTopModalLayer` 為否時不該無聲返回。
- [ ] 檢查其他同樣讀 `isTopModalLayer` 的呼叫點（`components/community/ui.tsx`、
      `components/discovery/detail-drawer.tsx`）是否有相同暴露。

## How to verify

```sh
cd apps/web && npx vitest run components/planner-overlay.test.tsx components/trip-editor.test.tsx
npm run lint:web && npm run typecheck:web && npm run test:web
```

手動：在行程規劃器連續開關同一個安排編輯器數次，包括剛改過內容、自動儲存正在跑的時候，
關閉鈕每次都要有可見結果。

## Notes

- **第二個缺陷，順帶修掉比較省事**：`panelWriteBusyRef` 是單一 ref，卻被三個
  `DraftNoteField` 共用（`trip-editor.tsx:1854` 當日備註、`:1886` 出發設定、
  `:2045` 行程備註），全都是 `onBusyChange={(pending) => { panelWriteBusyRef.current = pending; }}`。
  A 欄位設 `true`、B 欄位稍後寫完設 `false`，旗標就不再反映 A —— 可能卡住關不掉，
  也可能過早失效。應改為計數或 Set，而非單一布林。
- **這張任務目前不可直接認領**：`trip-editor.tsx` 被 in-review 的
  `2026-09-10-seoul-day2-transport-ux` 押著，板子因此把它列在「active work in the same scope」。
  這是加入正確 scope 之後才浮現的真實狀況——先前只列 planner-overlay 幾個檔時看不出來。
  等那張任務 done，或先與其擁有者協調。
- scope 未列 `trip-editor.test.tsx`：它同時被 `2026-09-11-pr388-seo-review` 與
  `2026-09-10-seoul-day2-transport-ux` 押著，要動得先協調。
- 由 PR #393 的 CI 調查順帶發現，非該 PR 造成。該 PR 的留言
  （https://github.com/x812033727/travel_scanner/pull/393#issuecomment-5632942149）
  把成因只歸給 `isTopModalLayer`，**那份歸因不完整**，以本檔為準。
- **另一支測試也在紅，方向相反**（2026-09-11，合併 #397／#399 時發現）：
  `trip-editor.test.tsx:292`「disables arrange and adjustment navigation until itinerary
  generation finishes」當天紅了兩次——#399 分支的 CI run 34614048730，以及 #397 合併 main 後的
  run 34617052934。這支測試在預覽請求在途時按「關閉」再按 Escape，期待 AI 對話框留著；
  失敗時 `getAllByRole("dialog")` 一個都找不到，也就是對話框在產生中**被關掉了**——這裡的閘門是
  該擋卻放行，與上面「該關卻吞掉」相反。main 的 `1da78504` 與 #397 合併前的 `e1768ae7` 都通過同一支
  測試，兩個 PR 也都沒碰 trip-editor，所以同樣是時序問題。修閘門時一併確認「產生中」的狀態在
  關閉鈕可被點到之前就已生效。
