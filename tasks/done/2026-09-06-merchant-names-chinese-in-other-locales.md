---
id: 2026-09-06-merchant-names-chinese-in-other-locales
title: 110 家店裡有 28 家在英日韓語系顯示中文譯名
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T20:53:40Z
created_at: 2026-09-06T20:09:39Z
completed_at: 2026-09-06T21:01:02Z
branch: claude/merchant-names
depends_on: []
scope:
  - apps/api/app/foods/trend_import.py
  - apps/api/app/foods/data/trend_merchants.json
  - apps/api/migrations/versions/0052_repair_trend_merchant_names.py
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

三種情況混在一起：

1. **中文譯名蓋掉原名**——`咖哩碗泰菜館`（`ชามแกง Charmgang`）、`波通餐廳`
   （`Restaurant Potong`）、`王子戲院豬肉粥`（`โจ๊กปรินซ์ Jok Prince`）。英文讀者拿到的
   是這家店在中文旅遊寫作裡的稱呼，不是招牌上的字。
2. **英文名後面被接了一段中文說明**——`C&C BREAKFAST 沖繩早餐店`、
   `Fuglen Tokyo 挪威咖啡館`、`The Roastery 咖啡烘焙館`。前半就是店名，後半是給中文讀者的註解。
3. **原名本來就是漢字**——`白金茶房`、`食堂faidama`、`金得春捲`。日文／中文讀者看到的
   正是招牌，不該動；缺的只是一個英文標籤。

## 訂正：這不是 `merchant_catalog.py` 的問題

原本把 scope 寫成 `apps/api/app/foods/merchant_catalog.py`，那是猜的，而且是錯的——
`MERCHANT_SEEDS` 裡**沒有任何一筆** `name` 含漢字。這 28 家來自
`apps/api/app/foods/data/trend_merchants.json`，欄位叫 `name_zh`（**設計上就是中文**），
而 `trend_import.py` 把它直接寫進 `FoodMerchant.name`。

`name` 的用途在 `merchant_names()` 的 docstring 裡寫得很清楚：「the catalog's English
label」。en 讀它，ja／ko 缺譯名時退回它。所以問題是匯入器把中文放進了一個英文欄位。

## Definition of done

- [x] `X-Travel-Locale: en` 讀完 110 家，`name` 不再有中文譯名。
- [x] zh-TW 讀者看到的名稱完全不變。
- [ ] 部署後在正式站重量一次（en 與 ja／ko；後兩者走同一條退回鏈，預期一起好）。

## Steps

- [x] `trend_import.py` 讀選填的 `name_en`：`display_name` 用它，沒有就維持 `name_zh`
      （寧可留中文，也不要機器音譯一個店名）。`name_en` 必須是拉丁字（用既有的
      `is_latin_script`，所以 `oHacorté` 過得了）。
- [x] `stored_names()`：只有泰國與越南把中文名寫進 `names_json.zh-TW`。日本、台灣、韓國
      的原文本來就是站上的語系之一，`merchant_names()` 已經會給中文讀者原文，不必存。
- [x] `trend_merchants.json` 為那 28 家補 `name_en`，逐家查過來源。
- [x] `0052_repair_trend_merchant_names`：資料庫裡已存在的列匯入器不會動，所以用遷移改。
      每一筆都以「現在的 name 仍等於那個中文字串」為條件，後台改過的不動。

## How to verify

```bash
curl -s -H 'X-Travel-Locale: en' \
  'https://mokaair.com/api/travel/foods/merchants?destination_id=bangkok&limit=50' \
  | python -c "import json,sys,re; print([i['name'] for i in json.load(sys.stdin)['items'] if re.search('[一-鿿]', i['name'])])"
```

應該回 `[]`。zh-TW 再跑一次，名稱與部署前逐字相同。

## Notes

- 名字的來源：`local_name` 裡本來就有拉丁招牌的直接用（16 家）；其餘查過——福岡市官方觀光
  指南的 Shirogane Sabo（白金茶房）、Tripadvisor 的 Harajuku Gyozaro（原宿餃子樓）與
  Tai Cheng Fruit Shop（泰成水果冰店）、店家自己的 Instagram／Facebook 帳號
  Kawamotoya（川本屋茶舖）與 XiuAnDoHua（修安扁擔豆花）、拉麵店官網的 征虎 Masatora。
  台灣幾家沒有自訂英文名的用漢語拼音。
- 量測腳本：對 `/foods/cities` 的每個城市 id 帶 **`destination_id`** 讀 `/foods/merchants`
  （`limit=50`，跟著 `next_cursor` 翻頁），用 slug 去重。**`?city=` 不是這支端點的參數**，
  FastAPI 直接忽略，於是每次都回同一批前 30 家——第一次量就是這樣得到假數字的。
- **還沒做完的那一半**：`trend_merchants.json` 有 146 列，其中 **123 列**的 `name_zh` 含漢字，
  這次只為已發布的 28 家補了 `name_en`。其餘 95 列還沒發布，等它們要上線時得逐家查名字。
  不要用音譯批次生成——`川本屋茶舖` 的 slug 就是這樣變成 `chuan-ben-wu-cha-pu`（拿普通話讀
  一個日文店名），而正確答案是 Kawamotoya。已另立
  [[2026-09-06-trend-merchant-english-names-backlog]]。
- 同一輪掃描找到的另一個問題（`destination_name` 在所有語系都回繁中）已修，見 PR #280。
- 景點那邊的地名（`高尾山`、`中野ブロードウェイ`、`香港海洋公園`）不在此列：那是當地寫法。
