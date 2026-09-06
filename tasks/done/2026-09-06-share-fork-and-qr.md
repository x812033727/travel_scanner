---
id: 2026-09-06-share-fork-and-qr
title: 分享頁「存成我的行程」與 QR code
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T10:50:19Z
created_at: 2026-09-06T02:24:53Z
completed_at: 2026-09-06T10:50:24Z
branch: claude/trip-api-extras
depends_on: []
scope:
  - apps/api/app/trips/share_router.py
  - apps/web/components/shared-trip-view.tsx
  - apps/api/app/main.py
  - apps/api/tests/test_trip_share_fork.py
  - apps/api/tests/test_integration_postgres_redis.py
  - apps/web/components/shared-trip-view.test.tsx
  - apps/web/package.json
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 分享頁「存成我的行程」與 QR code

## Why

`docs/planning-flow-spec.md` §1 步驟 11 與 §6 PR 12。分享連結目前只能看。「存成我的行程」比多人共編便宜 20 倍
（共編要重寫 `owned_trip()` 與它 20 個呼叫端），而且把分享流量轉成新帳號——共編做不到這件事。
QR code 讓現場掃碼就能拿到行程。

## Definition of done

- [x] `POST /shared-trips/{token}/fork`：登入者把分享的行程深拷貝到自己帳號（受 20 個行程上限），
      **不複製路段**（絕對時間、供應商署名），新行程以 routing-stale 開啟。
- [x] 分享頁有「存成我的行程」按鈕（未登入導向登入後回來）與 QR code。
- [x] **不動 `uq_trip_share_trip`**：`create_share` 是原地輪換 token，拿掉唯一約束會讓舊連結失效。

## Steps

- [x] `apps/api/app/trips/share_router.py`：fork 端點，複製 `TripPlanItem`／day settings／notes 不含 `trip_route_segments`；
      `limit_for(..., "saved_trips")` 檢查；審計一列。
- [x] `shared-trip-view.tsx`：按鈕＋QR（純前端產生，不呼叫外部服務）。
- [x] 整合測試：fork 後兩個行程獨立、原分享仍可開、超過上限 402/409。

## How to verify

無痕視窗開分享連結 → 登入 → 存成我的行程 → `/trips` 多一筆、原行程未變。

## Notes

分享 payload 在 `2026-09-06-share-payload-leaks-notes` 之後不再帶 `data` 與項目備註；fork 從資料庫的
原行程複製，而不是從分享 payload，所以不受那個縮減影響——但 fork 也**不該**複製原作者的備註。

2026-09-06 claude-opus-5：

- `apps/api/app/trips/share_router.py`：`POST /shared-trips/{token}/fork`。
  token 查法與 `GET /shared-trips/{token}` 相同（撤銷過的連結一樣 404），
  受 `limit_for(..., "saved_trips")` 的 20 筆上限保護（超過回 403 `trip_limit_reached`）。
  **`uq_trip_share_trip` 沒有動**。
- 複製的內容：行程本體（名稱、日期、時區、目的地、route_preference）＋每個 `TripPlanItem`
  ＋每天的 `TripRouteDaySetting`。**不複製** `trip_route_segments`（絕對時間與供應商署名），
  新行程的 `routing.status` 開在 `stale`、day setting 的 `auto_compute=False`。
  **不複製作者的備註**：`copied_item` 把 `notes` 設成 None，`data` 只留白名單七個鍵
  （timeline_section、flight_info、source_mode、needs_place_confirmation、generated_by、
  destination_city、destination_country），所以作者的報價快照與 AI 提示不會跟著走。
  `total_price` 歸零：那個數字來自作者自己的搜尋與日期，抄過來等於報一個沒人查證過的價。
- 前端 `shared-trip-view.tsx`：「存成我的行程」按鈕（401 就 `router.push` 到
  `/login?next=%2Fshare%2F<token>`，登入後回到同一個連結）與 QR code。
  QR **在瀏覽器裡畫**（新增 `qrcode` 相依，`QRCode.toDataURL(window.location.href)`），
  不呼叫任何外部服務——外部 QR 服務會知道每一條被打開過的分享連結。
- 測試：`tests/test_trip_share_fork.py`（複製規則的單元測試，備註被丟掉、白名單生效）、
  `test_integration_postgres_redis.py` 一支完整往返（複製後兩邊各自獨立、作者的備註還在、
  撤銷後不能再複製），以及 `shared-trip-view.test.tsx` 三支（複製後跳轉、未登入導向登入、QR 有畫出來）。
  超過 20 筆上限那條只在程式碼與 403 路徑上，整合測試沒有造 20 個行程去撞它。
