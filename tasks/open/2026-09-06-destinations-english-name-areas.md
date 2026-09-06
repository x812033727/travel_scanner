---
id: 2026-09-06-destinations-english-name-areas
title: destinations 的 english_name 存繁中、areas 不隨語系
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T13:20:48Z
created_at: 2026-09-06T09:56:54Z
completed_at:
branch: claude/place-names-i18n
depends_on: []
scope:
  - apps/api/app/destinations/localized.py
---

# destinations 的 english_name 存繁中、areas 不隨語系

## Why

2026-09-06 正式站實測 `GET /destinations`（`X-Travel-Locale: en`）：

```json
{"id":"tokyo","city":"Tokyo","local_name":"東京","english_name":"東京",
 "areas":["新宿","上野／淺草","東京站／銀座","澀谷"]}
```

- `city` 本地化正確（Tokyo），但 `english_name` 裝的是「東京」而不是英文名，欄位名與內容不符；
  用到這個欄位的地方會拿到中文。
- `areas[]` 在 en／ja／ko 都維持繁中，和同一支回應裡已經本地化的 `city` 不一致。
  （`/hotspots/facets` 的 areas 反而是本地化的，兩邊行為不一樣。）

## Definition of done

- [x] `english_name` 是英文：33 筆全部，退回順序改成 CITY_NAMES 的英文名再退回目錄文字。
- [ ] `/destinations` 的 `areas[]` 依 `X-Travel-Locale` 回該語系，與 `/hotspots/facets` 一致。

## How to verify

```bash
curl -s -H 'X-Travel-Locale: en' http://127.0.0.1:8090/api/v1/destinations | head -c 400
```

## Notes

國家與城市名稱在 `/hotspots/facets`、`/foods/cities` 完全沒本地化，是另一張票
`2026-09-06-food-hotspot-place-names-i18n`，兩者可能共用同一套 `localized_names` 修法。

## Result（一半完成，areas 需要產品決策）

`english_name` 修好了。33 筆裡有 19 筆沒設這個欄位，所有讀取端都退回 `profile.city`（繁中），
所以一個叫 english_name 的欄位回傳中文。`CITY_NAMES` 本來就有 33 筆已核對的英文名，改成先
退回那裡。現在 0 筆回傳中文。同一個修法也套用到 `/foods/cities`。

**areas 沒有動，因為它不是機械性修正。** 量測過：destinations 目錄有 132 個區域字串，
`HOTSPOT_AREAS` 有 390 個，兩者只有 **38 個（28%）** 名稱對得上。

- 只在地化那 28% 會產生中英夾雜的清單，比整份繁中更糟。
- 另外 94 個要新造翻譯，而 `localized.py` 的檔頭明確寫過這條設計決定：
  「areas、aliases 與 interest suggestions 刻意留在目錄語言，因為它們是地名與搜尋詞，
  沒有人對照地圖檢查過的翻譯比原文更糟。」

真正的問題是**同一批城市有兩份區域目錄**，內容本來就不同（destinations 的是「該住哪一區」，
hotspots 的是「篩景點用」）。要哪一份當權威，是產品決定，不該由這張票猜。

決定之後才動 areas；另外 `HOTSPOT_AREAS` 完全沒有 zh-CN 欄位，見
[[2026-09-06-zh-cn-area-labels-traditional]]，那個要先修，否則對齊過去也是繁體。
