---
id: 2026-09-06-seed-categories-assigned-by-quota
title: 種子分類是按配額輪流發的，不只 shopping 一類錯
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T17:39:45Z
created_at: 2026-09-06T17:24:21Z
completed_at: 2026-09-06T17:50:22Z
branch: claude/seed-category-quota
depends_on: []
scope:
  - apps/api/app/hotspots/secondary_bootstrap.json
  - apps/api/app/hotspots/deep_bootstrap.json
  - apps/api/app/hotspots/catalog.py
  - apps/api/tests/test_hotspot_seed_categories.py
---

# 種子分類是按配額輪流發的，不只 shopping 一類錯

## Why

`2026-09-06-seed-category-shopping-mistakes` 說有四筆景點被標成 `shopping`。清完那一類之後
發現不是四筆的問題：`secondary_bootstrap.json` 有 180 列，分類分布是
`culture 38 / food 36 / nature 36 / shopping 35 / viewpoint 35`，而且**每個城市每一類剛好三筆**。
分類不是照地方本身給的，是照配額輪流發的。

那一輪把 35 筆 `shopping` 裡的 34 筆改掉之後（只有廣島本通商店街本來就對），其他類同樣的錯還在：

| 現在的分類 | 實際上是什麼 |
| --- | --- |
| `nature` 金澤21世紀美術館、金澤能樂美術館、高雄市立美術館、Royal Portrait Museum、第二市場 | 美術館與市場 |
| `nature` 大崎八幡宮、旗津天后宮、芬皇寺、殿洞聖堂 | 神社與寺廟 |
| `food` 台中大都會歌劇院、衛武營國家藝術文化中心、臺中刑務所演武場 | 表演場館與古蹟 |
| `food` 西子灣風景區 | 風景區 |

`CATEGORY_CORRECTIONS`（`catalog.py`）目前有 68 筆，就是歷來一筆一筆補的結果——那張表在替
資料檔的錯誤擦屁股，而不是記錄少數例外。

**為什麼配額會存在**：三個 contract 測試以前明確要求配額——每個次要城市至少五種分類、
deep 每城至少三種且單一分類不超過兩筆、食物種子剛好 45 筆。shopping 那一輪已經把它們改成
不再逼出配額（見 `tests/test_secondary_destinations.py`、`test_hotspot_depth_catalog.py` 的註解）。
不先鬆開那些斷言，任何修正都會被測試擋回去。

## Definition of done

- [x] `secondary_bootstrap.json` 與 `deep_bootstrap.json` 每一列的 `category` 對得上那個地方是什麼。
- [x] `CATEGORY_CORRECTIONS` 只留真正的例外（單一名稱的判斷分歧），不再是資料檔的補丁清單。
- [x] `test_hotspot_seed_categories.py` 的規則從只擋 `shopping` 擴大到每一類，例外都要寫理由。

## Steps

- [x] **用 Wikidata P31 判定，不要用名稱猜。** 560 筆種子有 `wikidata_item_id`，
      `apps/api/app/hotspots/discovery.py` 已經有 P31 → 分類的對照表（`ALLOWED_TYPES`）。
      寫一支一次性腳本查 P31，產生「現在的分類 vs P31 建議的分類」對照，人工複核後改資料檔。
- [x] 沒有 QID 的列（約 3 筆）與 P31 對不到的列，逐筆人工判定並在 PR 寫下理由。
- [x] 改完把 `CATEGORY_CORRECTIONS` 裡已經沒有作用的鍵刪掉（資料檔已經正確就不需要覆寫）。
- [x] `test_hotspot_seed_categories.py` 的 `NOT_SHOPPING` 擴成每一類的關鍵詞表。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_seed_categories.py tests/test_secondary_destinations.py tests/test_hotspot_depth_catalog.py tests/test_food_catalog.py -q
cd apps/api && uv run python -c "import collections; from app.hotspots.catalog import HOTSPOT_SEEDS; print(collections.Counter(s.category for s in HOTSPOT_SEEDS))"
```

改完之後分類分布**不應該**再是平均的——那正是配額的指紋。

## Notes


- 分類會進 `search_text`，下一次 collect run 自己刷新，不需要資料遷移。
- 主題（`theme_bootstrap.json`）是另一個維度，跟這張無關，不要一起改。
- AI 規劃器把興趣對應到分類（`apps/api/app/hotspots/service.py:63-71`），所以分類錯＝推薦錯，
  這不只是篩選器的顯示問題。

### 做完之後（2026-09-07，claude-opus-5）

用 Wikidata P31 對 560 筆有 QID 的種子跑了一次，方法與數字：

- `wbgetentities` 一次 50 個，拿 P31 與英文標籤，再把 340 個不同的 P31 值也抓一次標籤，
  才看得懂比對表（腳本留在 scratchpad，不進 repo：一次性的東西）。
- P31 → 分類的對照表要**八類**不是五類：種子實際用到 culture/nature/viewpoint/shopping/food/
  family/beach/nightlife。第一版只寫五類，海灘全被判成「錯」，那是我的對照表錯不是資料錯。
- 對得上 256 筆、對不上 84 筆、220 筆 P31 不足以判斷（neighborhood、street、building 這種），
  不判斷的就不動——猜比錯更糟。

84 筆逐筆看完，**只改 39 筆**，其餘刻意不動並在腳本註解寫下理由：

- `viewpoint → nature` 15 筆（山、岬）不動：山本來就是「去看風景的地方」，viewpoint 是產品的判斷不是錯誤。
- `beach → nature` 4 筆不動：beach 比 nature 精確。
- `food ↔ shopping` 7 筆不動：商店街與市場兩邊都說得通。
- 海雲隘口（山口）維持 viewpoint、雞林（森林＋遺址）維持 nature、
  明月院與報國寺竹林維持 nature（繡球花與竹林才是來的理由）、
  札幌藝術之森與首爾文化備蓄基地維持 culture、國債報償運動紀念公園維持 culture（紀念公園）。

改掉的 39 筆是沒有爭議的那種：博物館、美術館、寺廟、神社、教堂、城、宮、陵墓、遺址被標成
nature 或 viewpoint（33 筆），公園、湖、庭園、洞窟被標成 culture（6 筆）。

**`CATEGORY_CORRECTIONS` 現在是空的。** 68 筆全部是在補這兩個資料檔的錯，把它們寫回資料檔之後
一筆都不再改變任何東西（實測：清空前後每個 slug 的有效分類完全相同）。表留著但空著，
註解寫明什麼情況才該放東西進去。

**又鬆了兩個配額斷言。** 上一張任務把「每城五類」降成三類、「deep 單類不超過兩筆」拿掉之後，
這次真話再度撞上剩下的門檻：某個 deep 城市五筆全是 culture，慶州十五筆有九筆 culture。
兩個 per-city 斷言都換成「分類值必須是已知的八類之一」，變異度改成對整份目錄斷言一次
（最大類別不超過一半、每一類至少五筆），放在新的 `test_hotspot_seed_categories.py` 裡。
per-city 的配額就是這串錯誤的來源，不該再用另一個門檻換掉它。
