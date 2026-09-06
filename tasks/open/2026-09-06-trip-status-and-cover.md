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

`docs/planning-flow-spec.md` §1 步驟 10 與 §6「狀態標籤＋封面圖（S）」。**後端已經做完一半以上**：
`0038_trip_metadata`（PR #155）加了 `trip_plans.status`（planning／ready／travelling／closed）與
`cover_image_url`，`PATCH /trips/{id}` 兩者都收（`TripMetadataPatchRequest`，https 檢查在
`router.py` 約 221 行），`serialize_trip` 也都輸出；`trip-meta-editor.tsx` 已經有狀態下拉選單。

還缺的是使用者看得到的部分：`/trips` 清單沒有狀態標籤、沒有任何地方能設定或顯示封面圖。
去趣的「規劃中／已出發／已完成」與封面是便宜的對等補齊。

## Definition of done

- [ ] `/trips` 清單（`account-list.tsx`）每張卡顯示狀態標籤，五語系（`trips.json` 的 `meta.status.*` 已有）。
- [ ] `trip-meta-editor.tsx` 可設定封面圖；行程頁與清單顯示它。
- [ ] 封面只接受站內上傳或既有目錄圖片（景點／店家的圖片 URL），不接受任意外部 URL——
      後端目前只驗 https，這裡要收緊成白名單主機，避免混合內容與 SSRF 味道的外連。
- [ ] 沒有手動設定狀態時，前端依日期推導顯示（今天在 start～end 之間顯示「旅行中」），不寫回資料庫。

## Steps

- [ ] `account-list.tsx` 加標籤；`trip-editor.tsx` 標頭顯示封面（有的話）。
- [ ] `trip-meta-editor.tsx` 加封面欄位（先做「從這趟行程的景點圖片挑一張」，不做上傳）。
- [ ] 後端 `cover_image_url` 驗證改成主機白名單（`TripMetadataPatchRequest`），加測試。
- [ ] 五語系文案。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_trip_reschedule.py -q -k metadata
cd apps/web && npx vitest run components/account-list components/trip-meta-editor
```

## Notes

不需要新遷移：欄位、索引（`ix_trip_plans_status`）與 PATCH 驗證都在 #155。
`TripMetadataPatchRequest` 的「至少改一個欄位」檢查排除了 `version` 與 `confirm_removed_days`，新欄位不必動它。
