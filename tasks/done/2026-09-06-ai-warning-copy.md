---
id: 2026-09-06-ai-warning-copy
title: AI 備援警告把 provider 名稱與 Python 例外類別秀給旅客看
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T15:52:51Z
created_at: 2026-09-06T14:52:00Z
completed_at: 2026-09-06T16:28:03Z
branch: claude/ai-warning-copy
depends_on: []
scope:
  - apps/api/app/ai/itinerary.py
  - apps/api/app/trips/router.py
  - apps/api/tests/test_ai_itinerary.py
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# AI 備援警告把 provider 名稱與 Python 例外類別秀給旅客看

## Why

2026-09-06 用登入的瀏覽器打開線上一趟真的行程（`/zh-TW/trips/c66c7a9d-…`），
頁面最上面那塊黃色提示裡有一行：

> ⚠ minimax 暫時無法產生有效行程（HTTPStatusError）

`minimax` 是我們挑的供應商代號，`HTTPStatusError` 是 httpx 的例外類別名稱。旅客
既看不懂也幫不上忙，而且這串是在 `apps/api/app/ai/itinerary.py` 用 f-string 寫死
繁中組出來的，英日韓的讀者也會看到同一句中文。

同一個 except 區塊上面已經有一行 `logger.warning`，帶著 status、url 與 body 片段
——維運要的細節在 log 裡已經齊了，不需要再送到畫面上。

## Definition of done

- [x] 旅客看到的是「AI 這次沒排出來，已改用核准景點目錄先排一版」這個層級的說法，
      沒有供應商代號、沒有例外類別。
- [x] 這些警告字串跟著請求語系走（或改成前端可翻譯的代碼），不再寫死繁中。
- [x] `logger.warning` 保留現在的細節。

## Steps

- [x] 把 `warnings.append(f"{provider.name} 暫時無法產生有效行程（…）")` 換成
      穩定的代碼（例如 `planner_provider_failed`），前端在 `trips.json` 對應文案。
- [x] 同一個函式裡另外三處（`AI 未完整涵蓋所有日期…`、`AI 行程規劃超過整體等待時間`、
      `已改用核准地點目錄產生備援草稿`）一起處理。
- [x] 測試：provider 丟 `httpx.HTTPStatusError` 時，回傳的 warnings 不含
      provider 名稱與例外類別。

## Notes

- 前端 `trip-editor.tsx` 目前是直接把 `trip.planning.warnings[]` 印出來，所以
  改成代碼之後前端要跟著加對應表；兩邊要同一個 PR 或有先後順序。
- 這是 2026-09-06 全站 UI/UX 健檢的一部分，其他項目見
  `tasks/open/2026-09-06-*`。

## Result（2026-09-07 完成）

API 現在送穩定代碼，前端在 `trips.json` 的 `editor.plannerWarning` 對應五種語系的文案。

**為什麼是代碼而不是伺服器端翻譯。** 這些警告會寫進 `trip.data["planning"]`，每次打開行程
都從那裡讀回來。伺服器端在產生當下翻譯，等於把「當時是誰用哪個語系排的」凍進資料裡；日文
讀者之後打開同一趟，看到的還是排行程那個人的語系。代碼是在畫面上翻譯的，隔多久都對。

**七個代碼**（前五個在 `ai/itinerary.py`，後兩個在 `trips/router.py`，它們往同一個
`warnings` 陣列 append，只改一半會變成一半代碼一半繁中，比原狀更糟）：
`planner_partial_days`、`planner_provider_failed`、`planner_timed_out`、
`planner_fallback_used`、`planner_blank_slots:{n}`、`planner_places_unconfirmed`、
`planner_places_need_review`。

**provider 失敗只送一次**，不是每個失敗的 provider 各送一行。旅客對「哪一家掛了」無從反應，
第二行相同的話只會把提示框拉長。

**舊資料**：已經存在行程裡的繁中句子（例如「minimax 暫時無法產生有效行程（HTTPStatusError）」）
不在代碼表裡，前端一律退回一句概括的提醒，所以那些句子也不會原樣顯示給讀者。同一個機制也擋住
未來 API 新增、前端還沒對應的代碼。

`logger.warning` 一個字都沒動，status、url 與 body 片段仍在 log 裡。

**畫面上會去重。** 正式站現在有四趟行程存著舊句子，其中三趟各存三句；不去重的話它們會退回
成三行一模一樣的概括文案，看起來像畫面壞掉。去重是對讀到的文案做，所以 API 之後萬一送出
重複代碼也一樣只顯示一次。「有 11 個時段留白」這種具體資訊並沒有真的消失——同一個提示框
底下的 `unscheduled_slots` 膠囊本來就把那些時段一個個列出來，還可以點。

**順帶發現但沒有一起改**：五個語系的 `trips.json` 都有重複的 `transfersCount` 鍵。
JSON.parse 只留最後一個，所以行為沒錯，但檔案是壞的。另開
[[2026-09-06-duplicate-transfers-count-key]]。這裡刻意用純文字插入而不是重寫 JSON，
就是為了不把那個折疊混進這個 diff。

檢查：`ruff`、`mypy`、`pytest`、`lint:web`、`check:i18n`、`typecheck:web`、
`test:web -- trip-editor`（37 passed）全綠。
