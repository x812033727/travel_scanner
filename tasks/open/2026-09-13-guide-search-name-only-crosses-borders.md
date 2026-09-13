---
id: 2026-09-13-guide-search-name-only-crosses-borders
title: 景點介紹搜尋只丟景點名字，河內玉山祠收到台灣玉山的文章
status: review
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-13T12:31:30Z
created_at: 2026-09-13T12:31:25Z
completed_at:
branch: claude/beautiful-hamilton-xb2g9q
depends_on: []
scope:
  - apps/api/app/hotspots/guides.py
  - apps/api/app/hotspots/guide_review.py
  - apps/api/app/destinations/localized.py
  - apps/api/tests/test_hotspot_guides.py
  - apps/api/tests/test_guide_review.py
  - apps/api/tests/test_destinations_localized.py
  - docs/hotspot-intelligence.md
---

# 景點介紹搜尋只丟景點名字，河內玉山祠收到台灣玉山的文章

## Why

使用者回報 `https://mokaair.com/zh-TW?content=article:ecfc44df-92d6-4e03-9d90-fa664e41e47e`：
那篇公開的介紹標題是「玉山山脈 > 交通部觀光署」，摘要寫「位於南臺灣的中央山脈西側，臺灣南投縣水里鄉」，
目的地卻標「河內」。它掛在河內的**玉山祠**（Ngọc Sơn，還劍湖上那座）底下。

兩個地方出錯：

1. `discover_guides` 把查詢寫成 `f"{name} {SEARCH_SUFFIXES[locale]}"`——只有景點名字。繁中查
   `玉山祠 旅遊 景點 部落格`，Brave 回的是台灣的玉山：國家公園、觀光署的山脈頁、新中橫的自駕遊記。
   AI 搜尋那條路徑一直都用城市與國家規劃查詢（`_localized_context` 帶 `city`／`country`），標準搜尋沒有。
2. `guide_review._decide` 只看模型給的相關性與品質分數。候選的標題裡就有「玉山」，模型給了高分，於是一篇
   台灣的文章被核准成河內景點的介紹。

同一個名字撞在一起的不只這一個：札幌圓山公園／台北圓山、金澤東山東／台南東山、峴港順福大橋／台灣一日遊、
廣島灰峰／台中景點。公開清單上查到的 52 筆退件工作在 `2026-09-13-reject-public-guides-about-another-country`。

## Definition of done

- [x] 標準搜尋的查詢帶上景點所在的城市與國家，五個語系都用讀者自己的寫法。
- [x] 覆核在看分數以前先看地點：內容指名另一個國家、又完全沒指到這個國家、這座城市或這個景點，就退件。
- [x] 新規則有測試，`ruff`、`mypy`、`pytest` 全綠。

## Steps

- [x] `app/destinations/localized.py`：`city_words` 把「大阪／京都」拆成搜尋用得上的兩個詞；
      `country_mentions` 認出文字裡指名的國家（國名與目錄城市、五語系、臺＝台）；`mentions_country`
      用目錄 alias（北海道、西貢、機場代碼）做較寬的「這裡有指到這個國家嗎」。
- [x] `app/hotspots/guides.py`：`guide_search_query` 與 `foreign_place`，`discover_guides` 改用前者。
- [x] `app/hotspots/guide_review.py`：`_decide` 先跑 `foreign_place`，理由寫「地點不符：內容講的是⋯」。
- [x] 三個測試檔各補測試，`docs/hotspot-intelligence.md` 補一節。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
```

重點測試：

```bash
cd apps/api && uv run pytest tests/test_hotspot_guides.py tests/test_guide_review.py \
  tests/test_destinations_localized.py -q
```

`test_a_candidate_about_another_country_is_rejected_whatever_it_scored` 就是這張票的回報案例：
玉山山脈那篇拿到 95 分的相關性，仍然被退件。

## Notes

- 規則刻意保守，只在「指名了另一個國家」且「完全沒指到自己」時才退。沒指名任何國家不算證據（「還劍湖旅遊
  指南｜熱門景點資訊」不會被退），同一個國家的另一座城市也不算（橫濱的文章寫「東京から日帰り」照常核准）。
- `mentions_country` 用目錄 alias 是刻意的：「北海道小樽手宮公園」沒寫札幌也沒寫日本，仍然是日本。alias 比
  國名模糊（西貢同時是胡志明市與香港的地名），所以只用來**保留**候選，不用來判定另一個國家。
- 規則看不見的一類：景點名字本身就跨國撞名，而文章同時寫了景點名與另一個國家——河內的西芳寺收到京都西芳寺
  的影片、香港淺水灣收到新北三芝淺水灣的影片。景點名在 `own_terms` 裡會保住它們。要連這類都擋，得再讀一層
  （例如同時比對來源網域的國別），現在靠查詢帶城市與國家從源頭減少。
- 誤判的一類：景點所在的鄉鎮不在目的地目錄裡，文章又提到別國地名。hoiana.com 那篇「會安古鎮」只因為列了
  「日本橋（來遠橋）」就被判成日本——會安不是目錄城市，所以沒有東西指回越南。真正在覆核時 `own_terms` 會
  帶景點名（會安古城），這種就救得回來。
- 沒有動 `ai_search.execute_ai_search`：那條路徑存進來的也是 `pending`，一樣得過 `_decide` 才會公開。
