---
id: 2026-09-06-non-chinese-seed-names-as-chinese-labels
title: seed 的韓文假名泰文名稱被當成中文標籤輸出
status: done
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T14:24:11Z
created_at: 2026-09-06T13:15:08Z
completed_at: 2026-09-06T14:36:03Z
branch: claude/seed-label-hygiene
depends_on: []
scope:
  - apps/api/app/hotspots/catalog.py
  - apps/api/app/localized_names.py
---

# seed 的韓文假名泰文名稱被當成中文標籤輸出

## Why

2026-09-06 稽核發現：26 筆 seed 的策展 `name` 本身就不是中文（韓文諺文、日文假名、泰文），
但 `name` 同時是 zh-TW 標籤、也是 zh-CN 沒有轉換時的退回值，所以中文讀者看到的是諺文或泰文。
沒有 Wikidata 標籤的那幾筆（例如 사려니숲길）連 en 與 ja 也是同一個字串。

另外 45 筆完全沒有中文名稱，zh-TW 與 zh-CN 顯示拉丁字母、諺文或越南文。

## Definition of done

- [x] 分辨「本來就沒有中文名稱」與「有但沒填」，前者補上，後者接受並記錄。
- [x] 中文語系不再出現整串諺文或泰文，除非那確實是該地點唯一的名稱。

## How to verify

```sql
SELECT h.name, l.locale, l.name FROM hotspot_localizations l JOIN travel_hotspots h ON h.id=l.hotspot_id WHERE l.locale IN ('zh-TW','zh-CN') AND l.name ~ '[가-힣ก-๛ぁ-ヿ]' LIMIT 30;
```

## Notes

從 2026-09-06 的部署稽核分出來。相關：[[2026-09-06-ko-ja-names-fall-back-to-english]]。

## Result

稽核說 26 筆，實測是 **70 筆**中文標籤完全沒有漢字：拉丁 48、諺文 11、泰文 11。

根因在 `HotspotSeed.localized_names`：`names={"zh-TW": self.name}` 假設策展名稱一定是中文。
對 22 筆諺文／泰文 seed 來說不成立，於是中文讀者看到諺文或泰文。

修法是只在策展名稱真的含漢字時才把它當 zh-TW 標籤，否則留空讓既有的退回鏈找到英文標籤，
`fallback` 仍保證不會有空值。結果：

| 中文標籤內容 | 修正前 | 修正後 |
|---|---|---|
| 無漢字 | 70 | 69 |
| 其中無法閱讀（諺文／泰文） | 22 | 5 |

例：흰여울문화마을 → Huinnyeoul Culture Village、เกาะเกร็ด → Ko Kret。
剩下 5 筆連英文標籤都沒有（例：사려니숲길），顯示原文是唯一誠實的答案，不動。
64 筆拉丁名稱本來就可讀，也不動。

## Notes（修正過程的一個錯誤）

我第一版的漢字偵測正則用字面字元寫範圍：`[㐀-鿿豈-﫿]`。`豈` 在原始碼裡是統一漢字
U+8C48 而非相容區的 U+F900，範圍因此變成 U+8C48–U+FAFF，把整個諺文音節區
（U+AC00–U+D7AF）都吞進去，於是韓文名稱被判定為中文，修正完全沒生效。
測試抓到了。改用明確的 Unicode 逸出：`[㐀-䶿一-鿿豈-﫿]`。
字元範圍不要用字面字元寫。
