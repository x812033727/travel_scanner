---
id: 2026-09-06-intent-diff-mismatch
title: 意圖列的 diff 與 apply 實際行為不一致
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T03:09:37Z
created_at: 2026-09-06T00:55:05Z
completed_at: 2026-09-06T03:25:12Z
branch: claude/intent-bar-fixes
depends_on: []
scope:
  - apps/api/app/trips/intents.py
  - apps/api/tests/test_trip_intents.py
---

# 意圖列的 diff 與 apply 實際行為不一致

## Why

意圖列（`POST /trips/{id}/intents`，PR #168，已合併進 main）的整個賣點是：使用者打「第二天下雨，改室內」，
先看到一份 diff（移除／新增／移動），確認後才套用。**這份 diff 目前會說謊。**

六路對抗式審查找到兩個 blocker，兩個都已隨 #168 進入 main：

1. **被算進 `unchanged_count` 的項目其實會被刪除再重建。** `intents.py:239-250` 只比對候選 key 是否仍在同一
   時段，但 apply 是把整列刪掉、從規劃器草稿重新插入。使用者在那一列上的備註、停留時間、手動改過的地點名稱，
   全部消失，而 diff 說「這 N 個安排維持不變」。

2. **AI 選的餐廳列會被 apply 整列覆寫**（備註、location_name、座標、provider_place_id、data），
   但 `build_intent_diff` 只在標題改變時才產出餐食項目。改了地點但同名的情況完全不會出現在 diff 裡。

少報的 diff 比沒有 diff 更糟：使用者是在「我已經看過會發生什麼」的前提下按下套用的。

## Definition of done

- [x] 對任何一次精修，diff 報告的內容與 apply 實際執行的刪除／新增／覆寫完全一致。
- [x] 被標為「維持不變」的項目，套用後使用者輸入的每一個值都還在（或該列根本沒被重寫）。
- [x] 有測試會在 diff 與 apply 不一致時失敗 —— 不是分別測兩邊，是交叉比對同一個輸入。

## Steps

- [x] 讀 `wip/intent-bar-blocker-fixes` 分支，round 1 已經做過一次完整的修法（見 Notes），先判斷要沿用還是重做。
- [x] 讓 diff 與 apply 共用同一份「這次會寫入什麼」的描述，而不是各自算一遍。
- [x] 決定並實作：被重新提出的項目，使用者的編輯是帶過去（carry forward）還是誠實回報為變更。
- [x] 餐廳列的比對要涵蓋 location_name、provider_place_id、座標，不只標題。
- [x] 加交叉比對測試：同一輸入下建 diff、再跑 apply 的列級路徑，兩者不一致就失敗。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_intents.py
```

手動：建一個有 AI 安排的行程，在某個未鎖定的 AI 項目上寫備註並改停留時間，
用意圖列精修同一天，確認 diff 若說該項目不變，套用後備註和停留時間都還在。

## Notes

**2026-09-06 完成（與其他三張意圖列任務同一個 PR）。** 以 `wip/intent-bar-blocker-fixes`（75d6103）
cherry-pick 到當前 main 為底：`apps/api/app/trips/replan.py` 的 `build_replan_write()` 是 diff 與 apply 唯一的
「這次會寫入什麼」描述，`build_intent_diff`、`_replan_records`、`apply_meal_writes`、`reuse_rows` 都讀它。
使用者的編輯（備註、停留時間＋重算 end_time、標題、確認過的地點、is_skipped）帶到重新提出的列上；
帶不過去的欄位進 `changed` 群組並列出欄位名，`unchanged_count` 只算真的不變的列。
測試 `apply_and_check()` 先建 diff、再跑 apply 自己的列級路徑（含 `reuse_rows`），不一致就失敗。

接 main 時補了 wip 沒有的兩件事：(1) main 在 #168 之後把餐食列的五語系 `names_json` 加進
`_sync_ai_meal_slots`／`unset_meal_title`，這兩個函式已搬進 replan.py，所以 `apply_meal_writes`、
`apply_carried_values`、`reuse_rows` 現在都維護 `names_json`（改名／自選地點時比照 `apply_item_request` 丟掉對應的目錄標籤）；
(2) round 2 留下的 `_hhmm`／`_zone` 是 `replan.wall_clock`／`trip_zone`。

**半成品分支：`wip/intent-bar-blocker-fixes`（commit `75d6103`，不可合併，不會 build）。**

那個分支上 round 1 已經把這兩個 blocker 修完並跑綠過（API 776 passed）。做法是：

- 新增 `apps/api/app/trips/replan.py`，內含 `build_replan_write()` —— 單一份「哪些列會被刪、哪些會被插入、
  每個餐廳時段會變成什麼」的描述，讓 `apply_trip_itinerary_preview`、`generate_trip_itinerary` 和
  `build_intent_diff` 三者都讀它。
- apply 改成把使用者的編輯帶到重新提出的列上（備註、停留時間＋重算 end_time、標題、確認過的地點、is_skipped）。
  規則是「當儲存值不等於規劃器自己寫的那個值時就帶過去」（`notes != data["reason"]`；
  `location_source` 不在 `{hotspot_catalog, food_merchant_catalog}`）。
- 帶不過去的欄位變成新的 `changed` 群組並列出欄位名，所以 `unchanged` 真的代表不變。
- 測試用 `apply_and_check()`：先建 diff，再跑 apply 自己的列級路徑，不一致就失敗。
  round 1 有把舊語意 monkeypatch 回去驗證這些測試真的會抓到問題。

**但那個分支不能直接用**：後續 round 2 被中途停止，留下 `tests/test_trip_intents.py` 引用了不存在的 `_hhmm`，
所以測試收集會失敗。要嘛補完那個符號，要嘛回退測試檔到 round 1 的狀態。

另外 round 2 的複查指出 round 1 的修法還不夠：見 `2026-09-06-intent-route-segment-cascade`，
帶欄位值不等於保住列的身分，交通時間仍會被 cascade 清掉。這兩張任務要一起想。
