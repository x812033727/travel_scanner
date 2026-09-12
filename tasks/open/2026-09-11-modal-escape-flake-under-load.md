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
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/lib/modal-sheet.ts
  - apps/web/lib/modal-sheet.test.tsx
  - apps/web/components/travel-card-actions.test.tsx
  - apps/web/vitest.config.ts
  - apps/web/vitest.setup.tsx
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-mode-panel.test.tsx
  - apps/web/components/planner-overlay.tsx
  - apps/web/components/planner-overlay.test.tsx
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

- [x] 能穩定重現。→ **第三個實例做到了**：`route-mode-panel` 的焦點被搶，已經有確定性的
      回歸測試。另外兩個（Escape 沒生效）還是重現不了。
- [x] 找到真正的成因，不是再一個沒有證據的假設。→ 第三個實例找到了，用焦點探針。
- [ ] 修好之後，連續三次整套 `npm run test:web` 都綠。→ 只修好三分之一，還不能宣告。
- [x] **不可以**用放寬斷言、加 `waitFor`、或 skip 來讓它變綠。→ 沒有這樣做。

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

## 第三個實例，以及一個新的假設（claude-opus-5, 2026-09-11）

合併 main（`ce553c2`）之後再跑一次整套，紅的換成第三個檔：

```
components/route-mode-panel.test.tsx
  × switches among cached route options and applies only the selected preview
  AssertionError: expected <section tabindex="-1" aria-label="乘車與移動步驟" …>
                  to be <button role="option" aria-selected="true" …>
```

單獨跑那個檔，43 條全過。

**這一條是焦點斷言**：`route-mode-panel.test.tsx:799-801` 把焦點放在「方案 1」、按 ArrowRight、
斷言焦點跑到「方案 2」。實際拿到的是 `.route-panel-detail`——一個 `tabindex="-1"` 的容器。

看 `route-mode-panel.tsx:295-300`：

```ts
useEffect(() => {
  if (!providerPreview || !focusNextPreviewRef.current || !detailRef.current) return;
  focusNextPreviewRef.current = false;
  detailRef.current.focus({ preventScroll: true });
  ...
}, [providerPreview]);
```

也就是說，有一個**延後執行的寫焦點動作**，條件只看一個 ref 旗標，不看「焦點現在在哪裡、是不是
已經被使用者移到別處了」。

### 把三個實例放在一起看

| 檔 | 斷言 | 拿到的 |
| --- | --- | --- |
| `trip-editor.test.tsx:292` | 對話框還在 | 一個 dialog 都找不到 |
| `travel-card-actions.test.tsx:64` | Escape 之後彈層關掉 | 彈層還在 |
| `route-mode-panel.test.tsx:801` | 焦點在下一個選項 | 焦點在 `tabindex="-1"` 的容器 |

三個都是**鍵盤／焦點在負載下行為不同**。第三個把方向指得比前兩個清楚：
**從延後的 callback（`requestAnimationFrame` 或 effect）寫焦點，而沒有重新確認那件事還該不該做。**

同樣形狀的地方至少還有：

- `planner-overlay.tsx:157` 的 `focusFrame` —— rAF 裡 `(panel.querySelector("[data-planner-close]") || panel).focus()`。
  只檢查 `isTop()` 與 `hasNestedModal()`，**不檢查焦點是不是已經在 panel 裡的某個地方**。
  負載下這個 rAF 晚一點才跑，就會把使用者剛移過去的焦點搶回關閉鈕——而 `.route-panel-detail`
  與 `panel` 一樣是 `tabindex="-1"` 的容器，症狀會長得一模一樣。
- `airline-fare-lab.tsx` 的 `moveFareTab` 也用 rAF 移焦點（我寫的，同一天）。

### 建議的下一步

不要再從「原語壞了」下手。先寫一個探針：在負載下（另開一個 build 佔住 CPU）重跑整套，
把每次 `focus()` 的呼叫點與當下的 `document.activeElement` 記下來，看是不是真的有延後的
callback 在事後搶焦點。有證據再改；前兩個假設都是沒證據就下判斷，結果都錯了。

## 進度：三個實例裡修好一個（claude-opus-5, 2026-09-11）

用探針找到了第三個實例的確切成因，而且是可以穩定重現的。另外兩個還沒。

### 探針怎麼做的

在 `vitest.setup.tsx` 裡暫時包住 `HTMLElement.prototype.focus`，記下每一次呼叫的
「從哪裡 → 到哪裡 @ 哪一行」（用 `process.stderr.write`，因為 vitest 會攔截 `console.log`）。
跑那條會紅的測試，順序一目了然：

```
FOCUSPROBE body -> section .route-panel-detail @ components/route-mode-panel.tsx:298
FOCUSPROBE section .route-panel-detail -> button role=option "方案 1" @ route-mode-panel.test.tsx:799
FOCUSPROBE button "方案 1" -> button role=option "方案 2" @ onKeyDown (route-mode-panel.tsx:538)
```

綠的時候是這個順序。紅的時候，第一行跑在最後——`route-mode-panel.tsx:295-300` 那個
effect 在路線回來之後**晚一個 commit** 才把焦點移到結果區，而測試在那個空檔裡已經把焦點
放到選項上了。

**這不只是測試的問題。** 同一個空檔裡，真的使用者也可能已經按了方向鍵。應用程式把焦點搶回去，
就是在跟正在操作的人爭。

### 修法

記下「按下查詢的那一刻焦點在哪裡」（`previewFocusOriginRef`，在送出請求之前讀，不是在回應
回來之後），effect 裡比對：焦點還在原處（或在 body、或已經在結果區裡）才移動，否則不動。

回歸測試 `route-mode-panel.test.tsx`「does not pull focus back to the results when the
reader has already moved it」把這個競態變成確定的事：把第二次的 preview 請求掛住，手動把
焦點放到選項上，再放行回應。移除守門那一行，這條就紅——實測過。

### 另外兩個還沒解決

| 檔 | 斷言 | 狀態 |
| --- | --- | --- |
| `route-mode-panel.test.tsx:801` | 焦點在下一個選項 | **已修**，有確定性的回歸測試 |
| `travel-card-actions.test.tsx:64` | Escape 之後彈層關掉 | 未解 |
| `trip-editor.test.tsx:292` | 對話框還在 | 未解 |

後兩個都不是焦點被搶（Escape 走 document 層級的 listener，和焦點無關），所以這次的修法
大概率不會順便修好它們。**不要假設整套從此不會再紅。**

### 給下一個人的建議

那支焦點探針很有用，做法寫在上面，十行左右。要查 Escape 那兩個，同樣的手法可以用在
`document.addEventListener("keydown")` 上：包住 listener，記下每次 Escape 進來時
`isTopModalLayer()` 的結果、`layers` 有幾層、以及哪一層是最上層。有證據再改。

**已經被推翻過的兩個假設，不要重走**（過程見
`tasks/done/2026-09-11-trip-editor-close-guard-order-dependence.md`）：
跨檔模組汙染（`isolate` 是 true，探針測過零洩漏）、`onCloseRef` 寫在 passive effect 會落後
DOM 一個 render（探針測過，`flushSync` 之後兩個 ref 都已更新）。

## 第四輪：三個假設用證據排除，但重現不出來（claude-opus-5-flake, 2026-09-12）

`#406` 合併之後，在合併後的 main 上重跑。**三次整套 + 四核心跑滿的負載：233 檔 /
2381 測試，三次全綠。** 沒有重現。

同時把探針裝在 `useModalSheet` 的 `onKeyDown` 裡（`MODAL_PROBE=1` 才出聲），記錄每一次
Escape 是被哪一個提前返回吃掉的。單獨跑 `travel-card-actions.test.tsx` 的基準線乾淨：
register／unregister 完全成對、深度恆為 1、`isTop=true`、`defaultPrevented=false`、
`foreignOpenDialogs=0`。

### 三個假設，用證據排除（不是推論）

| 假設 | 證據 | 結論 |
| --- | --- | --- |
| 外來的 `dialog[open]` 讓第二個守門返回 | 全站只有一個原生 `<dialog>`，在 `components/community/ui.tsx:62`。`isolate` 是 true，每個測試檔有自己的 jsdom，它到不了 `travel-card-actions.test.tsx` | 排除 |
| `event.defaultPrevented` 被另一個 listener 先搶走 | `travel-card-actions.tsx` 自己一個 `addEventListener` 都沒有；全站只有五個元件掛 document keydown（`route-map`、`admin-nav`、`hotspot-explorer`、`admin-shell`、`planner-overlay`），都在別的檔，隔離下到不了 | 排除 |
| `sheetRef.current` 在 effect 執行時是 null，effect 靜靜地什麼都不做 | 見下。四個 `open` 寫死 `true` 的呼叫點全部查過，ref 都是無條件掛上的 | 今天排除，但**原語有隱患** |

### 查到的一個隱患（不是這次的成因，另開任務）

`useModalSheet` 的 effect：

```ts
useEffect(() => {
  if (!open) return;
  const sheet = sheetRef.current;
  if (!sheet) return;   // ← 靜靜地放棄，而且 deps 是 [open]，永遠不會重試
  ...
}, [open]);
```

`open` 沒變的話 effect 不會再跑。所以只要有一個呼叫點在 effect 執行的那一刻還沒把 ref
掛上（例如彈層藏在 loading 狀態後面），那個彈層就會**永久**沒有 Escape、沒有 focus trap、
沒有捲動鎖、也沒有進 `layers`——而且完全不出聲。

四個把 `open` 寫死 `true` 的呼叫點風險最高，因為 effect 只在掛載時跑一次：
`hotspot-restaurants-panel:153`（ref 在 321，中間沒有提前 return）、
`admin-hotspot-guides-panel:945`（ref 在 956）、
`travel-services/booking-panel:125`（ref 在 165）、
`travel-services/stay22-public-hotels:38`（ref 在 56，loading 狀態在 div **裡面**，所以安全）。
**四個目前都沒事**，但這是一個等著被下一個呼叫點踩到的地雷。

### 一個容易誤導人的事實

`lib/modal-sheet.ts` **不是 `#406` 改的**——它上一次變動是 `#380` 與 `#338`。`#406` 改的是
呼叫端（十一個彈層搬過來用它）。所以「原語是新的、所以原語有問題」這個方向不成立；
變的是 `travel-card-actions.tsx` 開始走這條路。

## 結論：七次整套、零重現，任務釋出（claude-opus-5-flake, 2026-09-12）

| 跑法 | 次數 | Escape 相關的紅 |
| --- | --- | --- |
| 整套 + 四核心滿載（預設順序） | 3 | 0 |
| 整套 + 六個燒 CPU 的行程 + `--sequence.shuffle` | 4 | 0 |

**合計 16667 條測試，Escape 一次都沒紅。**

打亂順序那四次確實有紅，但**兩條都不是這張任務的東西**，而且都是真缺陷、不是 flake：

- `site-footer.test.tsx` 有一條沒設路徑就斷言 → `2026-09-12-site-footer`
- `admin-usage-settings-panel.test.tsx` 的分頁存在 URL、測試間沒重設 → `2026-09-12-admin-usage-settings-url`
  （四次打亂中紅了兩次，診斷等於被獨立驗證過）

兩張都寫了成因、一行修法與可重放的種子 `1789176414571`。

### 為什麼釋出而不是標 done

DoD 第三項（修好之後連續三次整套全綠）從字面上看已經滿足了，但**那會宣稱超出證據的東西**。
真實狀況是：三個實例裡只有 `route-mode-panel` 那個被找到成因並修好（`#406`，有確定性的回歸
測試）；另外兩個是**重現不出來**，不是**修好了**。這兩件事不該混為一談。

### 留給下一個人的東西

1. `travel-card-actions.test.tsx:64` 現在有失敗現場輸出了，和 `trip-editor.test.tsx:292` 同一個
   形狀。斷言一個字都沒放寬。故意把 `isTopModalLayer` 印出來，因為另外兩個守門這輪已經用證據
   排除（這個檔自己沒掛任何 listener；全站唯一的原生 `<dialog>` 在別的檔，`isolate` 下到不了）。
   **下次它在 CI 紅的時候先看那一行**：如果是 `true`，守門是清白的，handler 根本沒跑或沒掛上。
   驗證過這個輸出本身會動——暫時把 `closeRef.current()` 拿掉，它印出
   `dialogs in DOM: 1; sheet still the top layer: true; sheet connected: true;
   native dialog[open] anywhere: 0; body overflow: hidden`。
2. 這輪用證據排除的三個假設寫在上一節，**不要重走**。加上更早被推翻的兩個（跨檔模組汙染、
   `onCloseRef` 落後一個 render），現在總共有五個死路是有紀錄的。
3. 探針的做法（包住 `onKeyDown`，記錄每個守門的值）留在 commit `86cc4b2` 裡，要用可以撿回來。
4. `--sequence.shuffle` 很划算：一跑就撈到兩條真的順序相依。值得偶爾拿來掃。

### 一個順手查出來的隱患

`useModalSheet` 的 effect deps 只有 `[open]`，ref 是 null 就永久不再重試——彈層會變成看得見、
鍵盤完全沒反應、而且不出聲。二十一個呼叫點目前都沒踩到（四個 `open` 寫死 `true` 的都查過），
但這是下一個人踩得到的地雷。另開 `2026-09-12-usemodalsheet-effect-ref`，沒有在這張裡順手改
共用原語。

## 第四個實例（claude-opus-5-testfixes, 2026-09-12）

合併 main（`3230a33`，#419 的 sitemap／guides）之後跑整套，紅了一條：

```
components/route-mode-panel.test.tsx
  × supports the available Google transit fallback and exposes its actual steps before the optional map
```

單獨跑那個檔 44 條全過；整套重跑一次 233 檔 / 2383 全綠。**所以這是第四個實例，不是 #419
帶進來的回歸。**

值得注意的是它落在 `route-mode-panel.test.tsx`，但**不是**我在 `#406` 修好的那一條
（那條是「switches among cached route options and applies only the selected preview」）。
同一個檔、不同的測試。所以焦點守門的修正沒有讓這個檔免疫，只解決了它自己那一條。

四個實例現在長這樣：

| 檔 | 斷言 | 狀態 |
| --- | --- | --- |
| `route-mode-panel.test.tsx`（cached route options） | 焦點在下一個選項 | 已修（`#406`） |
| `route-mode-panel.test.tsx`（Google transit fallback） | — | **新，未解** |
| `travel-card-actions.test.tsx:64` | Escape 之後彈層關掉 | 未解 |
| `trip-editor.test.tsx:292` | 對話框還在 | 未解 |

觸發的情境也對得上先前的觀察：**main 帶進新的測試檔會改變整套的檔案順序與時序**，而這個
家族對那個很敏感。#419 一個字都沒碰 `route-mode-panel`。

下次要查的時候，這條比另外兩條好下手——它在一個已經裝過焦點探針、而且探針確實奏效的檔裡。
