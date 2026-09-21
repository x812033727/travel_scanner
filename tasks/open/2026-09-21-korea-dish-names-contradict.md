---
id: 2026-09-21-korea-dish-names-contradict
title: 韓國料理名在站內互相矛盾：막창說牛也說豬，고기국수有三個中文名
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-21T04:50:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/daegu-2-day-itinerary.json
  - apps/api/app/guides/content/jeju-gogi-guksu-food-guide.json
  - apps/api/app/guides/content/korea-food-guide-must-eat.json
  - apps/api/app/guides/taxonomy.py
---

# 韓國料理名在站內互相矛盾：막창說牛也說豬，고기국수有三個中文名

## Why

2026-09-21 改寫韓國美食那 22 篇、重繪它們的圖時，發現兩個跨文章的矛盾。
兩個都在正式站上，讀者同一天讀兩篇就會看到互相打架的說法。

### 一、막창是牛還是豬

`daegu-2-day-itinerary` 的菜色清單寫：

> 막창구이：烤牛的第四個胃 홍창，沾大醬醬料。

`daegu-makchang-food-guide` 的標題與導言寫：

> 大邱烤腸怎麼點：막창是大腸頭，菜單上豬牛都有，照區域挑店
> 韓國觀光公社的料理頁把막창寫成豬大腸末端的直腸

同一個網站、同一個城市、同一道菜，一篇說牛的第四個胃，一篇引韓國觀光公社說豬的直腸。

**兩邊都不是憑空來的。** 韓文的 막창 確實兩種都指：出自豬的是直腸，出自牛的是第四個胃
（皺胃，也叫 홍창）。問題在於**大邱最有名的那一種是豬**，而行程文只寫了牛那一個定義，
沒提豬，也沒提菜單上兩種都有。所以那一行不是「另一種說法」，是在大邱的脈絡下漏掉主角。

美食文的標題已經把話講全了（「菜單上豬牛都有」）。要改的是行程文那一行。

### 二、고기국수 有三個中文名

| 出處 | 寫成 |
|---|---|
| `jeju-gogi-guksu-food-guide` 正文 | 豬肉麵、濟州豬肉麵 |
| 同一篇的圖說與 `alt` | 肉湯麵、濟州肉湯麵 |
| `korea-food-guide-must-eat` | 肉湯麵 |
| `apps/api/app/guides/taxonomy.py` | 豬肉湯麵 |

`taxonomy.py` 那一筆同時餵給料理辭典與主題頁，所以這個名字會出現在麵包屑與列表上，
和文章內文不一致特別明顯。

2026-09-21 重繪圖時**刻意沒動圖上的 고기국수 → 肉湯麵**，因為只改圖會讓圖和
它自己內容包的 `alt` 對不上，反而多一個不一致。要改就四處一起改。

## Definition of done

- [ ] 站內搜尋 막창，每一處的定義彼此不衝突。
- [ ] 고기국수 的中文名只剩一個，正文、圖說、`alt`、hub 文章與 `taxonomy.py` 全部一致。

## Steps

- [ ] 決定 고기국수 用哪一個中文名。建議 **豬肉湯麵**：`taxonomy.py` 已經是這個，
      改動面最小，而且「湯麵」比「麵」準確（這道菜是湯的）。
- [ ] 四個地方一起改：內容包正文、內容包的 image `alt` 與 `caption`、
      `korea-food-guide-must-eat`、`taxonomy.py`。
- [ ] SVG 上的標籤也要改，改完重跑 `tools/lift-diagram-descriptions.py --slug jeju-gogi-guksu-food-guide`，
      並把內容包從 CRLF 轉回 LF（那個工具在 Windows 上會寫 CRLF）。
- [ ] 行程文那一行改成同時涵蓋豬與牛，或直接對齊美食文的說法。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --slug jeju-gogi-guksu-food-guide
```

再用 grep 確認站內只剩一個名字：

```bash
grep -ro "肉湯麵\|豬肉麵\|豬肉湯麵" apps/api/app/guides/ | sort | uniq -c
```

## Notes

- **`陣元祖全雞` 查過了，不要動。** `seoul-dak-hanmari-food-guide` 把 진원조닭한마리
  寫成陣元祖全雞，看起來像把 진 認成陣（眞元祖才合理），但那是
  Visit Seoul 繁體中文頁自己的寫法，內容包也把它列為來源。是對方的用字，不是我們抄錯。
- 22 篇的 hero `alt` 全部查過，提到飯的三篇（돼지국밥兩篇、비빔밥一篇）
  都是本來就有飯的菜，沒有問題。
- `daegu-2-day-itinerary` 不在 2026-09 韓國美食那一批裡，是另一個批次寫的，
  所以那一批的改寫沒有掃到它。同一批可能還有別的行程文引用美食名詞，值得一起看。
