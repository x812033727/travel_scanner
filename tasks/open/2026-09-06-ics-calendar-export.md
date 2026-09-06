---
id: 2026-09-06-ics-calendar-export
title: ICS 行事曆匯出
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T02:24:52Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/ics.py
  - apps/api/app/trips/export_router.py
  - apps/web/components/trip-tools-panel.tsx
---

# ICS 行事曆匯出

## Why

`docs/planning-flow-spec.md` §1 步驟 12 與 §6 PR 11 的前半。所有時間都已經算好（`start_time`／`end_time`、路段的
`departure_time`／`arrival_time`），匯出只是序列化。使用者把行程丟進手機行事曆之後，出門當天
不用再開網站。

## Definition of done

- [ ] `GET /trips/{id}/export.ics` 回傳合法的 RFC 5545 檔案，每個項目一個 `VEVENT`，時區正確（`trip.timezone`）。
- [ ] 路段以 `DESCRIPTION` 附在下一個項目上（模式、分鐘、票價、轉乘、月台／出口若有）。
- [ ] 估算的路段在五個語系都標成「估算」。
- [ ] 行程頁工具面板有「匯出到行事曆」按鈕。

## Steps

- [ ] `apps/api/app/trips/ics.py`：手寫序列化（折行 75 字元、`\,` 逸出、`VTIMEZONE` 或 `TZID` 引用），不加新 Python 相依。
- [ ] `apps/api/app/trips/export_router.py`：掛在 `owned_trip()` 之後，`Content-Disposition: attachment`。
- [ ] 前端按鈕（`trip-tools-panel.tsx` 或現有工具面板），五語系文案。
- [ ] 測試：用 Python 標準庫解析輸出、比對每個 `DTSTART` 與項目時間；多日、跨午夜航班、`is_skipped` 項目略過。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_trip_ics.py -q
```

手動：匯出後用 Google Calendar 與 iOS 行事曆各匯入一次，時間不偏移。

## Notes

規格把「列印版」與 ICS 放同一張 PR；這裡拆開，因為 ICS 純後端、風險低，可以先出。
