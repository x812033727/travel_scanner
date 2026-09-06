---
id: 2026-09-06-share-fork-and-qr
title: 分享頁「存成我的行程」與 QR code
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
  - apps/api/app/trips/share_router.py
  - apps/web/components/shared-trip-view.tsx
---

# 分享頁「存成我的行程」與 QR code

## Why

`docs/planning-flow-spec.md` §1 步驟 11 與 §6 PR 12。分享連結目前只能看。「存成我的行程」比多人共編便宜 20 倍
（共編要重寫 `owned_trip()` 與它 20 個呼叫端），而且把分享流量轉成新帳號——共編做不到這件事。
QR code 讓現場掃碼就能拿到行程。

## Definition of done

- [ ] `POST /shared-trips/{token}/fork`：登入者把分享的行程深拷貝到自己帳號（受 20 個行程上限），
      **不複製路段**（絕對時間、供應商署名），新行程以 routing-stale 開啟。
- [ ] 分享頁有「存成我的行程」按鈕（未登入導向登入後回來）與 QR code。
- [ ] **不動 `uq_trip_share_trip`**：`create_share` 是原地輪換 token，拿掉唯一約束會讓舊連結失效。

## Steps

- [ ] `apps/api/app/trips/share_router.py`：fork 端點，複製 `TripPlanItem`／day settings／notes 不含 `trip_route_segments`；
      `limit_for(..., "saved_trips")` 檢查；審計一列。
- [ ] `shared-trip-view.tsx`：按鈕＋QR（純前端產生，不呼叫外部服務）。
- [ ] 整合測試：fork 後兩個行程獨立、原分享仍可開、超過上限 402/409。

## How to verify

無痕視窗開分享連結 → 登入 → 存成我的行程 → `/trips` 多一筆、原行程未變。

## Notes

分享 payload 在 `2026-09-06-share-payload-leaks-notes` 之後不再帶 `data` 與項目備註；fork 從資料庫的
原行程複製，而不是從分享 payload，所以不受那個縮減影響——但 fork 也**不該**複製原作者的備註。
