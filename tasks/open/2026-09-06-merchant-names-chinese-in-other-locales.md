---
id: 2026-09-06-merchant-names-chinese-in-other-locales
title: 110 家店裡有 28 家在英日韓語系顯示中文譯名
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T20:59:56Z
created_at: 2026-09-06T20:09:39Z
completed_at:
branch: claude/merchant-name-locales
depends_on: []
scope:
  - apps/api/app/foods/data/trend_merchants.json
  - apps/api/app/foods/trend_import.py
  - apps/api/app/cli.py
  - apps/api/tests/test_trend_import.py
---

# 110 家店裡有 28 家在英日韓語系顯示中文譯名

## Why

2026-09-07 在正式站量的：把 `/foods/cities` 的 33 個城市逐一帶 `destination_id` 分頁讀完
`/foods/merchants`（`X-Travel-Locale: en`），110 家店裡有 **28 家**的 `name` 仍含漢字。

| 國家 | 家數 |
| --- | --- |
| JP | 17 |
| TH | 6 |
| TW | 5 |

不是全部都該改。三種不同的情況混在一起：

1. **中文譯名蓋掉原名**——`咖哩碗泰菜館`（`ชามแกง Charmgang`）、`波通餐廳`
   （`Restaurant Potong`）、`王子戲院豬肉粥`（`โจ๊กปรินซ์ Jok Prince`）。英文讀者拿到的
   是這家店在中文旅遊寫作裡的稱呼，不是招牌上的字，也不是他在 Google 上搜得到的字。
2. **英文名後面被接了一段中文說明**——`C&C BREAKFAST 沖繩早餐店`、
   `Fuglen Tokyo 挪威咖啡館`、`The Roastery 咖啡烘焙館`、`Camelback 三明治咖啡`。
   前半就是店名，後半是給中文讀者的註解，其他語系不需要。
3. **原名本來就是漢字**——`白金茶房`、`食堂faidama`。這些不該動，日文讀者看到的正是招牌。

第 3 類正是 `destinations/localized.py` 檔頭那條設計決定要保護的東西，所以這張票不能
一律「把漢字換掉」，得逐家判斷。

## Definition of done

- [x] `X-Travel-Locale: en` 讀完 110 家，`name` 含漢字的只剩「原名就是漢字」那一類，
      且每一家都在 Notes 裡記過為什麼留。
- [ ] ja／ko 同樣量一次（目前只量了 en）。
- [ ] zh-TW 的顯示完全不變。

## Steps

- [x] 先把 28 家分成上面三類，一家一行寫進任務檔。
- [x] 第 1、2 類補 `names` 的 en／ja／ko：第 2 類直接砍掉中文註解那一段；第 1 類用
      店家官網或官方觀光頁上的羅馬字招牌（`local_name` 通常已經有），**不要自己音譯**。
- [x] 種子改完要能重跑：`seed_food_catalog` 更新既有列時只動 seed-owned 的值
      （比照 #198 的 source 規則），別蓋掉後台改過的。

## How to verify

```bash
curl -s -H 'X-Travel-Locale: en' \
  'https://mokaair.com/api/travel/foods/merchants?destination_id=bangkok&limit=50' \
  | python -c "import json,sys,re; print([i['name'] for i in json.load(sys.stdin)['items'] if re.search('[一-鿿]', i['name'])])"
```

## Notes

- 量測腳本：對 `/foods/cities` 的每個城市 id 帶 `destination_id` 讀 `/foods/merchants`
  （`limit=50`，跟著 `next_cursor` 翻頁），用 slug 去重。**`?city=` 不是這支端點的參數**，
  FastAPI 會直接忽略，於是每次都回同一批前 30 家——第一次量就是這樣得到假數字的。
- 同一輪掃描找到的另一個問題（`destination_name` 在所有語系都回繁中）已經修掉，
  見 [[2026-09-06-food-hotspot-place-names-i18n]] 的後續 PR。
- 景點那邊的地名（`高尾山`、`中野ブロードウェイ`、`香港海洋公園`）不在此列：那是當地
  寫法，本來就該保留。

## Result（2026-09-07）

### 票指的檔案不對，數字對

`merchant_catalog.py` 的 173 筆種子裡，`name` 含漢字的是 **0 筆**。有問題的列在
`apps/api/app/foods/data/trend_merchants.json`（146 筆），而且原因寫在欄位名稱上：
那個檔案的名稱欄位叫 **`name_zh`**，`trend_import.py` 直接把它寫進 `FoodMerchant.name`，
而 `merchant_names()` 的文件說 `name` 是「the catalog's English label」。中文名被當成英文名送出去。

正式站的數字：146 筆裡 123 筆的 `name_zh` 含漢字，資料庫裡 121 筆，其中
**28 筆已發布**（`is_active` 且 `review_status='approved'`）——票量到的 28 就是這一批，
所以票的數字是對的，只是找錯了檔案。

### 修法：英文名從資料裡拿，不自己音譯

28 筆裡有 **17 筆的拉丁名本來就在自己的列裡**，多半在 `local_name`：

| 現在的 name | 真正的招牌 |
| --- | --- |
| 咖哩碗泰菜館 | ชามแกง **Charmgang** |
| 王子戲院豬肉粥 | โจ๊กปรินซ์ **Jok Prince** |
| 波通餐廳 | **Restaurant Potong** (โพทง) |
| C&C BREAKFAST 沖繩早餐店 | **C&C BREAKFAST OKINAWA** |
| The Roastery 咖啡烘焙館 | **THE ROASTERY BY NOZY COFFEE** |

新增 `name_en` 欄位放這 17 個值，並加一個測試逐筆確認每個值都是從該列的 `name_zh` 或
`local_name` 裡取出來的子字串——票說「不要自己音譯」，這個測試讓那條規則不能被偷偷違反。

**剩下 11 筆刻意不動**，它們的招牌本來就是漢字，屬於票裡的第 3 類：
白金茶房、食堂faidama、鶴屋吉信 本店、原宿餃子樓、川本屋茶舖、元祖咖哩擔擔麵 征虎總本店、
蠔爽 黃埔總店、金得春捲、泰成水果冰店、修安扁擔豆花、東區粉圓。

### 一個會咬人的細節：zh-TW 必須完全不變

`merchant_names()` 是 `{**defaults, **names_json}`，所以存進 `names_json` 的標籤會**覆蓋**預設值。
日本店的預設 `zh-TW` 是 `local_name`（招牌本身），如果照著把 `name_zh` 存進去，中文讀者看到的
就會從招牌變成中文譯名——那是這張票沒有要做的改動。所以 `chinese_label` 只在**非日本**的店
才寫，泰國那幾家的中文名才不會在 `name` 變成拉丁字之後消失。三個測試分別釘住這三種情況。

### 既有資料要另外回填

`trend_import` 對已存在的 slug 是「一律跳過、絕不合併」（檔頭第 27 行寫明的規則），所以改資料檔
不會動到已經匯入的列。新增 CLI `backfill-merchant-english-names`，預設 dry-run，只在 `name`
仍等於檔案裡的 `name_zh` 時才改（後台改過名的列不碰），重跑第二次不會再改任何東西。

檢查：`ruff`、`mypy`、`pytest`（1,184 passed、38 skipped）全綠。
