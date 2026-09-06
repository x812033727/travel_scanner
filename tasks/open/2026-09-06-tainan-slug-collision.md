---
id: 2026-09-06-tainan-slug-collision
title: 台南兩家不同的店共用 tainan-fu-sheng-hao 這個 slug，富盛號永遠匯不進來
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T22:22:32Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/trend_merchants.json
  - apps/api/app/foods/merchant_catalog.py
  - apps/api/tests/test_trend_import.py
---

# 台南兩家不同的店共用 tainan-fu-sheng-hao 這個 slug，富盛號永遠匯不進來

## Why

`tainan-fu-sheng-hao` 這個 slug 在兩個檔案裡指向**兩家不同的店**：

| 檔案 | name | local_name |
| --- | --- | --- |
| `merchant_catalog.py`（人工策展） | Fu Sheng Hao | 福生小食店 |
| `data/trend_merchants.json`（商圈掃描） | 富盛號 | 富盛號 |

`trend_import` 的規則是「slug 看過就跳過、絕不合併」，所以正式站holds的是策展那一家
（`local_name = 福生小食店`），而**富盛號從來沒有被匯入過，也永遠不會**。

富盛號是台南知名的碗粿店，`twtainan.net/zh-tw/shop/consume/8617/` 是它的官方頁；
福生小食店是另一家。兩家都是真的，只是 slug 撞在一起。

`slug_for()` 會從名稱推 slug，`富盛號` 與 `福生小食店` 的羅馬拼音都落在 `fu-sheng-hao`，
所以這是可預期會再發生的碰撞，不是一次性的手誤。

## 這是怎麼被發現的

不是靠讀檔案。`backfill-merchant-english-names --reset-drifted` 的 dry-run 清單裡多出一筆
預期外的變更：`tainan-fu-sheng-hao | Fu Sheng Hao -> 富盛號`。套用下去會把福生小食店改名成
另一家餐廳。那個指令現在會拒絕碰策展目錄擁有的 slug，並在測試裡釘住這一筆。

## Definition of done

- [ ] 兩家店都能存在：其中一家換一個 slug（建議動 trend 檔案那一筆，因為它還沒進資料庫）。
- [ ] `slug_for()` 或匯入驗證會在**兩個目錄之間**的 slug 碰撞時報錯，而不是靜靜跳過。
      目前 `parse_merchants` 只檢查檔案**內部**的重複。
- [ ] 掃一次還有沒有別的跨檔案碰撞（`skipped_existing_slug` 的計數就是線索）。

## Steps

- [ ] 先數：`persist_trend_merchants(..., apply=False)` 的 `outcomes.skipped_existing_slug`
      現在是 1，逐筆列出來確認每一筆是「同一家店」還是「撞名的兩家店」。
      整合測試的註解說那兩家台南店是「策展目錄已經有的」，但至少這一筆不是同一家。
- [ ] 富盛號改成 `tainan-fu-sheng-hao-wan-gui` 之類，或用 QID／地址消歧義。
- [ ] `parse_merchants` 加一條：slug 若已在 `CURATED_MERCHANT_SLUGS` 而 `local_name` 不同，
      就報錯而不是跳過。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_trend_import.py -q
```

## Notes

- 這張票不改 `backfill-merchant-english-names` 的行為，那邊的防護已經加好了：
  策展目錄擁有的 slug 一律不碰。
- 別直接把策展那一筆改名，`merchant_catalog.py` 的 slug 已經在正式站資料庫裡當主鍵用。
