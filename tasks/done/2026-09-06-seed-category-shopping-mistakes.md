---
id: 2026-09-06-seed-category-shopping-mistakes
title: 四個景點的分類被標成 shopping，其實是公園、城跡與神社
status: done
priority: P3
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T17:11:51Z
created_at: 2026-09-06T15:32:50Z
completed_at: 2026-09-06T17:25:30Z
branch: claude/seed-categories
depends_on: []
scope:
  - apps/api/app/hotspots/catalog.py
  - apps/api/tests/test_hotspot_seed_categories.py
  - apps/api/tests/test_secondary_destinations.py
  - apps/api/tests/test_hotspot_depth_catalog.py
  - apps/api/tests/test_food_catalog.py
---

# 四個景點的分類被標成 shopping，其實是公園、城跡與神社

## Why

種子檔把四個明顯不是購物的地方標成 `category: "shopping"`：

| slug | 名稱 | 實際是什麼 | 合理分類 |
| --- | --- | --- | --- |
| `sdj-q11541912` | 榴岡公園（仙台） | 賞櫻公園 | `nature` |
| `hij-q41977` | 廣島城 | 城跡與歷史博物館 | `culture` |
| `hij-q191763` | 嚴島神社 | 世界遺產神社 | `culture` |
| `tae-q624313` | 八公山（大邱） | 山與國立公園 | `nature` |

影響有三個：熱門景點頁的「購物」篩選會混進四個非購物景點；卡片的分類文字直接寫錯；AI 規劃器把 `shopping` 興趣對應到 `category="shopping"`（`apps/api/app/hotspots/service.py:63-71`），所以說「想逛街」的旅客會被排進嚴島神社。

發現於 2026-09-06 加季節主題時——這四個地方都要掛賞櫻或賞楓，一看分類就不對。主題是另一個維度，已經照實掛好，不受這張任務影響。

## Definition of done

- [x] 四筆的 `category` 改成上表的值，`/hotspots?category=shopping` 不再回傳它們。
- [x] 有一個測試擋住同類錯誤再發生。

## Steps

- [x] 在 `apps/api/app/hotspots/catalog.py` 的 `CATEGORY_CORRECTIONS` 加這四個名稱（那張表就是為了這種事存在的），或直接改對應 bootstrap JSON 的 `category`。兩者擇一，別兩邊都寫。
- [x] 順手看一遍其餘 81 筆 `shopping`，確認沒有第五個。
- [x] `tests/test_hotspot_seed_categories.py`（新）：`shopping` 的種子名稱不得出現「神社」「寺」「城」「公園」「山」這類字樣，例外要逐筆寫進允許清單並附理由。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_seed_categories.py tests/test_kanto_expansion.py -q
cd apps/api && uv run python -c "from app.hotspots.catalog import HOTSPOT_SEEDS; print([s.name for s in HOTSPOT_SEEDS if s.category=='shopping'])"
```

## Notes


- 改分類會動到 `search_text`（`catalog.py` 用分類組出來的），下一次 collect run 會自己刷新，不用資料遷移。
- 這四筆的季節主題（`theme_bootstrap.json`）不必動：主題和分類互相獨立。

### 做完之後（2026-09-07，claude-opus-5）

**不是四筆，是三十四筆。** 任務要我「順手看一遍其餘 81 筆 shopping」，看完發現
`secondary_bootstrap.json` 的 35 筆 shopping 裡只有廣島本通商店街是對的。其餘是神社、寺廟、
城跡、國家公園、濕地、瀑布、美術館、湖、山。全部進 `CATEGORY_CORRECTIONS`（34 筆），
那張表因此從 34 筆長到 68 筆。

**根因不在資料，在測試。** `secondary_bootstrap.json` 180 列的分類分布是 38/36/36/35/35，
每個城市每一類剛好三筆——這是配額，不是判斷。而配額是被三個 contract 測試逼出來的：

- `test_secondary_destinations`：每個次要城市的分類至少五種 → 改成三種。
  仙台的十五個景點裡就是沒有購物點，硬湊出來的那一個是榴岡公園。
- `test_hotspot_depth_catalog`：deep 每城至少三種、單一分類不超過兩筆 → 改成至少兩種、不設上限。
  金澤的五個深度景點真的是三間寺社，清萊真的是三座山兩間寺。
- `test_food_catalog`：食物種子剛好 45 筆 → 46（六合夜市從 shopping 移到 food，
  跟中華路夜市一致；台灣夜市是吃的，泰國 night bazaar 是逛的，兩者分開）。

scope 因此多了那三個測試檔：不鬆開斷言就改不動分類。

**其他分類同樣有病**，但沒有在這張任務裡動：`nature` 裡有金澤21世紀美術館與第二市場，
`food` 裡有台中大都會歌劇院與衛武營。那要用 Wikidata P31 重新推，不是照名字猜，
已另立 `2026-09-06-seed-categories-assigned-by-quota`。

新測試 `test_hotspot_seed_categories.py` 用關鍵詞擋（神社／寺／宮／城／公園／山／Museum／Park…），
例外五筆逐一寫理由（暹羅百麗宮、博多運河城、宮下公園、代官山蔦屋書店、東京中城——
名字裡有宮或城或公園，但真的是商場），並且釘住例外必須仍是 shopping 種子，
免得例外清單留著爛掉。
