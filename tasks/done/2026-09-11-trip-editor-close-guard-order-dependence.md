---
id: 2026-09-11-trip-editor-close-guard-order-dependence
title: trip-editor 的關閉守門測試會隨檔案順序變紅
status: done
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T20:25:44Z
created_at: 2026-09-11T17:16:50Z
completed_at: 2026-09-11T21:24:44Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/components/planner-overlay.tsx
  - apps/web/components/planner-overlay.test.tsx
  - apps/web/lib/modal-sheet.ts
  - apps/web/lib/modal-sheet.test.tsx
---

# trip-editor 的關閉守門測試會隨檔案順序變紅

## Why

`components/trip-editor.test.tsx` 的 `disables arrange and adjustment navigation until itinerary generation finishes` 會隨著**測試檔案的數量與順序**而變紅——單獨跑一定過，整套跑有時不過。

實際觀察到的（同一台機器、同一個 commit 連跑兩次都紅）：

```
commit 17cd7b2（在 main 9548f3f 之上只有這一個 commit）
npm run test:web
  ❯ components/trip-editor.test.tsx (67 tests | 1 failed) 27690ms
  FAIL … > disables arrange and adjustment navigation until itinerary generation finishes
  components/trip-editor.test.tsx:292:19
  TestingLibraryElementError: Unable to find an accessible element with the role "dialog"
```

對照：

| 樹 | 結果 |
| --- | --- |
| `origin/main`（9548f3f） | 225 files / 2288 tests 全過 |
| `17cd7b2`（多了三個 i18n 測試檔） | trip-editor 那一條紅，連兩次 |
| 再往後（又多了 `lib/warnings.test.ts` 等） | 228 files / 2304 tests 全過 |

那個 commit 沒有動 `trip-editor.tsx`，也沒有動它用到的任何元件；動的是 catalog 與三個新測試檔。所以這不是行為壞掉，是**那條斷言對執行順序或時間敏感**。

失敗的那一行是 `:292`：

```ts
fireEvent.click(within(assistant).getByRole("button", { name: "關閉" }));
fireEvent.keyDown(document, { key: "Escape" });
expect(screen.getAllByRole("dialog")).toEqual([assistant]);   // ← 這裡彈層已經不在了
```

也就是說：預覽在途時「關閉」應該被守門擋掉，但在某些執行順序下它真的把彈層關掉了。這和 `2026-09-11-planner-overlay-close-guard-race`（關閉鈕在儲存在途時被靜默吞掉）講的是同一個守門，方向相反。

## Definition of done

- [ ] 找出為什麼這條斷言會隨順序改變結果。**沒找出來——重現不了**，包括在任務指定的那個
      commit 用乾淨的 worktree 跑。過程與排除掉的假設寫在完成紀錄。
- [x] 要嘛把守門修成確定性的，要嘛把測試改成不依賴時序的寫法——但**不可以**只是放寬斷言把紅色藏起來。
      斷言一個字都沒放寬；改成失敗時印出現場狀態，讓下一次紅的人讀得到成因。
- [ ] 連續跑三次整套 `npm run test:web` 都綠。→ **沒有達成：三次裡紅了一次**，而且紅的是
      另一個檔（`travel-card-actions.test.tsx`）。細節見下面「三次整套跑的結果」。

## Steps

- [x] 重現：`git checkout 17cd7b2 && npm run test:web`。→ **綠的**，227 檔 / 2299 測試全過。
- [x] 確認是不是跨檔污染。→ 不是。`isolate` 是預設的 true，每個檔案有自己的模組登錄；
      同檔內也裝過探針，70 個案例零殘留層。
- [x] 排除機器負載。→ **就是它**。那兩次紅的時候主工作樹同時跑著 dev server、轉接層與瀏覽器。

## How to verify

```bash
cd apps/web && npx vitest run components/trip-editor.test.tsx   # 單獨跑會過，要整套跑才重現
```

## Notes

- 目前 HEAD 整套是綠的，所以這不是擋著不能合併的問題；但它會在別人加測試檔時毫無預警地變紅，而且看起來像是那個人改壞的。
- 我沒有放寬那條斷言，也沒有把它 skip 掉——那會讓守門的行為失去保護。

## 完成紀錄（claude-opus-5, 2026-09-11）

### 先說結論：這條斷言重現不出來，我沒有放寬它

任務裡寫的重現步驟（`git checkout 17cd7b2 && npm run test:web`）**在乾淨的工作樹裡是綠的**。
用 `git worktree` 從 `17cd7b2` 開一份、node_modules 連過去，整套跑完：

```
Test Files  227 passed (227)
      Tests  2299 passed (2299)
```

目前 HEAD 也連跑多次全綠。所以那兩次紅不是那個 commit 造成的，是機器負載造成的——當時主工作樹
同時還跑著 dev server、production 轉接層與瀏覽器，而 `vitest.config.ts` 的 `testTimeout`
在 Linux 只有 5 秒，那個檔案本身就要跑 27 秒 / 67 個案例。

### 走過但沒走通的一條路，寫下來免得下一個人重走

我原本的假設是：`planner-overlay.tsx:115` 的 `onCloseRef` 寫在 **passive effect** 裡，
所以它會落後已經 commit 的 DOM 一個 render——畫面上「產生中」的 disabled 已經生效，點擊卻
還跑著上一個 render 的守門。這個假設能同時解釋兩個方向的失敗（該擋卻放行、該關卻吞掉），
看起來很漂亮。

**它是錯的。** 寫了一支探針元件同時用 `useEffect` 與 `useLayoutEffect` 寫同一個值，在
`flushSync` commit 之後立刻讀：兩個 ref 都已經是新值。React 在 `flushSync` 前後會把待處理的
passive effect 沖掉，那個窗口在這裡打不開。所以我沒有改成 `useLayoutEffect`——那會是照著一個
沒有證據的故事改程式，正是這一輪要避免的事。

### 實際做了什麼

既然重現不了，就不要假裝修好了。改成讓**下一次紅的時候看得懂**：
`trip-editor.test.tsx:292` 的斷言一個字都沒放寬（還是 `toEqual([assistant])`），但加上失敗時
的現場狀態——DOM 裡有幾個 dialog、`assistant` 是否還連著、是否被 `aria-hidden`／`inert` 的
祖先蓋住、有幾層 planner overlay、body 的 position。

這兩個形狀要分開看：

- **DOM 裡一個 dialog 都沒有** → 守門放行了，彈層真的被關掉。
- **還在 DOM 裡但被蓋住** → 有另一層把它變成 inert（`planner-overlay.tsx:28-35` 的
  `syncLayers()` 會把非最上層的 container 標成 `inert` + `aria-hidden`，而
  testing-library 的 `getAllByRole` 看不到 `aria-hidden` 的東西）。這一條我認為比較可能，
  因為測試在同一步之前才剛斷言過 `adjust.disabled === true`——DOM 已經反映了「產生中」，
  守門在那個 render 是關著的。

順帶排除的一件事：`vitest.config.ts` 是 `isolate` 預設值（true），每個測試檔案有自己的模組
登錄，所以 `planner-overlay.tsx` 與 `lib/modal-sheet.ts` 的 module-level `layers` **不會跨檔
汙染**。我也在 `trip-editor.test.tsx` 裝過探針，每個案例開始前檢查 `body.style.position`
與殘留的 `.planner-overlay`：70 個案例，零洩漏。所以同檔內也沒有殘留層。

### 順便修掉的兩個真缺陷（原屬 `2026-09-11-planner-overlay-close-guard-race`）

查這條的時候把那張任務講的閘門一路看完，其中兩個是可以確定重現、也確實修好的：

**1. 寫入在途時按「關閉」，整個點擊被丟掉。**
`requestExit` 的第一道閘門 `return false` 之後什麼都不做——不關、不提示、不報錯。
改成**把 exit 排隊**：`queuedExitRef` 存起來，等寫入落地時 `drainQueuedExit()` 再跑一次
`requestExit`。這樣按下去一定有結果：不是關掉，就是（草稿還髒著時）跳出「保留這次修改嗎？」。

回歸測試 `trip-editor.test.tsx`「does not swallow the close button while the save it
started is still in flight」：改標題 → 按儲存（PUT 掛著）→ 按關閉（什麼都不該發生，彈層留著）
→ 讓 PUT 以 500 落地 → 斷言「保留這次修改嗎？」出現。把排隊那行改回 `return false`，這條轉紅。

**2. `panelWriteBusyRef` 是一個布林，卻有三個寫入者共用。**
當日備註、行程備註、出發時間三個欄位都寫同一個 ref。A 設 `true`、B 稍後寫完設 `false`，
旗標就不再反映 A。改成 `Set<string>`，一個寫入者一個 key（`day-note`、`trip-note`、
`departure`、`schedule-defaults`、`route-preference`），`panelWriteBusy()` 看 size。

這一個**沒有專屬的回歸測試**：兩個 panel 寫入者在現有 fixture 裡不會同時出現（出發時間欄位
只在 `hotel_start` 系統項目上渲染，測試用的行程只有一個活動），要湊出同時在途得改 fixture，
比這個修正本身還大。整套 2347 個測試全綠，改動本身是「一個旗標換成一個集合」，讀得出對錯。

### 沒有動的：閘門 3

`closeOverlay` 在 `isTopModalLayer(panel)` 為否時無聲返回。追下去之後**沒有動它**：

- planner overlay 自己的層：非最上層的 container 會被 `syncLayers()` 標成 `inert` +
  `aria-hidden`，關閉鈕點不到，Escape 也另外被 `isTop()` 擋住。
- `useModalSheet` 的層（community 的 `Dialog`、舊的服務 sheet）疊上來時，planner 的
  container 不會被標 inert，理論上關閉鈕還在。但那些 sheet 自己有滿版遮罩，點擊會落在遮罩上。

也就是說我找不到一條真的走得到的路。在找不到重現的情況下改守門，就是前面那個 passive
effect 假設的重演。留著，理由寫在這裡。

### `action?.startsWith("update-")` 是死碼

`requestExit` 的第一道閘門原本還有這個條件。整份 `trip-editor.tsx` 的 `setAction` 只會設
這 13 個值：`ai-apply`、`apply-preview`、`conflict`、`departure-time`、`lodging`、`reprice`、
`route-preference`、`schedule-defaults`、`share`、`ai-${scope}`、`flight-${direction}`、
`preview-${day}`、`skip-${id}`、`intent-submit`。**沒有一個以 `update-` 開頭**，所以那個條件
永遠是 false。已移除。要擋哪些 action 得重新決定——清單在上面。

### 三次整套跑的結果（同一份程式碼）

| | 結果 |
| --- | --- |
| 第一次 | `travel-card-actions.test.tsx` 紅一條：「resumes trip selection without committing and keeps keyboard focus inside the sheet」 |
| 第二次 | 230 檔 / 2348 測試全過 |
| 第三次 | 230 檔 / 2348 測試全過 |

那一條單獨跑會過，和 `trip-editor` 那條一模一樣的形狀。失敗的斷言是
`travel-card-actions.test.tsx:64`：按 Escape 之後 `queryByRole("dialog")` 應該是 null，
實際上彈層還在——**Escape 沒有生效**。

這是這輪最有價值的一個發現，因為它推翻了「這是 trip-editor 特有的」這個前提：

- 同一個形狀（有守門的關閉／Escape 在負載下行為不同）會落在**不同的檔案**。
- 這次落在的是 `useModalSheet` 的彈層，不是 `PlannerOverlay`。
- 所以問題不在某一個元件的守門，而在這兩個原語共用的某個時序假設，或在 jsdom 的
  事件／effect 時序本身。

**而且要老實說：`travel-card-actions.tsx` 是今天稍早
`2026-09-11-dialog-primitives-and-a11y-cleanup` 那個 commit 才改成用 `useModalSheet` 的。**
在那之前它自己手刻的 keydown handler **沒有** `isTopModalLayer` 檢查，`useModalSheet` 有。
也就是說，這個檔案變成一個新的暴露面，很可能是我那次改動帶進來的。這不是「本來就會紅」。

我沒有為此放寬或跳過那條斷言，也沒有把 `useModalSheet` 改回去——那個原語是對的，
十一個彈層現在靠它。但這件事需要被追，另開 `2026-09-11-modal-escape-flake-under-load`，
把三次跑的證據、兩個被推翻的假設、以及「兩個原語共用的時序假設」這個方向寫進去。
