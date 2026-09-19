---
id: 2026-09-12-hk-openrice-public
title: 香港 OpenRice 店家頁改為公開（僅電話訂位也顯示）
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-19T07:58:55Z
created_at: 2026-09-12T00:44:00Z
completed_at: 2026-09-19T08:00:05Z
branch: claude/host-steps-2026-09-19
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
- [x] 正式站套用後，香港有平台按鈕的店家從 2 間變成 16 間，全站從 45 間變成 59 間。
- [x] 其他國家「有頁面但不能訂位」的 23 筆維持不公開。

## Steps

- [x] 批次改判並重建資料檔；後端 loader 與前台 `reservationPlatformHref` 都驗過。
- [x] 更新查核報告的數字與說明，寫明香港的例外。
- [x] PR、合併、部署，在 api 容器重跑 `apply-food-platform-reviews`（先試跑再套用）。

## How to verify

- `cd apps/api && pytest tests/test_food_platform_review_import.py`
- 部署後試跑：`docker compose -f docker-compose.prod.yml exec -T api python -m app.cli apply-food-platform-reviews`，應顯示 14 筆 would_update。
- 套用後：`select count(distinct merchant_id) from food_merchant_platform_links where status='verified'` 應為 59；公開 API 的 `reservation_links` 非空店家數同樣是 59。

## Notes

- 這 14 筆在正式站上是由批次指令寫入的（沒有審核人），所以批次可以更新它們；
  2026-09-11 由後台帳號人工審核的 36 列仍然不會被動到。
- 香港另外 2 筆能線上訂位的是 Arca Society（inline）與 FRANCIS（SevenRooms），不受這次影響。
- 相關：`2026-09-11-food-reservation-link-backfill`（本次資料的來源）。

### 釋出認領（由站主授權，2026-09-19）

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

資料與程式已隨 PR #414 於 2026-09-12 合併。原持有者 claude-opus-5（2026-09-12 認領）。

正式站有沒有跑過 `apply-food-platform-reviews`（香港有平台按鈕的店家應從 2 間變 16 間）沒有紀錄。接手時先查正式站的數字，還沒套用就先試跑再套用。

### 2026-09-19 正式站查核（claude-fable-5-1）

公開 API `GET /api/travel/foods/merchants?limit=50` 逐頁（7 頁、331 家）統計：`reservation_links` 非空的
店家 59 家，其中香港 5 家（tim-ho-wan、yat-lok、arca-society、francis、oolaa-petite）。14 筆 OpenRice
若已套用，香港至少會有 16 家，所以 **`apply-food-platform-reviews` 還沒在正式站跑過**。全站 59 這個數字
是日本第二輪之後的基準（見 `2026-09-13-non-japan-platforms.md`），不再是本票寫的 45 → 59。

站主在主機上要跑的（先試跑再套用，兩者都在 api 容器）：

```bash
cd /root/travel_scanner
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli apply-food-platform-reviews            # 試跑：應列出 14 筆 would_update
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli apply-food-platform-reviews --apply    # 套用
```

套用後用同一支公開 API 重數：香港應為 16 家、全站 59 + 14 = 73 家（若同一家店已有其他平台連結，數字會少於 73；以
`select count(distinct merchant_id) from food_merchant_platform_links where status='verified'` 為準）。
這一輪沒有動任何資料檔，只補了這段查核；認領已釋出。

### 2026-09-19 主機執行（claude-opus-5，站主逐項同意；部署 `6a254971` 之後）

- 試跑 `apply-food-platform-reviews`：311 筆，`would_update 15`、`unchanged 296`、0 skipped。15 筆是 14 筆香港 OpenRice（verified）加 `seoul-hanikalgugsu` 的 CatchTable（ambiguous，不公開）；票上寫 14 筆，差的就是這一筆。
- 套用 `--apply`：`applied: true`、`updated 15`、0 skipped。被更新的列只有 verified 14、ambiguous 1，沒有任何 disabled 的列被改動，所以「有頁面但不能訂位」的列維持不公開。
- 公開 API `foods/merchants?destination_id=hong-kong`：21 間公開店家裡 19 間有訂位連結（openrice 17、inline 1、sevenrooms 1），#559 記錄的套用前是 5 間。預測的「2 → 16」是 9/12 的基準，中間其他批次也改過，這裡記實際數字。
