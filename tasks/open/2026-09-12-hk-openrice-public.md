---
id: 2026-09-12-hk-openrice-public
title: 香港 OpenRice 店家頁改為公開（僅電話訂位也顯示）
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-12T00:45:00Z
created_at: 2026-09-12T00:44:00Z
completed_at:
branch: claude/hk-openrice-public
depends_on: []
scope:
  - apps/api/app/foods/data/platform_reviews/2026-09-11-public-merchants.json
  - docs/catalog-content-reviews/2026-09-11-reservation-links-full.md
---

# 香港 OpenRice 店家頁改為公開（僅電話訂位也顯示）

## Why

2026-09-11 的規則是「平台頁不能線上訂位就不公開」，因此香港有 14 筆 OpenRice 店家頁被存成
停用。這些頁面都已確認是該店本身（店名與地址相符），也有營業時間、菜單與訂位電話，只是沒有
線上訂位功能——OpenRice 頁面上的 Book 按鈕其實屬於下方的推薦餐廳廣告。

2026-09-12 擁有者決定改為公開：OpenRice 是香港預設的美食平台，這些頁面對旅客仍然有用。
這個例外只適用香港，其他國家維持原規則。

## Definition of done

- [x] 14 筆香港 OpenRice 記錄由 `disabled` 改為 `verified`，每筆保留原有證據與查核說明。
- [ ] 正式站套用後，香港有平台按鈕的店家從 2 間變成 16 間，全站從 45 間變成 59 間。
- [ ] 其他國家「有頁面但不能訂位」的 23 筆維持不公開。

## Steps

- [x] 批次改判並重建資料檔；後端 loader 與前台 `reservationPlatformHref` 都驗過。
- [x] 更新查核報告的數字與說明，寫明香港的例外。
- [ ] PR、合併、部署，在 api 容器重跑 `apply-food-platform-reviews`（先試跑再套用）。

## How to verify

- `cd apps/api && pytest tests/test_food_platform_review_import.py`
- 部署後試跑：`docker compose -f docker-compose.prod.yml exec -T api python -m app.cli apply-food-platform-reviews`，應顯示 14 筆 would_update。
- 套用後：`select count(distinct merchant_id) from food_merchant_platform_links where status='verified'` 應為 59；公開 API 的 `reservation_links` 非空店家數同樣是 59。

## Notes

- 這 14 筆在正式站上是由批次指令寫入的（沒有審核人），所以批次可以更新它們；
  2026-09-11 由後台帳號人工審核的 36 列仍然不會被動到。
- 香港另外 2 筆能線上訂位的是 Arca Society（inline）與 FRANCIS（SevenRooms），不受這次影響。
- 相關：`2026-09-11-food-reservation-link-backfill`（本次資料的來源）。
