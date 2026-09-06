---
id: 2026-09-06-trip-stale-price-after-reschedule
title: 日期變更後行程價格停在舊報價且無法重新查價
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:55:30Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/reschedule.py
  - apps/api/app/trips/router.py
---

# 日期變更後行程價格停在舊報價且無法重新查價

## Why

`PATCH /trips/{id}` 已上線。`reschedule_trip_data`（`reschedule.py:403-438`）很仔細地重建了四個
帶日期的 `trip.data` 區塊，**但沒有動 `prices_checked`、`reoptimized_at`，也沒有動
`trip_plans.total_price` 欄位**。

同時 `search_dates_diverged` + `router.py:1396-1400` 的 409 讓
`POST /trips/{id}/reoptimize` 對任何日期變動過的行程**永久失敗** ——
因為它比對的是那份不可改寫的原始 SearchRequest。

結果：使用者把東京行程從 11 月平移到 12 月之後，行程標頭仍然印著 11 月那筆 NT$42,000，
`PriceAlertButton` 仍然用那個數字建立價格追蹤，而按下「重新查價」每次都得到 409。
**產品內沒有任何路徑可以把這個數字改回正確的。**

錯誤訊息建議「重新搜尋並另存新行程」，但帳號有 20 個已存行程的上限，等於要付出一個名額。

## Definition of done

- [ ] 日期變更後，行程不會繼續宣稱一個為舊日期報的價格。
- [ ] 使用者在產品內有辦法取得新日期的價格，或者清楚看到目前沒有報價。

## Steps

- [ ] 在 `reschedule_trip_data` 裡比照 routing 的作法讓價格失效：
      清掉 `prices_checked` / `reoptimized_at`，或標記 `prices_stale`。
- [ ] `serialize_trip`、網頁標頭與 `PriceAlertButton` 在價格失效時要隱藏或標註，而不是照常顯示。
- [ ] 或者（審查者提的另一條路）讓 `refreshed_plan` 用行程自己當下的 start_date/end_date 重建
      （`model_copy` 那個 `SearchCreate`），而不是硬性拒絕 —— 這樣就沒有死路了。
- [ ] 兩條路選一條並說明理由。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_reschedule.py
```

手動：存一個有總價的行程，平移日期，確認標頭不再宣稱舊價格，且重新查價不是死路。

## Notes

出處：補跑 #155 的六路審查，`reschedule-corruption` 審查者，嚴重度 high。

同一個審查者另外指出一個相關的中等問題（已另開任務
`2026-09-06-reoptimize-no-version-check`）：`search_dates_diverged` 在 `return_date` 為 NULL 時
第二個條件整個失效，所以單程搜尋建立的行程會繞過這個守衛，然後被永久 422 鎖住 ——
正是這個守衛當初要防的那件事。
