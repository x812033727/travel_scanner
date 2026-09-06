---
id: 2026-09-06-zh-cn-names-are-traditional
title: zh-CN 的景點名稱 568 筆全部是繁體
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T10:32:37Z
created_at: 2026-09-06T09:56:50Z
completed_at: 2026-09-06T10:32:39Z
branch: claude/zh-cn-simplified-seed
depends_on: []
scope:
  - apps/api/app/localized_names.py
  - apps/api/app/hotspots/localization.py
  - apps/api/app/hotspots/simplified_names.py
  - apps/api/app/cli.py
  - apps/api/tests/test_simplified_names.py
  - apps/api/app/hotspots/bootstrap.json
  - apps/api/app/hotspots/deep_bootstrap.json
  - apps/api/app/hotspots/secondary_bootstrap.json
  - apps/api/app/hotspots/food_area_bootstrap.json
  - apps/api/app/hotspots/kanto_expansion_bootstrap.json
---

# zh-CN 的景點名稱 568 筆全部是繁體

## Why

2026-09-06 對正式站做五語系實測時發現：`hotspot_localizations` 的 zh-CN 有 568 筆，
但**每一筆的 name 都和 zh-TW 逐字相同**，也就是簡體中文使用者看到的全是繁體字。

```sql
SELECT count(*) FILTER (WHERE l.name = t.name) FROM hotspot_localizations l
  JOIN hotspot_localizations t ON t.hotspot_id=l.hotspot_id AND t.locale='zh-TW'
 WHERE l.locale='zh-CN';   -- 568 / 568
```

實際回應（`GET /hotspots/rankings`，`X-Travel-Locale: zh-CN`）：
香港海洋公園、樂天世界、彩虹大橋、中野百老匯 —— 應為 海洋公园、乐天世界、彩虹大桥、中野百老汇。
同一支 API 的 ja 正確回「レインボーブリッジ」「中野ブロードウェイ」，所以讀取路徑沒問題，
是 zh-CN 這批資料當初直接複製 zh-TW。

`/hotspots/facets` 的 areas 也一樣：zh-CN 回「澀谷／原宿」「秋葉原／神田」而非「涩谷／原宿」「秋叶原／神田」。

## Definition of done

- [x] zh-CN 的景點名稱是簡體字，且與 zh-TW 不再逐字相同。
- [x] 沒有簡體對照的條目退回繁中（188 筆兩體通用，本來就不需要轉換）。

## Steps

- [x] 決定來源：純字形轉換（繁→簡）夠不夠，還是需要詞彙差異（如「百老匯／百老汇」屬字形，
      「計程車／出租车」屬詞彙）。
- [x] 一次性回填 `hotspot_localizations` 的 zh-CN，並確認 `hotspot_areas` 之類的區域名同步。
- [x] 加一條測試守住「zh-CN 不得與 zh-TW 全等」。

## How to verify

```sql
SELECT count(*) FILTER (WHERE l.name = t.name) FROM hotspot_localizations l JOIN hotspot_localizations t ON t.hotspot_id=l.hotspot_id AND t.locale='zh-TW' WHERE l.locale='zh-CN';
```

## Notes

同時期的 ko／ja 是另一種問題（退回英文），見 [[2026-09-06-ko-ja-names-fall-back-to-english]]。
國家與城市名稱完全沒本地化是第三個問題，見 `2026-09-06-food-hotspot-place-names-i18n`。

## Result

seed 檔的 zh-CN 標籤：374 筆轉換、188 筆兩體通用維持原樣、0 筆被驗證退回，15 次 Gemini 呼叫。
與 zh-TW 逐字相同的數量從 568 降到 0。

抽查最有風險的十筆（與輸入共用字最少的）全部正確：龍編橋→龙编桥、讀賣樂園→读卖乐园、
齋場御嶽→斋场御岳、閣堯艾島→阁尧艾岛。倫披尼公園現在是「伦披尼公园」，
而不是 Wikidata 給的「是樂園」。

資料庫端由 `collect-hotspots` 刷新：`seed_localizations` 每次執行都會重寫五個語系的名稱。
