---
id: 2026-09-06-ics-calendar-export
title: ICS 行事曆匯出
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T10:50:18Z
created_at: 2026-09-06T02:24:52Z
completed_at: 2026-09-06T10:50:22Z
branch: claude/trip-api-extras
depends_on: []
scope:
  - apps/api/app/trips/ics.py
  - apps/api/app/trips/export_router.py
  - apps/web/components/trip-tools-panel.tsx
  - apps/api/app/main.py
  - apps/api/tests/test_trip_ics.py
  - apps/web/components/trip-editor.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# ICS 行事曆匯出

## Why

`docs/planning-flow-spec.md` §1 步驟 12 與 §6 PR 11 的前半。所有時間都已經算好（`start_time`／`end_time`、路段的
`departure_time`／`arrival_time`），匯出只是序列化。使用者把行程丟進手機行事曆之後，出門當天
不用再開網站。

## Definition of done

- [x] `GET /trips/{id}/export.ics` 回傳合法的 RFC 5545 檔案，每個項目一個 `VEVENT`，時區正確（`trip.timezone`）。
- [x] 路段以 `DESCRIPTION` 附在下一個項目上（模式、分鐘、票價、轉乘、月台／出口若有）。
- [x] 估算的路段在五個語系都標成「估算」。
- [x] 行程頁工具面板有「匯出到行事曆」按鈕。

## Steps

- [x] `apps/api/app/trips/ics.py`：手寫序列化（折行 75 字元、`\,` 逸出、`VTIMEZONE` 或 `TZID` 引用），不加新 Python 相依。
- [x] `apps/api/app/trips/export_router.py`：掛在 `owned_trip()` 之後，`Content-Disposition: attachment`。
- [x] 前端按鈕（`trip-tools-panel.tsx` 或現有工具面板），五語系文案。
- [x] 測試：用 Python 標準庫解析輸出、比對每個 `DTSTART` 與項目時間；多日、跨午夜航班、`is_skipped` 項目略過。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_trip_ics.py -q
```

手動：匯出後用 Google Calendar 與 iOS 行事曆各匯入一次，時間不偏移。

## Notes

規格把「列印版」與 ICS 放同一張 PR；這裡拆開，因為 ICS 純後端、風險低，可以先出。

2026-09-06 claude-opus-5：

- `apps/api/app/trips/ics.py`：手寫序列化，沒有新的 Python 相依。折行以 **octet** 計（75 octets，
  續行前面一個空白也算），`\\`／`;`／`,`／換行照 RFC 5545 逸出。
- **時區的決定**：所有事件用 UTC 加 `Z` 輸出，不寫 `VTIMEZONE`。行程裡的時間本來就是帶時區的瞬間，
  UTC 在每個行事曆軟體都不會有歧義；自己寫 `VTIMEZONE` 規則反而會在某國改時制那天過期。
  `trip.timezone` 仍以 `X-WR-TIMEZONE` 帶出去給看得懂的軟體。
- 路段寫在「它抵達的那個項目」的 `DESCRIPTION`：交通方式、分鐘、轉乘次數、路線名、車資、
  月台與出口；估算的段在五個語系分別標成 估算／estimated／推定／추정。
- `export_router.py`：`GET /trips/{id}/export.ics`，走 `owned_trip()`，
  `Content-Disposition: attachment` 的檔名先轉成 ASCII slug（純中文名會退成 `trip-<id 前八碼>.ics`）。
  在 `main.py` 註冊，比照 `trip_stay_router`。
- 前端：**scope 寫的 `trip-tools-panel.tsx` 不存在**，工具面板是 `trip-editor.tsx` 裡的
  `PlannerOverlay`，所以按鈕加在那裡（`te("calendarTitle")` 一組五語系鍵），
  用 `<a download href="/api/travel/trips/{id}/export.ics">` 直接下載，走 BFF 帶 cookie。
- 測試：`tests/test_trip_ics.py` 六支——事件時間與 `DTSTART`、略過的項目不匯出、
  路段描述、五語系的估算標示、逸出與折行往返、跨時段航班、下載檔名。
  手動用 Google Calendar／iOS 匯入這件事還沒做，正式站部署後可驗。
