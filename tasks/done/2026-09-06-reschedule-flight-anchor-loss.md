---
id: 2026-09-06-reschedule-flight-anchor-loss
title: 延長行程會摧毀已填的航班訂位且不提示
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T02:42:57Z
created_at: 2026-09-06T00:55:17Z
completed_at: 2026-09-06T02:55:51Z
branch: claude/trip-api-p1
depends_on: []
scope:
  - apps/api/app/trips/reschedule.py
  - apps/api/tests/test_trip_reschedule.py
  - apps/web/components/trip-meta-editor.tsx
  - apps/web/components/trip-meta-editor.test.tsx
  - apps/web/lib/trip-types.ts
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 延長行程會摧毀已填的航班訂位且不提示

## Why

`PATCH /trips/{id}`（PR #155）已經上線。**純粹延長行程 —— 一個不會丟掉任何東西、
因此永遠不需要 `confirm_removed_days` 的操作 —— 會無聲清空使用者手動填入的回程航班訂位。**

情境（審查者給的可重現序列）：

行程 2026-11-10 → 11-12，使用者在 11-12 的 `return_flight` 錨點填了真實班機
（`data.flight_info` = JAL JL802、TPE→NRT、起降時間）。他們延長兩天：

```
PATCH /trips/{id} {"version": 4, "end_date": "2026-11-14"}
```

`content_offset` 是 0，沒有任何東西落到範圍外，所以 `plan.removed_days == ()`，
`ensure_shrink_confirmed`（`reschedule.py:391`）直接 return —— 不需要任何確認。
但 `plan_reschedule` 把 `flight_targets["return_flight"]` 設成 11-14，於是 11-12 的錨點被搬動，
因為 `keeper.day_date != day_target and keeper.data.get('flight_info')`（:237-240），
它的 id 進了 `invalidated_flight_item_ids`。`apply_reschedule`（:373-376）呼叫 `clear_flight_anchor`，
把 title、location_name、start_time、end_time、offer_id 清空，`data['flight_info']` 設為 None。

**班號沒了，無法復原。**

更糟的是回報看不到：`protected`（:256-265）只從 `removed_items` 建立，而 keeper 在 :243-244
被明確排除在 `removed_items` 之外，所以 `_protected_kind` 的 `booked_flight` 分類對被搬動的錨點
永遠不可能觸發。`reschedule_summary` 只回報一個計數 `invalidated_flight_anchors: 1`，沒有標題、沒有日期。

網頁端有一則 `meta.flightNotice` 提示（`trip-meta-editor.tsx:308`），所以有讀提示的網頁使用者會知道；
但伺服器端沒有任何把關，任何其他呼叫端、或沒讀提示的使用者，都會在一個「我只是加幾天」的操作裡失去手填的訂位資料。

現行測試 `test_trip_reschedule.py:640` 把這個行為釘成**預期行為**
（對一個會清掉同一個航班的縮短操作斷言 `kinds == {'activity'}`），所以修的時候要一併改那個測試。

## Definition of done

- [x] 任何會摧毀已填航班訂位的日期變更，都需要與刪除日期同一個確認機制。
- [x] 回報裡看得到是哪一班、哪一天被清掉，不只是一個數字。
- [x] 現行把這個行為釘成預期的測試被改成反向斷言。

## Steps

- [x] 對 `invalidated_flight_item_ids` 裡的每個 id 產生 `ProtectedRow(kind='booked_flight')`，
      帶上錨點的標題和目標日期。
- [x] 把 `ensure_shrink_confirmed` 的條件放寬成
      `if not (plan.removed_days or plan.invalidated_flight_item_ids) or confirmed: return`，
      讓同一個 `confirm_removed_days` 旗標也守住被摧毀的航班訂位。
- [x] 更新 `test_trip_reschedule.py:640` 及相關斷言。
- [x] 前端：延長操作也要顯示航班會被重設的警告與確認。

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider tests/test_trip_reschedule.py
```

手動：建立行程、在回程航班錨點填入班號與時間、只延長 end_date、
確認若沒有明確確認就不會清掉，且回報說得出是哪一班。

## Notes

**2026-09-06 完成。** `plan_reschedule` 對每個被重新定日的已訂航班 keeper 記一筆 `InvalidatedFlight`
（id、role、標題、班號、原日、目標日），同時把它以 `ProtectedRow(kind="booked_flight")` 併進 `protected_rows`；
`ensure_shrink_confirmed` 改成 `if confirmed or not (removed_days or invalidated_flights): return`，
純延長或平移而清掉訂位時回 422（同一個 `trip_shrink_confirmation_required` 代碼，訊息點名班號）；
`reschedule_summary` 新增 `invalidated_flights: [{role,title,flight_number,from_day,to_day}]`，舊的計數保留。
測試：原本釘住舊行為的 `test_shrinking_reports_the_content…` 改成斷言 `booked_flight` 出現；
`test_shrinks_that_drop_days_require…` 的「無害平移」現在分成兩段（有訂位的平移要確認、沒訂位的不用）；
新增 `test_a_pure_extension_that_clears_a_booked_flight_needs_the_same_consent`；
`test_shifting_a_fully_populated_trip…` 的 `protected_rows == ()` 改成兩筆 `booked_flight`。
前端 `trip-meta-editor.tsx`：`needsConfirmation = droppedDays.length > 0 || flightsReset`，
同一個確認框（文案依情況用 `meta.removedConfirm` 或新的 `meta.flightConfirm`），送 `confirm_removed_days: true`；
伺服器回 `trip_shrink_confirmation_required` 時顯示新的 `meta.confirmRequired`。
scope 加了 `tests/test_trip_reschedule.py`、`trip-meta-editor.tsx`（含測試）、`messages/*/trips.json`。

出處：補跑 #155 缺的六路對抗式審查，`reschedule-corruption` 審查者，嚴重度 high。
`suggestedFix` 就是上面 Steps 的前兩點，是審查者原文給的。

**這段程式碼已經在正式站上運作**，所以這不是「還沒上線的東西」，是既有使用者已經暴露在其中的風險。
