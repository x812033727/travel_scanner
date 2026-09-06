---
id: 2026-09-06-trip-status-and-cover
title: 行程狀態標籤與封面圖
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T11:07:21Z
created_at: 2026-09-06T02:24:53Z
completed_at: 2026-09-06T11:07:22Z
branch: claude/trip-status-cover
depends_on: []
scope:
  - apps/api/app/trips/metadata.py
  - apps/api/migrations/versions
  - apps/web/components/trip-meta-editor.tsx
  - apps/api/app/trips/router.py
  - apps/api/tests/test_trip_cover_image.py
  - apps/web/components/account-list.tsx
  - apps/web/components/account-list.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-meta-editor.test.tsx
  - apps/web/lib/trip-types.ts
  - apps/web/lib/trip-status.test.ts
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
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

- [x] `/trips` 清單（`account-list.tsx`）每張卡顯示狀態標籤，五語系（`trips.json` 的 `meta.status.*` 已有）。
- [x] `trip-meta-editor.tsx` 可設定封面圖；行程頁與清單顯示它。
- [x] 封面只接受站內上傳或既有目錄圖片（景點／店家的圖片 URL），不接受任意外部 URL——
      後端目前只驗 https，這裡要收緊成白名單主機，避免混合內容與 SSRF 味道的外連。
- [x] 沒有手動設定狀態時，前端依日期推導顯示（今天在 start～end 之間顯示「旅行中」），不寫回資料庫。

## Steps

- [x] `account-list.tsx` 加標籤；`trip-editor.tsx` 標頭顯示封面（有的話）。
- [x] `trip-meta-editor.tsx` 加封面欄位（先做「從這趟行程的景點圖片挑一張」，不做上傳）。
- [x] 後端 `cover_image_url` 驗證改成主機白名單（`TripMetadataPatchRequest`），加測試。
- [x] 五語系文案。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_trip_reschedule.py -q -k metadata
cd apps/web && npx vitest run components/account-list components/trip-meta-editor
```

## Notes

不需要新遷移：欄位、索引（`ix_trip_plans_status`）與 PATCH 驗證都在 #155。
`TripMetadataPatchRequest` 的「至少改一個欄位」檢查排除了 `version` 與 `confirm_removed_days`，新欄位不必動它。

2026-09-06 claude-opus-5：

- **scope 修正**：`apps/api/app/trips/metadata.py` 不存在，`TripMetadataPatchRequest` 與驗證都在
  `apps/api/app/trips/router.py`；也不需要遷移（欄位在 #155 就有）。scope 依實際改動補齊。
- 後端：`cover_image_url` 從「只要是 https」收緊成主機白名單 `COVER_IMAGE_HOSTS`
  （i.ytimg.com、img.youtube.com、lh3–lh5.googleusercontent.com、upload/commons.wikimedia.org、
  mokaair.com、www.mokaair.com），也就是本站已經在顯示圖片的那些來源。
  `tests/test_trip_cover_image.py` 釘住：允許的主機過、http 不過、`evil.i.ytimg.com.attacker.test`
  這種後綴假冒不過、`javascript:` 不過、內網 IP 不過，空字串仍然是「清除封面」。
- 清單：`account-list.tsx` 每張行程卡多一個狀態標籤（用既有的 `trips.meta.status.*`，五語系），
  有封面就用封面當縮圖、沒有就維持原本的圖示。
- 推導狀態：`displayTripStatus()` 放在 `lib/trip-types.ts`——**只有在狀態還停在預設的 planning
  且今天落在 start～end 之間**時才顯示「旅行中」，使用者自己選過的狀態一律照他的。不寫回資料庫。
  `lib/trip-status.test.ts` 釘住邊界（第一天、最後一天、前一天、後一天、已選狀態、沒有日期）。
- 封面設定：`trip-meta-editor.tsx` 多一個網址欄位，說明文字寫清楚接受哪些來源；
  行程頁標題與清單卡都會顯示它。

**沒有做「從這趟行程的景點圖片挑一張」**：`TripPlanItem` 上根本沒有任何圖片欄位或 URL
（`data` 裡也沒有），所以現在無圖可挑。要做那個 picker，得先讓行程項目帶著景點的縮圖
（景點介紹的 `thumbnail_url` 或 Google 地點照片），那是另一張票的規模；先做成貼網址＋白名單，
使用者仍然設得了封面，而且不可能貼進任意外部網域。
