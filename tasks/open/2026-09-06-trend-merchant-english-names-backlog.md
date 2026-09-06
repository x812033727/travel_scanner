---
id: 2026-09-06-trend-merchant-english-names-backlog
title: 商圈名單還有 95 家沒有英文店名，發布前要逐家查
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T21:10:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/data/trend_merchants.json
---

# 商圈名單還有 95 家沒有英文店名，發布前要逐家查

## Why

`apps/api/app/foods/data/trend_merchants.json` 有 146 列，其中 **123 列**的 `name_zh`
是中文（那個欄位設計上就是中文）。`FoodMerchant.name` 是英文標籤：en 讀它，ja／ko 缺譯名
時退回它。所以一列沒有 `name_en`，發布之後英日韓讀者看到的就是中文店名。

[[2026-09-06-merchant-names-chinese-in-other-locales]] 已經把**已經發布的 28 家**補完，
匯入器也改成讀 `name_en`。剩下的 **95 列還沒發布**，所以現在沒有人看得到——但它們一上線
就會複製同一個問題。

各城市的分布（`name_zh` 含漢字的列）：`osaka-kyoto` 15、`daegu` 14、`seoul` 13、
`tokyo` 10、`bangkok` 10、`sapporo` 8、`jeonju` 8、`fukuoka` 6，其餘分散。

## Definition of done

- [ ] `trend_merchants.json` 每一列要嘛 `name_zh` 本來就是拉丁字，要嘛有 `name_en`。
- [ ] 有一個測試在新增一列沒有英文名時失敗（現在只驗格式，不驗覆蓋率）。

## Steps

- [ ] 先撈 `local_name` 裡已經帶拉丁招牌的那些（在 28 家裡佔 16 家），那是最快的一批。
- [ ] 其餘逐家查：店家官網／官方 Instagram／當地觀光局頁面上的英文寫法優先，
      沒有才用標準羅馬字（日文用平文式、韓文用文觀部式、中文用漢語拼音）。
- [ ] **不要用音譯批次生成**。`川本屋茶舖` 的 slug 就是這樣變成 `chuan-ben-wu-cha-pu`
      ——拿普通話去讀一個日文店名——正確答案是 Kawamotoya。

## How to verify

```bash
cd apps/api && uv run python -c "
import json, re
rows = json.load(open('app/foods/data/trend_merchants.json', encoding='utf-8'))
han = re.compile('[一-鿿ぁ-ヿ]')
print(sum(1 for r in rows if han.search(r['name_zh']) and not r.get('name_en')), 'still need one')
"
```

## Notes

- 匯入器已經接受 `name_en`（`is_latin_script` 驗、`display_name` 用、泰越把中文名存進
  `names_json.zh-TW`），所以這張票純粹是補資料，不必動程式。
- 這 95 家還沒匯入正式機，所以做完之後不需要遷移，直接
  `python -m app.cli import-trend-merchants --apply` 就會帶著英文名建立。
