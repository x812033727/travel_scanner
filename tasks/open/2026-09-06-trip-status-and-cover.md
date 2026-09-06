---
id: 2026-09-06-trip-status-and-cover
title: 行程狀態標籤與封面圖
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T02:24:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/metadata.py
  - apps/api/migrations/versions
  - apps/web/components/trip-meta-editor.tsx
---

# 行程狀態標籤與封面圖

## Why

`docs/planning-flow-spec.md` §1 步驟 10 與 §6「狀態標籤＋封面圖（S）」。去趣有「規劃中／已出發／已完成」與封面，
是便宜的對等補齊；`/trips` 清單目前只有名稱與日期。

## Definition of done

- [ ] `trip_plans` 有 `status`（planning／upcoming／ongoing／done，預設由日期推導、可手動覆寫）與 `cover_image_url`。
- [ ] `PATCH /trips/{id}` 可改兩者；清單與行程頁顯示。
- [ ] 封面只接受站內上傳或既有目錄圖片，不接受任意外部 URL（避免 SSRF／混合內容）。

## Steps

- [ ] 遷移加兩欄（`if 欄位不存在` 形狀，並依 `2026-09-06-migration-backfill-untested` 的判準補測試）。
- [ ] `trip-meta-editor.tsx` 加欄位；`account-list.tsx` 顯示標籤。
- [ ] 五語系文案。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_trip_reschedule.py -q -k metadata
```

## Notes

`PATCH /trips/{id}` 的 CAS 與空 patch 驗證在 `router.py` 的 `TripMetadataPatchRequest`；新欄位要加進「至少改一個欄位」的判斷。
