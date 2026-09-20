---
id: 2026-09-20-korean-dish-seeds
title: 料理目錄補上韓國美食特輯要用的七道料理與代表店
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-20T04:58:00Z
created_at: 2026-09-20T04:57:30Z
completed_at: 2026-09-20T05:24:52Z
branch: claude/korean-dish-seeds
depends_on: []
scope:
  - apps/api/app/foods/catalog.py
  - apps/api/app/foods/category_catalog.py
  - apps/api/app/foods/merchant_catalog.py
  - apps/api/tests/test_food_catalog.py
  - apps/api/tests/test_food_taxonomy_catalog.py
  - apps/api/tests/test_food_platform_links.py
  - apps/api/tests/test_food_seed_ownership.py
  - apps/api/tests/test_food_integration.py
---

# 料理目錄補上韓國美食特輯要用的七道料理與代表店

## Why

站主 2026-09-20 的要求：「熱門的美食資料庫沒有就補」。韓國美食特輯（一道料理、一個城市寫一篇）要寫的料理裡，有七道料理目錄沒有：豬肉湯飯、小麥冷麵、牛骨湯、黑豬肉、豬肉湯麵、辣燉排骨、烤腸。補進去以後，料理卡與美食目錄的搜尋才找得到這些菜，AI 行程規劃也才會把它們納入候選。

**先查重再補。** 種子檔的韓國料理只有 10 道，正式站卻有 25 道：另外 15 道是後台建立的，slug 多半沒有 `kr-` 前綴（`dakhanmari`、`kalguksu`、`jokbal`、`ganjang-gejang`、`seolleongtang`、`mandu`、`ssambap`…）。`seed_food_catalog` 只用 slug 比對，照慣例補一個 `kr-dak-hanmari` 會在正式站生出第二個「一隻雞」，兩筆都是已核准、已啟用。這七道是用韓文名對 `GET /api/travel/foods?country_code=KR` 逐一查過、確定正式站沒有的。

## Definition of done

- [x] 七道料理進 `FOOD_SEEDS`（display_order 81–87，排在所有既有料理之後，不改變任何既有行程會挑到的料理）與 `DISH_CATEGORIES`。
- [x] 每個（城市, 料理）至少一間代表店，`validate_merchant_catalog` 的等式通過。
- [x] 代表店的官方來源都是今天親自重開、確認頁面同時寫了店名與這道料理（`research/check_anchors.py` 八筆全過）。
- [x] 寫死的數字跟著更新：料理 87、店家 179、（城市,料理）193、有商圈的店 82、分類連結 280、直接來源 119（韓國 25）。
- [x] 防重複測試：韓國種子的韓文名不得出現在「正式站後台建立的 15 道」名單裡。
- [x] 認養測試：既有已核准、已公開的店家 reseed 後只多一條料理連結，狀態、名稱、來源、分類都不動。
- [ ] 部署後在正式站跑 `seed-foods`，並照 How to verify 對數字。

## Steps

- [x] 七道料理的名稱、分類、適用城市、維基條目。
- [x] 六間新代表店與兩間既有種子加掛料理。
- [x] 測試與寫死數字。
- [ ] 後台待辦（上線後，見 Notes）。

## How to verify

```bash
cd apps/api
uv run ruff check . && uv run mypy app
uv run pytest -q tests/test_food_catalog.py tests/test_food_taxonomy_catalog.py \
  tests/test_food_seed_ownership.py tests/test_food_platform_links.py \
  tests/test_trend_import.py tests/test_merchant_styles.py
```

合併前再查一次正式站有沒有同名料理（這期間可能有人從後台又建了一道）：

```bash
curl -s -H 'User-Agent: Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' \
  'https://mokaair.com/api/travel/foods?country_code=KR&limit=50' | grep -o '"local_name":"[^"]*"'
```

部署後在主機（`seed-foods` 是冪等的，沒有 dry-run）：

```bash
curl -s https://mokaair.com/api/travel/foods/facets   # 之前：120 道、韓國 25
docker compose -f docker-compose.prod.yml exec -T api python -m app.cli seed-foods
curl -s https://mokaair.com/api/travel/foods/facets   # 之後：127 道、韓國 32
curl -s 'https://mokaair.com/api/travel/foods/merchants?destination_id=busan&q=豬肉湯飯'
```

最後那一筆應該回傳 송정3대국밥——它是正式站已經公開的店，被種子認養後會立刻掛上豬肉湯飯。

## Notes

- **認領用了 `--force`。** scope 與 `2026-09-07-fixed-email-in-integration-tests` 重疊（它握 `tests/test_food_integration.py`）。那張票的程式碼已經在 main（`14ce467d`，#563），停在 review 是在等「同一個資料庫連跑兩次整合測試」這一項人工驗收；票本身沒有動。
- **認養而不是新建**：種子 slug 與正式站既有店家完全相同時，`seed_food_catalog` 只加料理連結，不碰審核狀態、名稱、來源與分類（`app/foods/service.py`）。`busan-songjeong-samdae-gukbap`（釜山豬肉湯飯）與 `seoul-hadongkwan-main-store`（首爾牛骨湯）就是這樣掛上去的，兩家本來就公開。其餘四間新代表店落地是 pending／inactive／unverified，讀者看不到，要等後台補 Naver 地點頁與座標。
- **新料理落地是 approved＋active**，所以 `GET /foods` 與探索卡片立刻看得到；`/zh-TW/foods` 是店家目錄，幾乎不受影響。沒有公開店家的料理卡會顯示「目前沒有已驗證店家」（`kr-hotteok` 現在就是這樣），不會壞掉。
- **中文名是站主定的**（2026-09-20）：辣燉排骨（찜갈비，大邱版是辣蒜口味，這樣叫才不會跟首爾的醬油燉排骨混淆）、烤腸（막창，台灣旅遊文最通用；官方繁中站其實用「牛皺胃」，但那對讀者太陌生）、豬肉湯麵（고기국수，韓國觀光公社的繁中頁就是這樣配對）。五語系標籤的完整查核記錄在特輯的工作目錄裡。
- **`kr-jjim-galbi` 沒有填商圈**：東仁洞（`dongin`）是潮流街區，不在 `AREA_SEEDS` 裡，種子驗證只收 profile 商圈。
- **大邱的四家燉排骨店在 `data/trend_merchants.json` 裡**，不能當種子代表店（那個檔案的筆數與去重結果被兩個測試鎖住），所以另外找了一家有 daegufood.go.kr 官方頁的동원찜갈비。那四家已公開的店要連上這道料理，是後台的事。
- **後台待辦（上線後，建議另開一張票）**：把正式站既有的公開店家連到後台建立的料理（例：명동교자 → `kalguksu`）；那幾道料理各存一次讓 zh-TW 搜尋文字重建（現在 `q=一隻雞` 回 0 筆、`q=닭한마리` 回 1 筆）；`jokbal` 加上 `busan`；大邱四家燉排骨店連上 `kr-jjim-galbi`；把 `kalguksu` 的中文名從「刀削手擀麵」改成「刀切麵」（官方繁中站前者 0 筆、後者 147 筆，攻略的分類頁也用刀切麵）；`seoul-hadongkwan-main-store` 現在掛的是泡菜，官方頁寫它只賣곰탕與수육。
