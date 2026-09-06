---
id: 2026-09-06-trend-food-areas-not-seeded
title: 57 個潮流商圈只存在正式機資料庫
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:53:02Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/area_catalog.py
  - apps/api/tests/test_food_taxonomy_catalog.py
---

# 57 個潮流商圈只存在正式機資料庫

## Why

2026-09-05 我用腳本往正式機的 `food_areas` 寫了 57 個潮流街區商圈（聖水洞、藏前、
赤峰街、大南街⋯），`source='admin'`。它們**不在** `AREA_SEEDS` 裡。

所以：一個全新的資料庫（本機開發、CI、災難重建）不會有這 57 個商圈。目前有 99 家
店家掛在上面，那些店家的 `area_id` 在新環境會指向不存在的列 —— 換句話說，這批資料
的完整性只靠正式機的 pg_dump 撐著。

不能直接加進 `AREA_SEEDS`：`validate_area_catalog()` 釘死「剛好 132 個」而且要和
`DestinationProfile.areas` 一對一，加進去會同時弄壞目錄驗證和住宿推薦的區域清單。

## Definition of done

- [ ] 全新資料庫跑完 seed 之後，這 57 個商圈存在且欄位（五語系名稱、搜尋詞條、中心
      座標、display_order）與正式機一致。
- [ ] 種子驗證仍然守得住原本 132 個「和 DestinationProfile 綁定」的商圈，不會被潮流
      商圈污染。
- [ ] 重跑 seed 不會覆蓋管理員在後台改過的商圈。

## Steps

- [ ] 決定形狀：建議在 `area_catalog.py` 另開一個 `TREND_AREA_SEEDS`，與 `AREA_SEEDS`
      分開驗證（前者不綁 `DestinationProfile.areas`，後者維持一對一與 132 的釘數）。
- [ ] 把 57 列資料搬進來（來源見 Notes）。
- [ ] `seed_food_taxonomy` 一併寫入，且沿用既有的「不覆蓋 admin」語意。
- [ ] 測試：兩份種子的 slug 不重疊、五語系名稱齊全、`display_order` 在同目的地內唯一、
      潮流商圈不出現在 `DestinationProfile.areas` 的比對裡。

## How to verify

```bash
cd apps/api && ./.venv/Scripts/python.exe -m pytest tests/test_food_taxonomy_catalog.py -q
```

正式機重跑 seed 之後數量不該變（189 = 132 種子 + 57 潮流）：

```sql
SELECT source, count(*) FROM food_areas GROUP BY 1;
```

## Notes

**資料在哪**：正式機 `/root/trend-food-areas.json`（57 列，欄位
`destination/key/zh_tw/zh_cn/en/ja/ko/terms/lat/lng`），以及當次 session 的 scratchpad
同名檔案。slug 規則是 `{destination}-{key}`。

**譯名是查證過的，不要重譯**。這份表第一版有 16 個錯，是 4 個分語言的 agent 逐筆對照
當地旅遊媒體抓出來的，例如：審計新村的韓文是 **심계신촌**（漢字音讀）不是
「선지 뉴빌리지」；Jalan Besar 的日文是 **ジャラン・ベサール** 不是ブサール；
북성로 的日文是 **プクソンノ**（ㄹ→ㄴ 同化）不是プクソンロ；民生社區的日文就寫
**民生社区**，不要翻成「民生コミュニティ」。照抄 JSON 即可。

同一輪查核還抓到**兩個座標錯誤**，而且同樣錯在 `apps/api/app/hotspots/areas.py`：
港川外人住宅原本落在首里以東山區（差 4 公里）、河原町五條原本用了烏丸五條地鐵站
（差 800 公尺）。兩邊都已在 PR #157 校正，這份 JSON 是校正後的版本。

**公開頁不會被空商圈洗版**：`food-filter-chips.tsx` 會濾掉 `count === 0` 的籤，所以
即使某個商圈還沒有店家，旅客也看不到它。可以放心 `is_active=True`。
