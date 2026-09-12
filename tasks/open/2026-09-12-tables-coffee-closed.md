---
id: 2026-09-12-tables-coffee-closed
title: TABLES Coffee Bakery & Diner 已停業，仍公開在大阪美食清單
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-12T05:58:48Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/merchant_catalog.py
---

# TABLES Coffee Bakery & Diner 已停業，仍公開在大阪美食清單

## Why

查訂位平台連結時發現，食べログ 把 `osaka-kyoto-tables-coffee-bakery-diner`（大阪市西区南堀江2-9-10）
標成「[已停業]」，ぐるなび 的店頁（`c018405`）已經轉回首頁，ホットペッパー 的店頁（`strJ001010936`）回 404。
三個平台同時消失通常就是真的收了，但這家店現在還公開在 `/zh-TW/foods` 上。

## Definition of done

- [ ] 確認是否真的停業（官方帳號、Google 地圖、當地報導其中之一）。
- [ ] 若已停業，從公開清單下架，並記下判定來源。

## Steps

- [ ] 查證。
- [ ] 下架或保留，兩種結果都把證據寫進票裡。
- [ ] 順手看看同一批種子裡有沒有別家也是三個平台同時查無。

## How to verify

`https://mokaair.com/api/travel/foods/merchants?limit=50` 逐頁找 `tables-coffee-bakery-diner`，
下架後應該查不到。

## Notes

- 食べログ：`https://tabelog.com/tw/osaka/A2701/A270105/27067976/` 標題含「[已停業]」。
- 相關：`2026-09-12-japan-korea-reservation-platforms`（那輪把這家的食べログ頁存成停用，理由寫的是已停業）。
