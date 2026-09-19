---
id: 2026-09-12-tables-coffee-closed
title: TABLES Coffee Bakery & Diner 已停業，仍公開在大阪美食清單
status: done
priority: P2
area: ops
owner: claude-opus-5
claimed_at: 2026-09-19T07:58:57Z
created_at: 2026-09-12T05:58:48Z
completed_at: 2026-09-19T08:00:06Z
branch: claude/host-steps-2026-09-19
depends_on: []
scope:
  - apps/api/app/foods/data/trend_merchants.json
---

# TABLES Coffee Bakery & Diner 已停業，仍公開在大阪美食清單

## Why

查訂位平台連結時發現，食べログ 把 `osaka-kyoto-tables-coffee-bakery-diner`（大阪市西区南堀江2-9-10）
標成「[已停業]」，ぐるなび 的店頁（`c018405`）已經轉回首頁，ホットペッパー 的店頁（`strJ001010936`）回 404。
三個平台同時消失通常就是真的收了，但這家店現在還公開在 `/zh-TW/foods` 上。

## Definition of done

- [x] 確認是否真的停業（官方帳號、Google 地圖、當地報導其中之一）。（2026-09-19：經營公司官方公告，見 Notes）
- [x] 若已停業，從公開清單下架，並記下判定來源。

## Steps

- [x] 查證。
- [x] 下架或保留，兩種結果都把證據寫進票裡。
- [x] 順手看看同一批種子裡有沒有別家也是三個平台同時查無。（2026-09-19：三份平台查核檔裡只有這一家帶停業字樣；其餘「closed」都是公休日）

## How to verify

`https://mokaair.com/api/travel/foods/merchants?limit=50` 逐頁找 `tables-coffee-bakery-diner`，
下架後應該查不到。

## Notes

- 食べログ：`https://tabelog.com/tw/osaka/A2701/A270105/27067976/` 標題含「[已停業]」。
- 相關：`2026-09-12-japan-korea-reservation-platforms`（那輪把這家的食べログ頁存成停用，理由寫的是已停業）。

### 2026-09-19 查證結果（claude-fable-5-1）

**已停業，證據是官方公告。** 經營公司 CAFECO 的公告頁 `https://www.cafeco-foods.com/info/TABLESCoffeeBakeryDiner`
（標題「【TABLES Coffee Bakery & Diner】南堀江店 閉店のお知らせ」，發布 2026-07-06）寫明
「2026年7月31日（金）をもちまして、閉店させていただくこととなりました」。旁證：食べログ標題「[已停業]TABLES Coffee
Bakery & Diner」、ぐるなび `c018405` 轉回首頁、ホットペッパー `strJ001010936` 回 404。店家自己的官網
`tables-coffeebakerydiner.com` 還掛著，但最後一篇貼文是 2026-01-20，沒有更新，不能當作仍在營業的證據。

**這次改了什麼**：`apps/api/app/foods/data/trend_merchants.json` 這一筆的 `note` 改成停業說明（不刪，
`test_trend_import` 釘著 146 筆，而且匯入對既有 slug 會跳過，留著只是提醒下一輪不要再核准）。
正式站 2026-09-19 查公開 API 仍列出 `osaka-kyoto-tables-coffee-bakery-diner`。

**剩下要站主做的（正式資料）**：後台「美食店家」面板搜尋 `osaka-kyoto-tables-coffee-bakery-diner`，勾選後按
「停用」（`POST /api/v1/admin/foods/merchants/batch`，`action: "disable"`，會把 `review_status` 設為 `disabled`、
`is_active` 設為 false，留稽核）。之後用 `https://mokaair.com/api/travel/foods/merchants?limit=50` 逐頁確認
查不到，再把本票 `done`。認領已釋出。

### 2026-09-19 主機執行（claude-opus-5，站主逐項同意；部署 `6a254971` 之後）

- 站主在 `/zh-TW/admin/foods?tab=catalog&section=merchants` 勾選本店後按「批次停用」（`POST /admin/foods/merchants/batch`，action `disable`）。資料庫 2026-09-19 07:53:13 UTC 起為 `review_status = disabled`、`is_active = false`；公開 API 在 `osaka-kyoto` 查 `TABLES` 為 0 筆。
- 批次端點不收理由，判定來源就是本票上面的官方閉店公告與三個平台的狀態。
