---
id: 2026-09-11-planner-overlay-close-guard-race
title: 安排編輯器的關閉鈕在儲存在途時被靜默吞掉
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T21:04:03Z
created_at: 2026-09-11T10:24:18Z
completed_at: 2026-09-11T21:24:44Z
branch: claude/mokaair-website-access-k7xiku
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

- [x] 儲存在途時按下關閉，使用者一定看得到結果：要嘛關閉，要嘛明確顯示為何還不能關。
      （結果一定有；但是在寫入落地時才出現，不是按下的當下——差別寫在完成紀錄。）
- [x] 閘門 1 不再有「按了完全沒反應」的路徑。閘門 2 本來就有回饋。
      **閘門 3 沒有動**，查過找不到走得到的路，理由在完成紀錄。
- [x] 有一支回歸測試：自動儲存在途時按關閉（修好前失敗，實測過）。
- [x] `trip-editor.test.tsx` 不必再靠 `waitFor` 掩蓋這個行為。

## Steps

- [x] 確認假設。→ 閘門 1 成立且可重現；閘門 3 找不到走得到的路。
- [x] 閘門 1 改為**排隊而非丟棄**。（關閉鈕顯示「儲存中」那個選項沒有做。）
- [x] 閘門 3：查過，沒有動，理由在完成紀錄。
- [x] 檢查其他讀 `isTopModalLayer` 的呼叫點。→ `community/ui.tsx` 與
      `discovery/detail-drawer.tsx` 情況相同，都有滿版遮罩。

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

## 完成紀錄（claude-opus-5, 2026-09-11）

和 `2026-09-11-trip-editor-close-guard-order-dependence` 一起做的，改動都在同一個 commit。
那張任務的完成紀錄有完整的調查過程，這裡只記這張自己的三件事。

### 閘門 1：改成排隊，不再丟掉

`requestExit` 第一道閘門原本 `return false` 之後什麼都不做。改成把 `run` 存進
`queuedExitRef`，寫入落地時 `drainQueuedExit()` 再跑一次 `requestExit`。
落地點有三處：`saveDraft` 的 `finally`、`onBusy` 轉回 false、以及 `markPanelWrite(source, false)`。

所以按下關閉之後一定有結果：不是關掉，就是（草稿還髒著時）跳出「保留這次修改嗎？」。
**注意這改的是結果不是時機**——寫入在途時按下去，畫面當下仍然不動，等寫入落地才有反應。
要讓當下就有回饋（關閉鈕顯示「儲存中」並 disabled），是另一件事，沒有做。

回歸測試在 `trip-editor.test.tsx`：「does not swallow the close button while the save it
started is still in flight」。把排隊那行改回 `return false` 會轉紅，實測過。

### 閘門 3：查過，沒有動，理由在這裡

`closeOverlay` 在 `isTopModalLayer(panel)` 為否時無聲返回。追下去找不到真的走得到的路：

- planner overlay 自己的層——`syncLayers()`（`planner-overlay.tsx:28-35`）會把非最上層的
  container 標成 `inert` + `aria-hidden`，關閉鈕點不到；Escape 另外被 `isTop()` 擋住。
- `useModalSheet` 的層疊上來時，planner 的 container 不會被標 inert，理論上關閉鈕還在——
  但那些 sheet（community 的 `Dialog`、舊的服務 sheet）自己有滿版遮罩，點擊落在遮罩上。

`components/community/ui.tsx` 與 `components/discovery/detail-drawer.tsx` 兩個呼叫點也看過，
情況相同。在找不到重現的情況下改守門，就是在猜——所以留著，把理由寫下來。

### Notes 裡那個 `panelWriteBusyRef`：修了

改成 `Set<string>`，一個寫入者一個 key（`day-note`、`trip-note`、`departure`、
`schedule-defaults`、`route-preference`），`panelWriteBusy()` 看 size。

沒有專屬的回歸測試：兩個 panel 寫入者在現有 fixture 裡不會同時出現（出發時間欄位只在
`hotel_start` 系統項目上渲染，測試的行程只有一個活動），要湊出同時在途得改 fixture，
比這個修正本身還大。

### DoD 第四項：`waitFor` 留著，但它不是在掩蓋什麼

`999dbc5` 加的 `await waitFor(() => expect(queryByRole("dialog", …)).toBeNull())` 留著。
點擊不再被吞掉之後，那就是一般的「等狀態渲染完」——關閉確實會排入狀態更新，等得到。
原本它掩蓋不了問題（被吞掉的點擊等再久都不會關），現在它等的是真的會發生的事。

### 那條相反方向的測試

Notes 最後一段提到的 `trip-editor.test.tsx:292`（該擋卻放行）**沒有修好**，因為重現不出來。
過程與排除掉的假設寫在 `2026-09-11-trip-editor-close-guard-order-dependence` 的完成紀錄：
簡單說，我以為是 `onCloseRef` 寫在 passive effect 裡會落後 DOM 一個 render，探針證明不是。
那條斷言一個字都沒放寬，改成失敗時印出現場狀態。

### 追加：整套跑三次，紅了一次，而且是別的檔

同一份程式碼連跑三次整套：第二、三次全綠，第一次 `travel-card-actions.test.tsx` 紅一條
（按 Escape 之後彈層沒關）。那個檔用的是 `useModalSheet` 不是 `PlannerOverlay`，所以這個
時序問題不是這張任務的守門獨有的。

`travel-card-actions.tsx` 今天才改成用 `useModalSheet`（`2026-09-11-dialog-primitives-and-a11y-cleanup`），
在那之前它手刻的 handler 沒有 `isTopModalLayer` 檢查——很可能是那次改動帶出來的新暴露面。
證據與已排除的假設整理在 `2026-09-11-modal-escape-flake-under-load`。
