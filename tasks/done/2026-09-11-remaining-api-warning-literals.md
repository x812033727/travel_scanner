---
id: 2026-09-11-remaining-api-warning-literals
title: 後端仍有二十餘處警告字串是寫死的繁中
status: done
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-11T20:28:31Z
created_at: 2026-09-11T17:16:49Z
completed_at: 2026-09-11T20:52:04Z
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/api/app/trips/router.py
  - apps/api/app/trips/reschedule.py
  - apps/api/app/trips/share_router.py
  - apps/api/app/trips/schedule.py
  - apps/api/app/search/orchestrator.py
  - apps/api/app/crawlers/back_to_back.py
  - apps/api/app/providers/live_back_to_back.py
  - apps/api/app/warnings.py
  - apps/api/app/trips/routing.py
  - apps/api/app/trips/stay_router.py
  - apps/api/app/trips/route_tasks.py
  - apps/api/app/hotspots/router.py
  - apps/api/app/restaurants/user_router.py
  - apps/api/app/foods/selection.py
  - apps/api/tests/test_warning_codes.py
  - apps/web/lib/warnings.ts
  - apps/web/lib/warnings.test.ts
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-TW/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/components/search-experience.tsx
  - apps/web/components/route-segment-card.tsx
  - apps/web/components/route-segment-card.test.tsx
---

# 後端仍有二十餘處警告字串是寫死的繁中

## Why

`2026-09-11-api-warnings-leak-zh-tw` 把它列出的四個檔（`trips/routing.py`、`trips/router.py` 的天氣、`search/orchestrator.py`、`search/tasks.py`）改成代碼了，另外順手處理了同一個渲染點會吃到的 `trips/route_planner.py`、`trips/route_tasks.py`、`weather/google.py`、`weather/met_norway.py`。

做的時候掃了整個 `apps/api/app`，發現這個問題比那張任務描述的大得多。以下還是寫死的繁中，各自落在別的渲染點：

| 位置 | 內容 |
| --- | --- |
| `trips/router.py:2398,3310,3474,4272,4486,4642,5335` | 「背景路線服務暫時無法使用…」「行程已變更…」「地點已更新…」 |
| `trips/router.py:3532,3562,3748` | `warning=` 參數：「主要飯店已更新…」「每日時間已更新…」「餐食狀態已更新…」 |
| `trips/router.py:5141,5498` | 手動移動時間說明；`5498` 帶日期參數 |
| `trips/reschedule.py:496` | 「旅程日期已變更，移動時間需要重新計算。」 |
| `trips/share_router.py:150` | 「這是從分享連結存下的行程…」 |
| `trips/stay_router.py:86` `trips/schedule.py:101` | `LODGING_WARNING`、`USER_LODGING_KEPT_WARNING` |
| `trips/route_tasks.py:256,258` | 帶數量參數的兩則 |
| `search/orchestrator.py:440` | 帶 `{module}` 與 `{provider_name}` 兩個參數 |
| `crawlers/back_to_back.py:810,812` `providers/live_back_to_back.py:274` | 帶幣別／角色參數 |
| `hotspots/router.py:422` `restaurants/user_router.py:231` `foods/selection.py:111` | 「…已更新，請重新計算這一天的路線。」 |

其中不少帶參數，所以這張要先決定帶參數警告的表示法——原任務的 Steps 寫的是 `{code, params}`，但那會動到 schema 與 `warnings_json` 的既有資料。

## Definition of done

- [x] 上表所有位置都不再 append 繁中整句（另外多找到三處表上沒有的）。
- [x] 帶參數的警告有一個明確、有型別的表示法，且舊資料（已存進 `warnings_json` 的整句）不會炸掉。
- [ ] 每個渲染點都用 `apps/web/lib/warnings.ts` 的 `translateWarnings`。
      **三個票價實驗室的渲染點刻意沒改**，理由見完成紀錄，已另開任務。

## Steps

- [x] 先決定帶參數的表示法。`translateWarnings` 目前的規則是：像代碼的（`^[a-z][a-z0-9_]*$`）查表、查不到就不顯示；不像代碼的原樣顯示。所以舊資料會原樣顯示，不會消失——這給了漸進遷移的空間。
- [x] 一個檔一個檔改，每改一個就把對應的前端斷言換成代碼。
- [x] 五語系 catalog 補齊。

## How to verify

```bash
cd apps/api && uv run pytest -q
cd apps/web && npm run check:i18n && npm run test:web
```

## Notes

- 已完成的部分可以照抄：`apps/web/lib/warnings.ts`、`messages/*/trips.json` 的 `route.warning` 與 `weather.warning`、`messages/*/search.json` 的 `results.warning`。
- `search/orchestrator.py:440` 特別值得優先處理：它落在搜尋結果頁的警告區，是使用者最常看到的那一個。

## claim 用了 --force，理由（claude-opus-5, 2026-09-11）

唯一的重疊是 `apps/api/app/trips/router.py`，落在 `2026-09-10-seoul-day2-transport-ux`
（codex-seoul-day2-release）的 scope 裡。那張 claim 於 09-10 06:16，已超過 24 小時（協定上
stale），遠端分支 `codex/seoul-day2-transport-ux` 已不存在，工作也已合併進 main
（`5f34f77 fix: restore Seoul transit queries and readable travel details`，在 `origin/main` 上）。
只是那張任務沒標 `done`。

## 完成紀錄（claude-opus-5, 2026-09-11）

### 帶參數的表示法

`code?name=value&name2=value2`，值做 percent-encode，參數依名稱排序。

- 後端 `apps/api/app/warnings.py` 的 `warning_code(code, **params)`；非 lower_snake_case 的
  code 直接 `ValueError`，免得某天有人把一整句話當 code 送出去，前端會把它當代碼查表、
  查不到就整句消失。
- 前端 `apps/web/lib/warnings.ts` 以第一個 `?` 切開，用 `URLSearchParams` 解回值，交給
  `translate(key, values)`。
- **舊資料安全**：`translateWarnings` 一直是「看形狀決定」——不像代碼的原樣顯示。已經寫進
  `warnings_json` 的整句繁中因此照常顯示，不會消失也不會變成識別字。schema 沒有動，
  一則警告仍然是 JSON 陣列裡的一個字串。
- 兩邊都有測試：`apps/api/tests/test_warning_codes.py`、`apps/web/lib/warnings.test.ts`
  （含「句子裡剛好有問號」不能被誤判成代碼這一條）。

### 改了哪些

任務表列的都改了，另外**多找到三處表上沒有的**，是新加的 ratchet 掃出來的：

| 位置 | 代碼 |
| --- | --- |
| `trips/routing.py:2362-2363` | `odsay_current_service`、`odsay_polyline_is_stop_sequence` |
| `trips/route_tasks.py:335` | `route_computation_failed` |

前兩個特別值得記：它們是 ODsay 路線的 segment 警告，**真的會顯示在 `route-segment-card`
上**，也就是每一條韓國大眾運輸路線底下那兩行字，五個語系的讀者看到的都是繁中。

另外兩處原本不在「警告」的形狀裡、但其實是同一個問題：

- `trips/router.py` 的 `collect()` 把 `module_status.message` 當作警告丟給會員。那是
  provider registry 寫給營運主控台看的管理文案（「Amadeus 航班查價尚未啟用：缺少 Client ID
  或 Secret。」），不該出現在會員的搜尋結果上。改成 `provider_not_configured`。
- 同一處的 `str(exc)` 是 `amadeus/flight circuit is open`——那是 log 的句子，不是旅客的。
  改成 `provider_unavailable`。

### 一個因為改代碼而必須一起處理的地方

`trips/router.py:2229` 原本是 `detail = "；".join(warnings) or …`，把警告串成 `AppError`
的 detail 給讀者看。警告變成代碼之後，這行會把 `provider_fallback?module=flight&provider=X`
印給 zh-TW 的讀者看（`app_error_handler` 只有 zh-TW 用 `exc.detail`，其餘語系查
`ERROR_DETAILS`）。所以加了 `is_warning_code()`，只讓供應商真正寫出來的自由文字進那句話。

### 沒改的三處，以及理由

`crawlers/back_to_back.py:810,812` 與 `providers/live_back_to_back.py:274` **維持繁中整句**。

渲染端是 `airline-fare-lab.tsx:337`、`back-to-back-fare-search.tsx:651`、
`live-back-to-back-search.tsx:183`，三個都是 `result.warnings.map((warning) => …{warning})`
原樣印出，沒有 catalog 可查——送代碼過去只會把識別字印在畫面上，比現在更糟。而那三頁本來
就整頁寫死繁中，要做就是整頁做。`airline_fares` 是刻意關閉的四個功能之一（線上實測回
「尚未開放」），所以不急。另開 `2026-09-11-fare-lab-warnings-and-copy`，並把這三處寫進
ratchet 的 allow-list，理由就寫在測試檔裡。

**因此 DoD 第三項（每個渲染點都用 `translateWarnings`）沒有完全達成**：三個票價實驗室的
渲染點仍然原樣印出。不是漏掉，是刻意的，理由如上。

### 一個值得記下來的發現

`routing.warnings` 這一批——十幾個代碼——**目前沒有任何文字渲染點**。
`trip-editor.tsx:1811,1968` 只把它們數個數（「N 個路線問題」），沒有把內容印出來。
`_reoptimize` 回傳的 `provider_warnings` 更是整個前端都沒有人讀。

所以這次改完，使用者眼睛看得到的差別只有四處：搜尋結果的供應商替代通知、手動移動時間的
未驗證提醒、以及 ODsay 的那兩行。其餘是把資料改對——存進去的是代碼而不是某一種語言的句子，
哪天要顯示就顯示得出來。沒有為它們補 catalog key：`translateWarnings` 會把不認得的代碼
丟掉，補一堆沒人讀的 key 只是雜訊，等真的要顯示時再補。

### 防止復發

`apps/api/tests/test_warning_codes.py::test_no_new_warning_is_written_as_a_finished_sentence`
掃 `app/**/*.py`，在警告的上下文裡看到漢字就紅，allow-list 只有上面那三處。
`AppError(...)` 的 detail 排除在外——那是另一套契約，由 `app_error_handler` 依語系查
`ERROR_DETAILS`，zh-TW 的句子寫在那裡是對的。

寫成掃原始碼而不是打端點，是因為這些警告散在十幾個 router、好幾個在供應商呼叫後面；
只有原始碼層級的規則，在下一個人加第二十六處時還會是真的。
