---
id: 2026-09-06-merchant-names-chinese-in-other-locales
title: 110 家店裡有 28 家在英日韓語系顯示中文譯名
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T20:09:39Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/merchant_catalog.py
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

- [ ] `X-Travel-Locale: en` 讀完 110 家，`name` 含漢字的只剩「原名就是漢字」那一類，
      且每一家都在 Notes 裡記過為什麼留。
- [ ] ja／ko 同樣量一次（目前只量了 en）。
- [ ] zh-TW 的顯示完全不變。

## Steps

- [ ] 先把 28 家分成上面三類，一家一行寫進任務檔。
- [ ] 第 1、2 類補 `names` 的 en／ja／ko：第 2 類直接砍掉中文註解那一段；第 1 類用
      店家官網或官方觀光頁上的羅馬字招牌（`local_name` 通常已經有），**不要自己音譯**。
- [ ] 種子改完要能重跑：`seed_food_catalog` 更新既有列時只動 seed-owned 的值
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
