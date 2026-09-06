---
id: 2026-09-06-ai-warning-copy
title: AI 備援警告把 provider 名稱與 Python 例外類別秀給旅客看
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T14:52:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/ai/itinerary.py
  - apps/api/tests/test_ai_itinerary.py
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

- [ ] 旅客看到的是「AI 這次沒排出來，已改用核准景點目錄先排一版」這個層級的說法，
      沒有供應商代號、沒有例外類別。
- [ ] 這些警告字串跟著請求語系走（或改成前端可翻譯的代碼），不再寫死繁中。
- [ ] `logger.warning` 保留現在的細節。

## Steps

- [ ] 把 `warnings.append(f"{provider.name} 暫時無法產生有效行程（…）")` 換成
      穩定的代碼（例如 `planner_provider_failed`），前端在 `trips.json` 對應文案。
- [ ] 同一個函式裡另外三處（`AI 未完整涵蓋所有日期…`、`AI 行程規劃超過整體等待時間`、
      `已改用核准地點目錄產生備援草稿`）一起處理。
- [ ] 測試：provider 丟 `httpx.HTTPStatusError` 時，回傳的 warnings 不含
      provider 名稱與例外類別。

## Notes

- 前端 `trip-editor.tsx` 目前是直接把 `trip.planning.warnings[]` 印出來，所以
  改成代碼之後前端要跟著加對應表；兩邊要同一個 PR 或有先後順序。
- 這是 2026-09-06 全站 UI/UX 健檢的一部分，其他項目見
  `tasks/open/2026-09-06-*`。
